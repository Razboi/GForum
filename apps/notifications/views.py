from django.shortcuts import redirect, reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification


'''when te user clicks on a notification this view deactivates the notification and then 
redirects the user to the object that triggered the notification '''


class NotificationView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        notification_pk = self.kwargs.get("pk")
        notification = Notification.objects.get(pk=notification_pk)  # get the notification
        notification.active = False  # set it to false
        notification.save()
        # if the notification is a comment redirect to the comment anchor on the post
        if notification.is_comment:
            forum = notification.comment.post.forum.slug
            post = notification.comment.post.slug
            # gets the post url and adds the comment anchor
            return redirect(reverse("post:details", kwargs={"forum": forum, "slug": post})
                            + "#" + str(notification.comment.identifier))
        # if its a post redirect to the post
        else:
            return redirect(notification.post.get_absolute_url())

