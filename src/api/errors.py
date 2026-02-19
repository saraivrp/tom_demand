"""API exception handlers and domain exceptions."""

from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .models.common import ErrorResponse


def _encode_payload(payload: ErrorResponse) -> dict:
    if hasattr(payload, "model_dump"):
        return jsonable_encoder(payload.model_dump())
    return jsonable_encoder(payload.dict())


class AppError(Exception):
    """Application error mapped to structured API responses."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach custom exception handlers to the FastAPI app."""

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        payload = ErrorResponse(
            error="app_error",
            detail=exc.message,
            timestamp=datetime.utcnow(),
        )
        return JSONResponse(status_code=exc.status_code, content=_encode_payload(payload))

    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
        payload = ErrorResponse(
            error="http_error",
            detail=str(exc.detail),
            path=str(request.url.path),
            timestamp=datetime.utcnow(),
        )
        return JSONResponse(status_code=exc.status_code, content=_encode_payload(payload))

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, _: Exception) -> JSONResponse:
        payload = ErrorResponse(
            error="internal_server_error",
            detail="Unexpected server error",
            path=str(request.url.path),
            timestamp=datetime.utcnow(),
        )
        return JSONResponse(status_code=500, content=_encode_payload(payload))
