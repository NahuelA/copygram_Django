""" Direct messages views. """

# Rest-framework
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Models
from lazygram.applications.dm.models import Dm
from lazygram.applications.users.models import Profile

# Serializers
from lazygram.applications.dm.serializers import DmSerializer


class DmView(ModelViewSet):
    """Direct message view.
    Send and receive messages.
    """

    queryset = Dm.objects.all()
    serializer_class = DmSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        profile_from = self.request.auth
        to = ""

        # Get profile, if not found. Return error.
        try:
            to = Profile.manager_object.filter(
                user__username=self.request.data.get("to")
            ).first()
        except Profile.DoesNotExist:
            return Response("Profile does not exist.", status=status.HTTP_404_NOT_FOUND)
        serializer.save(profile_from=profile_from, to_profile=to)

    def list(self, request, *args, **kwargs):

        # Get profile, if not found. Return error.
        to = ""
        try:
            to = Profile.manager_object.filter(
                user__username=self.request.GET.get("to")
            ).first()
        except Profile.DoesNotExist:
            return Response("Profile does not exist.", status=status.HTTP_404_NOT_FOUND)

        queryset = self.filter_queryset(
            self.queryset.filter(profile_from=request.auth, to_profile=to)
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
