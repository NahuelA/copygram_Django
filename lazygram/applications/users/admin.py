""" Admin site from users app. """

# Django
from django.contrib import admin
from .models import Profile

# Register your models here.


@admin.register(Profile)
class AdminUsers(admin.ModelAdmin):
    """Profile admin site."""

    list_display = ("user", "created")
    list_filter = ("user", "phone_number", "created")
    search_fields = ("user__username", "phone_number", "date_of_birth")
