""" Urls from users app. """

from django.urls import path, include

# Posts views
from lazygram.applications.posts.api_views import (
    PostsView,
    PostSavesView,
    CommentsPostView,
)

# Rest-framework
from rest_framework import routers

router = routers.DefaultRouter()

router.register(prefix=r"posts", viewset=PostsView, basename="posts-list")

router.register(prefix=r"comments", viewset=CommentsPostView, basename="comments")

router.register(prefix=r"posts_saves", viewset=PostSavesView, basename="posts_saves")

urlpatterns = [
    path(
        route="",
        view=include(router.urls),
    ),
]
