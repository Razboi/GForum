from django.conf.urls import url
from .views import login_view, logout_view, register_view, UserProfile


urlpatterns = [
    url(r'^login/$', login_view, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^register/$', register_view, name="register"),
    url(r'^profile/(?P<user>[\w-]+)/$', UserProfile.as_view(), name="profile"),
]
