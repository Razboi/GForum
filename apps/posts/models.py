from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.conf import settings

from tinymce.models import HTMLField

from apps.forum.models import Forum
from utils.unique_slug_generator import unique_slug_generator

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    name = models.TextField()
    content = HTMLField()
    author = models.ForeignKey(User)
    forum = models.ForeignKey(Forum)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True, max_length=170)
    score = models.ManyToManyField(User, related_name="post_score", blank=True)
    post_views = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("post:details", kwargs={"slug": self.slug})

    @property
    def title(self):
        return self.name


# when a post is created generates a new slug for that post
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Post)
