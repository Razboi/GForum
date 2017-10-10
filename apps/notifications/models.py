from django.db import models
from django.conf import settings
from apps.comments.models import Comment
from apps.posts.models import Post

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    target = models.ForeignKey(User, related_name="user_notifications")
    content = models.CharField(max_length=200)
    creation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    comment = models.ForeignKey(Comment, null=True, related_name="notification_comment")
    is_comment = models.BooleanField(default=True)
    is_like = models.BooleanField(default=True)
    post = models.ForeignKey(Post, null=True, blank=True)
    author = models.ForeignKey(User, related_name="notification_author", null=True)

    class Meta:
        ordering = ["-creation"]

    def __str__(self):
        return str(self.target) + " | " + str(self.content)
