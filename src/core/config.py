"""Application configuration using pydantic-settings.

This module provides environment-based configuration for the application
with validation and type safety.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application metadata
    app_name: str = Field(default="RandomString API", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    app_description: str = Field(
        default="A FastAPI microservice that generates cryptographically secure random strings",
        description="Application description",
    )

    # Server configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port", ge=1, le=65535)
    reload: bool = Field(default=False, description="Enable auto-reload (development only)")

    # API configuration
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 path prefix")

    # CORS configuration
    cors_enabled: bool = Field(default=True, description="Enable CORS")
    cors_origins: list[str] = Field(
        default=["*"],
        description="Allowed CORS origins (* for all)",
    )
    cors_allow_credentials: bool = Field(default=False, description="Allow credentials in CORS")
    cors_allow_methods: list[str] = Field(
        default=["GET"],
        description="Allowed HTTP methods",
    )
    cors_allow_headers: list[str] = Field(
        default=["*"],
        description="Allowed HTTP headers",
    )

    # Rate limiting configuration
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_times: int = Field(
        default=100,
        description="Number of requests allowed per period",
        ge=1,
    )
    rate_limit_seconds: int = Field(
        default=60,
        description="Time period for rate limiting in seconds",
        ge=1,
    )

    # Security
    security_headers_enabled: bool = Field(
        default=True,
        description="Enable OWASP security headers",
    )

    # Logging configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    log_format: str = Field(
        default="json",
        description="Log format (json or text)",
    )

    # Development/Debug
    debug: bool = Field(default=False, description="Enable debug mode")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings instance with configuration loaded from environment.

    Note:
        Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings()


# Convenience instance for imports
settings = get_settings()
