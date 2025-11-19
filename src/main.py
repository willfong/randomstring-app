"""Main FastAPI application entry point.

This module creates and configures the FastAPI application with all middleware,
routes, and error handlers.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .api.routes import router as api_router
from .core.config import get_settings
from .core.logging import logger
from .middleware.logging import LoggingMiddleware
from .middleware.rate_limit import limiter
from .middleware.security import SecurityHeadersMiddleware
from .utils.string_generator import (
    generate_alphanumeric,
    generate_distinguishable,
    generate_lowercase,
    generate_password,
    generate_urlsafe,
)

# Get settings
settings = get_settings()

# Configure templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Configure static files
static_dir = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan events.

    Args:
        app: The FastAPI application instance.

    Yields:
        None during application runtime.
    """
    # Startup
    logger.info(
        f"Starting {settings.app_name} v{settings.app_version}",
        extra={
            "app_name": settings.app_name,
            "version": settings.app_version,
            "debug": settings.debug,
        },
    )

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

# Add CORS middleware
if settings.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    logger.info("CORS middleware enabled")

# Add security headers middleware
if settings.security_headers_enabled:
    app.add_middleware(SecurityHeadersMiddleware)
    logger.info("Security headers middleware enabled")

# Add logging middleware (should be last to capture everything)
app.add_middleware(LoggingMiddleware)
logger.info("Logging middleware enabled")

# Mount static files (must be after middleware)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
logger.info(f"Static files mounted at /static from {static_dir}")

# Include routers
app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
    tags=["API v1"],
)

# Also add health endpoint at root level for compatibility
app.include_router(
    api_router,
    tags=["Health"],
)


def is_browser(user_agent: str) -> bool:
    """Check if the User-Agent string indicates a web browser.

    Args:
        user_agent: The User-Agent header value.

    Returns:
        True if the request appears to be from a browser, False otherwise.
    """
    browser_indicators = [
        "Mozilla",
        "Chrome",
        "Safari",
        "Firefox",
        "Edge",
        "Opera",
        "MSIE",
        "Trident",
    ]
    return any(indicator in user_agent for indicator in browser_indicators)


def generate_plain_text_response(length: int) -> str:
    """Generate plain text response in original format.

    Args:
        length: Length of strings to generate.

    Returns:
        Formatted plain text with all string types.
    """
    return f"""Random Stuff:
{generate_alphanumeric(length)}

Easy to read:
{generate_distinguishable(length)}

Passwords:
{generate_password(length)}

URL-safe:
{generate_urlsafe(length)}

Lower-case:
{generate_lowercase(length)}

"""


@app.get("/", include_in_schema=False, response_class=Response)
async def root(request: Request) -> Response:
    """Handle root endpoint - serve web UI for browsers, return random strings for API clients.

    Args:
        request: The incoming HTTP request.

    Returns:
        HTML template for browsers, plain text random strings for other clients.
    """
    user_agent = request.headers.get("user-agent", "")

    # If it's a browser, serve the web UI
    if is_browser(user_agent):
        logger.debug(f"Browser detected ({user_agent}), serving web UI")
        # Generate initial random strings with default length
        length = 32
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "length": length,
                "strings": {
                    "alphanumeric": generate_alphanumeric(length),
                    "distinguishable": generate_distinguishable(length),
                    "password": generate_password(length),
                    "urlsafe": generate_urlsafe(length),
                    "lowercase": generate_lowercase(length),
                },
            },
        )

    # Otherwise, return random strings (backward compatible with original API)
    logger.debug(f"API client detected ({user_agent}), returning random strings")
    return PlainTextResponse(
        content=generate_plain_text_response(32),
        media_type="text/plain",
    )


@app.get("/{length}", include_in_schema=False)
async def root_with_length(length: int) -> PlainTextResponse:
    """Generate random strings with custom length (backward compatible endpoint).

    Args:
        length: The length of strings to generate.

    Returns:
        Plain text response with random strings.
    """
    # Validate and cap length like original (max 128, default to 32 if invalid)
    if length < 1 or length > 128:
        length = 32 if length < 1 else 128
        logger.warning(f"Invalid length requested, using {length}")

    logger.debug(f"Generating random strings with length={length}")
    return PlainTextResponse(
        content=generate_plain_text_response(length),
        media_type="text/plain",
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle 500 Internal Server Error.

    Args:
        request: The HTTP request that caused the error.
        exc: The exception that was raised.

    Returns:
        JSON response with error details.
    """
    logger.error(f"Internal server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
