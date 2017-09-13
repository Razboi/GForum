from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse

from .utils import unique_slug_generator


class Forum(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    # sends the object slug to the details url
    def get_absolute_url(self):
        return reverse("forum:details", kwargs={"slug": self.slug})


# if the object doesn't have a slug it uses the unique_slug_generator to create one before saving the object
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_receiver, sender=Forum)
