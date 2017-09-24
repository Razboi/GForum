from django.conf.urls import url
from .views import PMList

urlpatterns = [
    url(r'^inbox/$', PMList.as_view(), name="inbox"),
]
