from django.conf.urls import url
from .views import CreateComment


urlpatterns = [
    url(r'^create/$', CreateComment.as_view(), name="create"),

]
