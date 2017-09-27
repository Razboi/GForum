from django.conf.urls import url
from .views import CreateComment, UpdateComment, DeleteComment, CreateReply, Like


urlpatterns = [
    url(r'^create/(?P<slug>[\w-]+)/$', CreateComment.as_view(), name="create"),
    url(r'^update/(?P<pk>\d+)/$', UpdateComment.as_view(), name="update"),
    url(r'^delete/(?P<pk>\d+)/$', DeleteComment.as_view(), name="delete"),
    url(r'^reply/(?P<slug>[\w-]+)/(?P<pk>\d+)/$', CreateReply.as_view(), name="reply"),
    url(r'^like/(?P<pk>\d+)/$', Like.as_view(), name="like"),
]
