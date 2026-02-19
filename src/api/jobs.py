"""In-memory async job manager for workflow execution."""

from __future__ import annotations

import threading
import traceback
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, Optional


class JobManager:
    """Tracks background workflow jobs and their execution status."""

    def __init__(self) -> None:
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def create_job(self, job_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        job_id = str(uuid.uuid4())
        job = {
            "job_id": job_id,
            "job_type": job_type,
            "status": "queued",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "payload": payload,
            "result": None,
            "error": None,
            "traceback": None,
        }
        with self._lock:
            self._jobs[job_id] = job
        return job

    def get(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._jobs.get(job_id)

    def list(self, limit: int = 50) -> Dict[str, Any]:
        with self._lock:
            jobs = list(self._jobs.values())
        jobs.sort(key=lambda j: j["created_at"], reverse=True)
        return {"count": min(len(jobs), limit), "jobs": jobs[:limit]}

    def execute(self, job_id: str, worker: Callable[[], Dict[str, Any]]) -> None:
        self._set_status(job_id, "running")
        try:
            result = worker()
            self._set_result(job_id, result)
        except Exception as exc:
            self._set_error(job_id, str(exc), traceback.format_exc())

    def _set_status(self, job_id: str, status: str) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = status
                self._jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()

    def _set_result(self, job_id: str, result: Dict[str, Any]) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = "completed"
                self._jobs[job_id]["result"] = result
                self._jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()

    def _set_error(self, job_id: str, error: str, tb: str) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = "failed"
                self._jobs[job_id]["error"] = error
                self._jobs[job_id]["traceback"] = tb
                self._jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()


job_manager = JobManager()
