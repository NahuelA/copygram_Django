""" Posts app config. """

# Django
from django.apps import AppConfig


class LazygramAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lazygram.applications.posts"
    verbose_name = "Posts"
