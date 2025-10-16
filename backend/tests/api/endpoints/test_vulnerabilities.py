import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import tempfile
import os

from app.main import app
from app.services.database import DatabaseManager


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    yield db_path
    
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def client_with_db(temp_db):
    """Create a test client with mocked database."""
    with patch('app.api.endpoints.vulnerabilities.db_manager') as mock_db:
        # Create actual database manager for realistic testing
        actual_db_manager = DatabaseManager(temp_db)
        mock_db.return_value = actual_db_manager
        mock_db.get_vulnerability_by_id = actual_db_manager.get_vulnerability_by_id
        mock_db.get_vulnerabilities = actual_db_manager.get_vulnerabilities
        mock_db.get_vulnerability_statistics = actual_db_manager.get_vulnerability_statistics
        
        client = TestClient(app)
        yield client, actual_db_manager


class TestVulnerabilitiesEndpoints:
    """Test cases for vulnerabilities API endpoints."""
    
    def test_get_vulnerabilities_empty(self, client_with_db):
        """Test getting vulnerabilities when database is empty."""
        client, db_manager = client_with_db
        
        response = client.get("/api/vulnerabilities/")
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    def test_get_vulnerabilities_with_data(self, client_with_db):
        """Test getting vulnerabilities with data in database."""
        client, db_manager = client_with_db
        
        # Add test data
        test_vulns = [
            {
                'id': 'test-1',
                'package': 'requests',
                'severity': 'high',
                'description': 'Test vulnerability 1',
                'published_date': '2023-01-01'
            },
            {
                'id': 'test-2',
                'package': 'django',
                'severity': 'medium',
                'description': 'Test vulnerability 2',
                'published_date': '2023-02-01'
            }
        ]
        
        for vuln in test_vulns:
            db_manager.create_vulnerability(vuln)
        
        response = client.get("/api/vulnerabilities/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]['id'] == 'test-2'  # Should be ordered by published_date DESC
        assert data[1]['id'] == 'test-1'
    
    def test_get_vulnerabilities_with_package_filter(self, client_with_db):
        """Test filtering vulnerabilities by package."""
        client, db_manager = client_with_db
        
        # Add test data
        test_vulns = [
            {
                'id': 'req-1',
                'package': 'requests',
                'severity': 'high',
                'description': 'Requests vulnerability',
                'published_date': '2023-01-01'
            },
            {
                'id': 'django-1',
                'package': 'django',
                'severity': 'medium',
                'description': 'Django vulnerability',
                'published_date': '2023-02-01'
            }
        ]
        
        for vuln in test_vulns:
            db_manager.create_vulnerability(vuln)
        
        response = client.get("/api/vulnerabilities/?package=requests")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['package'] == 'requests'
    
    def test_get_vulnerabilities_with_severity_filter(self, client_with_db):
        """Test filtering vulnerabilities by severity."""
        client, db_manager = client_with_db
        
        # Add test data with different severities
        test_vulns = [
            {
                'id': 'high-1',
                'package': 'requests',
                'severity': 'high',
                'description': 'High severity',
                'published_date': '2023-01-01'
            },
            {
                'id': 'medium-1',
                'package': 'django',
                'severity': 'medium',
                'description': 'Medium severity',
                'published_date': '2023-02-01'
            }
        ]
        
        for vuln in test_vulns:
            db_manager.create_vulnerability(vuln)
        
        response = client.get("/api/vulnerabilities/?severity=high")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['severity'] == 'high'
    
    def test_get_vulnerabilities_with_limit_offset(self, client_with_db):
        """Test pagination with limit and offset."""
        client, db_manager = client_with_db
        
        # Add multiple test vulnerabilities
        for i in range(5):
            vuln_data = {
                'id': f'vuln-{i}',
                'package': 'test-package',
                'severity': 'medium',
                'description': f'Test vulnerability {i}',
                'published_date': f'2023-0{i+1}-01'
            }
            db_manager.create_vulnerability(vuln_data)
        
        # Test limit
        response = client.get("/api/vulnerabilities/?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        
        # Test offset
        response = client.get("/api/vulnerabilities/?limit=2&offset=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        # Results should be different from first page
    
    def test_get_vulnerabilities_invalid_limit(self, client_with_db):
        """Test invalid limit parameter."""
        client, db_manager = client_with_db
        
        # Limit too high
        response = client.get("/api/vulnerabilities/?limit=200")
        assert response.status_code == 422  # Validation error
        
        # Limit too low
        response = client.get("/api/vulnerabilities/?limit=0")
        assert response.status_code == 422  # Validation error
        
        # Invalid limit type
        response = client.get("/api/vulnerabilities/?limit=abc")
        assert response.status_code == 422  # Validation error
    
    def test_get_vulnerability_by_id(self, client_with_db):
        """Test getting a specific vulnerability by ID."""
        client, db_manager = client_with_db
        
        # Add test vulnerability
        vuln_data = {
            'id': 'specific-test',
            'package': 'numpy',
            'severity': 'critical',
            'description': 'Critical numpy vulnerability',
            'published_date': '2023-03-01',
            'affected_versions': '>=1.0.0,<1.21.0',
            'remediation': 'Update to 1.21.0 or later'
        }
        db_manager.create_vulnerability(vuln_data)
        
        response = client.get("/api/vulnerabilities/specific-test")
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 'specific-test'
        assert data['package'] == 'numpy'
        assert data['severity'] == 'critical'
        assert data['affected_versions'] == '>=1.0.0,<1.21.0'
        assert data['remediation'] == 'Update to 1.21.0 or later'
    
    def test_get_vulnerability_by_id_not_found(self, client_with_db):
        """Test getting a non-existent vulnerability."""
        client, db_manager = client_with_db
        
        response = client.get("/api/vulnerabilities/nonexistent-id")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data['detail']
    
    def test_get_packages(self, client_with_db):
        """Test getting list of packages."""
        client, db_manager = client_with_db
        
        # Add test data with different packages
        test_vulns = [
            {
                'id': 'req-1',
                'package': 'requests',
                'severity': 'high',
                'description': 'Requests vulnerability',
                'published_date': '2023-01-01'
            },
            {
                'id': 'req-2',
                'package': 'requests',
                'severity': 'medium',
                'description': 'Another requests vulnerability',
                'published_date': '2023-01-15'
            },
            {
                'id': 'django-1',
                'package': 'django',
                'severity': 'low',
                'description': 'Django vulnerability',
                'published_date': '2023-02-01'
            }
        ]
        
        for vuln in test_vulns:
            db_manager.create_vulnerability(vuln)
        
        response = client.get("/api/vulnerabilities/packages")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert 'requests' in data
        assert 'django' in data
    
    def test_get_severities(self, client_with_db):
        """Test getting list of severity levels."""
        client, db_manager = client_with_db
        
        # Add test data with different severities
        test_vulns = [
            {
                'id': 'high-1',
                'package': 'requests',
                'severity': 'high',
                'description': 'High severity',
                'published_date': '2023-01-01'
            },
            {
                'id': 'medium-1',
                'package': 'django',
                'severity': 'medium',
                'description': 'Medium severity',
                'published_date': '2023-02-01'
            },
            {
                'id': 'low-1',
                'package': 'flask',
                'severity': 'low',
                'description': 'Low severity',
                'published_date': '2023-03-01'
            }
        ]
        
        for vuln in test_vulns:
            db_manager.create_vulnerability(vuln)
        
        response = client.get("/api/vulnerabilities/severities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert 'high' in data
        assert 'medium' in data
        assert 'low' in data
    
    def test_get_statistics(self, client_with_db):
        """Test getting vulnerability statistics."""
        client, db_manager = client_with_db
        
        # Add test data
        test_vulns = [
            {
                'id': 'stat-1',
                'package': 'requests',
                'severity': 'high',
                'description': 'High severity',
                'published_date': '2023-01-01'
            },
            {
                'id': 'stat-2',
                'package': 'requests',
                'severity': 'medium',
                'description': 'Medium severity',
                'published_date': '2023-01-15'
            },
            {
                'id': 'stat-3',
                'package': 'django',
                'severity': 'high',
                'description': 'Django high',
                'published_date': '2023-02-01'
            }
        ]
        
        for vuln in test_vulns:
            db_manager.create_vulnerability(vuln)
        
        response = client.get("/api/vulnerabilities/statistics")
        assert response.status_code == 200
        data = response.json()
        
        assert 'total' in data
        assert data['total'] == 3
        
        assert 'by_severity' in data
        assert data['by_severity']['high'] == 2
        assert data['by_severity']['medium'] == 1
        
        assert 'top_packages' in data
        assert data['top_packages']['requests'] == 2
        assert data['top_packages']['django'] == 1
        
        assert 'by_month' in data
    
    @patch('app.api.endpoints.vulnerabilities.db_manager')
    def test_database_error_handling(self, mock_db_manager):
        """Test error handling when database operations fail."""
        client = TestClient(app)
        
        # Mock database manager to raise exceptions
        mock_db_manager.get_vulnerabilities.side_effect = Exception("Database error")
        mock_db_manager.get_vulnerability_by_id.side_effect = Exception("Database error")
        mock_db_manager.get_vulnerability_statistics.side_effect = Exception("Database error")
        
        # Test error handling for get_vulnerabilities
        response = client.get("/api/vulnerabilities/")
        assert response.status_code == 500
        assert "Error fetching vulnerabilities" in response.json()['detail']
        
        # Test error handling for get_vulnerability_by_id
        response = client.get("/api/vulnerabilities/test-id")
        assert response.status_code == 500
        assert "Error fetching vulnerability" in response.json()['detail']
        
        # Test error handling for get_statistics
        response = client.get("/api/vulnerabilities/statistics")
        assert response.status_code == 500
        assert "Error fetching statistics" in response.json()['detail']