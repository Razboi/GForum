from django.shortcuts import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .models import PrivateMessage
from .forms import PMCreateForm, PMReplyForm

User = get_user_model()


class PMList(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return PrivateMessage.objects.filter(contact=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(PMList, self).get_context_data(*args, **kwargs)
        context["title"] = "Inbox"
        context["form"] = PMReplyForm
        return context


class SentList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return PrivateMessage.objects.filter(author=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(SentList, self).get_context_data(*args, **kwargs)
        context["title"] = "Sent Messages"
        context["sent"] = True
        return context


class CreatePM(LoginRequiredMixin, CreateView):
    form_class = PMCreateForm
    template_name = "snippets/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        contact_username = form.cleaned_data.get("contact_username")
        instance.contact = User.objects.get(username__iexact=contact_username)
        return super(CreatePM, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CreatePM, self).get_context_data(*args, **kwargs)
        context["title"] = "New Message"
        return context


class ProfilePM(LoginRequiredMixin, CreateView):
    form_class = PMReplyForm
    template_name = "snippets/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        contact_username = self.kwargs.get("contact")
        instance.contact = User.objects.get(username__iexact=contact_username)
        return super(ProfilePM, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfilePM, self).get_context_data(**kwargs)
        context["title"] = "New message to " + self.kwargs.get("contact")
        return context


class DeletePM(LoginRequiredMixin, DeleteView):
    model = PrivateMessage
    template_name = "snippets/delete_confirmation.html"

    def get_queryset(self):
        return PrivateMessage.objects.filter(contact=self.request.user)

    def get_success_url(self):
        return reverse("messages:inbox")


class ReplyPM(LoginRequiredMixin, CreateView):
    form_class = PMReplyForm
    template_name = "snippets/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        contact_username = self.kwargs.get("contact")
        instance.contact = User.objects.get(username__iexact=contact_username)
        instance.is_reply = True
        parent_pk = self.kwargs.get("pk")
        parent = PrivateMessage.objects.get(pk=parent_pk)
        if parent.is_reply:
            parent = parent.parent
        instance.parent = parent
        return super(ReplyPM, self).form_valid(form)
