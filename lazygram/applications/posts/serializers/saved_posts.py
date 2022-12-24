""" Post saves serializer. """

# Django
from .__modules__ import *

# Local models.
from lazygram.applications.posts.models import SavedPosts
from lazygram.applications.users.serializers import ProfileSerializer
from lazygram.applications.posts.serializers import PostsSerializer


class SavedPostsSerializer(serializers.ModelSerializer):
    """Post saves serializer."""

    profile = ProfileSerializer(read_only=True)
    saved_post = PostsSerializer(read_only=True, many=True)

    class Meta:
        """Serializer meta class."""

        model = SavedPosts
        fields = ["saved_post", "profile"]
        lookup_field = "profile__user__username"

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

        if self.instance is not None:
            # If a post is in saved_post array, remove it. Else add it
            post = self.context.get("post_to_save")
            saved_post = self.instance.saved_post
            save = True

            for i in saved_post.all():
                if i == post:
                    self.instance.saved_post.remove(post)
                    self.instance.save()
                    save = False
                    break

            if save:
                self.instance.saved_post.add(post)
                self.instance.save()

            assert (
                self.instance is not None
            ), "`update()` did not return an object instance."

        return self.instance
