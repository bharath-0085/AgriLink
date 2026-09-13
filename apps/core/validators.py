"""
Agri Link — Input Validators
==============================
Reusable validators for phone numbers, coordinates, images, and more.
"""

import re
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """
    Validate phone number: must be digits only (after optional leading +),
    between 7 and 15 digits.
    """
    cleaned = value.strip()
    pattern = r"^\+?\d{7,15}$"
    if not re.match(pattern, cleaned):
        raise ValidationError(
            "Enter a valid phone number (7–15 digits, optional leading +)."
        )


def validate_latitude(value):
    """Latitude must be between -90 and 90."""
    if value is not None and (value < -90 or value > 90):
        raise ValidationError("Latitude must be between -90 and 90.")


def validate_longitude(value):
    """Longitude must be between -180 and 180."""
    if value is not None and (value < -180 or value > 180):
        raise ValidationError("Longitude must be between -180 and 180.")


def validate_rating(value):
    """Rating must be between 1 and 5."""
    if value < 1 or value > 5:
        raise ValidationError("Rating must be between 1 and 5.")


def validate_positive_price(value):
    """Price must be positive."""
    if value is not None and value < 0:
        raise ValidationError("Price cannot be negative.")


def validate_image_file(file):
    """
    Validate uploaded image file:
    - Max size: 10 MB
    - Allowed types: JPEG, PNG, WEBP
    """
    max_size = 10 * 1024 * 1024  # 10 MB
    allowed_types = ["image/jpeg", "image/png", "image/webp"]

    if file.size > max_size:
        raise ValidationError("Image file size must be under 10 MB.")

    if hasattr(file, "content_type") and file.content_type not in allowed_types:
        raise ValidationError(
            f"Unsupported image type '{file.content_type}'. "
            f"Allowed: JPEG, PNG, WEBP."
        )


def validate_country_code(value):
    """Validate country code starts with + followed by 1-3 digits."""
    if not re.match(r"^\+\d{1,3}$", value.strip()):
        raise ValidationError("Enter a valid country code (e.g. +91).")


def validate_password_strength(password):
    """
    Enforce strong password:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character.")
    if errors:
        raise ValidationError(errors)
