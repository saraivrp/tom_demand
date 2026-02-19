"""FastAPI entrypoint for TOM Demand API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .audit import audit_middleware
from .config import load_settings
from .errors import register_exception_handlers
from .routers.jobs import router as jobs_router
from .routers.reference_data import router as reference_data_router
from .routers.system import router as system_router
from .routers.workflows import router as workflows_router
from src import __version__


def create_app() -> FastAPI:
    """Create configured FastAPI application."""
    settings = load_settings()
    app = FastAPI(
        title="TOM Demand API",
        description="API layer for TOM Demand prioritization workflows.",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(system_router)
    app.include_router(workflows_router)
    app.include_router(reference_data_router)
    app.include_router(jobs_router)
    app.middleware("http")(audit_middleware)
    register_exception_handlers(app)

    return app


app = create_app()
