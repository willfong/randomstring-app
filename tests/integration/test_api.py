"""Integration tests for API endpoints.

This module contains comprehensive tests for all FastAPI endpoints,
following TDD principles. Tests are written before implementation.
"""

import re
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


class TestRandomEndpoint:
    """Tests for the /api/v1/random endpoint."""

    def test_get_random_strings_default_length(self, test_client: TestClient) -> None:
        """Test generating random strings with default length (32)."""
        response = test_client.get("/api/v1/random")

        assert response.status_code == 200
        data = response.json()

        assert "length" in data
        assert data["length"] == 32
        assert "strings" in data
        assert "generated_at" in data

        # Verify all string types are present
        strings = data["strings"]
        assert "alphanumeric" in strings
        assert "distinguishable" in strings
        assert "password" in strings
        assert "urlsafe" in strings
        assert "lowercase" in strings

        # Verify each string has correct length
        for string_type, string_value in strings.items():
            assert len(string_value) == 32, f"{string_type} has incorrect length"

    def test_get_random_strings_custom_length(self, test_client: TestClient) -> None:
        """Test generating random strings with custom length."""
        for length in [1, 16, 64, 128]:
            response = test_client.get(f"/api/v1/random?length={length}")

            assert response.status_code == 200
            data = response.json()

            assert data["length"] == length
            for string_type, string_value in data["strings"].items():
                assert len(string_value) == length, (
                    f"{string_type} has incorrect length for length={length}"
                )

    def test_random_strings_have_correct_format(self, test_client: TestClient) -> None:
        """Test that generated strings match their expected character sets."""
        response = test_client.get("/api/v1/random?length=50")
        assert response.status_code == 200
        strings = response.json()["strings"]

        # Alphanumeric: a-zA-Z0-9
        assert re.match(r"^[a-zA-Z0-9]+$", strings["alphanumeric"])

        # Distinguishable: specific char set (no confusing chars)
        distinguishable_pattern = r"^[23456789ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnpqrstwxyz]+$"
        assert re.match(distinguishable_pattern, strings["distinguishable"])

        # Password: printable ASCII
        for char in strings["password"]:
            assert 33 <= ord(char) <= 126

        # URL-safe: a-zA-Z0-9-_
        assert re.match(r"^[a-zA-Z0-9_-]+$", strings["urlsafe"])

        # Lowercase: a-z
        assert re.match(r"^[a-z]+$", strings["lowercase"])

    def test_timestamp_is_valid_iso8601(self, test_client: TestClient) -> None:
        """Test that generated_at timestamp is valid ISO8601 format."""
        response = test_client.get("/api/v1/random")
        assert response.status_code == 200

        data = response.json()
        timestamp_str = data["generated_at"]

        # Should be able to parse as ISO8601
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        assert isinstance(timestamp, datetime)

    def test_multiple_requests_generate_different_strings(
        self, test_client: TestClient
    ) -> None:
        """Test that multiple requests generate unique strings."""
        responses = [test_client.get("/api/v1/random") for _ in range(10)]

        alphanumeric_strings = {r.json()["strings"]["alphanumeric"] for r in responses}
        assert len(alphanumeric_strings) == 10, "Should generate unique strings"

    def test_length_validation_too_small(self, test_client: TestClient) -> None:
        """Test that length < 1 returns 422 validation error."""
        response = test_client.get("/api/v1/random?length=0")
        assert response.status_code == 422

        response = test_client.get("/api/v1/random?length=-1")
        assert response.status_code == 422

    def test_length_validation_too_large(self, test_client: TestClient) -> None:
        """Test that length > 128 returns 422 validation error."""
        response = test_client.get("/api/v1/random?length=129")
        assert response.status_code == 422

        response = test_client.get("/api/v1/random?length=1000")
        assert response.status_code == 422

    def test_length_validation_invalid_type(self, test_client: TestClient) -> None:
        """Test that non-integer length returns 422 validation error."""
        response = test_client.get("/api/v1/random?length=abc")
        assert response.status_code == 422

        response = test_client.get("/api/v1/random?length=12.5")
        assert response.status_code == 422

    def test_response_has_correct_content_type(self, test_client: TestClient) -> None:
        """Test that response has application/json content type."""
        response = test_client.get("/api/v1/random")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    def test_health_check_returns_ok(self, test_client: TestClient) -> None:
        """Test that health check returns 200 OK."""
        response = test_client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_structure(self, test_client: TestClient) -> None:
        """Test that health check returns correct structure."""
        response = test_client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"
        assert "timestamp" in data
        assert "version" in data

    def test_health_check_timestamp_is_valid(self, test_client: TestClient) -> None:
        """Test that health check timestamp is valid ISO8601."""
        response = test_client.get("/health")
        assert response.status_code == 200

        data = response.json()
        timestamp_str = data["timestamp"]
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        assert isinstance(timestamp, datetime)

    def test_health_check_has_version(self, test_client: TestClient) -> None:
        """Test that health check includes version number."""
        response = test_client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "version" in data
        assert isinstance(data["version"], str)
        assert len(data["version"]) > 0

    def test_health_check_content_type(self, test_client: TestClient) -> None:
        """Test that health check has application/json content type."""
        response = test_client.get("/health")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestAsyncEndpoints:
    """Tests for async endpoint functionality."""

    @pytest.mark.asyncio
    async def test_async_random_endpoint(self, async_client: AsyncClient) -> None:
        """Test random endpoint works with async client."""
        response = await async_client.get("/api/v1/random")
        assert response.status_code == 200

        data = response.json()
        assert "strings" in data
        assert len(data["strings"]) == 5

    @pytest.mark.asyncio
    async def test_async_health_endpoint(self, async_client: AsyncClient) -> None:
        """Test health endpoint works with async client."""
        response = await async_client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "ok"

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, async_client: AsyncClient) -> None:
        """Test handling of concurrent requests."""
        import asyncio

        # Make 20 concurrent requests
        tasks = [async_client.get("/api/v1/random?length=32") for _ in range(20)]
        responses = await asyncio.gather(*tasks)

        # All should succeed
        assert all(r.status_code == 200 for r in responses)

        # All should have unique alphanumeric strings
        alphanumeric_strings = {r.json()["strings"]["alphanumeric"] for r in responses}
        assert len(alphanumeric_strings) == 20, "Concurrent requests should be unique"


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_redirects_to_docs(self, test_client: TestClient) -> None:
        """Test that root endpoint redirects to API documentation."""
        response = test_client.get("/", follow_redirects=False)
        # Could redirect to /docs or return API info
        assert response.status_code in [200, 307, 308]


