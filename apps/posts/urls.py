from django.conf.urls import url
from .views import PostDetails, CreatePost


urlpatterns = [
    url(r'^(?P<forum>[\w-]+)/(?P<slug>[\w-]+)/$', PostDetails.as_view(), name="details"),
    url(r'^create/$', CreatePost.as_view(), name="create"),
]