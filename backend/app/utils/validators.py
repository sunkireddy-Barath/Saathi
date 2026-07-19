"""
Custom field-level validators used in Pydantic schemas.

Centralising validators here prevents duplication across schema files and
gives us a single place to update validation logic.
"""

import re
from typing import Any


def validate_phone_number(value: str) -> str:
    """
    Validate and normalise an Indian mobile phone number.

    Accepts:
        - 10-digit numbers: 9876543210
        - With country code: +919876543210

    Returns:
        The normalised 10-digit number (without country code or spaces).

    Raises:
        ValueError: If the number does not match any accepted format.
    """
    cleaned = re.sub(r"[\s\-()]", "", value)
    if cleaned.startswith("+91"):
        cleaned = cleaned[3:]
    if cleaned.startswith("91") and len(cleaned) == 12:
        cleaned = cleaned[2:]
    if not re.fullmatch(r"[6-9]\d{9}", cleaned):
        raise ValueError("Invalid Indian mobile number. Must be a 10-digit number starting with 6-9.")
    return cleaned


def validate_gst_number(value: str) -> str:
    """
    Validate an Indian GST identification number (GSTIN).

    Format: 2-digit state code + 10-char PAN + 1-digit entity + 1 'Z' + 1 check digit
    Example: 27ABCDE1234F1Z5
    """
    pattern = r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$"
    if not re.fullmatch(pattern, value.upper()):
        raise ValueError("Invalid GSTIN format. Example: 27ABCDE1234F1Z5")
    return value.upper()


def validate_aadhaar_number(value: str) -> str:
    """
    Validate an Indian Aadhaar number (12 digits, cannot start with 0 or 1).
    """
    cleaned = value.replace(" ", "")
    if not re.fullmatch(r"[2-9]\d{11}", cleaned):
        raise ValueError("Invalid Aadhaar number. Must be 12 digits and not start with 0 or 1.")
    return cleaned


def validate_positive_number(value: float, field_name: str = "value") -> float:
    """Raise ValueError if *value* is not strictly positive."""
    if value <= 0:
        raise ValueError(f"{field_name} must be a positive number.")
    return value


def validate_non_negative_number(value: float, field_name: str = "value") -> float:
    """Raise ValueError if *value* is negative."""
    if value < 0:
        raise ValueError(f"{field_name} must be zero or a positive number.")
    return value


def validate_password_strength(password: str) -> str:
    """
    Enforce a minimum password policy:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character

    Raises:
        ValueError: With a descriptive message if policy is not met.
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-]", password):
        raise ValueError("Password must contain at least one special character.")
    return password
