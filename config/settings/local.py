"""Development settings."""

from .base import *  # NOQA
from .base import env

# Base
DEBUG = True

# Security
SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="PB3aGvTmCkzaLGRAxDc3aMayKTPTDd5usT8gw4pCmKOk5AlJjh12pTrnNgQyOHCH",
)

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

# SIMPLE-JWT
SIMPLE_JWT[
    "AUTH_COOKIE_DOMAIN"
] = "localhost"  # A string like "example.com", or None for standard domain cookie.
SIMPLE_JWT[
    "AUTH_COOKIE_SECURE"
] = False  # Whether the auth cookies should be secure (https:// only).

# CORS
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# Templates
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG  # NOQA

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = "587"
EMAIL_USE_TLS = True

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
