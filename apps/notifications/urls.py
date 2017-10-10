from django.conf.urls import url
from .views import NotificationView


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', NotificationView.as_view(), name="details"),
]
