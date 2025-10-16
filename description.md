Business Requirements for RAG Application: Security Vulnerabilities Knowledge Base

Overview

The objective of the application is to provide rapid, accurate, and context-aware responses regarding security vulnerabilities specifically sourced from package vulnerability listings at https://security.snyk.io/vuln/pip/. This Retrieval-Augmented Generation (RAG) system will parse vulnerability details, store them efficiently, and provide insightful responses through natural language queries.

Functional Requirements

Data Collection

The system must parse security vulnerability data from the Snyk vulnerabilities webpage.

Attributes of the data entries have to be analyzed from the website.

Data Storage

Data must be stored in a structured and query-optimized manner suitable for efficient retrieval in some vector databases 

Storage solution must support:

Rapid full-text search

Vector similarity searches (embeddings)

Efficient querying based on metadata (severity, package, date)

Embeddings Generation

Generate vector embeddings for each parsed vulnerability record.

Utilize pre-trained embedding models suitable for technical and security-related textual data.

Retrieval-Augmented Generation (RAG)

Provide a conversational interface allowing users to query vulnerabilities in natural language.

Generate responses that accurately summarize relevant vulnerabilities and remediation steps.

System must augment responses using relevant vulnerability context from stored data.

Tools to be used:

AzureOpenAI for embeddings and chat completions. You should use openai library

SQLite for database

BeautifulSoup for scraping the data from the website and analyzing the website structure 