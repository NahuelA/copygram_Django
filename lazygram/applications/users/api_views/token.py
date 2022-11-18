""" JWT tokens. """

# Rest-framework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Utils
from django.utils.module_loading import import_string

# Rest-framework-simplejwt
from config.settings.base import SIMPLE_JWT
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Serializers
from lazygram.applications.users.serializers import (
    TokenValidationSerializer,
)

# CSRF
from django.middleware import csrf

# Cookies
from lazygram.applications.users.utils import jwt_cookie

# Utils
from django.utils.cache import patch_vary_headers


class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None
    _serializer_class = ""

    www_authenticate_realm = "api"

    def get_serializer_class(self):
        """
        If serializer_class is set, use it directly. Otherwise get the class from settings.
        """

        if self.serializer_class:
            return self.serializer_class
        try:
            return import_string(self._serializer_class)
        except ImportError:
            msg = "Could not import serializer '%s'" % self._serializer_class
            raise ImportError(msg)

    def get_authenticate_header(self, request):
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response = Response(status=status.HTTP_200_OK)

        try:
            serializer.is_valid(raise_exception=True)

            # Set jwt cookie in the browser
            jwt_cookie(serializer.validated_data.get("access"), response)
            response.data = serializer.validated_data

            csrf.get_token(request)  # Set CSRF token in the response
            # Set the Vary header since content varies with the sessiontoken cookie.
            patch_vary_headers(response, ("Cookie",))

        except TokenError as e:
            raise InvalidToken(e.args[0])

        return response


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    _serializer_class = SIMPLE_JWT.get("TOKEN_OBTAIN_SERIALIZER")


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    _serializer_class = SIMPLE_JWT.get("TOKEN_REFRESH_SERIALIZER")


class TokenValidationRegister(APIView):
    """Verify if your token is registered, then active account."""

    serializer_class = TokenValidationSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
