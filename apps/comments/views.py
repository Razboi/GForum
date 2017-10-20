from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import CommentCreateForm
from apps.posts.models import Post
from apps.notifications.models import Notification
from .models import Comment


# view to like/unlike a comment
class Like(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        comment_pk = kwargs.get("pk")
        comment = Comment.objects.get(pk=comment_pk)
        score_list = comment.score.all()
        # if the like author is not in the likes list add him and create a notification to the comment author
        if request.user not in score_list:
            comment.score.add(self.request.user)
            notification_content = str(request.user.username) + " liked your comment"
            notification = Notification(target=comment.author, content=notification_content,
                                        comment=comment, author=request.user)
            notification.save()

        # else remove him from the list (unlike) and delete the notification
        else:
            comment.score.remove(self.request.user)
            notification = Notification.objects.filter(target=comment.author, comment=comment, author=request.user)
            if notification:
                notification.delete()

        return redirect(comment.get_absolute_url())


# create a reply for a comment
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

        messages.success(self.request, "Your reply has been created.")
        return super(CreateReply, self).form_valid(form)


# create a new comment
class CreateComment(LoginRequiredMixin, CreateView):
    form_class = CommentCreateForm
    template_name = "snippets/form.html"

    # if the form is valid set the object variables and save it
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        slug = self.kwargs.get("slug")
        instance.post = Post.objects.get(slug=slug)
        instance.identifier = len(Comment.objects.filter(post=instance.post)) +1

        messages.success(self.request, "Your comment has been created.")
        return super(CreateComment, self).form_valid(form)


# update a comment
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


# delete a comment
class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "snippets/delete_confirmation.html"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        comment = Comment.objects.get(pk=pk)
        return comment.get_absolute_url()
