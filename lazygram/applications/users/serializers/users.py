""" User serializer. """

# Rest-framework
from .__modules__ import *
from rest_framework.validators import UniqueValidator

# Django
from django.core.validators import EmailValidator
from django.contrib.auth.models import User

# Celery tasks
from lazygram.taskapp.tasks import send_confirmation_email


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
            send_confirmation_email.delay(user_id=self.instance.id)

        return self.instance
