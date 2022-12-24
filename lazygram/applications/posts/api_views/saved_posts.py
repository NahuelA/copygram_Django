""" Post saves view. """

# Modules
from .__modules__ import *

# Models
from lazygram.applications.posts.models import Posts
from lazygram.applications.users.models import Profile
from lazygram.applications.posts.models import SavedPosts
from lazygram.applications.posts.serializers import SavedPostsSerializer


class SavedPostsView(ModelViewSet):
    """Save your favorite posts."""

    queryset = SavedPosts.objects.all()
    serializer_class = SavedPostsSerializer
    http_method_names = [
        "get",
        "post",
        "put",
        "head",
        "options",
        "trace",
    ]
    lookup_field = "profile__user__username"
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """Filter saved posts from matched profile."""
        profile = Profile.manager_object.get(user__username=request.user)
        queryset = self.queryset.filter(profile=profile)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Set favorite posts."""
        partial = kwargs.pop("partial", True)
        instance = self.get_object()

        # Getting authenticated user.
        post_to_save = Posts.objects.filter(id=request.data.get("saved_post")).first()
        dict_saved_post = post_to_save.__dict__

        data = {"saved_post": [dict_saved_post]}

        serializer = self.get_serializer(
            instance, data=data, partial=partial, context={"post_to_save": post_to_save}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data, status=status.HTTP_201_CREATED)
