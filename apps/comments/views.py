from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CommentCreateForm
from apps.posts.models import Post


class CreateComment(CreateView):
    form_class = CommentCreateForm
    template_name = "snippets/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        slug = self.kwargs.get("slug")
        instance.post = Post.objects.get(slug=slug)
        return super(CreateComment, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CreateComment, self).get_context_data(*args, **kwargs)
        context["title"] = "New Comment"
        return context
