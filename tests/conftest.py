"""Pytest configuration and shared fixtures for all tests.

This module provides shared test fixtures and configuration that can be used
across all test modules.
"""

from collections.abc import AsyncGenerator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def test_client() -> TestClient:
    """Provide a synchronous test client for FastAPI app.

    Returns:
        TestClient instance for making synchronous requests to the app.

    Note:
        This fixture will be used after the main app is implemented.
    """
    # Import here to avoid circular dependency during initial TDD phase
    from src.main import app

    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, Any]:
    """Provide an asynchronous test client for FastAPI app.

    Returns:
        AsyncClient instance for making asynchronous requests to the app.

    Note:
        This fixture will be used after the main app is implemented.
    """
    # Import here to avoid circular dependency during initial TDD phase
    from src.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore[arg-type]
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def sample_lengths() -> list[int]:
    """Provide a list of sample lengths for testing.

    Returns:
        List of valid length values to test with.
    """
    return [1, 10, 32, 64, 128]


@pytest.fixture
def invalid_lengths() -> list[int]:
    """Provide a list of invalid lengths for testing.

    Returns:
        List of invalid length values to test error handling.
    """
    return [-1, 0, 129, 200, 1000]
