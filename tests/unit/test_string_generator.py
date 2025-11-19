"""Unit tests for random string generator module.

This module contains comprehensive tests for all string generation functions,
following TDD principles. Tests are written before implementation.
"""

import re
import string

import pytest

from src.utils.string_generator import (
    generate_alphanumeric,
    generate_distinguishable,
    generate_lowercase,
    generate_password,
    generate_urlsafe,
)


class TestAlphanumericGenerator:
    """Tests for alphanumeric string generation."""

    def test_generates_correct_length(self) -> None:
        """Verify generated string has the requested length."""
        result = generate_alphanumeric(32)
        assert len(result) == 32

    def test_generates_different_length(self) -> None:
        """Verify generation works with different lengths."""
        for length in [1, 10, 64, 128]:
            result = generate_alphanumeric(length)
            assert len(result) == length

    def test_contains_only_alphanumeric(self) -> None:
        """Verify string contains only alphanumeric characters (a-z, A-Z, 0-9)."""
        result = generate_alphanumeric(100)
        pattern = re.compile(r"^[a-zA-Z0-9]+$")
        assert pattern.match(result), f"String contains non-alphanumeric: {result}"

    def test_generates_unique_strings(self) -> None:
        """Verify multiple calls generate different strings (statistically)."""
        strings = {generate_alphanumeric(32) for _ in range(100)}
        # With cryptographically secure randomness, all should be unique
        assert len(strings) == 100

    def test_minimum_length(self) -> None:
        """Verify generation works with minimum length of 1."""
        result = generate_alphanumeric(1)
        assert len(result) == 1

    def test_maximum_length(self) -> None:
        """Verify generation works with maximum length of 128."""
        result = generate_alphanumeric(128)
        assert len(result) == 128


class TestDistinguishableGenerator:
    """Tests for distinguishable character string generation."""

    # Characters that are easily distinguishable (no 0/O, 1/l/I confusion)
    DISTINGUISHABLE_CHARS = "23456789ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnpqrstwxyz"

    def test_generates_correct_length(self) -> None:
        """Verify generated string has the requested length."""
        result = generate_distinguishable(32)
        assert len(result) == 32

    def test_contains_only_distinguishable_chars(self) -> None:
        """Verify string contains only easily distinguishable characters."""
        result = generate_distinguishable(100)
        for char in result:
            assert char in self.DISTINGUISHABLE_CHARS, (
                f"Character '{char}' is not in distinguishable set"
            )

    def test_excludes_confusing_characters(self) -> None:
        """Verify most confusing characters are excluded (0, O, 1, l, I)."""
        # Most critically confusing characters that should be excluded
        confusing = ["0", "O", "1", "l", "I"]
        # Generate multiple strings to test character exclusion
        result = "".join(generate_distinguishable(128) for _ in range(10))
        for char in confusing:
            assert char not in result, f"Found confusing character: {char}"

    def test_generates_unique_strings(self) -> None:
        """Verify multiple calls generate different strings."""
        strings = {generate_distinguishable(32) for _ in range(100)}
        assert len(strings) == 100

    def test_various_lengths(self) -> None:
        """Verify generation works with various lengths."""
        for length in [1, 16, 64, 128]:
            result = generate_distinguishable(length)
            assert len(result) == length


class TestPasswordGenerator:
    """Tests for password string generation (ASCII printable)."""

    def test_generates_correct_length(self) -> None:
        """Verify generated string has the requested length."""
        result = generate_password(32)
        assert len(result) == 32

    def test_contains_printable_ascii(self) -> None:
        """Verify string contains only ASCII printable characters."""
        result = generate_password(100)
        for char in result:
            assert char in string.printable, f"Non-printable character: {repr(char)}"
            # Should be in the range of visible ASCII (no control chars)
            assert 33 <= ord(char) <= 126, f"Character outside printable range: {char}"

    def test_includes_special_characters(self) -> None:
        """Verify password can include special characters."""
        # Generate enough strings to statistically get special chars
        combined = "".join(generate_password(50) for _ in range(20))
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        has_special = any(char in combined for char in special_chars)
        assert has_special, "Password generator should include special characters"

    def test_generates_unique_strings(self) -> None:
        """Verify multiple calls generate different strings."""
        strings = {generate_password(32) for _ in range(100)}
        assert len(strings) == 100

    def test_various_lengths(self) -> None:
        """Verify generation works with various lengths."""
        for length in [1, 20, 64, 128]:
            result = generate_password(length)
            assert len(result) == length


