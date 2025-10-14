"""
Script to test the improved Snyk vulnerability scraper.
This script runs the scraper on a limited number of pages and prints the results.
"""
import json
import sys
import os
from pprint import pprint

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.scraper import SnykScraper
from app.core.config import settings

def test_scraper(pages=1):
    """Test the Snyk scraper on a limited number of pages."""
    print(f"Testing Snyk scraper for {pages} page(s)...")
    
    scraper = SnykScraper(base_url="https://security.snyk.io/vuln/pip/")
    
    # Just parse the data without storing in the database
    all_vulnerabilities = []
    
    for page in range(1, pages + 1):
        print(f"Fetching page {page}...")
        html_content = scraper.fetch_page(page)
        if html_content:
            print(f"Parsing vulnerabilities from page {page}...")
            vulnerabilities = scraper.parse_vulnerabilities(html_content)
            all_vulnerabilities.extend(vulnerabilities)
            print(f"Found {len(vulnerabilities)} vulnerabilities on page {page}")
        else:
            print(f"Failed to fetch content for page {page}")
    
    print(f"\nTotal vulnerabilities found: {len(all_vulnerabilities)}")
    
    if all_vulnerabilities:
        print("\nSample vulnerability data:")
        pprint(all_vulnerabilities[0])
        
        # Save all vulnerabilities to a JSON file for inspection
        with open('scraped_vulnerabilities.json', 'w') as f:
            json.dump(all_vulnerabilities, f, indent=4)
        print("\nAll vulnerabilities saved to 'scraped_vulnerabilities.json'")

if __name__ == "__main__":
    # Default to 1 page for testing
    pages = 1
    
    # Check if a command-line argument was provided for number of pages
    if len(sys.argv) > 1:
        try:
            pages = int(sys.argv[1])
        except ValueError:
            print("Invalid number of pages. Using default of 1.")
    
    test_scraper(pages)