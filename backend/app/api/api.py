from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.endpoints import vulnerabilities, query

api_router = APIRouter()
api_router.include_router(vulnerabilities.router, prefix="/vulnerabilities", tags=["vulnerabilities"])
api_router.include_router(query.router, prefix="/query", tags=["query"])

@api_router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for Docker healthcheck"""
    return JSONResponse(content={"status": "healthy"}, status_code=200)
