""" Comments view. """

# Modules
from .__modules__ import *

# Models
from lazygram.applications.posts.models import Comments, Posts
from lazygram.applications.users.models import Profile
from ..serializers import CommentsSerializer


class CommentsPostView(ModelViewSet):
    """Comments for posts.
    Comments system for writing comments in the posts.
    """

    model = Comments
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    http_method_names = ["get", "post", "put", "patch", "head", "options"]
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(commented_by=kwargs["commented_by"])

    def list(self, request, *args, **kwargs):
        try:
            id = int(request.GET["id_post"])
            queryset = self.get_queryset().filter(post=id)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            raise Response("")

    def create(self, request, *args, **kwargs):
        # Getting instances.
        post = Posts.objects.get(id=request.data["post"])
        profile = Profile.manager_object.filter(user=request.user).first()

        data_ = {
            "post": post.id,
            "comment": request.data["comment"],
        }

        serializer = self.get_serializer(data=data_)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, commented_by=profile)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
