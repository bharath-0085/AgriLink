"""
Agri Link — Custom DRF Authentication
=======================================
Token-based authentication using AuthToken model.
Supports both Firebase-verified users and email/password users.
"""

import logging

from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class TokenAuthentication(BaseAuthentication):
    """
    Custom token authentication.

    Expects header:
        Authorization: Token <auth_token>

    Looks up the token in the AuthToken model.
    """

    keyword = "Token"

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        token_value = parts[1]
        return self._authenticate_token(token_value)

    def _authenticate_token(self, token_value):
        # Import here to avoid circular imports
        from apps.accounts.models import AuthToken

        try:
            token = AuthToken.objects.get(token=token_value)
        except AuthToken.DoesNotExist:
            raise AuthenticationFailed("Invalid authentication token.")

        # Check expiry (tokens expire after 30 days)
        if token.is_expired():
            token.delete()
            raise AuthenticationFailed("Authentication token has expired.")

        if not token.user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        # Update last used timestamp
        token.last_used_at = timezone.now()
        token.save(update_fields=["last_used_at"])

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword


class OptionalTokenAuthentication(TokenAuthentication):
    """
    Token authentication that falls back to None (AnonymousUser) if the token is
    invalid, expired, or missing, rather than raising AuthenticationFailed.
    Enables public/demo endpoints to identify logged-in users when possible without
    blocking unauthenticated or guest users.
    """

    def _authenticate_token(self, token_value):
        try:
            return super()._authenticate_token(token_value)
        except AuthenticationFailed:
            return None

