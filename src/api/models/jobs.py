"""Async job API models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class JobSubmitResponse(BaseModel):
    job_id: str
    job_type: str
    status: str
    created_at: str


class JobStatusResponse(BaseModel):
    job_id: str
    job_type: str
    status: str
    created_at: str
    updated_at: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class JobListResponse(BaseModel):
    count: int
    jobs: List[JobStatusResponse]
