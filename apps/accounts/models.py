from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to="profile/", blank=True)

    def __str__(self):
        return self.user.username