class TestUrlSafeGenerator:
    """Tests for URL-safe string generation."""

    # URL-safe characters: A-Z, a-z, 0-9, -, _
    URL_SAFE_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")

    def test_generates_correct_length(self) -> None:
        """Verify generated string has the requested length."""
        result = generate_urlsafe(32)
        assert len(result) == 32

    def test_contains_only_urlsafe_chars(self) -> None:
        """Verify string contains only URL-safe characters."""
        result = generate_urlsafe(100)
        assert self.URL_SAFE_PATTERN.match(result), (
            f"String contains non-URL-safe characters: {result}"
        )

    def test_no_special_chars_needing_encoding(self) -> None:
        """Verify string doesn't contain characters that need URL encoding."""
        # Generate multiple strings to test character exclusion
        result = "".join(generate_urlsafe(128) for _ in range(10))
        forbidden = [" ", "/", "?", "#", "&", "=", "+", "%", "@", "!", "*"]
        for char in forbidden:
            assert char not in result, f"Found character needing encoding: {char}"

    def test_generates_unique_strings(self) -> None:
        """Verify multiple calls generate different strings."""
        strings = {generate_urlsafe(32) for _ in range(100)}
        assert len(strings) == 100

    def test_various_lengths(self) -> None:
        """Verify generation works with various lengths."""
        for length in [1, 32, 64, 128]:
            result = generate_urlsafe(length)
            assert len(result) == length


class TestLowercaseGenerator:
    """Tests for lowercase-only string generation."""

    def test_generates_correct_length(self) -> None:
        """Verify generated string has the requested length."""
        result = generate_lowercase(32)
        assert len(result) == 32

    def test_contains_only_lowercase_letters(self) -> None:
        """Verify string contains only lowercase a-z characters."""
        result = generate_lowercase(100)
        pattern = re.compile(r"^[a-z]+$")
        assert pattern.match(result), f"String contains non-lowercase: {result}"

    def test_no_uppercase_or_numbers(self) -> None:
        """Verify string contains no uppercase letters or numbers."""
        # Generate multiple strings to test character constraints
        result = "".join(generate_lowercase(128) for _ in range(10))
        for char in result:
            assert char.islower(), f"Found non-lowercase character: {char}"
            assert char.isalpha(), f"Found non-alphabetic character: {char}"

    def test_generates_unique_strings(self) -> None:
        """Verify multiple calls generate different strings."""
        strings = {generate_lowercase(32) for _ in range(100)}
        assert len(strings) == 100

    def test_various_lengths(self) -> None:
        """Verify generation works with various lengths."""
        for length in [1, 16, 64, 128]:
            result = generate_lowercase(length)
            assert len(result) == length


class TestInputValidation:
    """Tests for input validation across all generators."""

    @pytest.mark.parametrize(
        "generator",
        [
            generate_alphanumeric,
            generate_distinguishable,
            generate_password,
            generate_urlsafe,
            generate_lowercase,
        ],
    )
    def test_rejects_zero_length(self, generator) -> None:  # type: ignore[no-untyped-def]
        """Verify generators reject zero-length requests."""
        with pytest.raises(ValueError, match="Length must be between 1 and 128"):
            generator(0)

    @pytest.mark.parametrize(
        "generator",
        [
            generate_alphanumeric,
            generate_distinguishable,
            generate_password,
            generate_urlsafe,
            generate_lowercase,
        ],
    )
    def test_rejects_negative_length(self, generator) -> None:  # type: ignore[no-untyped-def]
        """Verify generators reject negative length."""
        with pytest.raises(ValueError, match="Length must be between 1 and 128"):
            generator(-1)

    @pytest.mark.parametrize(
        "generator",
        [
            generate_alphanumeric,
            generate_distinguishable,
            generate_password,
            generate_urlsafe,
            generate_lowercase,
        ],
    )
    def test_rejects_too_large_length(self, generator) -> None:  # type: ignore[no-untyped-def]
        """Verify generators reject length > 128."""
        with pytest.raises(ValueError, match="Length must be between 1 and 128"):
            generator(129)


class TestCryptographicSecurity:
    """Tests to verify cryptographic security properties."""

    def test_uses_cryptographically_secure_randomness(self) -> None:
        """Verify strings use cryptographically secure random generation.

        This test checks that the distribution is reasonably uniform,
        which is a basic property of cryptographically secure randomness.
        """
        # Generate many strings and check character distribution
        combined = "".join(generate_alphanumeric(10) for _ in range(1000))

        # Count character frequencies
        char_counts = {}
        for char in combined:
            char_counts[char] = char_counts.get(char, 0) + 1

        # All alphanumeric characters should appear
        # (statistically very likely with 10000 characters)
        assert len(char_counts) > 50, "Character distribution seems too narrow"

        # Check that distribution is reasonably uniform
        # No character should dominate (appear > 3% of the time for 62 possible chars)
        max_count = max(char_counts.values())
        expected_frequency = len(combined) / 62  # 62 alphanumeric chars
        assert max_count < expected_frequency * 1.5, "Distribution seems biased"

    def test_no_predictable_patterns(self) -> None:
        """Verify generated strings don't have obvious patterns."""
        strings = [generate_alphanumeric(32) for _ in range(100)]

        # No string should be a substring of another
        for i, s1 in enumerate(strings):
            for j, s2 in enumerate(strings):
                if i != j:
                    assert s1 not in s2, "Found one string as substring of another"

        # No sequential patterns (like "abc", "123")
        for s in strings:
            # Check for 3+ sequential characters
            for i in range(len(s) - 2):
                if s[i:i + 3].isalpha():
                    chars = [ord(c) for c in s[i:i + 3]]
                    # Not sequential
                    assert not (
                        chars[1] == chars[0] + 1 and chars[2] == chars[1] + 1
                    ), f"Found sequential pattern in {s}"
