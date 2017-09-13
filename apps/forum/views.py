from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Forum, Post


class ForumList(ListView):

    def get_queryset(self, **kwargs):
        return Forum.objects.all()


class ForumDetails(ListView):

    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        return Post.objects.filter(forum__slug__iexact=slug)
