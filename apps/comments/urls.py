from django.conf.urls import url
from .views import CreateComment, UpdateComment, DeleteComment


urlpatterns = [
    url(r'^create/(?P<slug>[\w-]+)/$', CreateComment.as_view(), name="create"),
    url(r'^update/(?P<pk>\d+)/$', UpdateComment.as_view(), name="update"),
    url(r'^delete/(?P<pk>\d+)/$', DeleteComment.as_view(), name="delete"),

]
