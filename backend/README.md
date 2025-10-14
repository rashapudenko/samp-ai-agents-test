# Security Vulnerabilities Knowledge Base - Backend

This is the backend API for the Security Vulnerabilities Knowledge Base, a RAG (Retrieval Augmented Generation) application that provides information about Python package vulnerabilities.

## Features

- Scrapes vulnerability data from [Snyk Security](https://security.snyk.io/vuln/pip/)
- Stores vulnerability data in SQLite database
- Generates embeddings using Azure OpenAI API
- Stores embeddings in ChromaDB vector database
- Provides a REST API for querying vulnerabilities
- Uses RAG to generate responses to natural language queries

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and update the configuration values:
   ```
   cp .env.example .env
   ```
5. Configure your Azure OpenAI API key and endpoint in the `.env` file

## Configuration

The application is configured using environment variables. See `.env.example` for all available options.

Key configuration options:
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT`: The name of your Azure OpenAI embeddings deployment
- `AZURE_OPENAI_COMPLETIONS_DEPLOYMENT`: The name of your Azure OpenAI completions deployment
- `DATABASE_PATH`: Path to the SQLite database file
- `VECTOR_DB_PATH`: Path to the ChromaDB vector database directory

## Usage

### Running the API server

```
python run.py
```

This will start the FastAPI server on `http://localhost:8000`.

### Running the scraper

To fetch vulnerability data:

```
python -m app.scraper_job --scrape
```

To process fetched vulnerabilities and create embeddings:

```
python -m app.scraper_job --embed
```

To do both (recommended):

```
python -m app.scraper_job --full
```

To schedule regular updates (every 24 hours):

```
python -m app.scraper_job --schedule 24
```

### Testing the scraper

To test the scraper without saving to the database:

```
python -m app.test_scraper 2  # Scrape 2 pages
```

## Scraper Implementation

The scraper has been updated to correctly parse the Snyk vulnerabilities website structure. Key improvements:

1. **Proper CSS selectors**: Updated to match the current Snyk website structure
   - Uses `.vulns-table tbody tr` to find vulnerability rows
   - Extracts vulnerability ID from links with `a[href^="/vuln/"]`
   - Maps severity abbreviations (C, H, M, L) to full names (Critical, High, Medium, Low)

2. **Data Extraction**:
   - Vulnerability title from `a[data-snyk-cy-test="vuln table title"]`
   - Package name from `a[data-snyk-test-package-manager="pip"]`
   - Affected versions from `.vulns-table__semver`
   - Published date from `.table__data-cell--last-column`

3. **Details Retrieval**:
   - Fetches additional information from individual vulnerability pages
   - Uses multiple selectors to handle different page layouts
   - Implements fallbacks to find remediation information

4. **Error Handling and Logging**:
   - Comprehensive error handling
   - Detailed logging for debugging
   - Rate limiting to be respectful to the Snyk server

## API Endpoints

### Query Vulnerabilities

```
POST /api/query
```

Request body:
```json
{
  "query": "What are the latest vulnerabilities in Django?"
}
```

### Get Vulnerabilities

```
GET /api/vulnerabilities?package=django&severity=critical&limit=10&offset=0
```

Parameters:
- `package`: Filter by package name
- `severity`: Filter by severity level
- `limit`: Limit results (default: 10, max: 100)
- `offset`: Pagination offset

### Get Vulnerability Details

```
GET /api/vulnerabilities/{vulnerability_id}
```

### Get Statistics

```
GET /api/vulnerabilities/statistics
```

### Get Packages

```
GET /api/vulnerabilities/packages
```

### Get Severities

```
GET /api/vulnerabilities/severities
```

## Development

To run the API in development mode with auto-reload:

```
python run.py
```

## Scraper Usage

The `SnykScraper` class can be used programmatically:

```python
from app.services.scraper import SnykScraper

# Initialize the scraper
scraper = SnykScraper(base_url="https://security.snyk.io/vuln/pip/")

# Fetch and parse vulnerabilities from a specific page
html_content = scraper.fetch_page(page_num=1)
vulnerabilities = scraper.parse_vulnerabilities(html_content)

# Store vulnerabilities in the database
stored_count = scraper.store_vulnerabilities(vulnerabilities)

# Or run the complete scraping process
total_count, stored_count = scraper.run_scraper(pages=5)
```

## Known Limitations

- The scraper may need periodic updates if the Snyk website structure changes
- Detailed information is limited to what's available on the Snyk website
- Rate limiting is implemented to be respectful to the Snyk website