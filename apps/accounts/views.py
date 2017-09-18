from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.urlresolvers import reverse

from .forms import UserLoginForm, UserRegisterForm


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
