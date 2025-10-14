from fastapi import APIRouter, Depends, HTTPException

from app.models.vulnerability import QueryRequest, QueryResponse
from app.services.rag_engine import RAGEngine
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)
rag_engine = RAGEngine()

@router.post("/", response_model=QueryResponse)
async def query_vulnerabilities(request: QueryRequest):
    """Query vulnerabilities using natural language."""
    try:
        logger.info(f"Processing query: {request.query}")
        
        result = rag_engine.process_query(request.query)
        
        return QueryResponse(
            response=result['response'],
            sources=result['sources']
        )
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
