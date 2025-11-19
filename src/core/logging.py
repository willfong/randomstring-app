"""Structured JSON logging configuration.

This module provides structured logging with JSON format for better log aggregation
and analysis in production environments.
"""

import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any

from pythonjsonlogger.json import JsonFormatter

from .config import get_settings

# Context variable for request correlation ID
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")


class CustomJsonFormatter(JsonFormatter):
    """Custom JSON formatter that adds correlation ID to log records."""

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        """Add custom fields to log record.

        Args:
            log_record: The log record dict to be formatted.
            record: The original LogRecord.
            message_dict: Additional message data.
        """
        super().add_fields(log_record, record, message_dict)

        # Add correlation ID if available
        correlation_id = correlation_id_var.get()
        if correlation_id:
            log_record["correlation_id"] = correlation_id

        # Add standard fields
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["timestamp"] = self.formatTime(record, self.datefmt)


def setup_logging() -> logging.Logger:
    """Configure and return the application logger.

    Returns:
        Configured logger instance.
    """
    settings = get_settings()

    # Get logger
    logger = logging.getLogger("randomstring_app")
    logger.setLevel(settings.log_level.upper())
    logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.log_level.upper())

    # Set formatter based on configuration
    if settings.log_format == "json":
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(level)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Don't propagate to root logger
    logger.propagate = False

    return logger


def get_correlation_id() -> str:
    """Get the current correlation ID from context.

    Returns:
        Current correlation ID or empty string if not set.
    """
    return correlation_id_var.get()


def set_correlation_id(correlation_id: str | None = None) -> str:
    """Set correlation ID in context.

    Args:
        correlation_id: Optional correlation ID. If None, generates a new UUID.

    Returns:
        The correlation ID that was set.
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    correlation_id_var.set(correlation_id)
    return correlation_id


def clear_correlation_id() -> None:
    """Clear the correlation ID from context."""
    correlation_id_var.set("")


# Create logger instance
logger = setup_logging()
