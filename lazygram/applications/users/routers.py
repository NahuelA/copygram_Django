""" Urls from users app. """

from django.urls import path, include

# User views
from lazygram.applications.users.api_views import (
    LoginView,
    UserView,
    LogoutView,
    VerifyView,
    TokenView,
    ProfileView,
    ProfilesSearchView,
    FollowingView,
    FollowersView,
    IsFollowedView,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix=r"profiles", viewset=ProfileView, basename="profiles-router")

router.register(prefix=r"users", viewset=UserView, basename="users")

router.register(prefix=r"followers", viewset=FollowersView, basename="followers")

router.register(prefix=r"followings", viewset=FollowingView, basename="following")


# Crud
urlpatterns = [
    path("", include(router.urls)),
]

# Utils
urlpatterns += [
    # Login
    path(
        route="login/",
        view=LoginView.as_view(),
        name="login",
    ),
    # Logout
    # path(
    #     route="logout/",
    #     view=LogoutView.as_view(),
    #     name="logout",
    # ),
    # Verify account
    path(route="verify-account/", view=VerifyView.as_view(), name="verify_account"),
    # Verify token
    path(route="verify-token/", view=TokenView.as_view(), name="verify_token"),
    # Isfollowed
    path(
        route="isfollowed/<str:profile>",
        view=IsFollowedView.as_view(),
        name="isfollowed",
    ),
    # Search profile
    path(
        route="profile/<str:search_profiles>",
        view=ProfilesSearchView.as_view(),
        name="search_profile",
    ),
    path(
        route="profile/",
        view=ProfilesSearchView.as_view(),
        name="search_profile",
    ),
]
