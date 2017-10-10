from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification


class NotificationView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        notification_pk = self.kwargs.get("pk")
        notification = Notification.objects.get(pk=notification_pk)
        notification.active = False
        notification.save()
        if notification.is_comment:
            forum= notification.comment.post.forum.slug
            post = notification.comment.post.slug
            return redirect(reverse("post:details", kwargs={"forum": forum, "slug": post})
                     + "#" + str(notification.comment.identifier))
        else:
            return redirect(notification.post.get_absolute_url())

