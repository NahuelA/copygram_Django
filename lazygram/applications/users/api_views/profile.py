""" Profile view from users app. """

# Django
from .__modules__ import *
from django.shortcuts import get_object_or_404
from lazygram.applications.users.models import Profile
from django.core.cache import cache
from rest_framework.generics import ListAPIView

# Rest-framework
from lazygram.applications.users.serializers import ProfileSerializer


class ProfileView(ModelViewSet):
    """Profile view."""

    model = Profile
    queryset = Profile.manager_object.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "put", "patch", "delete", "head", "options", "trace"]
    lookup_field = "user__username"
    update_status = status.HTTP_201_CREATED

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        """List all posts the user follows."""

        if cache.get("profiles") == None:
            queryset = self.filter_queryset(self.get_queryset())
            cache.set(key="profiles", value=queryset, timeout=86400)

        # Paginate
        page = self.paginate_queryset(cache.get("profiles"))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(cache.get("profiles"), many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update profile from user

        Some fields is updates automatically:
            - date_joined
            - last_login
            - modified
        """
        instance = self.get_object()
        partial = kwargs.pop("partial", False)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        self.update_status = status.HTTP_201_CREATED

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=self.update_status)


class ProfilesSearchView(ListAPIView):
    """Search profiles."""

    model = Profile
    queryset = Profile.manager_object.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    update_status = status.HTTP_200_OK

    def list(self, request, *args, **kwargs):

        if kwargs.get("search_profiles") != None:
            queryset = self.filter_queryset(
                self.queryset.filter(
                    user__username__istartswith=kwargs.get("search_profiles")
                )
            )

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=self.update_status)
        else:
            if cache.get("recent") is not None:  # Get visited profiles
                return Response(cache.get("recent"), status=self.update_status)
            return Response("Does not results.", status=self.update_status)
