""" Posts model. """
# Django imports
from django.db import models
from lazygram.applications.users.models import Profile

# Create your models here.


class Posts(models.Model):
    """Model Posts.
    Posts submit from all users.
    """

    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.DO_NOTHING,
        null=True,
    )

    picture = models.ImageField(
        upload_to="uploads/pictures_posted",
        null=True,
    )

    likes = models.PositiveIntegerField(
        verbose_name="Likes",
        default=0,
        null=True,
        blank=True,
    )

    profile_likedit = models.ManyToManyField(
        to=Profile,
        verbose_name="Liked it",
        related_name="liked_by",
        help_text="Profiles that liked it a post.",
        null=True,
        blank=True,
    )

    description = models.CharField(
        max_length=250,
        blank=True,
        default="",
        db_index=True,
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        auto_created=True,
        db_index=True,
    )

    last_modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        db_index=True,
    )

    def __str__(self):
        """Return profile and created date in string format."""
        return "%s" % (self.profile)

    class Meta:
        """Meta options from model Posts."""

        verbose_name_plural = "Posts"
