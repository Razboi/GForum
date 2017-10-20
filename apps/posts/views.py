from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.contrib import messages

from .models import Post
from .forms import PostCreateForm
from apps.forum.models import Forum
from apps.comments.models import Comment
from apps.notifications.models import Notification

from apps.comments.forms import CommentCreateForm


# like/unlike posts
class Like(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        post_slug = kwargs.get("slug")
        post = Post.objects.get(slug=post_slug)
        score_list = post.score.all()  # get the likes list
        # if the user (liker) is not in the likes list add him
        if request.user not in score_list:
            post.score.add(self.request.user)
            notification_content = str(request.user.username) + " liked your post"
            notification = Notification(target=post.author, content=notification_content,
                                        post=post, author=request.user, is_comment=False)
            notification.save()
        # if he's already on the list delete him (unlike)
        else:
            post.score.remove(self.request.user)
            notification = Notification.objects.filter(target=post.author, post=post, author=request.user)
            if notification:
                notification.delete()

        return redirect(post.get_absolute_url())


# search posts
class PostSearch(ListView):
    # get the posts which names contains the searched keyword
    def get_queryset(self, **kwargs):
        search = self.request.GET.get("q")
        results = Post.objects.filter(name__icontains=search).order_by("-created")
        return results

    def get_context_data(self, *args, **kwargs):
        context = super(PostSearch, self).get_context_data(*args, **kwargs)
        context["title"] = "Search Results"
        context["search"] = True
        return context


# post details
class PostDetails(DetailView):

    def get_queryset(self, **kwargs):
        slug = self.kwargs.get("slug")
        # when a user clicks on a post this will add 1 to the post views count
        post = Post.objects.filter(slug__iexact=slug).update(post_views=F("post_views")+1)
        # return the post
        return Post.objects.filter(slug__iexact=slug)

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetails, self).get_context_data(*args, **kwargs)
        slug = self.kwargs.get("slug")
        post = Post.objects.get(slug__iexact=slug)

        forum = Forum.objects.get(post=post)
        forum_slug = forum.slug
        context["slug"] = forum_slug
        context["title"] = post.name
        context["icon"] = forum.icon.url
        context["back_to_forum"] = forum.get_absolute_url
        comments = Comment.objects.filter(post=post)  # gets all the comments of the post
        context["comment_list"] = comments  # adds to the context all the comments
        context["form"] = CommentCreateForm
        storage = messages.get_messages(self.request)  # allows django messages to be displayed on this page
        context["messages"] = storage  # adds the messages to be displayed
        return context


# new post
class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    template_name = "snippets/form.html"

    # used to add data before saving the object
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        slug = self.kwargs.get("slug")
        forum = Forum.objects.get(slug=slug)
        instance.forum = forum
        return super(CreatePost, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CreatePost, self).get_context_data(*args, **kwargs)
        context["title"] = "New Post"
        slug = self.kwargs.get("slug")
        forum = Forum.objects.get(slug=slug)
        context["icon"] = forum.icon.url
        context["back_to_forum"] = forum.get_absolute_url
        return context


# update a post
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


# delete a post
class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "snippets/delete_confirmation.html"

    def get_queryset(self):
        # makes sure that only the author gets to delete the post
        return Post.objects.filter(author=self.request.user)

    # after deleting the post gets the post's forum and redirects to its url
    def get_success_url(self):
        slug = self.kwargs.get("slug")
        post = Post.objects.get(slug=slug)
        forum = post.forum
        return forum.get_absolute_url()
