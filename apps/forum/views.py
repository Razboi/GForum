from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Forum
from apps.posts.models import Post
from apps.comments.models import Comment


class ForumList(ListView):

    def get_queryset(self, **kwargs):
        return Forum.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ForumList, self).get_context_data(**kwargs)
        context["general_forums"] = Forum.objects.filter(category="General")
        context["programming_forums"] = Forum.objects.filter(category="Programming")
        context["title"] = "Forums index"
        return context


class ForumDetails(ListView):

    # Creates the main queryset
    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        return Post.objects.filter(forum__slug__iexact=slug)

    # Adds context arguments to the queryset
    def get_context_data(self, *args, **kwargs):
        context = super(ForumDetails, self).get_context_data(*args, **kwargs)
        slug = self.kwargs.get("slug")
        forum = Forum.objects.get(slug__iexact=slug)  # get the forum with the slug that we are using
        context["title"] = forum.name  # get the current forum name to use it as title

        post = Post.objects.filter(forum__slug__iexact=slug)
        post_comments = Comment.objects.filter(post=post)
        context["comment_list"] = post_comments
        return context
