from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .forms import PostCreateForm
from apps.forum.models import Forum


class PostDetails(DetailView):

    def get_queryset(self, **kwargs):
        slug = self.kwargs.get("slug")
        return Post.objects.filter(slug__iexact=slug)

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetails, self).get_context_data(*args, **kwargs)
        slug = self.kwargs.get("slug")
        post = Post.objects.filter(slug__iexact=slug)
        print(post)
        forum = Forum.objects.get(post=post)
        print(forum)
        forum_slug = forum.slug
        print(forum_slug)
        context["slug"] = forum_slug
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    template_name = "posts/form.html"

    # used to add data before saving the object
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        return super(CreatePost, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CreatePost, self).get_context_data(*args, **kwargs)
        context["title"] = "New Post"
        return context


class UpdatePost(LoginRequiredMixin, UpdateView):
    form_class = PostCreateForm
    template_name = "posts/form.html"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(UpdatePost, self).get_context_data(*args, **kwargs)
        context["title"] = "Edit Post"
        return context
