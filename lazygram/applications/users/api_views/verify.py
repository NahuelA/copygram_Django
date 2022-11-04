""" Verify new user. """

# Django
from .__modules__ import *

# Rest-framework
from rest_framework.settings import api_settings

# Local serializers
from lazygram.applications.users.serializers import (
    VerifyUserSerializer,
    LoginSerializer,
    TokenValidationSerializer,
)


class VerifyView(APIView):
    """Validate account."""

    serializer_class = VerifyUserSerializer
    update_status = status.HTTP_200_OK

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request):
        """Save validation token account."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=self.update_status, headers=headers)


class TokenView(APIView):
    """Getting token to validation your authentication."""

    serializer_class = TokenValidationSerializer
    update_status = status.HTTP_200_OK

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save(serializer.validated_data)

        headers = self.get_success_headers(serializer.data)
        return Response(token, status=self.update_status, headers=headers)
