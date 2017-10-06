from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    target = models.ForeignKey(User, related_name="user_notifications")
    content = models.CharField(max_length=200)
    creation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.target) + " | " + str(self.content)
