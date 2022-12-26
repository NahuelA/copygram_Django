""" Posts serializer. """

# Django
from readline import insert_text
from .__modules__ import *

# Local models.
from ..models import Posts
from lazygram.applications.users.serializers import ProfileSerializer


class PostsSerializer(serializers.ModelSerializer):
    """Post serializer.
    Serialize and validate fields from posts.
    """

    profile = ProfileSerializer(read_only=True)
    picture = serializers.FileField(required=True)

    class Meta:
        """Meta serializer from posts."""

        model = Posts
        fields = "__all__"

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
            profile_likedit = validated_data["profile_likedit"]
            if profile_likedit is not None:

                likedit = None
                profile_likedit_all = self.instance.profile_likedit
                # Look profile that liked it.
                for i in profile_likedit_all.all():
                    if i == profile_likedit[0]:
                        likedit = i
                        break
                del validated_data["profile_likedit"]

                if likedit != None and self.instance.likes > 0:
                    # Remove like and profile that liked it
                    self.instance.profile_likedit.remove(profile_likedit[0].id)
                    self.instance.likes -= 1
                else:
                    # Add Like and profile that liked it
                    self.instance.profile_likedit.add(profile_likedit[0].id)
                    self.instance.likes += 1

            self.instance = self.update(self.instance, validated_data)

            assert (
                self.instance is not None
            ), "`update()` did not return an object instance."

        else:
            self.instance = self.create(validated_data)
            # Add +1 post
            self.instance.profile.posts_count += 1
            self.instance.profile.save()

            assert (
                self.instance is not None
            ), "`create()` did not return an object instance."

        return self.instance
