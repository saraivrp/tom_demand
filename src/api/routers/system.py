"""System-level endpoints (health/version)."""

from datetime import datetime

from fastapi import APIRouter

from ..models.common import HealthResponse, VersionResponse
from src import __version__

router = APIRouter(prefix="/api/v1", tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return basic liveness status."""
    return HealthResponse(timestamp=datetime.utcnow())


@router.get("/version", response_model=VersionResponse)
def version_info() -> VersionResponse:
    """Return service and API versions."""
    return VersionResponse(app_version=__version__)
