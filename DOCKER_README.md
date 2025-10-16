# Docker Setup for Security Vulnerabilities Knowledge Base

This document explains how to run the Security Vulnerabilities Knowledge Base application using Docker.

## Prerequisites

- Docker and Docker Compose installed on your system
- Basic knowledge of Docker commands

## Quick Start

1. Configure the environment variables:
   - Update the values in `backend/.env` with your Azure OpenAI API key and other settings
   - Update the values in `frontend/.env.local` if needed

2. Start the application:
   ```bash
   docker-compose up
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Configuration

### Backend Environment Variables

The backend service uses the following environment variables:

- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT`: The name of your Azure OpenAI embeddings deployment
- `AZURE_OPENAI_COMPLETIONS_DEPLOYMENT`: The name of your Azure OpenAI completions deployment
- `DATABASE_PATH`: Path to the SQLite database file (default: app/data/vulnerabilities.db)
- `VECTOR_DB_PATH`: Path to the ChromaDB vector database directory (default: app/data/vector_db)
- `API_HOST`: Host to listen on (default: 0.0.0.0)
- `API_PORT`: Port to listen on (default: 8000)
- `ALLOWED_ORIGINS`: CORS allowed origins (default: http://localhost:3000)

### Frontend Environment Variables

The frontend service uses the following environment variables:

- `NEXT_PUBLIC_API_URL`: URL of the backend API (default: http://localhost:8000)

## First-time Setup

Before using the application, you need to populate the database with vulnerability data. After starting the containers:

1. Connect to the backend container:
   ```bash
   docker-compose exec backend bash
   ```

2. Run the scraper job:
   ```bash
   python -m app.scraper_job --full
   ```

This will fetch vulnerability data and generate embeddings.

## Development Workflow

The Docker Compose setup mounts the local directories as volumes in the containers, so any changes you make to the code will be reflected in the containers.

### Backend Development

After making changes to the backend code:
- The changes will be automatically reloaded by the FastAPI server

### Frontend Development

After making changes to the frontend code:
- The changes will be automatically reloaded by the Next.js development server