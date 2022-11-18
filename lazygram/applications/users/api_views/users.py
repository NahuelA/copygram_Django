""" Users view from users app. """

# Django
from .__modules__ import *

# Rest-framework
from lazygram.applications.users.serializers.users import UserSerializer

# Local serializers
from lazygram.applications.users.models import (
    Profile,
    FollowersModel,
    FollowingModel,
)


class UserView(ModelViewSet):
    """User view.
    Make crud and validations from user model.
    """

    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    update_status = status.HTTP_201_CREATED

    def get_permissions(self):
        """
        Instantiates and returns the list
        of permissions that this view requires.
        """
        permissions = (IsAuthenticated,)
        if self.action in ["create"]:
            permissions = (AllowAny,)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Create a new user and create your profile instance."""
        # Trim
        trimed_user = str(serializer.validated_data["username"]).replace(" ", "")
        lower_trimed_user = trimed_user.lower()
        serializer.save(is_active=False, username=lower_trimed_user)

        new_user = User.objects.filter(username=serializer.data["username"]).first()

        # Create a new profile instance.
        new_profile = Profile.manager_object.create(user=new_user)
        # Create a new follows instance.
        FollowersModel.objects.create(profile=new_profile)
        FollowingModel.objects.create(profile=new_profile)

    def perform_update(self, serializer):
        """Update an instance of the user."""
        trimed_user = str(serializer.validated_data["username"]).replace(" ", "")
        serializer.save(username=trimed_user, password=self.get_object().password)

    def create(self, request):
        """Sign up user from Lazygram."""
        # Validate a password confirmation match
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=self.update_status, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
