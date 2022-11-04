""" Login from users app. """

# Django
from .__modules__ import *

# Serializers
from lazygram.applications.users.serializers import LoginSerializer

# CSRF
from django.middleware import csrf

# Cache
from django.core.cache import cache

# Utils
from django.utils.cache import patch_vary_headers

# Settings
from config.settings import base


class LoginView(APIView):
    """Lazygram login system.
    Login with your logged account.
    """

    http_method_names = ["get", "post", "head", "options"]
    serializer_class = LoginSerializer

    def post(self, request):
        """[POST] Sign in to an account.
        Login after register.
        """
        serializer_login = LoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer_login.is_valid(raise_exception=True)
        validated_data = serializer_login.validate_login(serializer_login.data)
        response = Response(
            status=status.HTTP_201_CREATED,
        )

        # Set cookie
        response.set_cookie(
            key=base.SIMPLE_JWT["AUTH_COOKIE"],
            value=validated_data.get("access"),
            expires=base.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=base.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=base.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=base.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        csrf.get_token(request)  # Set CSRF token in the response
        response.data = {"success": "Login successfully", **validated_data}
        cache.set("refresh_token", validated_data.get("refresh"))

        # Set the Vary header since content varies with the sessiontoken cookie.
        patch_vary_headers(response, ("Cookie",))

        return response
