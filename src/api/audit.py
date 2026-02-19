"""Audit logging middleware."""

from __future__ import annotations

import json
import os
from datetime import datetime

from fastapi import Request, Response

from .config import load_settings


async def audit_middleware(request: Request, call_next) -> Response:
    response = await call_next(request)

    settings = load_settings()
    log_path = settings.audit_log_path
    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "role": request.headers.get("x-role", "viewer"),
        "client": request.client.host if request.client else None,
    }

    with open(log_path, "a") as log_file:
        log_file.write(json.dumps(record) + "\n")

    return response
