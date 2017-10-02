from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to="profile/", blank=True, null=True)

    def __str__(self):
        return self.user.username

    def create_profile(sender, **kwargs):
        if kwargs["created"]:
            user_profile = UserProfile.objects.create(user=kwargs["instance"])

    post_save.connect(create_profile, sender=User)
