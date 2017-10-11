from .models import Notification


def active_notifications_processor(request):
    if request.user.is_authenticated():
        active_notifications = Notification.objects.filter(active=True, target=request.user)
        return {"active_notifications": active_notifications}
    return {"active_notifications": None}
