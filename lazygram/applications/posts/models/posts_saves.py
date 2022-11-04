""" Post saves model. """

# Django
from django.db import models

# Local
from lazygram.applications.posts.models import Posts
from lazygram.applications.users.models import Profile


class PostSaves(models.Model):
    """Post saves model.
    Save posts to be archived to you.
    """

    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.DO_NOTHING,
        verbose_name="Profile ID",
        related_name="profile_id",
        null=True,
    )

    saved_post = models.ManyToManyField(
        to=Posts,
        verbose_name="Saved post",
        related_name="saved_posts",
    )

    def __str__(self):
        """Return the id of the post in string format."""
        return self.post

    # Validations
    def validate_post_exist(self, postid):
        """If post exist, return true, else false"""
        return Posts.objects.filter(id=postid).exists()
