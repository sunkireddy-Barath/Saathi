"""
FastAPI application factory and entrypoint.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import api_router
from app.core.config import settings
from app.core.database import create_all_tables
from app.core.middleware import RequestLoggingMiddleware, cors_middleware_config
from app.utils.exceptions import (
    SaathiException,
    http_exception_handler,
    saathi_exception_handler,
    unhandled_exception_handler,
)
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events running on application startup and shutdown.
    """
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode")
    
    # In dev, create tables if they don't exist
    if not settings.is_production:
        await create_all_tables()
        logger.info("Database tables verified.")

    yield
    
    logger.info(f"Shutting down {settings.APP_NAME}")


def create_app() -> FastAPI:
    """Factory function to configure and return the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Saathi Backend API — Predictive Marketplace for Handloom Artisans",
        lifespan=lifespan,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
    )

    # Middlewares
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(CORSMiddleware, **cors_middleware_config)

    # Exception Handlers
    app.add_exception_handler(SaathiException, saathi_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Routers
    app.include_router(api_router)

    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "ok", "version": settings.APP_VERSION}

    return app


app = create_app()
