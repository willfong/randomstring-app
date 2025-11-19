"""Rate limiting middleware using slowapi.

This middleware implements rate limiting to prevent abuse and ensure
fair usage of the API.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from ..core.config import get_settings


def get_limiter() -> Limiter:
    """Create and configure rate limiter instance.

    Returns:
        Configured Limiter instance.
    """
    settings = get_settings()

    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[f"{settings.rate_limit_times}/{settings.rate_limit_seconds}seconds"],
        enabled=settings.rate_limit_enabled,
    )

    return limiter


# Create global limiter instance
limiter = get_limiter()
