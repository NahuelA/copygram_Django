""" Verify new user. """

# Django
from .__modules__ import *
from django.conf import settings

# User
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# JWT
import jwt


class VerifyUserSerializer(serializers.Serializer):
    """Verify account serializer."""

    token = serializers.CharField()

    def validate_token(self, token):
        """Validate token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            raise serializers.ValidationError("Verification link has expired.")
        except jwt.exceptions.InvalidTokenError:
            raise serializers.ValidationError("Invalid token.")
        if payload["type"] != "email_confirmation":
            raise serializers.ValidationError(
                "Invalid type of verification. Most be email verification type."
            )
        self.context["payload"] = payload
        return token

    def save(self):
        """Activate account."""
        payload = self.context["payload"]
        user = User.objects.get(username=payload["user"])
        user.is_active = True
        user.save()


class TokenValidationSerializer(serializers.Serializer):
    """Serializer from Token."""

    token_related_user = serializers.CharField()

    def save(self, data):
        try:
            user = User.objects.get(username=data["token_related_user"])
            token = Token.objects.get(user=user.id)
        except jwt.exceptions.InvalidTokenError:
            serializers.ValidationError("Invalid token 'Unauthorized action!'")
        return token.key
