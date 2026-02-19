"""API runtime settings."""

import os
from dataclasses import dataclass


@dataclass
class ApiSettings:
    auth_enabled: bool
    api_key: str
    audit_log_path: str
    cors_allow_origins: list[str]


def load_settings() -> ApiSettings:
    auth_enabled = os.getenv("AUTH_ENABLED", "false").lower() == "true"
    api_key = os.getenv("API_KEY", "")
    audit_log_path = os.getenv("AUDIT_LOG_PATH", "data/output/api_audit.jsonl")
    cors_raw = os.getenv(
        "CORS_ALLOW_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    cors_allow_origins = [origin.strip() for origin in cors_raw.split(",") if origin.strip()]
    return ApiSettings(
        auth_enabled=auth_enabled,
        api_key=api_key,
        audit_log_path=audit_log_path,
        cors_allow_origins=cors_allow_origins,
    )
