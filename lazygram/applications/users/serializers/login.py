""" Login serializer. """

# Django
from .__modules__ import *
from django.contrib.auth import (
    authenticate,
)

# Utils
import datetime

# Rest-framework jwt
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    """Login serializer class."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        trim_whitespace=True,
    )

    password = serializers.CharField(
        required=True,
        min_length=8,
    )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    # Validations
    def validate_login(self, data):
        """If the credentials not found."""
        response = {}

        if self.context.get("request") is None:
            raise serializers.ValidationError(
                "Context serializer need the request object to validate data."
            )

        auth = authenticate(
            username=data.get("username"),
            password=data.get("password"),
        )

        if auth is None:
            raise serializers.ValidationError(
                "Sorry, invalid credentials or not activated account. Please activate your account before sign up."
            )

        token = self.get_tokens_for_user(auth)
        auth.last_login = datetime.date.today()
        auth.save()

        response = {
            **token,
            "user": data.get("username"),
        }
        return response
