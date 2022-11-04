""" Comments model. """

# Django
from email.policy import default
from django.db import models

# Local
from lazygram.applications.users.models import Profile
from lazygram.applications.posts.models import Posts


class Comments(models.Model):
    """Comments model.
    Comments of the users comment a posts.
    """

    post = models.ForeignKey(
        to=Posts,
        verbose_name="Post",
        on_delete=models.DO_NOTHING,
        related_name="post",
        null=True,
    )

    commented_by = models.ForeignKey(
        to=Profile,
        on_delete=models.DO_NOTHING,
        verbose_name="Commented by",
        null=True,
    )

    comment = models.CharField(
        verbose_name="Comment",
        max_length=255,
        default="",
    )

    likes = models.PositiveIntegerField(
        verbose_name="Likes of comments", default=0, blank=True
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        null=True,
    )

    last_modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    def __str__(self):
        """Return the id of the post that is commented on in string format."""
        return self.post

    class Meta:
        """Meta options from comments model."""

        verbose_name_plural = "Comments"


class ReplyComments(models.Model):
    """Comments replies."""

    commentid = models.ForeignKey(to=Comments, on_delete=models.DO_NOTHING)

    replied_by = models.ManyToManyField(
        to=Profile,
        verbose_name="Replied by",
    )

    reply = models.CharField(
        verbose_name="Comment replies",
        max_length=255,
        default="",
        blank=True,
    )

    like_reply = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        """Return the id of the post that is commented on in string format."""
        return self.commentid

    class Meta:
        """Meta options from comments model."""

        verbose_name_plural = "Replies"
