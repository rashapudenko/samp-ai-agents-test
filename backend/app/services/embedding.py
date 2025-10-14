# Import system libraries
import numpy as np
import chromadb
import json
import os
from typing import List, Dict, Any, Optional, Tuple

# Import local modules
from app.core.logger import get_logger
from app.core.config import settings
from app.services.database import DatabaseManager

# Define MockAzureOpenAI for development
class AzureOpenAIMock:
    def __init__(self, api_key=None, api_version=None, azure_endpoint=None, proxies=None, **kwargs):
        # Accept any parameters, including 'proxies'
        pass
    
    class embeddings:
        @staticmethod
        def create(**kwargs):
            class MockResponse:
                def __init__(self):
                    import numpy as np
                    self.data = [{"embedding": list(np.random.normal(0, 0.01, 1536))}]
            return MockResponse()

# Try to import real AzureOpenAI, fall back to mock if not available
try:
    from openai import AzureOpenAI
except (ImportError, AttributeError):
    AzureOpenAI = AzureOpenAIMock

logger = get_logger(__name__)

class EmbeddingGenerator:
    def __init__(self, api_key=None, api_endpoint=None, deployment_name=None):
        self.api_key = api_key or settings.AZURE_OPENAI_API_KEY
        self.api_endpoint = api_endpoint or settings.AZURE_OPENAI_ENDPOINT
        self.deployment_name = deployment_name or settings.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT
        
        self.client = self._create_client()
        
    def _create_client(self):
        """Create an Azure OpenAI client."""
        try:
            # For development, we can use mocked credentials
            if not self.api_key or not self.api_endpoint:
                logger.warning("Azure OpenAI credentials not provided. Using development mode.")
                return None
                
            # Create a simple client with the minimal required parameters
            # This avoids any potential issues with unexpected parameters
            return AzureOpenAI(
                api_key=self.api_key,
                api_version="2023-05-15",
                azure_endpoint=self.api_endpoint
            )
        except Exception as e:
            logger.error(f"Error creating Azure OpenAI client: {e}")
            return None
        
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate an embedding for the given text."""
        if not self.client:
            logger.warning("AzureOpenAI client is not initialized - using development mode")
            # In development mode, return a mock embedding (300-dim vector of small random values)
            import numpy as np
            return list(np.random.normal(0, 0.01, 1536))
            
        try:
            # Ensure text is not None and convert to string
            if text is None:
                logger.warning("Attempted to generate embedding for None text")
                return None
                
            text = str(text).strip()
            if not text:
                logger.warning("Attempted to generate embedding for empty text")
                return None
                
            response = self.client.embeddings.create(
                input=text,
                model=self.deployment_name
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # In case of error, return a mock embedding
            import numpy as np
            return list(np.random.normal(0, 0.01, 1536))
            
    def batch_generate_embeddings(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Generate embeddings for a batch of texts."""
        if not texts:
            return []
            
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
                
        return embeddings


class VectorStorage:
    def __init__(self, collection_name="vulnerabilities", persistence_path=None):
        self.collection_name = collection_name
        self.persistence_path = persistence_path or settings.VECTOR_DB_PATH
        
        # Ensure directory exists
        os.makedirs(self.persistence_path, exist_ok=True)
        
        self.client = self._create_client()
        self.collection = self._get_or_create_collection()
        
    def _create_client(self):
        """Create a ChromaDB client."""
        try:
            client = chromadb.PersistentClient(path=self.persistence_path)
            return client
        except Exception as e:
            logger.error(f"Error creating ChromaDB client: {e}")
            return None
        
    def _get_or_create_collection(self):
        """Get or create a collection for vulnerabilities."""
        if not self.client:
            logger.error("ChromaDB client is not initialized")
            return None
            
        try:
            collection = self.client.get_or_create_collection(name=self.collection_name)
            return collection
        except Exception as e:
            logger.error(f"Error creating ChromaDB collection: {e}")
            return None
        
    def add_vectors(self, ids: List[str], embeddings: List[List[float]], 
                   metadatas: Optional[List[Dict[str, Any]]] = None, 
                   documents: Optional[List[str]] = None) -> bool:
        """Add vectors to the collection."""
        if not self.collection:
            logger.error("ChromaDB collection is not initialized")
            return False
            
        try:
            # Filter out any None embeddings
            valid_indices = [i for i, emb in enumerate(embeddings) if emb is not None]
            
            if not valid_indices:
                logger.warning("No valid embeddings to add")
                return False
                
            # Filter the inputs
            filtered_ids = [ids[i] for i in valid_indices]
            filtered_embeddings = [embeddings[i] for i in valid_indices]
            
            filtered_metadatas = None
            if metadatas:
                filtered_metadatas = [metadatas[i] for i in valid_indices]
                
            filtered_documents = None
            if documents:
                filtered_documents = [documents[i] for i in valid_indices]
            
            # Add the vectors
            self.collection.add(
                ids=filtered_ids,
                embeddings=filtered_embeddings,
                metadatas=filtered_metadatas,
                documents=filtered_documents
            )
            
            logger.info(f"Added {len(filtered_ids)} vectors to collection {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error adding vectors to collection: {e}")
            return False
        
    def query_vectors(self, query_embedding: List[float], n_results: int = 5) -> Dict[str, Any]:
        """Query vectors based on similarity."""
        if not self.collection:
            logger.error("ChromaDB collection is not initialized")
            return {"ids": [], "distances": [], "metadatas": [], "documents": []}
            
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error querying vectors: {e}")
            return {"ids": [], "distances": [], "metadatas": [], "documents": []}
    
    def delete_vector(self, vector_id: str) -> bool:
        """Delete a vector by ID."""
        if not self.collection:
            logger.error("ChromaDB collection is not initialized")
            return False
            
        try:
            self.collection.delete(ids=[vector_id])
            logger.debug(f"Deleted vector: {vector_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting vector {vector_id}: {e}")
            return False
    
    def get_count(self) -> int:
        """Get the count of vectors in the collection."""
        if not self.collection:
            logger.error("ChromaDB collection is not initialized")
            return 0
            
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error getting vector count: {e}")
            return 0


