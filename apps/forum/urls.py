from django.conf.urls import url
from .views import ForumDetails


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', ForumDetails.as_view(), name="details"),
]