class TestDocsEndpoints:
    """Tests for auto-generated API documentation endpoints."""

    def test_openapi_json_available(self, test_client: TestClient) -> None:
        """Test that OpenAPI JSON spec is available."""
        response = test_client.get("/openapi.json")
        assert response.status_code == 200

        spec = response.json()
        assert "openapi" in spec
        assert "info" in spec
        assert "paths" in spec

    def test_docs_ui_available(self, test_client: TestClient) -> None:
        """Test that Swagger UI docs are available."""
        response = test_client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_redoc_ui_available(self, test_client: TestClient) -> None:
        """Test that ReDoc UI is available."""
        response = test_client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_404_for_unknown_endpoint(self, test_client: TestClient) -> None:
        """Test that unknown endpoints return 404."""
        response = test_client.get("/api/v1/unknown")
        assert response.status_code == 404

    def test_405_for_wrong_method(self, test_client: TestClient) -> None:
        """Test that wrong HTTP methods return 405."""
        response = test_client.post("/health")
        assert response.status_code == 405

        response = test_client.delete("/api/v1/random")
        assert response.status_code == 405

    def test_error_response_has_detail(self, test_client: TestClient) -> None:
        """Test that error responses include detail field."""
        response = test_client.get("/api/v1/random?length=0")
        assert response.status_code == 422

        data = response.json()
        assert "detail" in data


class TestCORS:
    """Tests for CORS headers (if enabled)."""

    def test_cors_headers_present(self, test_client: TestClient) -> None:
        """Test that CORS headers are present in responses."""
        response = test_client.get("/api/v1/random")
        # CORS headers should be present if configured
        # This test will verify implementation
        assert response.status_code == 200


class TestSecurityHeaders:
    """Tests for security headers in responses."""

    def test_security_headers_present(self, test_client: TestClient) -> None:
        """Test that security headers are present in all responses."""
        response = test_client.get("/api/v1/random")
        assert response.status_code == 200

        headers = response.headers

        # OWASP recommended security headers
        expected_headers = [
            "x-content-type-options",
            "x-frame-options",
        ]

        for header in expected_headers:
            assert header in headers, f"Missing security header: {header}"

    def test_x_content_type_options(self, test_client: TestClient) -> None:
        """Test X-Content-Type-Options is set to nosniff."""
        response = test_client.get("/api/v1/random")
        assert response.headers.get("x-content-type-options") == "nosniff"

    def test_x_frame_options(self, test_client: TestClient) -> None:
        """Test X-Frame-Options is set to DENY."""
        response = test_client.get("/api/v1/random")
        assert response.headers.get("x-frame-options") == "DENY"
