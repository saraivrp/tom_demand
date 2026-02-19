"""Simple API-key and role-based access controls."""

from typing import Optional

from fastapi import Depends, Header

from .config import load_settings
from .errors import AppError

ROLE_LEVELS = {"viewer": 1, "editor": 2, "executor": 3, "admin": 4}


def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    settings = load_settings()
    if not settings.auth_enabled:
        return
    if not settings.api_key:
        raise AppError("Server auth misconfiguration: API_KEY is empty.", status_code=500)
    if x_api_key != settings.api_key:
        raise AppError("Invalid API key.", status_code=401)


def require_role(min_role: str):
    min_level = ROLE_LEVELS.get(min_role, 1)

    def _check_role(
        _: None = Depends(require_api_key),
        x_role: Optional[str] = Header(default="viewer"),
    ) -> None:
        role = (x_role or "viewer").lower()
        role_level = ROLE_LEVELS.get(role, 0)
        if role_level < min_level:
            raise AppError(
                f"Insufficient role. Required '{min_role}', received '{role}'.",
                status_code=403,
            )

    return _check_role
