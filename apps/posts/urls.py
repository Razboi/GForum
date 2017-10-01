from django.conf.urls import url
from .views import PostDetails, CreatePost, UpdatePost, DeletePost, PostSearch, Like


urlpatterns = [
    url(r'^update/(?P<slug>[\w-]+)/$', UpdatePost.as_view(), name="update"),
    url(r'^create/(?P<slug>[\w-]+)/$', CreatePost.as_view(), name="create"),
    url(r'^delete/(?P<slug>[\w-]+)/$', DeletePost.as_view(), name="delete"),
    url(r'^search/$', PostSearch.as_view(), name="search"),
    url(r'^like/(?P<slug>[\w-]+)/$', Like.as_view(), name="like"),

    # to avoid mismatches this url should be always the last one
    url(r'^(?P<forum>[\w-]+)/(?P<slug>[\w-]+)/$', PostDetails.as_view(), name="details"),
]
