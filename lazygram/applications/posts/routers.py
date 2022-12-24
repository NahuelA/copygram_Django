""" Urls from users app. """

from django.urls import path, include

# Posts views
from lazygram.applications.posts.api_views import (
    PostsView,
    ProfilePost,
    SavedPostsView,
    CommentsPostView,
)

# Rest-framework
from rest_framework import routers

router = routers.DefaultRouter()

router.register(prefix=r"posts", viewset=PostsView, basename="posts-list")

router.register(prefix=r"comments", viewset=CommentsPostView, basename="comments")

router.register(prefix=r"saved_posts", viewset=SavedPostsView, basename="saved_posts")

urlpatterns = [
    path(
        route="",
        view=include(router.urls),
    ),
    path(route="profile-posts/<str:profile>", view=ProfilePost.as_view()),
]
