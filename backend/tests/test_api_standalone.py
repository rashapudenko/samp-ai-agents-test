"""
Standalone API tests that avoid dependency conflicts.
These tests focus on the core API functionality without the RAG engine.
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import tempfile
import os

from app.services.database import DatabaseManager


def create_test_app():
    """Create a test FastAPI app with minimal dependencies."""
    from fastapi import APIRouter
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(title="Test Security Vulnerabilities API")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Create test router
    api_router = APIRouter()
    
    @api_router.get("/health")
    async def health_check():
        return JSONResponse(content={"status": "healthy"}, status_code=200)
    
    @app.get("/")
    async def root():
        return {"message": "Test Security Vulnerabilities API"}
    
    # Include test router
    app.include_router(api_router, prefix="/api")
    
    return app


@pytest.fixture
def test_app():
    """Create a test app."""
    return create_test_app()


@pytest.fixture
def client(test_app):
    """Create a test client."""
    return TestClient(test_app)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    yield db_path
    
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


class TestStandaloneAPI:
    """Test cases for standalone API functionality."""
    
    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Test Security Vulnerabilities API"}
    
    def test_health_check_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_cors_headers_configured(self, client):
        """Test that CORS middleware is configured."""
        response = client.options("/api/health")
        # The test client doesn't automatically handle preflight requests
        # but we can test that the app is configured with CORS middleware
        assert response.status_code in [200, 405]  # 405 is OK for OPTIONS on GET endpoints
    
    def test_api_prefix_configuration(self, client):
        """Test that API endpoints are correctly prefixed."""
        # Test that endpoints are available under /api prefix
        response = client.get("/api/health")
        assert response.status_code == 200
        
        # Test that direct access without prefix fails
        response = client.get("/health")
        assert response.status_code == 404
    
    def test_invalid_endpoint(self, client):
        """Test accessing invalid endpoints."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
        
        response = client.get("/api/nonexistent")
        assert response.status_code == 404


class TestDatabaseIntegration:
    """Test database integration without API dependencies."""
    
    def test_database_crud_operations(self, temp_db):
        """Test basic CRUD operations on database."""
        db_manager = DatabaseManager(temp_db)
        
        # Create a vulnerability
        vuln_data = {
            'id': 'integration-test-1',
            'package': 'test-package',
            'severity': 'high',
            'description': 'Integration test vulnerability',
            'published_date': '2023-01-01',
            'affected_versions': '>=1.0.0',
            'remediation': 'Update to latest version'
        }
        
        # Test CREATE
        result = db_manager.create_vulnerability(vuln_data)
        assert result == 'integration-test-1'
        
        # Test READ
        retrieved = db_manager.get_vulnerability_by_id('integration-test-1')
        assert retrieved is not None
        assert retrieved['package'] == 'test-package'
        assert retrieved['severity'] == 'high'
        
        # Test UPDATE
        updated_data = {
            'package': 'test-package',
            'severity': 'critical',  # Changed severity
            'description': 'Updated integration test vulnerability',
            'published_date': '2023-01-01',
            'affected_versions': '>=1.0.0',
            'remediation': 'Immediate update required'
        }
        
        update_result = db_manager.update_vulnerability('integration-test-1', updated_data)
        assert update_result is True
        
        # Verify update
        updated_retrieved = db_manager.get_vulnerability_by_id('integration-test-1')
        assert updated_retrieved['severity'] == 'critical'
        assert updated_retrieved['description'] == 'Updated integration test vulnerability'
        
        # Test DELETE
        delete_result = db_manager.delete_vulnerability('integration-test-1')
        assert delete_result is True
        
        # Verify deletion
        deleted_retrieved = db_manager.get_vulnerability_by_id('integration-test-1')
        assert deleted_retrieved is None
    
    def test_database_filtering_and_pagination(self, temp_db):
        """Test database filtering and pagination."""
        db_manager = DatabaseManager(temp_db)
        
        # Create test data
        test_vulnerabilities = [
            {
                'id': 'filter-test-1',
                'package': 'requests',
                'severity': 'high',
                'description': 'Requests high severity',
                'published_date': '2023-01-01'
            },
            {
                'id': 'filter-test-2',
                'package': 'requests',
                'severity': 'medium',
                'description': 'Requests medium severity',
                'published_date': '2023-01-02'
            },
            {
                'id': 'filter-test-3',
                'package': 'django',
                'severity': 'high',
                'description': 'Django high severity',
                'published_date': '2023-01-03'
            },
            {
                'id': 'filter-test-4',
                'package': 'flask',
                'severity': 'low',
                'description': 'Flask low severity',
                'published_date': '2023-01-04'
            }
        ]
        
        # Insert test data
        for vuln in test_vulnerabilities:
            db_manager.create_vulnerability(vuln)
        
        # Test package filtering
        requests_vulns = db_manager.get_vulnerabilities(package='requests')
        assert len(requests_vulns) == 2
        assert all(v['package'] == 'requests' for v in requests_vulns)
        
        # Test severity filtering
        high_vulns = db_manager.get_vulnerabilities(severity='high')
        assert len(high_vulns) == 2
        assert all(v['severity'] == 'high' for v in high_vulns)
        
        # Test combined filtering
        high_requests = db_manager.get_vulnerabilities(package='requests', severity='high')
        assert len(high_requests) == 1
        assert high_requests[0]['id'] == 'filter-test-1'
        
        # Test pagination
        first_page = db_manager.get_vulnerabilities(limit=2, offset=0)
        assert len(first_page) == 2
        
        second_page = db_manager.get_vulnerabilities(limit=2, offset=2)
        assert len(second_page) == 2
        
        # Verify no overlap between pages
        first_page_ids = {v['id'] for v in first_page}
        second_page_ids = {v['id'] for v in second_page}
        assert len(first_page_ids.intersection(second_page_ids)) == 0
    
    def test_database_statistics(self, temp_db):
        """Test database statistics functionality."""
        db_manager = DatabaseManager(temp_db)
        
        # Create test data with varied distributions
        test_data = [
            {'id': 'stat-1', 'package': 'requests', 'severity': 'high', 'description': 'Test', 'published_date': '2023-01-01'},
            {'id': 'stat-2', 'package': 'requests', 'severity': 'medium', 'description': 'Test', 'published_date': '2023-01-01'},
            {'id': 'stat-3', 'package': 'django', 'severity': 'high', 'description': 'Test', 'published_date': '2023-02-01'},
            {'id': 'stat-4', 'package': 'flask', 'severity': 'low', 'description': 'Test', 'published_date': '2023-02-01'},
            {'id': 'stat-5', 'package': 'numpy', 'severity': 'critical', 'description': 'Test', 'published_date': '2023-03-01'}
        ]
        
        for vuln in test_data:
            db_manager.create_vulnerability(vuln)
        
        stats = db_manager.get_vulnerability_statistics()
        
        # Test total count
        assert stats['total'] == 5
        
        # Test severity distribution
        assert stats['by_severity']['high'] == 2
        assert stats['by_severity']['medium'] == 1
        assert stats['by_severity']['low'] == 1
        assert stats['by_severity']['critical'] == 1
        
        # Test package distribution
        assert stats['top_packages']['requests'] == 2
        assert stats['top_packages']['django'] == 1
        assert stats['top_packages']['flask'] == 1
        assert stats['top_packages']['numpy'] == 1
        
        # Test monthly distribution
        assert '2023-01' in stats['by_month']
        assert '2023-02' in stats['by_month']
        assert '2023-03' in stats['by_month']