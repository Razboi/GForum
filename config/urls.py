"""GForum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from apps.forum.views import ForumList

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', ForumList.as_view(), name="index"),
    url(r'^forum/', include("apps.forum.urls", namespace="forum")),
    url(r'^post/', include("apps.posts.urls", namespace="post")),
    url(r'^comment/', include("apps.comments.urls", namespace="comment")),
    url(r'^accounts/', include("apps.accounts.urls", namespace="accounts")),
    url(r'^messages/', include("apps.private_messages.urls", namespace="messages")),
    url(r'^reports/', include("apps.reports.urls", namespace="reports")),
    url(r'^tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
