from django.db import models
from django.conf import settings

from apps.posts.models import Post

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

