"""Shared API models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Service health payload."""

    status: str = Field(default="ok")
    service: str = Field(default="tom-demand-api")
    timestamp: datetime


class VersionResponse(BaseModel):
    """Version payload."""

    service: str = Field(default="tom-demand-api")
    api_version: str = Field(default="v1")
    app_version: str


class ErrorResponse(BaseModel):
    """Standard API error shape."""

    error: str
    detail: Optional[str] = None
    path: Optional[str] = None
    timestamp: datetime
