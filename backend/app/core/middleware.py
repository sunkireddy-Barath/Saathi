"""
CORS middleware and request logging middleware.

Both are registered in main.py via app.add_middleware().
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.utils.logger import logger


# ── CORS configuration (exported for use in main.py) ──────────────────────────
cors_middleware_config = {
    "allow_origins": settings.get_allowed_origins(),
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}


# ── Request logging middleware ─────────────────────────────────────────────────
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every incoming request with a unique request-id, method, path,
    status code, and elapsed time in milliseconds.

    The request-id is injected into the response headers so that clients
    (and support teams) can correlate logs with specific requests.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        start = time.perf_counter()

        # Attach request_id so downstream code can read it if needed
        request.state.request_id = request_id

        response = await call_next(request)

        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "{method} {path} → {status} ({elapsed:.1f}ms) [{rid}]",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            elapsed=elapsed_ms,
            rid=request_id,
        )

        return response
