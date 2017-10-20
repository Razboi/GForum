from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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


# View used to update the user profile (password and image)
class UpdateProfile(LoginRequiredMixin, View):
    template_name = "accounts/settings.html"

    # passes the password/image forms and the title to settings.html
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
        # get the forms with the data
        image_form = ProfileImageForm(request.POST, request.FILES)
        password_form = PasswordChangeForm(data=request.POST, user=request.user)
        # if the password form is valid save it
        if password_form.is_valid():
            password_form.save()
            return redirect("index")

        # if the image form is valid set the profile image to the submitted image and save it
        if image_form.is_valid():
            profile = UserProfile.objects.get(user=request.user)
            profile.image = image_form.cleaned_data["image"]
            profile.save()
            return redirect("index")

        # if the form is not valid return it again
        context = {
            "password_form": PasswordChangeForm(user=request.user),
            "image_form": ProfileImageForm,
            "title": "Settings",
        }
        return render(request, self.template_name, context)


# view to display the user profile page
class UserProfileView(ListView):
    template_name = "accounts/user_profile.html"

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)

        # add the username to context and get the user object
        username = self.kwargs.get("user")
        context["username"] = username
        user = User.objects.get(username=username)
        # set the title
        context["title"] = "Overview for " + str(username)
        # filter all the posts where the author is the user and order them by newest
        posts = Post.objects.filter(author=user).order_by("-created")
        context["posts_list"] = posts
        # filter all the comments where the author is the user and order them by newest
        comments = Comment.objects.filter(author=user).order_by("-created")
        context["comments_list"] = comments
        # if the user has a profile image pass it, else the default image will be set on the template
        if user.userprofile.image:
            context["profile_picture"] = user.userprofile.image.url
        return context


# function to login users
def login_view(request):
    # GET part
    form = UserLoginForm(request.POST or None)  # get the form with the data (if posted) or empty (if get)
    is_login = True  # when its true the template will be styled for the login, else for the registration
    context = {
        "form": form,
        "title": "Login",
        "login": is_login,
    }
    template_name = "accounts/form.html"

    # POST part
    # if the form is valid the user will be authenticated and logged
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

    # if its a get request or the posted form is not valid render the form
    return render(request, template_name, context)


# function used to register users
def register_view(request):
    form = UserRegisterForm(request.POST or None)
    # if the form is valid set the user object and save it
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.is_active = False
        user.email = form.cleaned_data.get("email")
        user.save()

        current_site = get_current_site(request)
        # get the template + data and create the email message
        message = render_to_string("accounts/acc_activate_email.html", {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),

        })
        # set the email subject
        mail_subject = "Active your GForum account."
        # set the email address
        to_email = form.cleaned_data.get("email")
        # get the message, subject and address and send the email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        messages.info(request, "A confirmation email has been sent to your email address.")
        return redirect("index")

    template_name = "accounts/form.html"
    context = {
        "form": form,
        "title": "Sign Up"
    }

    # if its a get request or the posted form is not valid render the form
    return render(request, template_name, context)


# logout function
def logout_view(request):
    logout(request)
    return redirect("index")


# function to activate the user account
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  # get the uid from the activation token
        user = User.objects.get(pk=uid)  # get the user with the uid
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # if the link is valid activate the account and login the user, else return an error message
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        messages.success(request, "Your account has been activated! Now you can login and enjoy GForum.")
        return redirect("index")
    else:
        messages.error(request,
                       """The activation link was invalid, possibly because it has already been used.
                        Please contact us.""")
        return redirect("index")
