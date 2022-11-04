""" Direct messages model. """

from django.db import models
from lazygram.applications.users.models import Profile


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_<username>/<filename>
    return "dm_profile_{0}/{1}".format(instance.profile_from.user.username, filename)


class Dm(models.Model):
    """Model from direct messages."""

    profile_from = models.ForeignKey(
        verbose_name="Profile",
        to=Profile,
        related_name="profile_from",
        on_delete=models.DO_NOTHING,
    )

    to = models.ForeignKey(
        verbose_name="To profile",
        to=Profile,
        related_name="to",
        on_delete=models.DO_NOTHING,
    )

    message = models.TextField(
        verbose_name="Message",
        max_length=500,
    )

    file = models.FileField(
        verbose_name="Files",
        upload_to=user_directory_path,
        max_length=500,
        null=True,
        blank=True,
    )

    viewed = models.BooleanField(verbose_name="Viewed", default=False)

    created = models.DateTimeField(
        verbose_name="Created at", auto_now_add=True, null=True
    )

    def __str__(self):
        """Return string name."""
        return self.profile_from.user.username

    class Meta:
        """Meta options to Direct message model."""

        verbose_name_plural = "Direct messages"
