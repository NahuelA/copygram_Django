""" Direct messages serializer. """

# Rest framework serializers
from rest_framework import serializers

# Serializers
from lazygram.applications.users.serializers import ProfileSerializer

# Models
from lazygram.applications.dm.models import Dm


class DmSerializer(serializers.ModelSerializer):
    """Serializer from Direct messages model."""

    profile_from = ProfileSerializer(read_only=True)
    to = ProfileSerializer(read_only=True)
    message = serializers.CharField(max_length=500, min_length=1, allow_blank=False)
    file = serializers.FileField(max_length=500, allow_empty_file=False)

    class Meta:
        model = Dm
        fields = "__all__"
