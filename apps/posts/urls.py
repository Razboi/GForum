from django.conf.urls import url
from .views import PostDetails


urlpatterns = [
    url(r'^(?P<forum>[\w-]+)/(?P<slug>[\w-]+)/$', PostDetails.as_view(), name="details"),
]