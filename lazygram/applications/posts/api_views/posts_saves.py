""" Post saves view. """

# Modules
from lazygram.applications.posts.models.posts import Posts
from lazygram.applications.users.models.profiles import Profile
from .__modules__ import *

# Models
from lazygram.applications.posts.models import PostSaves
from lazygram.applications.posts.serializers import PostsSavesSerializer


class PostSavesView(ModelViewSet):
    """Post saves.
    To save favorite posts.
    """

    model = PostSaves
    queryset = model.objects.all()
    serializer_class = PostsSavesSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """Save favorite posts."""
        profile = Profile.manager_object.get(user__username=request.user)
        saved_post = Posts.objects.filter(id=request.data.get("saved_post")).first()
        data_ = {
            "profile": profile,
            "saved_post": saved_post,
        }

        serializer = self.get_serializer(data=data_)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
