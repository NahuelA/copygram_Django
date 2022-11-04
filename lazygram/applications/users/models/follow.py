""" Follow model. """

# Django
from django.db import models
from lazygram.applications.users.models import Profile


class FollowersModel(models.Model):
    """Followers model.
    Followers from any profile.
    """

    profile = models.ForeignKey(
        verbose_name="Profile", to=Profile, on_delete=models.CASCADE
    )

    followers_length = models.PositiveIntegerField(default=0)
    followers = models.ManyToManyField(
        verbose_name="Followers", to=Profile, related_name="followers"
    )

    class Meta:
        """Meta options from followers model."""

        verbose_name = "Followers"


class FollowingModel(models.Model):
    """Followings model.
    Followings from any profile.
    """

    profile = models.ForeignKey(
        verbose_name="Profile", to=Profile, on_delete=models.CASCADE
    )

    following_length = models.PositiveIntegerField(default=0)
    following = models.ManyToManyField(
        verbose_name="Following",
        to=Profile,
        related_name="Following",
    )

    class Meta:
        """Meta options from following model."""

        verbose_name = "Following"
