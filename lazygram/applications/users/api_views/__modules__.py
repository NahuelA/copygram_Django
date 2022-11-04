""" Modules from users app. """

# Django
from django.contrib.auth import (
    authenticate,
    login,
)

# HttpResponse
from django.contrib.auth.models import User

# Rest-framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
