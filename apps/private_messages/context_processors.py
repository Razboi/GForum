from .models import PrivateMessage


def active_messages_processor(request):
    if request.user.is_authenticated():
        active_messages = PrivateMessage.objects.filter(active=True, contact=request.user)
        return {"active_messages": active_messages}
    return {"active_messages": None}
