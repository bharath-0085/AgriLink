"""
Agri Link — Middleware
=======================
Request logging and security middleware.
"""

import logging
import time

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """
    Log every incoming request: method, path, status code, response time.
    Useful for debugging and monitoring.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration_ms = (time.time() - start) * 1000

        logger.info(
            "%s %s → %s (%.1f ms)",
            request.method,
            request.get_full_path(),
            response.status_code,
            duration_ms,
        )
        return response


class SecurityHeadersMiddleware:
    """
    Add common security headers to all responses.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
