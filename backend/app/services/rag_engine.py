# Import tools
from typing import List, Dict, Any, Optional, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Import local modules
from app.core.logger import get_logger
from app.core.config import settings
from app.services.database import DatabaseManager
from app.services.embedding import EmbeddingGenerator, VectorStorage

# Define MockAzureOpenAI for development
class AzureOpenAIMock:
    def __init__(self, api_key=None, api_version=None, azure_endpoint=None, proxies=None, **kwargs):
        # Accept any parameters, including 'proxies'
        pass
    
    class chat:
        class completions:
            @staticmethod
            def create(**kwargs):
                class MockResponse:
                    def __init__(self):
                        class MockChoice:
                            def __init__(self):
                                class MockMessage:
                                    def __init__(self):
                                        self.content = "This is a mock response for development mode."
                                self.message = MockMessage()
                        self.choices = [MockChoice()]
                return MockResponse()

# Try to import real AzureOpenAI, fall back to mock if not available
try:
    from openai import AzureOpenAI
except (ImportError, AttributeError):
    AzureOpenAI = AzureOpenAIMock

logger = get_logger(__name__)

class RAGEngine:
    def __init__(self, embedding_generator=None, vector_storage=None, db_manager=None):
        self.embedding_generator = embedding_generator or EmbeddingGenerator()
        self.vector_storage = vector_storage or VectorStorage()
        self.db_manager = db_manager or DatabaseManager(settings.DATABASE_PATH)
        
        self.client = self._create_azure_client()
        
    def _create_azure_client(self):
        """Create an Azure OpenAI client for completions."""
        try:
            # For development, we can use mocked responses
            if not settings.AZURE_OPENAI_API_KEY or not settings.AZURE_OPENAI_ENDPOINT:
                logger.warning("Azure OpenAI credentials not provided. Using development mode.")
                return None
                
            # Create a simple client with the minimal required parameters
            # This avoids any potential issues with unexpected parameters
            return AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version="2025-01-01-preview",
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )
        except Exception as e:
            logger.error(f"Error creating Azure OpenAI client: {e}")
            return None
        
    def process_query(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Process a user query."""
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_generator.generate_embedding(query)
            if not query_embedding:
                logger.error("Failed to generate embedding for query")
                return {
                    "response": "Sorry, I couldn't process your query. Please try again.",
                    "sources": []
                }
                
            # Find similar vectors
            similar_vectors = self.vector_storage.query_vectors(query_embedding, n_results=n_results)
            
            # Check if we got results
            if not similar_vectors or not similar_vectors['ids'] or not similar_vectors['ids'][0]:
                logger.warning("No similar vectors found for query")
                return {
                    "response": "I couldn't find any relevant vulnerabilities in my database.",
                    "sources": []
                }
                
            # Get the full vulnerability details for each result
            vulnerability_ids = []
            for metadata in similar_vectors['metadatas'][0]:
                vulnerability_ids.append(metadata['vulnerability_id'])
                
            vulnerabilities = []
            for vid in vulnerability_ids:
                vuln = self.db_manager.get_vulnerability_by_id(vid)
                if vuln:
                    vulnerabilities.append(vuln)
                    
            if not vulnerabilities:
                logger.warning("No vulnerabilities found for the matched vectors")
                return {
                    "response": "I found some matches but couldn't retrieve the vulnerability details.",
                    "sources": []
                }
                    
            # Generate context for the model
            context = self._prepare_context(vulnerabilities)
            
            # Generate a response using the context
            response = self._generate_response(query, context)
            
            return {
                "response": response,
                "sources": vulnerabilities
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "response": "An error occurred while processing your query. Please try again later.",
                "sources": []
            }
        
    def _prepare_context(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        """Prepare context from vulnerabilities for the model."""
        context_parts = []
        for idx, vuln in enumerate(vulnerabilities):
            context_parts.append(f"""
Vulnerability #{idx+1}:
ID: {vuln.get('id', 'Unknown')}
Package: {vuln.get('package', 'Unknown')}
Severity: {vuln.get('severity', 'Unknown')}
Published Date: {vuln.get('published_date', 'Unknown')}
Description: {vuln.get('description', 'No description')}
Affected Versions: {vuln.get('affected_versions', 'Not specified')}
Remediation: {vuln.get('remediation', 'Not specified')}
            """)
        
        return "\n\n".join(context_parts)
        
    def _generate_response(self, query: str, context: str) -> str:
        """Generate a response using AzureOpenAI."""
        if not self.client:
            logger.warning("AzureOpenAI client for completions is not initialized - using development mode")
            # In development mode, return a mock response
            return f"This is a development mode response. I found information about several vulnerabilities that might be relevant to your query about '{query}'."
            
        prompt_template = """
You are a security advisor specializing in Python package vulnerabilities.

Use the following vulnerability information to answer the user's question:

{context}

User question: {query}

Provide a concise and informative response that directly addresses the user's question.
Focus on practical advice and clear explanations. If the information is not available 
in the provided context, say so instead of making up information.

Remember to cite your sources by referring to the vulnerability IDs when providing specific information.
        """
        
        prompt = prompt_template.format(context=context, query=query)
        
        try:
            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_COMPLETIONS_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "You are a security advisor specializing in Python package vulnerabilities."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error while generating a response."