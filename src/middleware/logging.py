"""Logging middleware for request/response logging with correlation IDs.

This middleware adds correlation IDs to requests and logs request/response
information for monitoring and debugging.
"""

import time
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from ..core.logging import clear_correlation_id, logger, set_correlation_id


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs requests and responses with correlation IDs."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process request, log details, and add correlation ID.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or endpoint handler.

        Returns:
            HTTP response with X-Correlation-ID header.
        """
        # Generate and set correlation ID
        correlation_id = request.headers.get("X-Correlation-ID")
        correlation_id = set_correlation_id(correlation_id)

        # Start timing
        start_time = time.time()

        # Skip logging for health check endpoints
        should_log = request.url.path not in ["/health", "/api/v1/health"]

        # Process request
        try:
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log response (single line, skip health checks)
            if should_log:
                logger.info(
                    f"{request.method} {request.url.path} {response.status_code} in {round(duration, 3)}s",
                    extra={
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                        "duration_seconds": round(duration, 3),
                        "correlation_id": correlation_id,
                    },
                )

            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id

            return response

        except Exception as e:
            # Calculate duration
            duration = time.time() - start_time

            # Always log errors, even for health checks
            logger.error(
                f"{request.method} {request.url.path} failed: {str(e)}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "duration_seconds": round(duration, 3),
                    "correlation_id": correlation_id,
                },
                exc_info=True,
            )
            raise

        finally:
            # Clear correlation ID from context
            clear_correlation_id()
