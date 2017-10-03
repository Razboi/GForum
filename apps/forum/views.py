from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from operator import attrgetter

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
        context["title"] = "Forums"
        most_liked = Post.objects.annotate(num_likes=Count("score")).order_by("-num_likes")[:7]
        context["top_posts"] = most_liked
        new_posts = Post.objects.order_by("-created")[:8]
        context["new_posts"] = new_posts
        context["icon"] = None
        return context


class ForumDetails(ListView):

    # Creates the main queryset
    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        filter_key = self.kwargs.get("filter")
        if filter_key == "top":
            posts = Post.objects.filter(forum__slug__iexact=slug)
            most_liked = posts.annotate(num_likes=Count("score")).order_by("-num_likes")
            return most_liked
        return Post.objects.filter(forum__slug__iexact=slug).order_by("-created")

    # Adds context arguments to the queryset
    def get_context_data(self, *args, **kwargs):
        context = super(ForumDetails, self).get_context_data(*args, **kwargs)
        slug = self.kwargs.get("slug")
        forum = Forum.objects.get(slug__iexact=slug)  # get the forum with the slug that we are using
        context["title"] = forum.name  # get the current forum name to use it as title
        context["icon"] = forum.icon.url
        context["slug"] = self.kwargs.get("slug")

        post = Post.objects.filter(forum__slug__iexact=slug)
        post_comments = Comment.objects.filter(post=post)
        context["comment_list"] = post_comments
        return context
