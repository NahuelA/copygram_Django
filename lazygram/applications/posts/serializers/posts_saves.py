""" Post saves serializer. """

# Django
from lazygram.applications.posts.serializers import PostsSerializer
from .__modules__ import *

# Local models.
from lazygram.applications.posts.models import PostSaves
from lazygram.applications.users.serializers import ProfileSerializer


class PostsSavesSerializer(serializers.ModelSerializer):
    """Post saves serializer."""

    profile = ProfileSerializer(read_only=True)
    post = PostsSerializer(read_only=True)

    class Meta:
        """Serializer meta class."""

        model = PostSaves
        fields = ["saved_post", "profile"]

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
            self.instance = self.create(validated_data)
            assert (
                self.instance is not None
            ), "`create()` did not return an object instance."

        return self.instance