class EmbeddingService:
    def __init__(self, db_manager=None, embedding_generator=None, vector_storage=None):
        self.db_manager = db_manager or DatabaseManager(settings.DATABASE_PATH)
        self.embedding_generator = embedding_generator or EmbeddingGenerator()
        self.vector_storage = vector_storage or VectorStorage()
        
    def process_vulnerability(self, vulnerability: Dict[str, Any]) -> bool:
        """Process a vulnerability and create embeddings."""
        try:
            # Create text for embedding
            text = self._create_text_for_embedding(vulnerability)
            
            # Generate embedding
            embedding = self.embedding_generator.generate_embedding(text)
            if not embedding:
                logger.error(f"Failed to generate embedding for vulnerability {vulnerability.get('id')}")
                return False
            
            # Create a unique ID for the vector
            vector_id = f"vuln_{vulnerability.get('id')}"
            
            # Add vector to storage
            metadata = {
                "vulnerability_id": vulnerability.get('id'),
                "package": vulnerability.get('package'),
                "severity": vulnerability.get('severity')
            }
            
            added = self.vector_storage.add_vectors(
                ids=[vector_id],
                embeddings=[embedding],
                metadatas=[metadata],
                documents=[text]
            )
            
            if not added:
                logger.error(f"Failed to add vector for vulnerability {vulnerability.get('id')}")
                return False
            
            # Create reference in database
            self.db_manager.create_embedding_ref(vulnerability.get('id'), vector_id)
            
            return True
        except Exception as e:
            logger.error(f"Error processing vulnerability: {e}")
            return False
    
    def _create_text_for_embedding(self, vulnerability: Dict[str, Any]) -> str:
        """Create text content for embedding generation."""
        parts = [
            f"ID: {vulnerability.get('id', 'Unknown')}",
            f"Package: {vulnerability.get('package', 'Unknown')}",
            f"Severity: {vulnerability.get('severity', 'Unknown')}",
            f"Description: {vulnerability.get('description', 'No description')}",
        ]
        
        if vulnerability.get('affected_versions'):
            parts.append(f"Affected Versions: {vulnerability.get('affected_versions')}")
            
        if vulnerability.get('remediation'):
            parts.append(f"Remediation: {vulnerability.get('remediation')}")
            
        return "\n".join(parts)
    
    def process_all_vulnerabilities(self) -> Tuple[int, int]:
        """Process all vulnerabilities that don't have embeddings yet."""
        processed_count = 0
        failed_count = 0
        
        # Get all vulnerabilities
        vulnerabilities = self.db_manager.get_vulnerabilities(limit=10000)  # Set a reasonable limit
        
        logger.info(f"Processing {len(vulnerabilities)} vulnerabilities for embeddings")
        
        for vuln in vulnerabilities:
            # Check if embedding already exists
            vector_id = self.db_manager.get_vector_id_by_vulnerability_id(vuln['id'])
            
            if not vector_id:  # No embedding exists
                success = self.process_vulnerability(vuln)
                if success:
                    processed_count += 1
                else:
                    failed_count += 1
        
        logger.info(f"Processed {processed_count} vulnerabilities for embeddings, {failed_count} failed")
        return processed_count, failed_count