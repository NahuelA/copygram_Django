from django.apps import AppConfig


class DmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lazygram.applications.dm"
    verbose_name = "Direct message"
