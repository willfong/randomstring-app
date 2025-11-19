"""Tests for backward compatibility with original Node.js API.

This module tests that the Python FastAPI version maintains compatibility
with the original Node.js API behavior.
"""

import re

from fastapi.testclient import TestClient


class TestBackwardCompatibleEndpoints:
    """Tests for backward compatible endpoints (/, /:length)."""

    def test_root_with_curl_user_agent_returns_plain_text(
        self, test_client: TestClient
    ) -> None:
        """Test that curl user agent gets plain text random strings."""
        response = test_client.get("/", headers={"User-Agent": "curl/7.68.0"})

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"

        content = response.text
        assert "Random Stuff:" in content
        assert "Easy to read:" in content
        assert "Passwords:" in content
        assert "URL-safe:" in content
        assert "Lower-case:" in content

    def test_root_with_browser_user_agent_serves_html(
        self, test_client: TestClient
    ) -> None:
        """Test that browser user agent gets served the HTML web interface."""
        response = test_client.get(
            "/",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"
            },
            follow_redirects=False,
        )

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Verify HTML content contains expected elements
        content = response.text
        assert "<!DOCTYPE html>" in content
        assert "Random String Generator" in content
        assert "Generate New Strings" in content
        assert "/docs" in content  # Link to API docs
        assert "Tailwind" in content or "tailwindcss" in content  # Tailwind CSS

    def test_root_with_python_requests_returns_plain_text(
        self, test_client: TestClient
    ) -> None:
        """Test that python-requests user agent gets plain text."""
        response = test_client.get(
            "/", headers={"User-Agent": "python-requests/2.25.1"}
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"

    def test_root_with_empty_user_agent_returns_plain_text(
        self, test_client: TestClient
    ) -> None:
        """Test that empty user agent gets plain text (backward compatible)."""
        response = test_client.get("/", headers={"User-Agent": ""})

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"

    def test_length_endpoint_returns_correct_length(
        self, test_client: TestClient
    ) -> None:
        """Test /:length endpoint with various lengths."""
        for length in [5, 16, 64, 128]:
            response = test_client.get(f"/{length}")

            assert response.status_code == 200
            assert response.headers["content-type"] == "text/plain; charset=utf-8"

            # Extract strings from response
            content = response.text
            lines = content.split("\n")

            # Find the alphanumeric string (second line after "Random Stuff:")
            for i, line in enumerate(lines):
                if "Random Stuff:" in line:
                    random_string = lines[i + 1]
                    assert len(random_string) == length, (
                        f"Expected length {length}, got {len(random_string)}"
                    )
                    break

    def test_length_endpoint_with_invalid_length_caps_to_128(
        self, test_client: TestClient
    ) -> None:
        """Test that lengths > 128 are capped to 128."""
        response = test_client.get("/200")

        assert response.status_code == 200
        content = response.text

        # Extract first string to verify it's 128 chars
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "Random Stuff:" in line:
                random_string = lines[i + 1]
                assert len(random_string) == 128
                break

    def test_length_endpoint_with_zero_defaults_to_32(
        self, test_client: TestClient
    ) -> None:
        """Test that length of 0 defaults to 32."""
        response = test_client.get("/0")

        assert response.status_code == 200
        content = response.text

        # Extract first string to verify it's 32 chars
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "Random Stuff:" in line:
                random_string = lines[i + 1]
                assert len(random_string) == 32
                break

    def test_response_format_matches_original(self, test_client: TestClient) -> None:
        """Test that response format matches original Node.js format."""
        response = test_client.get("/", headers={"User-Agent": "curl/7.0"})

        assert response.status_code == 200
        content = response.text

        # Verify format matches original:
        # Random Stuff:\n<string>\n\nEasy to read:\n<string>\n\n...
        assert content.startswith("Random Stuff:\n")
        assert "\n\nEasy to read:\n" in content
        assert "\n\nPasswords:\n" in content
        assert "\n\nURL-safe:\n" in content
        assert "\n\nLower-case:\n" in content
        assert content.endswith("\n\n")

    def test_all_strings_are_different(self, test_client: TestClient) -> None:
        """Test that all 5 string types are different from each other."""
        response = test_client.get("/32", headers={"User-Agent": "curl/7.0"})

        assert response.status_code == 200
        content = response.text

        # Extract all strings
        strings = []
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if any(
                label in line
                for label in [
                    "Random Stuff:",
                    "Easy to read:",
                    "Passwords:",
                    "URL-safe:",
                    "Lower-case:",
                ]
            ):
                if i + 1 < len(lines):
                    strings.append(lines[i + 1])

        # Verify we have 5 strings
        assert len(strings) == 5

        # Verify they're all different
        assert len(set(strings)) == 5, "All generated strings should be unique"

    def test_concurrent_requests_return_different_strings(
        self, test_client: TestClient
    ) -> None:
        """Test that multiple requests return different strings."""
        responses = [
            test_client.get("/", headers={"User-Agent": "curl/7.0"}) for _ in range(10)
        ]

        # Extract first string from each response
        first_strings = []
        for response in responses:
            lines = response.text.split("\n")
            for i, line in enumerate(lines):
                if "Random Stuff:" in line:
                    first_strings.append(lines[i + 1])
                    break

        # All should be unique (cryptographically random)
        assert len(set(first_strings)) == 10
