from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostDetails(DetailView):

    def get_queryset(self, **kwargs):
        slug = self.kwargs.get("slug")
        return Post.objects.filter(slug__iexact=slug)
