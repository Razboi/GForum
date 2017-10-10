from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from apps.posts.models import Post

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="replies")
    is_reply = models.BooleanField(default=False)
    identifier = models.IntegerField(null=True, blank=True)
    score = models.ManyToManyField(User, related_name="comment_score")

    # this will redirect the user to the post in which they commented (created a comment)
    def get_absolute_url(self):
        slug = self.post.slug
        forum = self.post.forum
        return reverse("post:details", kwargs={"slug": slug, "forum": forum})

    def __str__(self):
        basic_description = str(self.author) + " | " + str(self.post.name)
        return basic_description


def create_notification(sender, **kwargs):
    if kwargs["created"]:
        comment = kwargs["instance"]
        if comment.is_reply:
            notification_content = str(comment.author.username) + " replied to your comment"
            notification = comment.notification_comment.create(
                target=comment.parent.author, content=notification_content, comment=comment, author=comment.author,
                is_like=False
            )
        else:
            notification_content = str(comment.author.username) + " commented your post"
            notification = comment.notification_comment.create(
                target=comment.post.author, content=notification_content, comment=comment, author=comment.author,
                is_like=False
            )


post_save.connect(create_notification, sender=Comment)

