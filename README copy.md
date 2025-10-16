# Security Vulnerabilities Knowledge Base

A comprehensive Retrieval-Augmented Generation (RAG) system that provides context-aware responses about Python package security vulnerabilities. This project enables developers and security professionals to quickly access, query, and understand Python package vulnerabilities through natural language interactions.

## Overview
test more changes
more changes
This project creates an intelligent knowledge base of Python package security vulnerabilities sourced from [Snyk Security](https://security.snyk.io/vuln/pip/). The system combines the power of traditional database storage with modern vector embeddings and AI to deliver:

### Key Features

✨ **Natural Language Queries**: Ask questions in plain English about security vulnerabilities  
🔍 **Advanced Search**: Filter and search vulnerabilities by package, severity, and date  
📊 **Detailed Analysis**: Get comprehensive vulnerability information including:
- Affected package versions
- Severity ratings and CVSS scores
- Detailed remediation steps
- Publication dates and timelines

🤖 **AI-Powered Responses**: Context-aware answers powered by Azure OpenAI  
⚡ **Real-time Data**: Automated scraping keeps vulnerability data current  
🐳 **Docker Support**: Complete containerized deployment for easy setup

## Architecture

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

### Components

🕷️ **Data Scraper & Processor**: Automated web scraping system that:
- Collects vulnerability data from Snyk Security database
- Processes and normalizes vulnerability information
- Generates vector embeddings for semantic search
- Stores data in both structured and vector formats

🗄️ **Vector Database & Storage Layer**: Dual storage system featuring:
- **SQLite**: Fast, reliable structured data storage
- **ChromaDB**: High-performance vector database for semantic similarity search
- Optimized indexing for quick query responses

⚡ **Backend API**: FastAPI-powered REST API that provides:
- `/api/query` - Natural language vulnerability queries
- `/api/vulnerabilities` - Structured vulnerability search
- `/api/health` - System health monitoring
- Real-time RAG processing with Azure OpenAI integration

🖥️ **Frontend**: Modern Next.js React application offering:
- Interactive chat interface for natural language queries
- Advanced search and filtering capabilities
- Responsive design optimized for all devices
- Real-time vulnerability data visualization

## Tech Stack

### 🐍 Backend
- **Python 3.11+** - Modern Python runtime with enhanced performance
- **FastAPI** - High-performance, easy-to-use API framework
- **SQLite** - Lightweight, serverless database engine
- **ChromaDB** - Vector database for embedding storage and similarity search
- **Azure OpenAI API** - GPT-4 and text-embedding models
- **BeautifulSoup4** - Web scraping and HTML parsing
- **Pandas** - Data manipulation and analysis
- **Uvicorn** - Lightning-fast ASGI server

### ⚛️ Frontend
- **Next.js 13+** - React framework with App Router
- **React 18** - Modern React with concurrent features
- **TypeScript** - Type-safe JavaScript development
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - Promise-based HTTP client
- **React Markdown** - Markdown rendering in React

### 🐳 DevOps & Infrastructure
- **Docker & Docker Compose** - Containerized deployment
- **Multi-stage builds** - Optimized container images
- **Health checks** - Container monitoring and reliability
- **Volume management** - Persistent data storage

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following:

- **Docker & Docker Compose** (recommended) OR
- **Python 3.11+** and **Node.js 18+** for local development
- **Azure OpenAI API key and endpoint** ([Get yours here](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/))

### 🐳 Option 1: Docker Setup (Recommended)

The fastest way to get started is using Docker Compose:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd security-vulnerabilities-kb
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Azure OpenAI credentials:
   ```bash
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   ```

3. **Start the application:**
   ```bash
   docker-compose up -d
   ```

4. **Access the application:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

The application will automatically:
- Build optimized Docker images
- Start both frontend and backend services
- Initialize the database
- Begin scraping vulnerability data

### 💻 Option 2: Local Development Setup

For local development without Docker:

#### 🐍 Backend Setup

1. **Clone and navigate to backend:**
   ```bash
   git clone <repository-url>
   cd security-vulnerabilities-kb/backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your Azure OpenAI credentials.

5. **Initialize database and start scraping:**
   ```bash
   python -m app.scraper_job --full
   ```

6. **Start the backend server:**
   ```bash
   python run.py
   ```
   Backend will be available at [http://localhost:8000](http://localhost:8000)

#### ⚛️ Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment:**
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend will be available at [http://localhost:3000](http://localhost:3000)

## 📖 Usage Guide

### 💬 Chat Interface

The AI-powered chat interface allows you to ask natural language questions about Python package vulnerabilities:

**Example Queries:**
- *"What are the most critical vulnerabilities in Django from the last 6 months?"*
- *"How do I fix the SSL verification vulnerability in requests?"*
- *"Show me all high-severity vulnerabilities that affect Flask applications"*
- *"What security issues should I be aware of when using SQLAlchemy?"*
- *"Are there any recent RCE vulnerabilities in popular Python packages?"*

**Features:**
- Natural language processing powered by GPT-4
- Context-aware responses with relevant vulnerability details
- Source citations for all information provided
- Conversation history within your session

### 🔍 Search Interface

The advanced search interface provides structured access to the vulnerability database:

**Search Capabilities:**
- **Package Search**: Find vulnerabilities by specific package names
- **Severity Filtering**: Filter by LOW, MODERATE, HIGH, or CRITICAL severity levels
- **Date Ranges**: Search vulnerabilities by publication date
- **Keyword Search**: Full-text search across vulnerability descriptions

**Browse Features:**
- Paginated results for efficient browsing
- Sortable columns (severity, date, package name)
- Expandable vulnerability details
- Direct links to original Snyk Security entries

### 🔧 API Endpoints

The backend provides RESTful API endpoints for programmatic access:

```bash
# Query vulnerabilities using natural language
POST /api/query
{
  "query": "What are the latest Django vulnerabilities?"
}

# Search vulnerabilities with filters
GET /api/vulnerabilities?package=django&severity=HIGH&limit=10

# Health check
GET /api/health
```

Full API documentation is available at `/docs` when running the backend.

## 🔧 Configuration

### Environment Variables

The application uses the following environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | - | ✅ |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint URL | - | ✅ |
| `AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT` | Embeddings model deployment name | `text-embedding-ada-002` | ❌ |
| `AZURE_OPENAI_COMPLETIONS_DEPLOYMENT` | Chat model deployment name | `gpt-4o` | ❌ |
| `SCRAPER_PAGES_TO_FETCH` | Number of pages to scrape initially | `10` | ❌ |
| `BACKEND_WORKERS` | Number of backend worker processes | `1` | ❌ |

### Performance Tuning

For production deployments, consider:

- **Backend Workers**: Increase `BACKEND_WORKERS` for higher concurrent request handling
- **Scraper Frequency**: Adjust `SCRAPER_PAGES_TO_FETCH` based on your needs
- **Database Optimization**: Use SSDs for better I/O performance
- **Memory Allocation**: Ensure adequate RAM for vector database operations

## 🛠️ Troubleshooting

### Common Issues

#### Docker Issues

**Problem**: Containers fail to start  
**Solution**: 
```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up
```

**Problem**: Port conflicts (3000 or 8000 already in use)  
**Solution**: Update port mappings in `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Use different external port
  frontend:
    ports:
      - "3001:3000"  # Use different external port
```

#### Backend Issues

**Problem**: Azure OpenAI API errors  
**Solution**: 
- Verify your API key and endpoint are correct
- Check your Azure OpenAI quota and limits
- Ensure your deployment names match your Azure configuration

**Problem**: Database connection errors  
**Solution**:
```bash
# Reset database
rm -rf backend/app/data/
docker-compose restart backend
```

**Problem**: Scraping failures  
**Solution**: 
- Check internet connectivity
- Verify Snyk website accessibility
- Reduce `SCRAPER_PAGES_TO_FETCH` if encountering rate limits

#### Frontend Issues

**Problem**: API connection errors  
**Solution**: 
- Verify backend is running on correct port
- Check `NEXT_PUBLIC_API_URL` environment variable
- Ensure CORS settings allow frontend domain

**Problem**: Build failures  
**Solution**:
```bash
# Clean install
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Performance Issues

**Slow query responses**: 
- Check Azure OpenAI service region and performance tier
- Monitor vector database performance
- Consider increasing backend worker count

**High memory usage**: 
- Reduce batch sizes in scraping operations
- Implement pagination for large datasets
- Monitor ChromaDB memory usage

### Getting Help

If you encounter issues:

1. Check the [troubleshooting guide](#troubleshooting) above
2. Review container logs: `docker-compose logs`
3. Verify environment configuration
4. Check network connectivity and API quotas

For persistent issues, please check the project's issue tracker or create a new issue with:
- Environment details (OS, Docker version, etc.)
- Error messages and logs
- Steps to reproduce the problem

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Snyk Security](https://security.snyk.io/vuln/pip/) for providing vulnerability data
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/) for AI capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the backend API framework
- [Next.js](https://nextjs.org/) for the frontend framework