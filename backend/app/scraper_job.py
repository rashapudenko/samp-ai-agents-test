import argparse
import time
import schedule
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.scraper import SnykScraper
from app.services.database import DatabaseManager
from app.services.embedding import EmbeddingGenerator, VectorStorage, EmbeddingService
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

def run_scraper_job(pages=None):
    """Run the scraper job to fetch and process vulnerability data."""
    try:
        logger.info("Starting thescraper job")
        
        # Initialize services
        db_manager = DatabaseManager(settings.DATABASE_PATH)
        scraper = SnykScraper(base_url=settings.SNYK_BASE_URL, db_manager=db_manager)
        
        # Run the scraper
        total_count, stored_count = scraper.run_scraper(pages=pages or settings.SCRAPER_PAGES_TO_FETCH)
        
        logger.info(f"Scraper job completed. Found: {total_count}, Stored: {stored_count}")
        
        return total_count, stored_count
    except Exception as e:
        logger.error(f"Error in scraper job: {e}")
        return 0, 0

def run_embedding_job():
    """Run the embedding job to create embeddings for vulnerabilities."""
    try:
        logger.info("Starting embedding job")
        
        # Initialize services
        db_manager = DatabaseManager(settings.DATABASE_PATH)
        embedding_generator = EmbeddingGenerator()
        vector_storage = VectorStorage()
        embedding_service = EmbeddingService(
            db_manager=db_manager,
            embedding_generator=embedding_generator,
            vector_storage=vector_storage
        )
        
        # Process vulnerabilities
        processed_count, failed_count = embedding_service.process_all_vulnerabilities()
        
        logger.info(f"Embedding job completed. Processed: {processed_count}, Failed: {failed_count}")
        
        return processed_count, failed_count
    except Exception as e:
        logger.error(f"Error in embedding job: {e}")
        return 0, 0

def run_full_job(pages=None):
    """Run both scraper and embedding jobs."""
    total_count, stored_count = run_scraper_job(pages)
    if stored_count > 0:
        # Only run embedding job if new vulnerabilities were stored
        processed_count, failed_count = run_embedding_job()
    else:
        processed_count, failed_count = 0, 0
        
    logger.info(f"Full job completed. Scraped: {total_count}, Stored: {stored_count}, "
                f"Processed for embeddings: {processed_count}, Failed embeddings: {failed_count}")

def schedule_jobs(interval_hours=24):
    """Schedule jobs to run at regular intervals."""
    logger.info(f"Scheduling jobs to run every {interval_hours} hours")
    
    # Schedule the full job
    schedule.every(interval_hours).hours.do(run_full_job)
    
    # Run the job immediately on startup
    run_full_job()
    
    # Keep running the scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run scraper and embedding jobs")
    parser.add_argument("--scrape", action="store_true", help="Run scraper job")
    parser.add_argument("--embed", action="store_true", help="Run embedding job")
    parser.add_argument("--full", action="store_true", help="Run both scraper and embedding jobs")
    parser.add_argument("--schedule", type=int, help="Schedule jobs to run every N hours")
    parser.add_argument("--pages", type=int, help="Number of pages to scrape")
    
    args = parser.parse_args()
    
    if args.scrape:
        run_scraper_job(args.pages)
    elif args.embed:
        run_embedding_job()
    elif args.full:
        run_full_job(args.pages)
    elif args.schedule:
        schedule_jobs(args.schedule)
    else:
        # Default: run both jobs once
        run_full_job(args.pages)