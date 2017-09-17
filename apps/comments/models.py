from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from apps.posts.models import Post

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # this will redirect the user to the post in which they commented (created a comment)
    def get_absolute_url(self):
        slug = self.post.slug
        forum = self.post.forum
        return reverse("post:details", kwargs={"slug": slug, "forum": forum})

    def __str__(self):
        basic_description = str(self.author) + " | " + str(self.post.name)
        return basic_description
