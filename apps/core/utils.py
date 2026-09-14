"""
Agri Link — Shared Utilities
==============================
Cloudinary upload helper, pagination, response formatters, geo helpers.
"""

import logging
import math
import uuid

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


# ============================================================
# Standard JSON Response Helpers
# ============================================================

def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """Return a consistent success JSON envelope."""
    return Response(
        {"success": True, "message": message, "data": data},
        status=status_code,
    )


def error_response(message="An error occurred", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """Return a consistent error JSON envelope."""
    return Response(
        {"success": False, "message": message, "error": message, "errors": errors},
        status=status_code,
    )


# ============================================================
# Pagination
# ============================================================

class StandardPagination(PageNumberPagination):
    """Standard pagination with configurable page size."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "success": True,
                "message": "Success",
                "data": {
                    "count": self.page.paginator.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "results": data,
                },
            }
        )


# ============================================================
# Cloudinary Upload
# ============================================================

def upload_to_cloudinary(file, folder="agrilink"):
    """
    Upload a file to Cloudinary and return the secure URL.

    Args:
        file: Django UploadedFile or file-like object.
        folder: Cloudinary folder name.

    Returns:
        str: Secure URL of the uploaded image.

    Raises:
        Exception: If Cloudinary upload fails.
    """
    try:
        import cloudinary.uploader

        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="image",
            public_id=f"{folder}_{uuid.uuid4().hex[:12]}",
            overwrite=True,
            transformation=[
                {"quality": "auto", "fetch_format": "auto"},
            ],
        )
        return result.get("secure_url", "")
    except ImportError:
        logger.error("Cloudinary is not configured. Set CLOUDINARY_* env vars.")
        raise ValueError("Cloudinary is not configured.")
    except Exception as e:
        logger.error("Cloudinary upload failed: %s", e)
        raise ValueError(f"Image upload failed: {e}")


# ============================================================
# Geographic Utilities
# ============================================================

def haversine_distance(lat1, lng1, lat2, lng2):
    """
    Calculate the great-circle distance between two GPS points (in km).

    Uses the Haversine formula.
    """
    R = 6371  # Earth radius in km

    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def get_nearby_users(queryset, lat, lng, radius_km=50):
    """
    Filter a queryset of objects with gps_lat/gps_lng fields
    to those within `radius_km` km of the given coordinates.

    Returns a list of (object, distance_km) tuples sorted by distance.
    """
    results = []
    for obj in queryset.filter(
        gps_lat__isnull=False,
        gps_lng__isnull=False,
    ):
        dist = haversine_distance(lat, lng, obj.gps_lat, obj.gps_lng)
        if dist <= radius_km:
            results.append((obj, round(dist, 2)))
    results.sort(key=lambda x: x[1])
    return results


# ============================================================
# Profile Completion Calculator
# ============================================================

def calculate_profile_completion(user):
    """
    Calculate profile completion percentage based on filled fields.
    Returns an integer 0–100.
    """
    fields = [
        user.name,
        user.phone,
        user.email,
        user.profile_photo_url,
        user.address,
        user.district,
        user.state,
        user.village,
        user.gps_lat,
        user.gps_lng,
    ]
    filled = sum(1 for f in fields if f)
    return int((filled / len(fields)) * 100)


# ============================================================
# Token Generation
# ============================================================

def generate_auth_token():
    """Generate a random 64-char hex token."""
    return uuid.uuid4().hex + uuid.uuid4().hex


def generate_verification_token():
    """Generate a random token for email verification / password reset."""
    return uuid.uuid4().hex
