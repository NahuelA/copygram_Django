""" Logout from users app. """

# Django
from .__modules__ import *

# CSRF
from django.middleware import csrf

# Cache
from django.core.cache import cache

# JWT
from rest_framework_simplejwt.authentication import JWTAuthentication


class LogoutView(JWTAuthentication):
    """Logout from account."""

    http_method_names = ["get", "post", "head", "options"]

    def post(self, request):
        """[POST] Sign in to an account.
        Login after register.
        """
        print("My cookies", request.COOKIES)
        print("My refresh token in cache", cache.get("refresh_token"))

        user, token = self.authenticate(request)
        if token is not None:
            csrf.get_token(request)

            if cache.get("refresh_token") != None:
                cache.delete("refresh_token")
                request.COOKIES.pop("refresh_token")

        return Response(status=status.HTTP_204_NO_CONTENT)
