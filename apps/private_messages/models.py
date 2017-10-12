from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL


class PrivateMessage(models.Model):
    author = models.ForeignKey(User, related_name="sender")
    contact = models.ForeignKey(User, related_name="receiver")
    subject = models.CharField(max_length=120)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="replies")
    is_reply = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        basic_description = str(self.author) + " to " + str(self.contact) + " | " + str(self.subject)
        return basic_description

    def get_absolute_url(self):
        return reverse("messages:sent")
