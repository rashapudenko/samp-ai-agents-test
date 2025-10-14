from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import threading

from app.api.api import api_router
from app.core.config import settings
from app.core.logger import get_logger
from app.scraper_job import run_full_job

logger = get_logger(__name__)

# test
# Create FastAPI app
app = FastAPI(title="Security Vulnerabilities Knowledge Base")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)

# Run initial data scraping in a separate thread to avoid blocking app startup
def run_initial_scraping():
    logger.info("Starting initial data scraping")
    run_full_job(pages=settings.SCRAPER_PAGES_TO_FETCH)
    logger.info("Initial data scraping completed")

# Start scraping thread on app startup
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up")
    scraping_thread = threading.Thread(target=run_initial_scraping)
    scraping_thread.daemon = True  # Allow the thread to be terminated when the app stops
    scraping_thread.start()
    logger.info("Initial data scraping thread started")

@app.get("/")
async def root():
    return {"message": "Security Vulnerabilities Knowledge Base API"}

if __name__ == "__main__":
    logger.info(f"Starting server on {settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
