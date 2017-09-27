from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import CommentCreateForm
from apps.posts.models import Post
from .models import Comment


class Like(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        comment_pk = kwargs.get("pk")
        comment = Comment.objects.get(pk=comment_pk)
        score_list = comment.score.all()
        if request.user not in score_list:
            comment.score.add(self.request.user)
        else:
            comment.score.remove(self.request.user)

        return redirect(comment.get_absolute_url())


class CreateReply(LoginRequiredMixin, CreateView):
    form_class = CommentCreateForm
    template_name = "snippets/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        # set author
        instance.author = self.request.user
        # set parent post
        slug = self.kwargs.get("slug")
        instance.post = Post.objects.get(slug=slug)
        # set is_reply
        instance.is_reply = True
        # set parent
        parent_pk = self.kwargs.get("pk")
        instance.parent = Comment.objects.get(pk=parent_pk)
        # set identifier
        instance.identifier = len(Comment.objects.filter(post=instance.post)) +1
        return super(CreateReply, self).form_valid(form)



class CreateComment(LoginRequiredMixin, CreateView):
    form_class = CommentCreateForm
    template_name = "snippets/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        slug = self.kwargs.get("slug")
        instance.post = Post.objects.get(slug=slug)
        instance.identifier = len(Comment.objects.filter(post=instance.post)) +1
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
