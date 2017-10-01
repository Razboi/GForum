from django.conf.urls import url
from .views import login_view, logout_view, register_view, UserProfileView, UpdateProfile


urlpatterns = [
    url(r'^login/$', login_view, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^register/$', register_view, name="register"),
    url(r'^profile/(?P<user>[\w-]+)/$', UserProfileView.as_view(), name="profile"),
    url(r'^profile/settings/(?P<user>[\w-]+)/$', UpdateProfile.as_view(), name="settings"),
]
