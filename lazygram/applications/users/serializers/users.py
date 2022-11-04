""" User serializer. """

# Rest-framework
from .__modules__ import *
from rest_framework.validators import UniqueValidator

# Django
from django.template.loader import render_to_string
from django.core.validators import EmailValidator
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.models import User

# Local settings
from django.conf import settings

# Utilities
from datetime import timedelta
from django.utils import timezone

# JWT
import jwt


class UserSerializer(serializers.ModelSerializer):
    """User serializer class."""

    username = serializers.CharField(
        required=True,
        max_length=170,
        min_length=2,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        max_length=170,
        min_length=8,
        validators=[EmailValidator(), UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True,
    )

    first_name = serializers.CharField(max_length=100, required=False)

    last_name = serializers.CharField(max_length=100, required=False)

    class Meta:
        """Meta options for serializer users."""

        model = User
        exclude = ["id", "is_staff", "is_superuser", "groups", "user_permissions"]
        lookup_field = "username"

    def save(self, **kwargs):
        assert hasattr(
            self, "_errors"
        ), "You must call `.is_valid()` before calling `.save()`."

        assert (
            not self.errors
        ), "You cannot call `.save()` on a serializer with invalid data."

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert "commit" not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, "_data"), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert (
                self.instance is not None
            ), "`update()` did not return an object instance."
        else:
            self.instance = User.objects.create_user(**validated_data)
            assert (
                self.instance is not None
            ), "`create()` did not return an object instance."
            self.send_confirmation_email(self.instance)

        return self.instance

    def send_confirmation_email(self, user):
        """Send email to confirmation account."""
        verification_token = self.verification_token(user)
        subject = f"Welcome @{user}, please verify your account then you will be redirected to your Lazygram profile."
        from_email = "Lazygram <noreply@lazygram.com>"
        html_content = render_to_string(
            "emails/users/account_verification.html",
            {"user": user, "token": verification_token},
        )
        msg = EmailMultiAlternatives(subject, html_content, from_email, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def verification_token(self, user):
        """Verify account with JWT."""

        exp_date = timezone.now() + timedelta(hours=1)
        payload = {
            "user": user.username,
            "exp": int(exp_date.timestamp()),
            "type": "email_confirmation",
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
