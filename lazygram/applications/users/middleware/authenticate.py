""" JWT authentication. """
from rest_framework_simplejwt.authentication import JWTAuthentication
from config.settings import base

from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions


class CustomAuthentication(JWTAuthentication):
    """Autenticated user.
    Middleware to authenticate users that sign in.
    """

    def enforce_csrf(self, request):
        """Check and add header CSRF_COOKIE."""
        check = CSRFCheck(request)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)

    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(base.SIMPLE_JWT.get("AUTH_COOKIE")) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        self.enforce_csrf(request)
        return self.get_user(validated_token), validated_token
