from django.conf.urls import url
from .views import CreateComment


urlpatterns = [
    url(r'^create/(?P<slug>[\w-]+)/$', CreateComment.as_view(), name="create"),

]
