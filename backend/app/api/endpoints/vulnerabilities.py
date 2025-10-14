from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.models.vulnerability import VulnerabilityResponse
from app.services.database import DatabaseManager
from app.core.config import settings

router = APIRouter()
db_manager = DatabaseManager(settings.DATABASE_PATH)

@router.get("/", response_model=List[VulnerabilityResponse])
async def get_vulnerabilities(
    package: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get vulnerabilities with optional filters."""
    try:
        vulnerabilities = db_manager.get_vulnerabilities(
            package=package,
            severity=severity,
            limit=limit,
            offset=offset
        )
        return vulnerabilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vulnerabilities: {str(e)}")

@router.get("/packages", response_model=List[str])
async def get_packages():
    """Get list of packages with vulnerabilities."""
    try:
        stats = db_manager.get_vulnerability_statistics()
        return list(stats['top_packages'].keys())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching packages: {str(e)}")

@router.get("/severities", response_model=List[str])
async def get_severities():
    """Get list of available severity levels."""
    try:
        stats = db_manager.get_vulnerability_statistics()
        return list(stats['by_severity'].keys())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching severities: {str(e)}")

@router.get("/statistics")
async def get_statistics():
    """Get vulnerability statistics."""
    try:
        return db_manager.get_vulnerability_statistics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")

@router.get("/{vulnerability_id}", response_model=VulnerabilityResponse)
async def get_vulnerability(vulnerability_id: str):
    """Get a specific vulnerability by ID."""
    try:
        vulnerability = db_manager.get_vulnerability_by_id(vulnerability_id)
        if not vulnerability:
            raise HTTPException(status_code=404, detail=f"Vulnerability with ID {vulnerability_id} not found")
        return vulnerability
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vulnerability: {str(e)}")
