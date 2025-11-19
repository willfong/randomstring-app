"""Security middleware for adding OWASP recommended security headers.

This middleware adds security headers to all HTTP responses to protect
against common web vulnerabilities.
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware that adds OWASP recommended security headers to responses."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process request and add security headers to response.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or endpoint handler.

        Returns:
            HTTP response with security headers added.
        """
        response = await call_next(request)

        # OWASP recommended security headers
        security_headers = {
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            # Prevent clickjacking attacks
            "X-Frame-Options": "DENY",
            # Enable XSS protection (legacy, but still useful)
            "X-XSS-Protection": "1; mode=block",
            # Enforce HTTPS
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            # Content Security Policy
            # Allow inline scripts and styles for the app, and CDN resources for Swagger UI
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data:; "
                "font-src 'self' data:"
            ),
            # Control referrer information
            "Referrer-Policy": "strict-origin-when-cross-origin",
            # Disable dangerous browser features
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }

        # Add all security headers to response
        for header, value in security_headers.items():
            response.headers[header] = value

        return response
