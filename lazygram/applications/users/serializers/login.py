""" Login serializer. """

# Django
from .__modules__ import *
from django.contrib.auth import (
    authenticate,
)

from .__modules__ import *

# Login update
from django.contrib.auth.models import update_last_login

# Settings
from config.settings.base import SIMPLE_JWT

# Rest-framework jwt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer

# Utils
import datetime


class LoginSerializer(TokenObtainSerializer):
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

    token_class = RefreshToken

    # Validations
    def validate(self, attrs):
        """If the credentials not found."""
        data = super().validate(attrs)

        auth = authenticate(
            username=attrs.get("username"),
            password=attrs.get("password"),
        )

        if auth is None:
            raise serializers.ValidationError(
                "Sorry, invalid credentials or not activated account. Please activate your account before sign up."
            )

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if SIMPLE_JWT.get("UPDATE_LAST_LOGIN"):
            update_last_login(None, self.user)

        response = {
            **data,
            "user": attrs.get("username"),
        }
        return response
