# Technical Architecture for Security Vulnerabilities RAG Application

## 1. System Architecture Overview

The proposed architecture follows a modern web application pattern with clear separation of concerns between data collection, storage, processing, and presentation layers:

```
┌────────────────┐    ┌─────────────────────┐    ┌────────────────────┐
│                │    │                     │    │                    │
│  Data Scraper  │───►│  Vector Database    │◄───┤  Backend API       │
│  & Processor   │    │  & Storage Layer    │    │  (FastAPI)         │
│                │    │                     │    │                    │
└────────────────┘    └─────────────────────┘    └─────────┬──────────┘
                                                           │
                                                           ▼
                                                 ┌─────────────────────┐
                                                 │                     │
                                                 │  Frontend           │
                                                 │  (Next.js + React)  │
                                                 │                     │
                                                 └─────────────────────┘
```

The architecture consists of four main components:

1. **Data Scraper & Processor**: Collects vulnerability data from Snyk, processes it, and generates embeddings
2. **Storage Layer**: Stores raw vulnerability data and vector embeddings
3. **Backend API**: Handles user queries and retrieval logic
4. **Frontend**: Provides user interface for querying vulnerabilities

## 2. Key Technologies and Frameworks

### Frontend
- **Next.js**: React framework for server-rendered React applications
- **React**: JavaScript library for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- **Axios**: HTTP client for API requests

### Backend
- **FastAPI**: Modern, high-performance web framework for building APIs
- **SQLite**: Lightweight database for storing vulnerability data
- **ChromaDB** or **FAISS**: Vector database for storing and querying embeddings
- **BeautifulSoup**: For web scraping the vulnerability data from Snyk
- **AzureOpenAI**: For generating embeddings and chat completions
- **Langchain**: Framework for developing applications powered by language models

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing tools
- **Scikit-learn**: Additional ML utilities if needed

## 3. Data Flow Description

### Data Collection & Processing Flow
1. **Scraping**: Regular scheduled jobs use BeautifulSoup to scrape vulnerability data from https://security.snyk.io/vuln/pip/
2. **Data Processing**: Raw HTML is parsed to extract structured data about vulnerabilities:
   - Vulnerability ID
   - Package name
   - Severity level
   - Description
   - Published date
   - Affected versions
   - Remediation steps
3. **Embedding Generation**: AzureOpenAI generates embeddings for each vulnerability record
4. **Storage**: 
   - Structured data stored in SQLite
   - Embeddings stored in vector database (ChromaDB)

### Query Processing Flow
1. User submits natural language query via the frontend
2. Backend processes query:
   - Generates embedding for user query using AzureOpenAI
   - Performs similarity search in vector database to find relevant vulnerabilities
   - Retrieves detailed information from SQLite
3. Backend sends relevant context to AzureOpenAI for response generation
4. Generated response is returned to the frontend
5. Frontend displays the response to the user

## 4. Infrastructure Requirements

### Compute Resources
- **Web Server**: 2 vCPUs, 4GB RAM for frontend and backend services
- **Database Server**: 4GB RAM, 20GB storage for SQLite and vector database
- **Development Environment**: Local development machines with similar specifications

### Storage Requirements
- **Database Storage**: Initially 10GB, scaling as data grows
- **Backup Storage**: Additional 20GB for database backups

### External Services
- **Azure OpenAI API**: Required for embedding generation and chat completions
- **GitHub Actions or similar**: For CI/CD pipeline

### Networking
- HTTPS for secure client-server communication
- API rate limiting to prevent abuse
- Basic authentication for API access

## Backend Components

The backend consists of the following key components:

1. **Data Ingestion Service**:
   - Scheduled scraping jobs using BeautifulSoup
   - Data normalization and cleaning pipelines
   - Embedding generation using AzureOpenAI

2. **FastAPI Application**:
   - RESTful API endpoints for querying vulnerabilities
   - Authentication middleware
   - Rate limiting middleware
   - Query processing logic

3. **Database Access Layer**:
   - SQLite connectors
   - Vector database (ChromaDB) interface
   - Query optimization

4. **RAG Engine**:
   - Query embedding generation
   - Vector similarity search
   - Context retrieval
   - Response generation

## Frontend Components

The frontend is a Next.js application with:

1. **Chat Interface**:
   - Message input
   - Response display
   - Message history

2. **Search Components**:
   - Advanced filters (by severity, package, etc.)
   - Auto-suggestions

3. **Results Display**:
   - Formatted vulnerability information
   - Highlighting key information
   - Expandable details

## Component Interaction

1. Frontend communicates with backend via RESTful API calls
2. Backend queries databases and external services as needed
3. Response flows back through the backend to the frontend

## Scalability, Security, and Performance Considerations

### Scalability
- Containerized deployment for easy scaling
- Separation of concerns allowing independent scaling of components
- Caching common queries to reduce load

### Security
- HTTPS for all communications
- Authentication for API access
- Input validation and sanitization
- Rate limiting to prevent abuse
- Regular security audits

### Performance
- Vector database indexing for fast similarity searches
- Query optimization
- Asynchronous processing where applicable
- Response caching

This architecture provides a solid foundation for a security vulnerability RAG system that meets all the specified requirements while maintaining simplicity and focus on the core functionality.