from django.db import models
from apps.posts.models import Post
from apps.comments.models import Comment


class PostReport(models.Model):
    author = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)
    content = models.TextField()

    def __str__(self):
        basic_description = str(self.author) + " | " + str(self.content)
        return basic_description


class CommentReport(models.Model):
    author = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment)
    content = models.TextField()

    def __str__(self):
        basic_description = str(self.author) + " | " + str(self.content)
        return basic_description
