import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def mock_rag_engine():
    """Create a mock RAG engine."""
    with patch('app.api.endpoints.query.rag_engine') as mock:
        yield mock


class TestQueryEndpoint:
    """Test cases for the query API endpoint."""
    
    def test_query_vulnerabilities_success(self, client, mock_rag_engine):
        """Test successful query processing."""
        # Mock the RAG engine response
        mock_response = {
            'response': 'Django has several known vulnerabilities including SQL injection and XSS.',
            'sources': [
                {
                    'id': 'django-1',
                    'package': 'django',
                    'severity': 'high',
                    'description': 'SQL injection vulnerability in Django ORM',
                    'published_date': '2023-01-01',
                    'affected_versions': '>=2.0.0,<3.2.0',
                    'remediation': 'Update to Django 3.2.0 or later'
                }
            ]
        }
        mock_rag_engine.process_query.return_value = mock_response
        
        # Make request
        query_data = {"query": "What vulnerabilities exist in Django?"}
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data['response'] == mock_response['response']
        assert len(data['sources']) == 1
        assert data['sources'][0]['package'] == 'django'
        
        # Verify RAG engine was called with correct query
        mock_rag_engine.process_query.assert_called_once_with("What vulnerabilities exist in Django?")
    
    def test_query_vulnerabilities_empty_query(self, client, mock_rag_engine):
        """Test query with empty string."""
        mock_response = {
            'response': 'Please provide a specific question about security vulnerabilities.',
            'sources': []
        }
        mock_rag_engine.process_query.return_value = mock_response
        
        query_data = {"query": ""}
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert 'Please provide' in data['response']
        assert data['sources'] == []
    
    def test_query_vulnerabilities_complex_query(self, client, mock_rag_engine):
        """Test complex query with multiple packages."""
        mock_response = {
            'response': 'Both requests and urllib3 have had critical vulnerabilities. Requests versions before 2.28.0 are affected by SSL certificate verification bypass. urllib3 has connection pool issues in versions before 1.26.5.',
            'sources': [
                {
                    'id': 'requests-1',
                    'package': 'requests',
                    'severity': 'critical',
                    'description': 'SSL certificate verification bypass',
                    'published_date': '2022-05-01',
                    'affected_versions': '<2.28.0',
                    'remediation': 'Update to requests 2.28.0 or later'
                },
                {
                    'id': 'urllib3-1',
                    'package': 'urllib3',
                    'severity': 'high',
                    'description': 'Connection pool vulnerability',
                    'published_date': '2021-03-15',
                    'affected_versions': '<1.26.5',
                    'remediation': 'Update to urllib3 1.26.5 or later'
                }
            ]
        }
        mock_rag_engine.process_query.return_value = mock_response
        
        query_data = {"query": "Compare vulnerabilities between requests and urllib3 libraries"}
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert 'requests' in data['response']
        assert 'urllib3' in data['response']
        assert len(data['sources']) == 2
        
        packages = [source['package'] for source in data['sources']]
        assert 'requests' in packages
        assert 'urllib3' in packages
    
    def test_query_vulnerabilities_no_results(self, client, mock_rag_engine):
        """Test query that returns no vulnerability sources."""
        mock_response = {
            'response': 'I could not find any specific vulnerability information for the obscure-package in the knowledge base.',
            'sources': []
        }
        mock_rag_engine.process_query.return_value = mock_response
        
        query_data = {"query": "Are there vulnerabilities in obscure-package?"}
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert 'could not find' in data['response']
        assert data['sources'] == []
    
    def test_query_vulnerabilities_missing_query_field(self, client):
        """Test request without query field."""
        response = client.post("/api/query/", json={})
        assert response.status_code == 422  # Validation error
        
        error_detail = response.json()['detail']
        assert any('query' in str(error) for error in error_detail)
    
    def test_query_vulnerabilities_invalid_json(self, client):
        """Test request with invalid JSON."""
        response = client.post("/api/query/", data="invalid json")
        assert response.status_code == 422
    
    def test_query_vulnerabilities_wrong_content_type(self, client):
        """Test request with wrong content type."""
        response = client.post("/api/query/", data="query=test")
        assert response.status_code == 422
    
    def test_query_vulnerabilities_additional_fields(self, client, mock_rag_engine):
        """Test that additional fields in request are ignored."""
        mock_response = {
            'response': 'Flask has several security vulnerabilities.',
            'sources': []
        }
        mock_rag_engine.process_query.return_value = mock_response
        
        query_data = {
            "query": "Flask vulnerabilities?",
            "extra_field": "should be ignored",
            "another_field": 123
        }
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 200
        # Should still work despite extra fields
        mock_rag_engine.process_query.assert_called_once_with("Flask vulnerabilities?")
    
    def test_query_vulnerabilities_rag_engine_error(self, client, mock_rag_engine):
        """Test handling of RAG engine errors."""
        # Mock RAG engine to raise an exception
        mock_rag_engine.process_query.side_effect = Exception("RAG engine failed")
        
        query_data = {"query": "What about NumPy vulnerabilities?"}
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 500
        error_detail = response.json()['detail']
        assert "Error processing query" in error_detail
        assert "RAG engine failed" in error_detail
    
    def test_query_vulnerabilities_rag_engine_timeout(self, client, mock_rag_engine):
        """Test handling of RAG engine timeout."""
        # Mock RAG engine to raise a timeout exception
        from concurrent.futures import TimeoutError
        mock_rag_engine.process_query.side_effect = TimeoutError("Query timed out")
        
        query_data = {"query": "Long complex query that might timeout"}
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 500
        error_detail = response.json()['detail']
        assert "Error processing query" in error_detail
    
    def test_query_vulnerabilities_malformed_rag_response(self, client, mock_rag_engine):
        """Test handling of malformed RAG engine response."""
        # Mock RAG engine to return malformed response
        mock_rag_engine.process_query.return_value = {
            'response': 'Valid response',
            # Missing 'sources' field
        }
        
        query_data = {"query": "Test query"}
        response = client.post("/api/query/", json=query_data)
        
        # Should handle gracefully and return 500 error
        assert response.status_code == 500
    
    def test_query_vulnerabilities_with_special_characters(self, client, mock_rag_engine):
        """Test query with special characters and unicode."""
        mock_response = {
            'response': 'Handling special characters: áéíóú, 中文, 🔒',
            'sources': []
        }
        mock_rag_engine.process_query.return_value = mock_response
        
        query_data = {"query": "What about vulnerabilities with special chars: áéíóú, 中文, 🔒?"}
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert '🔒' in data['response']
        mock_rag_engine.process_query.assert_called_once()
    
    def test_query_vulnerabilities_long_query(self, client, mock_rag_engine):
        """Test very long query."""
        long_query = "What vulnerabilities exist in " + "very " * 1000 + "long query about packages?"
        
        mock_response = {
            'response': 'Processed long query successfully.',
            'sources': []
        }
        mock_rag_engine.process_query.return_value = mock_response
        
        query_data = {"query": long_query}
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 200
        mock_rag_engine.process_query.assert_called_once_with(long_query)
    
    @patch('app.api.endpoints.query.logger')
    def test_query_logging(self, mock_logger, client, mock_rag_engine):
        """Test that queries are properly logged."""
        mock_response = {
            'response': 'Test response',
            'sources': []
        }
        mock_rag_engine.process_query.return_value = mock_response
        
        query_data = {"query": "Test logging query"}
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 200
        
        # Verify that the query was logged
        mock_logger.info.assert_called_with("Processing query: Test logging query")
    
    @patch('app.api.endpoints.query.logger')
    def test_query_error_logging(self, mock_logger, client, mock_rag_engine):
        """Test that query errors are properly logged."""
        error_msg = "Test error message"
        mock_rag_engine.process_query.side_effect = Exception(error_msg)
        
        query_data = {"query": "Error test query"}
        response = client.post("/api/query/", json=query_data)
        
        assert response.status_code == 500
        
        # Verify that the error was logged
        mock_logger.error.assert_called()
        error_call_args = mock_logger.error.call_args[0][0]
        assert "Error processing query" in error_call_args