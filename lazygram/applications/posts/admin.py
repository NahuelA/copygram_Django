""" Admin site from posts app. """

# Django
from django.contrib import admin

# Models
from lazygram.applications.posts.models import Posts, SavedPosts

# Register your models here.


@admin.register(Posts)
class AdminPosts(admin.ModelAdmin):
    """Posts admin site."""

    list_display = ("profile", "created")
    list_filter = ("created",)
    search_fields = ("profile",)


@admin.register(SavedPosts)
class AdminSavedPosts(admin.ModelAdmin):
    """Saved post admin site."""

    list_display = ("profile",)
    list_filter = ("profile",)
    search_fields = ("profile",)
