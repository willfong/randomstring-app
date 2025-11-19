"""Cryptographically secure random string generator.

This module provides functions to generate various types of random strings
using Python's secrets module for cryptographic security.

All functions validate input length (1-128 characters) and raise ValueError
for invalid inputs.
"""

import secrets
import string


# Constants for character sets
ALPHANUMERIC_CHARS = string.ascii_letters + string.digits  # a-zA-Z0-9
DISTINGUISHABLE_CHARS = "23456789ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnpqrstwxyz"
# Shell-safe password characters: exclude all shell metacharacters and problematic chars
# Excluded: space, !, ", #, $, &, ', (, ), *, ;, <, >, ?, @, [, \, ], ^, `, {, |, }, ~
SHELL_UNSAFE_CHARS = set(" !\"#$&'()*;<>?@[\\]^`{|}~")
PASSWORD_CHARS = "".join(
    chr(i) for i in range(33, 127) if chr(i) not in SHELL_UNSAFE_CHARS
)
URLSAFE_CHARS = string.ascii_letters + string.digits + "-_"  # a-zA-Z0-9-_
LOWERCASE_CHARS = string.ascii_lowercase  # a-z

# Length constraints
MIN_LENGTH = 1
MAX_LENGTH = 128


def _validate_length(length: int) -> None:
    """Validate that the requested length is within acceptable bounds.

    Args:
        length: The requested string length.

    Raises:
        ValueError: If length is not between MIN_LENGTH and MAX_LENGTH.
    """
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        msg = f"Length must be between {MIN_LENGTH} and {MAX_LENGTH}"
        raise ValueError(msg)


def generate_alphanumeric(length: int) -> str:
    """Generate a cryptographically secure random alphanumeric string.

    The generated string contains only characters from: a-z, A-Z, 0-9

    Args:
        length: The desired length of the string (1-128).

    Returns:
        A random alphanumeric string of the specified length.

    Raises:
        ValueError: If length is not between 1 and 128.

    Example:
        >>> s = generate_alphanumeric(32)
        >>> len(s)
        32
        >>> all(c.isalnum() for c in s)
        True
    """
    _validate_length(length)
    return "".join(secrets.choice(ALPHANUMERIC_CHARS) for _ in range(length))


def generate_distinguishable(length: int) -> str:
    """Generate a random string using easily distinguishable characters.

    This function generates strings that avoid visually similar characters,
    making them easier to read and transcribe. It excludes characters like:
    0/O, 1/l/I, g/q, u/v, etc.

    Character set: 23456789ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnpqrstwxyz

    Args:
        length: The desired length of the string (1-128).

    Returns:
        A random string of easily distinguishable characters.

    Raises:
        ValueError: If length is not between 1 and 128.

    Example:
        >>> s = generate_distinguishable(32)
        >>> len(s)
        32
        >>> "0" not in s and "O" not in s  # Confusing chars excluded
        True
    """
    _validate_length(length)
    return "".join(secrets.choice(DISTINGUISHABLE_CHARS) for _ in range(length))


def generate_password(length: int) -> str:
    """Generate a cryptographically secure shell-safe password.

    The generated string includes letters, numbers, and safe special characters.
    All shell metacharacters and problematic characters are excluded to ensure
    the password can be used directly in command-line contexts without escaping.

    Included: a-z, A-Z, 0-9, and safe punctuation: % + , - . / : = _
    Excluded: All shell metacharacters and quotes

    Args:
        length: The desired length of the password (1-128).

    Returns:
        A random shell-safe password string.

    Raises:
        ValueError: If length is not between 1 and 128.

    Example:
        >>> s = generate_password(32)
        >>> len(s)
        32
        >>> all(c.isalnum() or c in "%+,-./:=_" for c in s)
        True
    """
    _validate_length(length)
    return "".join(secrets.choice(PASSWORD_CHARS) for _ in range(length))


def generate_urlsafe(length: int) -> str:
    """Generate a URL-safe random string.

    The generated string contains only characters that are safe for use in URLs
    without encoding: a-z, A-Z, 0-9, -, _

    Args:
        length: The desired length of the string (1-128).

    Returns:
        A random URL-safe string.

    Raises:
        ValueError: If length is not between 1 and 128.

    Example:
        >>> s = generate_urlsafe(32)
        >>> len(s)
        32
        >>> all(c.isalnum() or c in "-_" for c in s)
        True
    """
    _validate_length(length)
    return "".join(secrets.choice(URLSAFE_CHARS) for _ in range(length))


def generate_lowercase(length: int) -> str:
    """Generate a random lowercase letter-only string.

    The generated string contains only lowercase letters: a-z

    Args:
        length: The desired length of the string (1-128).

    Returns:
        A random lowercase string.

    Raises:
        ValueError: If length is not between 1 and 128.

    Example:
        >>> s = generate_lowercase(32)
        >>> len(s)
        32
        >>> s.islower() and s.isalpha()
        True
    """
    _validate_length(length)
    return "".join(secrets.choice(LOWERCASE_CHARS) for _ in range(length))
