""" Followers and following app. """

# Django
from .__modules__ import *

# Local models
from lazygram.applications.users.models import Profile, FollowersModel, FollowingModel

# Rest-framework
from lazygram.applications.users.serializers import (
    FollowersSerializer,
    FollowingSerializer,
)


class FollowersView(ModelViewSet):
    """Profile followers."""

    model = Profile
    queryset = FollowersModel.objects.all()
    serializer_class = FollowersSerializer
    permission_classes = (IsAuthenticated,)
    update_status = status.HTTP_201_CREATED
    lookup_field = "profile__user__username"
    http_method_names = ["get", "put", "patch", "delete", "head", "options"]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        to = Profile.manager_object.get(user__username=request.data.get("profile"))
        follow_to = Profile.manager_object.get(
            user__username=request.data.get("followers")
        )

        # Profile
        data_ = {
            "profile": to,
            "followers": [follow_to.id],
        }

        serializer = self.get_serializer(instance, data=data_, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=self.update_status)


class FollowingView(ModelViewSet):
    """Profile followers."""

    model = Profile
    queryset = FollowingModel.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = (IsAuthenticated,)
    update_status = status.HTTP_201_CREATED
    lookup_field = "profile__user__username"
    http_method_names = ["get", "put", "patch", "delete", "head", "options"]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        to = Profile.manager_object.get(user__username=request.data.get("profile"))
        follow_to = Profile.manager_object.get(
            user__username=request.data.get("following")
        )

        # Profile
        data_ = {
            "profile": to,
            "following": [follow_to.id],
        }

        serializer = self.get_serializer(instance, data=data_, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=self.update_status)


class IsFollowedView(APIView):
    """If a profile is followed, return false."""

    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "head", "options"]

    def get(self, request, *args, **kwargs):
        myfollowing = FollowingModel.objects.get(
            profile__user__username=kwargs.get("profile")
        )
        profile = Profile.manager_object.get(
            user__username=request.GET.get("myprofile")
        )

        if myfollowing != None and profile in myfollowing.following.all():
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_200_OK)
