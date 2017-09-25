from django.conf.urls import url
from .views import PMList, CreatePM, SentList, ReplyPM

urlpatterns = [
    url(r'^inbox/$', PMList.as_view(), name="inbox"),
    url(r'^sent/$', SentList.as_view(), name="sent"),
    url(r'^create/$', CreatePM.as_view(), name="create"),
    url(r'^reply/(?P<contact>[\w-]+)/(?P<pk>\d+)/$', ReplyPM.as_view(), name="reply"),
]
