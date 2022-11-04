""" Profile serializer. """

# Django
from .__modules__ import *
import traceback
from django.core.validators import RegexValidator, URLValidator

# Local models
from lazygram.applications.users.models import Profile
from lazygram.applications.users.serializers.users import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer class."""

    user = UserSerializer(read_only=True)

    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )

    phone_number = serializers.CharField(
        validators=[phone_regex],
        max_length=17,
        required=False,
    )

    website = serializers.URLField(
        validators=[URLValidator(schemes=["https"])], required=False
    )
    picture = serializers.FileField(required=False)
    date_of_birth = serializers.DateTimeField(required=False)
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)
    posts_count = serializers.IntegerField(required=False)

    class Meta:
        """Meta options from serializer profile."""

        model = Profile
        fields = [
            "user",
            "created",
            "modified",
            "picture",
            "biography",
            "date_of_birth",
            "website",
            "phone_number",
            "posts_count",
        ]
        lookup_field = "user__username"

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

        return self.instance
