""" Admin site from posts app. """

# Django
from django.contrib import admin

# Models
from lazygram.applications.posts.models import Posts

# Register your models here.


@admin.register(Posts)
class AdminPosts(admin.ModelAdmin):
    """Posts admin site."""

    list_display = ("profile", "created")
    list_filter = ("created",)
    search_fields = ("profile",)
