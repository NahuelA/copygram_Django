""" Verify token. """

from rest_framework import serializers
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings


class TokenValidationSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                    # Active user
                    user = self.context.get("user")
                    user.is_active = True
                    user.save()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)
            data["user"] = str(self.context.get("user"))

        return data
