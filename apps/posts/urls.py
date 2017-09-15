from django.conf.urls import url
from .views import PostDetails, CreatePost,UpdatePost


urlpatterns = [
    url(r'^update/(?P<slug>[\w-]+)/$', UpdatePost.as_view(), name="update"),
    url(r'^(?P<forum>[\w-]+)/(?P<slug>[\w-]+)/$', PostDetails.as_view(), name="details"),
    url(r'^create/$', CreatePost.as_view(), name="create"),

]