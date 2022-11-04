from django.contrib import admin

# Register your models here.
from lazygram.applications.dm.models import Dm


@admin.register(Dm)
class AdminDM(admin.ModelAdmin):
    """Posts admin site."""

    list_display = ("profile_from", "to", "created")
    list_filter = ("created", "profile_from", "viewed")
    search_fields = ("profile_from", "to", "created")
