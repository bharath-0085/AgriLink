"""
Agri Link — Custom Exception Handling
=======================================
Custom exceptions and DRF exception handler for consistent JSON error responses.
"""

import logging

from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status

logger = logging.getLogger(__name__)


# ============================================================
# Custom DRF Exception Handler
# ============================================================

def custom_exception_handler(exc, context):
    """
    Wrap all DRF exceptions in a consistent JSON envelope:
    {
        "success": false,
        "message": "...",
        "errors": {...} or null
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Extract error detail
        if isinstance(response.data, dict):
            detail = response.data.get("detail", None)
            errors = {
                k: v for k, v in response.data.items() if k != "detail"
            } or None
            message = str(detail) if detail else "Validation error."
            if not detail and errors:
                # Flatten first error as message
                first_key = next(iter(errors))
                first_val = errors[first_key]
                if isinstance(first_val, list):
                    message = f"{first_key}: {first_val[0]}"
                else:
                    message = f"{first_key}: {first_val}"
        elif isinstance(response.data, list):
            message = response.data[0] if response.data else "An error occurred."
            errors = response.data
        else:
            message = str(response.data)
            errors = None

        response.data = {
            "success": False,
            "message": message,
            "errors": errors,
        }
    else:
        # Unhandled exception — log and return 500
        logger.exception("Unhandled exception in %s", context.get("view", "unknown"))

    return response


# ============================================================
# Custom Exception Classes
# ============================================================

class AgriLinkException(APIException):
    """Base exception for Agri Link."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "An error occurred."
    default_code = "error"


class InvalidFirebaseTokenError(AgriLinkException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid or expired Firebase token."
    default_code = "invalid_firebase_token"


class UserAlreadyExistsError(AgriLinkException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "A user with this phone number or email already exists."
    default_code = "user_already_exists"


class UserNotFoundError(AgriLinkException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User not found."
    default_code = "user_not_found"


class InvalidCredentialsError(AgriLinkException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid credentials."
    default_code = "invalid_credentials"


class PermissionDeniedError(AgriLinkException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"


class ResourceNotFoundError(AgriLinkException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Requested resource not found."
    default_code = "not_found"


class AIModelError(AgriLinkException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "AI model is currently unavailable."
    default_code = "ai_model_error"


class ExternalServiceError(AgriLinkException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "External service is unavailable."
    default_code = "external_service_error"


class OTPError(AgriLinkException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = "Too many OTP requests. Please wait before retrying."
    default_code = "otp_rate_limited"


class EmailNotVerifiedError(AgriLinkException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Email address has not been verified."
    default_code = "email_not_verified"
