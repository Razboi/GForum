from django.shortcuts import reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .models import PostReport, CommentReport
from apps.posts.models import Post
from apps.comments.models import Comment


User = get_user_model()


class CreatePostReport(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        post_pk = self.kwargs.get("pk")
        post = Post.objects.get(pk=post_pk)
        post_author = post.author.username
        post_content = post.content
        PostReport(author=post_author, post=post, content=post_content).save()
        return redirect(post.get_absolute_url())


class CreateCommentReport(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        comment_pk = self.kwargs.get("pk")
        comment = Comment.objects.get(pk=comment_pk)
        comment_author = comment.author.username
        comment_content = comment.content
        CommentReport(author=comment_author, comment=comment, content=comment_content).save()
        return redirect(comment.get_absolute_url())
