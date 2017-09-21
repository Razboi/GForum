from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import CommentCreateForm
from apps.posts.models import Post
from .models import Comment


class CreateReply(LoginRequiredMixin, CreateView):
    form_class = CommentCreateForm
    template_name = "snippets/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        slug = self.kwargs.get("slug")
        instance.post = Post.objects.get(slug=slug)
        instance.is_reply = True
        parent = self.kwargs.get("pk")
        instance.parent = Comment.objects.get(pk=parent)
        return super(CreateReply, self).form_valid(form)



class CreateComment(LoginRequiredMixin, CreateView):
    form_class = CommentCreateForm
    template_name = "snippets/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        slug = self.kwargs.get("slug")
        instance.post = Post.objects.get(slug=slug)
        return super(CreateComment, self).form_valid(form)


class UpdateComment(LoginRequiredMixin, UpdateView):
    form_class = CommentCreateForm
    template_name = "snippets/form.html"

    def get_queryset(self):
        # makes sure that only the author gets to update the post
        return Comment.objects.filter(author=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateComment, self).get_context_data(*args, **kwargs)
        context["title"] = "Edit Comment"
        return context


class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "snippets/delete_confirmation.html"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        comment = Comment.objects.get(pk=pk)
        return comment.get_absolute_url()
