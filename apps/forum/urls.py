from django.conf.urls import url
from .views import ForumDetails


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', ForumDetails.as_view(), name="details"),
    url(r'^(?P<slug>[\w-]+)/(?P<filter>[\w-]+)/$', ForumDetails.as_view(), name="filter"),
]
