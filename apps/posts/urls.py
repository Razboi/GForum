from django.conf.urls import url
from .views import PostDetails, CreatePost, UpdatePost, DeletePost


urlpatterns = [
    url(r'^update/(?P<slug>[\w-]+)/$', UpdatePost.as_view(), name="update"),
    url(r'^create/$', CreatePost.as_view(), name="create"),
    url(r'^delete/(?P<slug>[\w-]+)/$', DeletePost.as_view(), name="delete"),

    # to avoid mismatches this url should be always the last one
    url(r'^(?P<forum>[\w-]+)/(?P<slug>[\w-]+)/$', PostDetails.as_view(), name="details"),
]