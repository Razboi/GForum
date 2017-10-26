from django.db import models
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.db.models.signals import post_save

from tinymce.models import HTMLField

from apps.posts.models import Post

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    author = models.ForeignKey(User)
    content = HTMLField()
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # only will have a parent if its a reply
    parent = models.ForeignKey("self", null=True, blank=True, related_name="replies")
    is_reply = models.BooleanField(default=False)
    identifier = models.IntegerField(null=True, blank=True)
    score = models.ManyToManyField(User, related_name="comment_score")  # likes list

    # this will redirect the user to the post in which they commented (created a comment)
    def get_absolute_url(self):
        slug = self.post.slug
        return reverse("post:details", kwargs={"slug": slug})

    def __str__(self):
        basic_description = str(self.author) + " | " + str(self.post.name)
        return basic_description


# create a notification when a comment is created
def create_notification(sender, **kwargs):
    if kwargs["created"]:
        comment = kwargs["instance"]
        # reply notification
        if comment.is_reply:
            notification_content = str(comment.author.username) + " replied to your comment"
            notification = comment.notification_comment.create(
                target=comment.parent.author, content=notification_content, comment=comment, author=comment.author,
                is_like=False
            )
        # comment notification to post author
        else:
            if comment.post.author != comment.author:
                notification_content = str(comment.author.username) + " commented your post"
                notification = comment.notification_comment.create(
                    target=comment.post.author, content=notification_content, comment=comment, author=comment.author,
                    is_like=False
                )


post_save.connect(create_notification, sender=Comment)
