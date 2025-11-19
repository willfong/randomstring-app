"""API route handlers for random string generation.

This module defines all API endpoints for the random string generation service.
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Query
from slowapi import Limiter

from ..core.config import get_settings
from ..core.logging import logger
from ..middleware.rate_limit import limiter
from ..models.schemas import HealthResponse, RandomStringsResponse
from ..utils.string_generator import (
    generate_alphanumeric,
    generate_distinguishable,
    generate_lowercase,
    generate_password,
    generate_urlsafe,
)

# Get settings
settings = get_settings()

# Create API router
router = APIRouter()


@router.get(
    "/random",
    response_model=RandomStringsResponse,
    summary="Generate random strings",
    description="Generate cryptographically secure random strings in various formats",
    tags=["Random Strings"],
)
async def get_random_strings(
    length: int = Query(
        default=32,
        ge=1,
        le=128,
        description="Length of strings to generate (1-128)",
    )
) -> RandomStringsResponse:
    """Generate random strings of various types.

    Args:
        length: The length of strings to generate (default: 32, range: 1-128).

    Returns:
        RandomStringsResponse containing all generated strings.

    Raises:
        HTTPException: If length validation fails.
    """
    logger.debug(f"Generating random strings with length={length}")

    try:
        # Generate all string types
        strings = {
            "alphanumeric": generate_alphanumeric(length),
            "distinguishable": generate_distinguishable(length),
            "password": generate_password(length),
            "urlsafe": generate_urlsafe(length),
            "lowercase": generate_lowercase(length),
        }

        logger.debug(f"Successfully generated {len(strings)} string types")

        return RandomStringsResponse(
            length=length,
            strings=strings,
            generated_at=datetime.now(UTC),
        )

    except ValueError as e:
        logger.error(f"Validation error generating strings: {e}")
        raise


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of the service",
    tags=["Health"],
)
async def health_check() -> HealthResponse:
    """Perform health check.

    Returns:
        HealthResponse with current status and timestamp.
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(UTC),
        version=settings.app_version,
    )
