""" Routes from Direct messages. """

# Django
from django.urls import path, include
from lazygram.applications.dm.api_views import DmView

# Rest-framework
from rest_framework import routers

router = routers.DefaultRouter()

# Register view
router.register(prefix=r"direct-message", viewset=DmView, basename="direct-message")

urlpatterns = [
    path(
        route="",
        view=include(router.urls),
    ),
]
