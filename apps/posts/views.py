from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from .forms import PostCreateForm


class PostDetails(DetailView):

    def get_queryset(self, **kwargs):
        slug = self.kwargs.get("slug")
        return Post.objects.filter(slug__iexact=slug)


class CreatePost(CreateView):
    form_class = PostCreateForm
    template_name = "posts/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        return super(CreatePost, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CreatePost, self).get_context_data(*args, **kwargs)
        context["title"] = "New Post"
        return context
