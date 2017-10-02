from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm

from .forms import UserLoginForm, UserRegisterForm, ProfileImageForm
from .models import UserProfile
from apps.posts.models import Post
from apps.comments.models import Comment
from apps.forum.views import ForumList

User = get_user_model()


class UpdateProfile(LoginRequiredMixin, View):
    template_name = "accounts/settings.html"

    def get(self, request, *args, **kwargs):
        password_update = PasswordChangeForm(user=request.user)
        image_update = ProfileImageForm
        context = {
            "password_form": password_update,
            "image_form": image_update,
            "title": "Settings",
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        image_form = ProfileImageForm(request.POST, request.FILES)
        print(image_form)
        password_form = PasswordChangeForm(data=request.POST, user=request.user)
        if password_form.is_valid():
            password_form.save()
            return redirect("index")

        if image_form.is_valid():
            profile = UserProfile.objects.get(user=request.user)
            profile.image = image_form.cleaned_data["image"]
            profile.save()
            return redirect("index")

        context = {
            "password_form": PasswordChangeForm(user=request.user),
            "image_form": ProfileImageForm,
            "title": "Settings",
        }
        return render(request, self.template_name, context)


class UserProfileView(ListView):
    template_name = "accounts/user_profile.html"

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        username = self.kwargs.get("user")
        context["username"] = username
        user = User.objects.get(username=username)
        context["title"] = "Overview for " + str(username)
        posts = Post.objects.filter(author=user).order_by("-created")
        context["posts_list"] = posts
        comments = Comment.objects.filter(author=user).order_by("-created")
        context["comments_list"] = comments
        if user.userprofile.image:
            context["profile_picture"] = user.userprofile.image.url
        return context


def login_view(request):
    form = UserLoginForm(request.POST or None)
    context = {
        "form": form,
        "title": "Login"
    }
    template_name = "accounts/form.html"
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        next_url = request.GET.get("next")
        if next_url:
            return HttpResponseRedirect(next_url)
        else:
            return redirect("index")

    return render(request, template_name, context)

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        if new_user is not None:
            login(request, new_user)
            return redirect("index")

    template_name = "accounts/form.html"
    context = {
        "form": form,
        "title": "Sign Up"
    }
    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    return redirect("index")
