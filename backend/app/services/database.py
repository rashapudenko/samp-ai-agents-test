import sqlite3
from contextlib import contextmanager
import logging
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd

from app.core.logger import get_logger

logger = get_logger(__name__)

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        
        # Make sure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self._create_tables_if_not_exist()
        
    @contextmanager
    def get_connection(self):
        """Get a database connection with context management. For tsting"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
            
    def _create_tables_if_not_exist(self):
        """Create necessary tables if they don't exist."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create vulnerabilities table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS vulnerabilities (
                    id TEXT PRIMARY KEY,
                    package TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    description TEXT NOT NULL,
                    published_date TEXT NOT NULL,
                    affected_versions TEXT,
                    remediation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                # Create embeddings reference table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS embeddings_ref (
                    vulnerability_id TEXT PRIMARY KEY,
                    vector_id TEXT NOT NULL,
                    FOREIGN KEY (vulnerability_id) REFERENCES vulnerabilities(id)
                )
                ''')
                
                # Create indexes for frequently queried fields
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_vulnerabilities_package ON vulnerabilities(package)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_vulnerabilities_severity ON vulnerabilities(severity)')
                
                conn.commit()
                logger.info("Database tables created successfully")
                
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def get_vulnerability_by_id(self, vulnerability_id: str) -> Optional[Dict[str, Any]]:
        """Get a vulnerability by its ID."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM vulnerabilities WHERE id = ?", (vulnerability_id,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Error getting vulnerability by ID {vulnerability_id}: {e}")
            return None
    
    def get_vulnerabilities_by_package(self, package_name: str) -> List[Dict[str, Any]]:
        """Get vulnerabilities by package name."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM vulnerabilities WHERE package = ? ORDER BY published_date DESC", 
                    (package_name,)
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting vulnerabilities by package {package_name}: {e}")
            return []
    
    def get_vulnerabilities(self, package: Optional[str] = None, severity: Optional[str] = None,
                            limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """Get vulnerabilities with optional filters."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Build query with filters
                query = "SELECT * FROM vulnerabilities"
                params = []
                
                # Add WHERE clauses based on filters
                where_clauses = []
                if package:
                    where_clauses.append("package = ?")
                    params.append(package)
                if severity:
                    where_clauses.append("severity = ?")
                    params.append(severity)
                
                if where_clauses:
                    query += " WHERE " + " AND ".join(where_clauses)
                
                # Add ordering and limits
                query += " ORDER BY published_date DESC LIMIT ? OFFSET ?"
                params.extend([limit, offset])
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting vulnerabilities with filters: {e}")
            return []
    
    def create_vulnerability(self, vulnerability_data: Dict[str, Any]) -> Optional[str]:
        """Create a new vulnerability entry."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Prepare data
                vulnerability_id = vulnerability_data.get('id')
                package = vulnerability_data.get('package')
                severity = vulnerability_data.get('severity')
                description = vulnerability_data.get('description')
                published_date = vulnerability_data.get('published_date')
                affected_versions = vulnerability_data.get('affected_versions')
                remediation = vulnerability_data.get('remediation')
                
                # Insert vulnerability
                cursor.execute('''
                INSERT INTO vulnerabilities (id, package, severity, description, published_date, affected_versions, remediation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (vulnerability_id, package, severity, description, published_date, affected_versions, remediation))
                
                conn.commit()
                logger.debug(f"Created vulnerability: {vulnerability_id} - {package}")
                return vulnerability_id
                
        except Exception as e:
            logger.error(f"Error creating vulnerability: {e}")
            return None
    
    def update_vulnerability(self, vulnerability_id: str, vulnerability_data: Dict[str, Any]) -> bool:
        """Update an existing vulnerability."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Prepare data
                package = vulnerability_data.get('package')
                severity = vulnerability_data.get('severity')
                description = vulnerability_data.get('description')
                published_date = vulnerability_data.get('published_date')
                affected_versions = vulnerability_data.get('affected_versions')
                remediation = vulnerability_data.get('remediation')
                
                # Update vulnerability
                cursor.execute('''
                UPDATE vulnerabilities
                SET package = ?, severity = ?, description = ?, published_date = ?, 
                    affected_versions = ?, remediation = ?
                WHERE id = ?
                ''', (package, severity, description, published_date, 
                      affected_versions, remediation, vulnerability_id))
                
                conn.commit()
                logger.debug(f"Updated vulnerability: {vulnerability_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error updating vulnerability {vulnerability_id}: {e}")
            return False
    
    def delete_vulnerability(self, vulnerability_id: str) -> bool:
        """Delete a vulnerability by ID."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Also delete any embedding references
                cursor.execute("DELETE FROM embeddings_ref WHERE vulnerability_id = ?", (vulnerability_id,))
                
                # Delete vulnerability
                cursor.execute("DELETE FROM vulnerabilities WHERE id = ?", (vulnerability_id,))
                
                conn.commit()
                logger.debug(f"Deleted vulnerability: {vulnerability_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error deleting vulnerability {vulnerability_id}: {e}")
            return False
    
    def create_embedding_ref(self, vulnerability_id: str, vector_id: str) -> bool:
        """Create a reference between a vulnerability and its embedding."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if reference already exists
                cursor.execute(
                    "SELECT 1 FROM embeddings_ref WHERE vulnerability_id = ?", 
                    (vulnerability_id,)
                )
                if cursor.fetchone():
                    # Update existing reference
                    cursor.execute(
                        "UPDATE embeddings_ref SET vector_id = ? WHERE vulnerability_id = ?",
                        (vector_id, vulnerability_id)
                    )
                else:
                    # Create new reference
                    cursor.execute(
                        "INSERT INTO embeddings_ref (vulnerability_id, vector_id) VALUES (?, ?)",
                        (vulnerability_id, vector_id)
                    )
                
                conn.commit()
                logger.debug(f"Created/updated embedding reference: {vulnerability_id} - {vector_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error creating embedding reference: {e}")
            return False
    
    def get_vector_id_by_vulnerability_id(self, vulnerability_id: str) -> Optional[str]:
        """Get vector ID for a vulnerability."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT vector_id FROM embeddings_ref WHERE vulnerability_id = ?", 
                    (vulnerability_id,)
                )
                result = cursor.fetchone()
                return dict(result)['vector_id'] if result else None
        except Exception as e:
            logger.error(f"Error getting vector ID for vulnerability {vulnerability_id}: {e}")
            return None
    
    def get_vulnerability_id_by_vector_id(self, vector_id: str) -> Optional[str]:
        """Get vulnerability ID for a vector."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT vulnerability_id FROM embeddings_ref WHERE vector_id = ?", 
                    (vector_id,)
                )
                result = cursor.fetchone()
                return dict(result)['vulnerability_id'] if result else None
        except Exception as e:
            logger.error(f"Error getting vulnerability ID for vector {vector_id}: {e}")
            return None
            
    def count_vulnerabilities(self) -> int:
        """Count total vulnerabilities in database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) as count FROM vulnerabilities")
                result = cursor.fetchone()
                return dict(result)['count'] if result else 0
        except Exception as e:
            logger.error(f"Error counting vulnerabilities: {e}")
            return 0
            
    def get_vulnerability_statistics(self) -> Dict[str, Any]:
        """Get statistics about vulnerabilities."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get total count
                cursor.execute("SELECT COUNT(*) as total FROM vulnerabilities")
                total = dict(cursor.fetchone())['total']
                
                # Get severity distribution
                cursor.execute("""
                    SELECT severity, COUNT(*) as count 
                    FROM vulnerabilities 
                    GROUP BY severity
                    ORDER BY count DESC
                """)
                severity_counts = {dict(row)['severity']: dict(row)['count'] for row in cursor.fetchall()}
                
                # Get package distribution (top 10)
                cursor.execute("""
                    SELECT package, COUNT(*) as count 
                    FROM vulnerabilities 
                    GROUP BY package
                    ORDER BY count DESC
                    LIMIT 10
                """)
                package_counts = {dict(row)['package']: dict(row)['count'] for row in cursor.fetchall()}
                
                # Get date distribution by month
                cursor.execute("""
                    SELECT substr(published_date, 1, 7) as month, COUNT(*) as count 
                    FROM vulnerabilities 
                    GROUP BY month
                    ORDER BY month DESC
                    LIMIT 12
                """)
                month_counts = {dict(row)['month']: dict(row)['count'] for row in cursor.fetchall()}
                
                return {
                    'total': total,
                    'by_severity': severity_counts,
                    'top_packages': package_counts,
                    'by_month': month_counts
                }
                
        except Exception as e:
            logger.error(f"Error getting vulnerability statistics: {e}")
            return {
                'total': 0,
                'by_severity': {},
                'top_packages': {},
                'by_month': {}
            }