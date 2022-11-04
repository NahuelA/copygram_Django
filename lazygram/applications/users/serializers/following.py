""" Following serializer. """

# Django
from lazygram.applications.users.models.follow import FollowingModel
from lazygram.applications.users.serializers.profile import ProfileSerializer
from .__modules__ import *


class FollowingSerializer(serializers.ModelSerializer):
    """Following serializer class."""

    profile = ProfileSerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = FollowingModel
        lookup_field = "user__usename"

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
            # New follow instance
            new_follow = validated_data["following"]

            if new_follow is not None:
                following = None
                followings = self.instance.following
                # Look profile that liked it.
                for i in followings.all():
                    if i == new_follow[0]:
                        following = i
                        break
                del validated_data["following"]

                # Remove like and profile that liked it
                if following != None and self.instance.following_length > 0:
                    self.instance.following.remove(new_follow[0].id)
                    self.instance.following_length -= 1

                # Add Like and profile that liked it
                else:
                    self.instance.following.add(new_follow[0].id)
                    self.instance.following_length += 1

            self.instance = self.update(self.instance, validated_data)

            assert (
                self.instance is not None
            ), "`update()` did not return an object instance."
        return self.instance
