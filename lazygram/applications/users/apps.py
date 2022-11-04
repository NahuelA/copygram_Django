""" Users app config. """

# Django
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lazygram.applications.users"
    verbose_name = "Users"
