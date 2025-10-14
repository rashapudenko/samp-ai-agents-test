import pytest
import os
import tempfile
import sqlite3
from unittest.mock import patch, Mock

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
def db_manager(temp_db):
    """Create a DatabaseManager instance with temporary database."""
    return DatabaseManager(temp_db)


class TestDatabaseManager:
    """Test cases for the DatabaseManager class."""
    
    def test_init_creates_database_and_tables(self, temp_db):
        """Test that initialization creates database and tables."""
        db_manager = DatabaseManager(temp_db)
        
        # Check that database file was created
        assert os.path.exists(temp_db)
        
        # Check that tables were created
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            assert 'vulnerabilities' in tables
            assert 'embeddings_ref' in tables
    
    def test_create_vulnerability(self, db_manager):
        """Test creating a new vulnerability."""
        vulnerability_data = {
            'id': 'test-vuln-1',
            'package': 'requests',
            'severity': 'high',
            'description': 'Test vulnerability description',
            'published_date': '2023-01-01',
            'affected_versions': '>=2.0.0',
            'remediation': 'Update to latest version'
        }
        
        result = db_manager.create_vulnerability(vulnerability_data)
        assert result == 'test-vuln-1'
        
        # Verify the vulnerability was stored
        retrieved = db_manager.get_vulnerability_by_id('test-vuln-1')
        assert retrieved is not None
        assert retrieved['package'] == 'requests'
        assert retrieved['severity'] == 'high'
    
    def test_get_vulnerability_by_id(self, db_manager):
        """Test retrieving vulnerability by ID."""
        # First create a vulnerability
        vulnerability_data = {
            'id': 'test-vuln-2',
            'package': 'django',
            'severity': 'medium',
            'description': 'Test Django vulnerability',
            'published_date': '2023-02-01'
        }
        db_manager.create_vulnerability(vulnerability_data)
        
        # Retrieve it
        result = db_manager.get_vulnerability_by_id('test-vuln-2')
        assert result is not None
        assert result['id'] == 'test-vuln-2'
        assert result['package'] == 'django'
        assert result['severity'] == 'medium'
        
        # Test non-existent ID
        result = db_manager.get_vulnerability_by_id('non-existent')
        assert result is None
    
    def test_get_vulnerabilities_by_package(self, db_manager):
        """Test retrieving vulnerabilities by package name."""
        # Create multiple vulnerabilities for the same package
        vuln1 = {
            'id': 'flask-1',
            'package': 'flask',
            'severity': 'high',
            'description': 'Flask vulnerability 1',
            'published_date': '2023-01-01'
        }
        vuln2 = {
            'id': 'flask-2',
            'package': 'flask',
            'severity': 'medium',
            'description': 'Flask vulnerability 2',
            'published_date': '2023-02-01'
        }
        vuln3 = {
            'id': 'django-1',
            'package': 'django',
            'severity': 'low',
            'description': 'Django vulnerability',
            'published_date': '2023-01-15'
        }
        
        db_manager.create_vulnerability(vuln1)
        db_manager.create_vulnerability(vuln2)
        db_manager.create_vulnerability(vuln3)
        
        # Get Flask vulnerabilities
        flask_vulns = db_manager.get_vulnerabilities_by_package('flask')
        assert len(flask_vulns) == 2
        
        # Check ordering (should be by published_date DESC)
        assert flask_vulns[0]['id'] == 'flask-2'  # 2023-02-01
        assert flask_vulns[1]['id'] == 'flask-1'  # 2023-01-01
        
        # Get Django vulnerabilities
        django_vulns = db_manager.get_vulnerabilities_by_package('django')
        assert len(django_vulns) == 1
        assert django_vulns[0]['id'] == 'django-1'
    
    def test_get_vulnerabilities_with_filters(self, db_manager):
        """Test getting vulnerabilities with various filters."""
        # Create test data
        vulnerabilities = [
            {'id': 'v1', 'package': 'requests', 'severity': 'high', 
             'description': 'High severity', 'published_date': '2023-01-01'},
            {'id': 'v2', 'package': 'requests', 'severity': 'medium', 
             'description': 'Medium severity', 'published_date': '2023-02-01'},
            {'id': 'v3', 'package': 'flask', 'severity': 'high', 
             'description': 'Flask high', 'published_date': '2023-03-01'},
            {'id': 'v4', 'package': 'django', 'severity': 'low', 
             'description': 'Django low', 'published_date': '2023-04-01'}
        ]
        
        for vuln in vulnerabilities:
            db_manager.create_vulnerability(vuln)
        
        # Test no filters
        all_vulns = db_manager.get_vulnerabilities()
        assert len(all_vulns) == 4
        
        # Test package filter
        requests_vulns = db_manager.get_vulnerabilities(package='requests')
        assert len(requests_vulns) == 2
        assert all(v['package'] == 'requests' for v in requests_vulns)
        
        # Test severity filter
        high_vulns = db_manager.get_vulnerabilities(severity='high')
        assert len(high_vulns) == 2
        assert all(v['severity'] == 'high' for v in high_vulns)
        
        # Test combined filters
        high_requests = db_manager.get_vulnerabilities(package='requests', severity='high')
        assert len(high_requests) == 1
        assert high_requests[0]['id'] == 'v1'
        
        # Test limit and offset
        limited = db_manager.get_vulnerabilities(limit=2)
        assert len(limited) == 2
        
        offset_limited = db_manager.get_vulnerabilities(limit=2, offset=2)
        assert len(offset_limited) == 2
    
    def test_update_vulnerability(self, db_manager):
        """Test updating an existing vulnerability."""
        # Create vulnerability
        original = {
            'id': 'update-test',
            'package': 'numpy',
            'severity': 'medium',
            'description': 'Original description',
            'published_date': '2023-01-01'
        }
        db_manager.create_vulnerability(original)
        
        # Update vulnerability
        updated_data = {
            'package': 'numpy',
            'severity': 'high',
            'description': 'Updated description',
            'published_date': '2023-01-01',
            'remediation': 'Update to latest version'
        }
        
        result = db_manager.update_vulnerability('update-test', updated_data)
        assert result is True
        
        # Verify update
        retrieved = db_manager.get_vulnerability_by_id('update-test')
        assert retrieved['severity'] == 'high'
        assert retrieved['description'] == 'Updated description'
        assert retrieved['remediation'] == 'Update to latest version'
    
    def test_delete_vulnerability(self, db_manager):
        """Test deleting a vulnerability."""
        # Create vulnerability
        vuln_data = {
            'id': 'delete-test',
            'package': 'test-package',
            'severity': 'low',
            'description': 'To be deleted',
            'published_date': '2023-01-01'
        }
        db_manager.create_vulnerability(vuln_data)
        
        # Verify it exists
        assert db_manager.get_vulnerability_by_id('delete-test') is not None
        
        # Delete it
        result = db_manager.delete_vulnerability('delete-test')
        assert result is True
        
        # Verify it's gone
        assert db_manager.get_vulnerability_by_id('delete-test') is None
    
    def test_count_vulnerabilities(self, db_manager):
        """Test counting vulnerabilities."""
        # Initially should be 0
        assert db_manager.count_vulnerabilities() == 0
        
        # Add some vulnerabilities
        for i in range(5):
            vuln_data = {
                'id': f'count-test-{i}',
                'package': 'test-package',
                'severity': 'low',
                'description': f'Test vulnerability {i}',
                'published_date': '2023-01-01'
            }
            db_manager.create_vulnerability(vuln_data)
        
        assert db_manager.count_vulnerabilities() == 5
    
    def test_get_vulnerability_statistics(self, db_manager):
        """Test getting vulnerability statistics."""
        # Create test data with varied packages and severities
        test_data = [
            {'id': 'stat1', 'package': 'requests', 'severity': 'high', 
             'description': 'Test', 'published_date': '2023-01-01'},
            {'id': 'stat2', 'package': 'requests', 'severity': 'medium', 
             'description': 'Test', 'published_date': '2023-01-15'},
            {'id': 'stat3', 'package': 'django', 'severity': 'high', 
             'description': 'Test', 'published_date': '2023-02-01'},
            {'id': 'stat4', 'package': 'flask', 'severity': 'low', 
             'description': 'Test', 'published_date': '2023-02-15'}
        ]
        
        for vuln in test_data:
            db_manager.create_vulnerability(vuln)
        
        stats = db_manager.get_vulnerability_statistics()
        
        assert stats['total'] == 4
        assert 'by_severity' in stats
        assert stats['by_severity']['high'] == 2
        assert stats['by_severity']['medium'] == 1
        assert stats['by_severity']['low'] == 1
        
        assert 'top_packages' in stats
        assert stats['top_packages']['requests'] == 2
        assert stats['top_packages']['django'] == 1
        assert stats['top_packages']['flask'] == 1
        
        assert 'by_month' in stats
        assert '2023-01' in stats['by_month']
        assert '2023-02' in stats['by_month']
    
    def test_embedding_ref_operations(self, db_manager):
        """Test embedding reference operations."""
        # Create a vulnerability first
        vuln_data = {
            'id': 'embed-test',
            'package': 'test-package',
            'severity': 'medium',
            'description': 'Test for embedding',
            'published_date': '2023-01-01'
        }
        db_manager.create_vulnerability(vuln_data)
        
        # Create embedding reference
        result = db_manager.create_embedding_ref('embed-test', 'vector-123')
        assert result is True
        
        # Retrieve vector ID
        vector_id = db_manager.get_vector_id_by_vulnerability_id('embed-test')
        assert vector_id == 'vector-123'
        
        # Retrieve vulnerability ID by vector ID
        vuln_id = db_manager.get_vulnerability_id_by_vector_id('vector-123')
        assert vuln_id == 'embed-test'
        
        # Update embedding reference
        result = db_manager.create_embedding_ref('embed-test', 'vector-456')
        assert result is True
        
        # Verify update
        vector_id = db_manager.get_vector_id_by_vulnerability_id('embed-test')
        assert vector_id == 'vector-456'
    
    @patch('app.services.database.logger')
    def test_database_error_handling(self, mock_logger, temp_db):
        """Test error handling in database operations."""
        # Create manager with invalid database path
        invalid_path = "/nonexistent/directory/db.sqlite"
        
        with pytest.raises(Exception):
            DatabaseManager(invalid_path)
    
    def test_connection_context_manager(self, db_manager):
        """Test the database connection context manager."""
        with db_manager.get_connection() as conn:
            assert conn is not None
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1
    
    def test_duplicate_vulnerability_creation(self, db_manager):
        """Test handling of duplicate vulnerability IDs."""
        vuln_data = {
            'id': 'duplicate-test',
            'package': 'test-package',
            'severity': 'medium',
            'description': 'First vulnerability',
            'published_date': '2023-01-01'
        }
        
        # First creation should succeed
        result1 = db_manager.create_vulnerability(vuln_data)
        assert result1 == 'duplicate-test'
        
        # Second creation with same ID should fail
        vuln_data['description'] = 'Second vulnerability'
        result2 = db_manager.create_vulnerability(vuln_data)
        assert result2 is None  # Should fail due to unique constraint