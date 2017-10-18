from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views.generic import ListView, View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages

from .forms import UserLoginForm, UserRegisterForm, ProfileImageForm
from .models import UserProfile
from apps.posts.models import Post
from apps.comments.models import Comment
from .tokens import account_activation_token

User = get_user_model()


class UpdateProfile(LoginRequiredMixin, View):
    template_name = "accounts/settings.html"

    def get(self, request, *args, **kwargs):
        password_update = PasswordChangeForm(user=request.user)
        image_update = ProfileImageForm
        context = {
            "password_form": password_update,
            "errors": password_update.errors,
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
    is_login = True
    context = {
        "form": form,
        "title": "Login",
        "login": is_login,
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
        user.is_active = False
        user.email = form.cleaned_data.get("email")
        user.save()
        current_site = get_current_site(request)
        message = render_to_string("accounts/acc_activate_email.html", {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),

        })
        mail_subject = "Active your GForum account."
        to_email = form.cleaned_data.get("email")
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        messages.info(request, "A confirmation email has been sent to your email address.")
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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        messages.success(request, "Your account has been activated! Now you can login and enjoy GForum.")
        return redirect("index")
    else:
        messages.error(request, "Activation link invalid, please contact us.")
        return redirect("index")
