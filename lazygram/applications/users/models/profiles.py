""" Profile model. """

# Django
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_picture_<username>/<filename>
    return "profile_picture_{0}/{1}".format(instance.user.username, filename)


class ProfileManager(models.Manager):
    """Profile object model manager."""

    def get_by_natural_key(self, by_username):
        return self.get(username=by_username)


class Profile(models.Model):
    """Profile model.
    Add more information to sign in.
    """

    user = models.OneToOneField(
        to=User,
        verbose_name="Username",
        on_delete=models.CASCADE,
        limit_choices_to={"is_active": True},
    )

    biography = models.CharField(
        max_length=350,
        default="",
        blank=True,
        editable=True,
    )

    manager_object = ProfileManager()

    picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    date_of_birth = models.DateTimeField(
        blank=True,
        null=True,
    )

    website = models.URLField(max_length=200, default="", blank=True)

    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )

    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True
    )

    posts_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return user in admin site."""
        return "%s" % (self.user)

    def user__username(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

    def natural_key(self):
        """Natural key to serialization."""
        return self.user.username

    class Meta:
        """Meta class from profile model."""

        verbose_name_plural = "Profiles"
