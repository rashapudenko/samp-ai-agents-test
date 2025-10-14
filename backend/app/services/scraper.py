from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import time
import os
from datetime import datetime
import re
import uuid

from app.core.logger import get_logger
from app.core.config import settings
from app.services.database import DatabaseManager

logger = get_logger(__name__)

class SnykScraper:
    def __init__(self, base_url=None, db_manager=None):
        self.base_url = base_url or settings.SNYK_BASE_URL
        self.db_manager = db_manager or DatabaseManager(settings.DATABASE_PATH)
        self.logger = logger
        
    def fetch_page(self, page_num=1):
        """Fetch a page from the Snyk vulnerability database."""
        url = f"{self.base_url}?page={page_num}"
        try:
            self.logger.info(f"Fetching page {page_num} from {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.text
            else:
                self.logger.error(f"Failed to fetch page {page_num}. Status code: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Exception while fetching page {page_num}: {e}")
            return None
            
    def parse_vulnerabilities(self, html_content):
        """Parse the HTML content to extract vulnerabilities."""
        if not html_content:
            return []
            
        soup = BeautifulSoup(html_content, 'html.parser')
        vulnerabilities = []
        
        # Based on our analysis, vulnerabilities are in table rows with class="table__row"
        vuln_elements = soup.select('.vulns-table tbody tr')
        
        for element in vuln_elements:
            try:
                # Extract the vulnerability ID from the link href
                vuln_link = element.select_one('a[href^="/vuln/"]')
                if vuln_link:
                    vuln_id = vuln_link.get('href').split('/')[-1]
                else:
                    vuln_id = str(uuid.uuid4())
                
                # Extract the severity from the severity indicator
                # The severity is in an abbreviation element with class="severity__text"
                severity_elem = element.select_one('.severity__text')
                if severity_elem:
                    # Severity appears as a single letter (H, C, M, L)
                    severity_letter = severity_elem.text.strip()
                    # Map to full severity name
                    severity_map = {
                        'C': 'Critical',
                        'H': 'High',
                        'M': 'Medium',
                        'L': 'Low'
                    }
                    severity = severity_map.get(severity_letter, 'Unknown')
                else:
                    severity = 'Unknown'
                
                # Extract the vulnerability title
                title_elem = element.select_one('a[data-snyk-cy-test="vuln table title"]')
                description = title_elem.text.strip() if title_elem else "No description available"
                
                # Extract the package name
                package_elem = element.select_one('a[data-snyk-test-package-manager="pip"]')
                package = package_elem.text.strip() if package_elem else "Unknown"
                
                # Extract the affected versions
                semver_elem = element.select_one('.vulns-table__semver')
                affected_versions = semver_elem.text.strip() if semver_elem else None
                
                # Extract the published date
                date_elem = element.select_one('.table__data-cell--last-column')
                if date_elem:
                    published_date = date_elem.text.strip()
                else:
                    published_date = datetime.now().strftime("%d %b %Y")
                
                # Get the details URL for fetching additional information
                details_url = None
                if vuln_link:
                    details_url = f"https://security.snyk.io{vuln_link.get('href')}"
                
                remediation = None
                
                # If we have a details URL, fetch additional information
                if details_url:
                    details_data = self._fetch_vulnerability_details(details_url)
                    if details_data:
                        # We already got affected versions from the list page, but we might get more detailed info here
                        if details_data.get('affected_versions'):
                            affected_versions = details_data.get('affected_versions')
                        remediation = details_data.get('remediation')
                
                vuln = {
                    'id': vuln_id,
                    'package': package,
                    'severity': severity,
                    'description': description,
                    'published_date': published_date,
                    'affected_versions': affected_versions,
                    'remediation': remediation,
                }
                
                vulnerabilities.append(vuln)
                self.logger.debug(f"Parsed vulnerability: {vuln['id']} - {vuln['package']}")
                
            except Exception as e:
                self.logger.error(f"Error parsing vulnerability element: {e}")
                self.logger.error(f"Element HTML: {element}")
        
        return vulnerabilities
    
    def _fetch_vulnerability_details(self, details_url):
        """Fetch additional details for a vulnerability."""
        try:
            # Add a small delay to be respectful to the server
            time.sleep(1)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(details_url, headers=headers)
            
            if response.status_code != 200:
                self.logger.warning(f"Failed to fetch details from {details_url}. Status code: {response.status_code}")
                return None
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # The actual selectors might need adjustment based on the details page structure
            # We'll look for common patterns where this information might be found
            affected_versions = None
            remediation = None
            
            # Look for affected versions
            # Try different potential selectors
            affected_versions_selectors = [
                '.vulnerable-versions',
                '.affected-versions',
                '.vulnerability-versions',
                'h2:contains("Affected Versions") + div',
                '.version-info'
            ]
            
            for selector in affected_versions_selectors:
                try:
                    elem = soup.select_one(selector)
                    if elem and elem.text.strip():
                        affected_versions = elem.text.strip()
                        break
                except:
                    continue
            
            # Look for remediation info
            remediation_selectors = [
                '.remediation',
                '.remediation-info',
                '.remediation-action',
                'h2:contains("Remediation") + div',
                '.fix-info'
            ]
            
            for selector in remediation_selectors:
                try:
                    elem = soup.select_one(selector)
                    if elem and elem.text.strip():
                        remediation = elem.text.strip()
                        break
                except:
                    continue
                    
            # If we still don't have remediation info, try to find paragraphs that mention remediation
            if not remediation:
                for p in soup.find_all('p'):
                    text = p.text.lower()
                    if 'remediate' in text or 'fix' in text or 'update' in text or 'upgrade' in text:
                        remediation = p.text.strip()
                        break
            
            return {
                'affected_versions': affected_versions,
                'remediation': remediation
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching vulnerability details: {e}")
            return None
    
    def store_vulnerabilities(self, vulnerabilities):
        """Store vulnerabilities in the database."""
        if not vulnerabilities:
            self.logger.warning("No vulnerabilities to store.")
            return 0
        
        stored_count = 0
        for vuln in vulnerabilities:
            try:
                # Check if vulnerability already exists
                existing_vuln = self.db_manager.get_vulnerability_by_id(vuln['id'])
                
                if not existing_vuln:
                    # Store new vulnerability
                    self.db_manager.create_vulnerability(vuln)
                    stored_count += 1
                    self.logger.debug(f"Stored vulnerability: {vuln['id']} - {vuln['package']}")
                else:
                    # Update existing vulnerability
                    self.db_manager.update_vulnerability(vuln['id'], vuln)
                    self.logger.debug(f"Updated vulnerability: {vuln['id']} - {vuln['package']}")
            
            except Exception as e:
                self.logger.error(f"Error storing vulnerability {vuln.get('id', 'unknown')}: {e}")
        
        self.logger.info(f"Stored {stored_count} new vulnerabilities.")
        return stored_count
    
    def run_scraper(self, pages=None):
        """Run the scraper for multiple pages."""
        pages_to_fetch = pages or settings.SCRAPER_PAGES_TO_FETCH
        all_vulnerabilities = []
        
        self.logger.info(f"Starting scraper for {pages_to_fetch} pages")
        
        for page in range(1, pages_to_fetch + 1):
            html_content = self.fetch_page(page)
            if html_content:
                vulnerabilities = self.parse_vulnerabilities(html_content)
                all_vulnerabilities.extend(vulnerabilities)
                self.logger.info(f"Parsed {len(vulnerabilities)} vulnerabilities from page {page}")
            else:
                self.logger.warning(f"No content fetched for page {page}")
            
            # Add a delay between requests to be respectful to the server
            # time.sleep(2)
        
        # Store the vulnerabilities in the database
        stored_count = self.store_vulnerabilities(all_vulnerabilities)
        
        self.logger.info(f"Scraping completed. Total vulnerabilities found: {len(all_vulnerabilities)}, Stored: {stored_count}")
        return len(all_vulnerabilities), stored_count