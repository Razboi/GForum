from django.conf.urls import url
from .views import CreatePostReport, CreateCommentReport

urlpatterns = [
    url(r'^post/(?P<pk>\d+)/$', CreatePostReport.as_view(), name="post"),
    url(r'^comment/(?P<pk>\d+)/$', CreateCommentReport.as_view(), name="comment"),

]
