from django.conf.urls import url
from .views import PMList, CreatePM

urlpatterns = [
    url(r'^inbox/$', PMList.as_view(), name="inbox"),
    url(r'^create/$', CreatePM.as_view(), name="create"),
]
