"""Pydantic models and schemas for API requests and responses.

This module defines all data models used for API validation and serialization.
"""

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class StringType(str, Enum):
    """Enumeration of available string types."""

    ALPHANUMERIC = "alphanumeric"
    DISTINGUISHABLE = "distinguishable"
    PASSWORD = "password"
    URLSAFE = "urlsafe"
    LOWERCASE = "lowercase"


class RandomStringsResponse(BaseModel):
    """Response model for random string generation endpoint."""

    length: int = Field(..., description="The length of each generated string", ge=1, le=128)
    strings: dict[str, str] = Field(..., description="Generated strings by type")
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="ISO8601 timestamp of generation",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "length": 32,
                "strings": {
                    "alphanumeric": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
                    "distinguishable": "23456789ABCDEFGHJKMNPQRSTWXYZ2345",
                    "password": "!@#$%^&*()_+-=[]{}|;:,.<>?abc123XYZ",
                    "urlsafe": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh",
                    "lowercase": "abcdefghijklmnopqrstuvwxyzabcdefgh",
                },
                "generated_at": "2025-01-15T12:34:56.789Z",
            }
        }
    }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(default="ok", description="Health status of the service")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Current server timestamp",
    )
    version: str = Field(default="0.1.0", description="Application version")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "ok",
                "timestamp": "2025-01-15T12:34:56.789Z",
                "version": "0.1.0",
            }
        }
    }


class ErrorResponse(BaseModel):
    """Response model for error responses."""

    detail: str = Field(..., description="Error message")
    error_code: str | None = Field(None, description="Application-specific error code")

    model_config = {
        "json_schema_extra": {
            "example": {"detail": "Invalid length parameter", "error_code": "INVALID_LENGTH"}
        }
    }


class RandomStringQuery(BaseModel):
    """Query parameters for random string generation."""

    length: int = Field(
        default=32,
        description="Length of strings to generate",
        ge=1,
        le=128,
    )
    string_type: StringType | None = Field(
        default=None,
        alias="type",
        description="Optional: specific type of string to generate",
    )

    @field_validator("length")
    @classmethod
    def validate_length(cls, v: int) -> int:
        """Validate that length is within acceptable bounds.

        Args:
            v: The length value to validate.

        Returns:
            The validated length value.

        Raises:
            ValueError: If length is not between 1 and 128.
        """
        if not 1 <= v <= 128:
            msg = "Length must be between 1 and 128"
            raise ValueError(msg)
        return v

    model_config = {
        "json_schema_extra": {
            "example": {"length": 32, "type": "alphanumeric"},
        },
        "populate_by_name": True,
    }
