"""Forgot password serializer."""

# Rest-framework
from rest_framework import serializers, status
from django.contrib.auth.hashers import make_password

# PyJwt
import jwt

# Models
from django.contrib.auth.models import User

# Django
from django.core.validators import EmailValidator

# Celery
from lazygram.taskapp.tasks import send_forgot_password_email


class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True, max_length=170, min_length=8, validators=[EmailValidator()]
    )

    def validate(self, attrs):
        data = super().validate(attrs)

        try:
            instance = User.objects.get(email=data.get("email"))
            print(instance)
            if instance is not None:
                send_forgot_password_email.delay(instance.id)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Email not registered, please sign up.", status.HTTP_404_NOT_FOUND
            )

        return {}


class SetNewPasswordSerializer(serializers.Serializer):
    """Validate a new password."""

    password = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True,
    )

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.context.get("user")
        confirm_passwd = self.context.get("confirm_passwd")

        if confirm_passwd is None:
            raise serializers.ValidationError("Confirmation password is required.")

        if data.get("password") == confirm_passwd:
            user.password = make_password(data.get("password"))
            user.save()
        else:
            raise serializers.ValidationError(
                "Password and confirmation password does not match"
            )

        return data
