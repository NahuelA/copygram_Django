"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    # Posts
    path(
        route="",
        view=include(
            ("lazygram.applications.posts.routers", "posts"),
            namespace="posts",
        ),
    ),
    # Accounts
    path(
        route="accounts/",
        view=include(
            ("lazygram.applications.users.routers", "users"),
            namespace="users",
        ),
    ),
    # Direct messages
    path(
        route="direct-messages/",
        view=include(
            ("lazygram.applications.dm.routers", "dm"),
            namespace="dm",
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
