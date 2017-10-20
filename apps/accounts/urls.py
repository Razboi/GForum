from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .views import (login_view, logout_view, register_view, UserProfileView,
                    UpdateProfile, activate)


urlpatterns = [
    url(r'^login/$', login_view, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^register/$', register_view, name="register"),
    url(r'^profile/(?P<user>[\w-]+)/$', UserProfileView.as_view(), name="profile"),
    url(r'^profile/settings/(?P<user>[\w-]+)/$', UpdateProfile.as_view(), name="settings"),

    # password activate
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name="activate"),

    # password reset urls
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),

    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),

    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



]
