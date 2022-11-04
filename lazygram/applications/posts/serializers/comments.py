""" Comments serializer. """

# Django
from lazygram.applications.users.serializers import ProfileSerializer
from .__modules__ import *

# Local models.
from ..models import Comments


class CommentsSerializer(serializers.ModelSerializer):
    """Comment serializer."""

    commented_by = ProfileSerializer(read_only=True)
    likes = serializers.IntegerField(min_value=0, required=False)

    class Meta:
        """Serializer meta class."""

        model = Comments
        fields = "__all__"
