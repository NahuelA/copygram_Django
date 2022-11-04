""" Create posts view. """

# Modules
from .__modules__ import *

# Models
from lazygram.applications.posts.models import Posts

# Serializer
from lazygram.applications.posts.serializers import PostsSerializer
from lazygram.applications.users.models import Profile


class PostsView(ModelViewSet):
    """Posts view.
    Return posts submited for the logged in users.
    """

    model = Posts
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    # permission_classes = (IsAuthenticated,)
    update_status = status.HTTP_201_CREATED
    serializer_class = PostsSerializer

    def perform_create(self, serializer, **kwargs):
        serializer.save(profile=kwargs["profile"])

    def perform_update(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):

        try:
            if request.GET.get("own_post") != None:
                try:
                    profile = Profile.manager_object.get(
                        user__username=request.GET.get("own_post")
                    )
                    queryset = self.model.objects.filter(profile=profile)
                except Exception as exc:
                    print(exc)
                    queryset = self.filter_queryset(self.get_queryset())
            else:
                queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # Exception
        except self.model.DoesNotExist as NotExist:
            return Response(NotExist.__dict__)

    def create(self, request, *args, **kwargs):

        # Getting instances and delete usernames in string type.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Getting profile
        profile = Profile.manager_object.get(user__username=request.user)
        self.perform_create(serializer, profile=profile)
        status_code = status.HTTP_201_CREATED
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status_code, headers=headers)

    def update(self, request, *args, **kwargs):
        """Update posts"""
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        # Getting authenticated user.
        profile = Profile.manager_object.get(user__username=request.user)
        profile_likedit = {"profile_likedit": [profile.id]}
        serializer = self.get_serializer(
            instance, data=profile_likedit, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
