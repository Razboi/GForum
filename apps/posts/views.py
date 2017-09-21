from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .forms import PostCreateForm
from apps.forum.models import Forum
from apps.comments.models import Comment

from apps.comments.forms import CommentCreateForm


class PostSearch(ListView):

    def get_queryset(self, **kwargs):
        search = self.request.GET.get("q")
        results = Post.objects.filter(name__icontains=search)
        return results

    def get_context_data(self, *args, **kwargs):
        context = super(PostSearch, self).get_context_data(*args, **kwargs)
        context["title"] = "Search Results"
        return context


class PostDetails(DetailView):

    def get_queryset(self, **kwargs):
        slug = self.kwargs.get("slug")
        return Post.objects.filter(slug__iexact=slug)

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetails, self).get_context_data(*args, **kwargs)
        slug = self.kwargs.get("slug")
        post = Post.objects.filter(slug__iexact=slug)

        forum = Forum.objects.get(post=post)
        forum_slug = forum.slug
        context["slug"] = forum_slug

        comments = Comment.objects.filter(post=post, is_reply=False)
        context["comment_list"] = comments

        context["form"] = CommentCreateForm
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    template_name = "snippets/form.html"

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
    template_name = "snippets/form.html"

    def get_queryset(self):
        # makes sure that only the author gets to update the post
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(UpdatePost, self).get_context_data(*args, **kwargs)
        context["title"] = "Edit Post"
        return context


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "snippets/delete_confirmation.html"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    # after deleting the post gets the post's forum and redirects to its url
    def get_success_url(self):
        slug = self.kwargs.get("slug")
        post = Post.objects.get(slug=slug)
        forum = post.forum
        return forum.get_absolute_url()
