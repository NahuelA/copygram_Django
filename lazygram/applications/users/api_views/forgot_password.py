"""Forgot password."""

# Rest-framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User

# Serializers
from lazygram.applications.users.serializers import (
    ForgotPasswordSerializer,
    SetNewPasswordSerializer,
)


class ForgotPassword(APIView):
    """Capture email and verify if is registered in the db.
    Send access token to allow change the password."""

    serializer_class = ForgotPasswordSerializer
    http_method_names = ["get", "post", "head", "options"]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ValidateSetPassword(APIView):
    """Authentication for set a new password."""

    user_model = User
    http_method_names = ["get", "post", "head", "options"]

    def authenticate(self, raw_token):
        if raw_token is None:
            return None

        validated_token = JWTAuthentication.get_validated_token(
            self, raw_token=raw_token
        )

        return (
            JWTAuthentication.get_user(self, validated_token=validated_token),
            validated_token,
        )

    def post(self, request):

        access_token = request.data.get("access")

        if access_token is not None:
            user = self.authenticate(access_token)

            data = {"access": str(user[1]), "username": str(user[0])}
            return Response(data, status=status.HTTP_200_OK)


class SetNewPassword(APIView):
    """Set new password."""

    permission_classes = (IsAuthenticated,)
    serializer_class = SetNewPasswordSerializer
    http_method_names = ["get", "post", "head", "options"]

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data,
            context={
                "confirm_passwd": request.data.get("confirm_passwd"),
                "user": request.user,
            },
        )
        serializer.is_valid(raise_exception=True)
        return Response({}, status=status.HTTP_201_CREATED)
