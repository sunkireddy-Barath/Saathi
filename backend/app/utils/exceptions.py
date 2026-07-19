"""
Application-wide custom exceptions and their FastAPI exception handlers.

Every domain error in the codebase raises one of these typed exceptions
so that HTTP responses are always consistent and never leak stack traces.
"""

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


# ── Base application exception ─────────────────────────────────────────────────
class SaathiException(Exception):
    """Root exception for all Saathi domain errors."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An unexpected error occurred."

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)


# ── 400 Bad Request ────────────────────────────────────────────────────────────
class BadRequestException(SaathiException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad request."


# ── 401 Unauthorised ──────────────────────────────────────────────────────────
class CredentialsException(SaathiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials."


# ── 403 Forbidden ─────────────────────────────────────────────────────────────
class ForbiddenException(SaathiException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You do not have permission to perform this action."


class AccountSuspendedException(SaathiException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Your account has been suspended."


# ── 404 Not Found ──────────────────────────────────────────────────────────────
class NotFoundException(SaathiException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found."


# ── 409 Conflict ──────────────────────────────────────────────────────────────
class ConflictException(SaathiException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists."


# ── 422 Business rule violations ──────────────────────────────────────────────
class UnprocessableException(SaathiException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "The request could not be processed."


class BelowFairPriceException(UnprocessableException):
    detail = "Offer price is below the fair price floor and cannot be accepted."


class NegotiationLockedException(UnprocessableException):
    detail = "This product is already locked by another buyer."


class InsufficientTrustScoreException(ForbiddenException):
    detail = "Your trust score is too low to initiate negotiations."


# ── Exception handlers (registered in main.py) ────────────────────────────────
async def saathi_exception_handler(request: Request, exc: SaathiException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "request_id": getattr(request.state, "request_id", None),
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "request_id": getattr(request.state, "request_id", None),
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "An internal server error occurred.",
            "request_id": getattr(request.state, "request_id", None),
        },
    )
