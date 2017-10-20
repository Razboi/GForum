from django.shortcuts import reverse
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import PrivateMessage
from .forms import PMCreateForm, PMReplyForm

User = get_user_model()


# returns all the received private messages for the user
class PMList(LoginRequiredMixin, ListView):

    def get_queryset(self):
        pms = PrivateMessage.objects.filter(contact=self.request.user)
        pms.update(active=False)
        return pms

    def get_context_data(self, *args, **kwargs):
        context = super(PMList, self).get_context_data(*args, **kwargs)
        context["title"] = "Inbox"
        context["form"] = PMReplyForm
        return context


# returns all the sent private messages for the user
class SentList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return PrivateMessage.objects.filter(author=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(SentList, self).get_context_data(*args, **kwargs)
        context["title"] = "Sent Messages"
        context["sent"] = True
        storage = messages.get_messages(self.request)  # gets all the django messages to be displayed
        context["messages"] = storage
        return context


# creates a new private message
class CreatePM(LoginRequiredMixin, CreateView):
    form_class = PMCreateForm
    template_name = "snippets/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        contact_username = form.cleaned_data.get("contact_username")
        instance.contact = User.objects.get(username__iexact=contact_username)
        messages.success(self.request, "Your message has been sent.")  # creates a django message
        return super(CreatePM, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CreatePM, self).get_context_data(*args, **kwargs)
        context["title"] = "New Message"
        return context


# creates a new private message for the owner of the profile
class ProfilePM(LoginRequiredMixin, CreateView):
    form_class = PMReplyForm
    template_name = "snippets/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        contact_username = self.kwargs.get("contact")
        instance.contact = User.objects.get(username__iexact=contact_username)
        messages.success(self.request, "Your message has been sent.")  # creates a django message
        return super(ProfilePM, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfilePM, self).get_context_data(**kwargs)
        context["title"] = "New message to " + self.kwargs.get("contact")
        return context


# delete a received private message
class DeletePM(LoginRequiredMixin, DeleteView):
    model = PrivateMessage
    template_name = "snippets/delete_confirmation.html"

    def get_queryset(self):
        return PrivateMessage.objects.filter(contact=self.request.user)

    def get_success_url(self):
        return reverse("messages:inbox")


# reply to a received message
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
        parent = PrivateMessage.objects.get(pk=parent_pk)  # gets the message to which we are responding
        # if the message is also a reply set the parent to the message parent (parent of the parent)
        # this will allow all the replies to have the same parent (the message that initiated the thread)
        if parent.is_reply:
            parent = parent.parent
        instance.parent = parent
        messages.success(self.request, "Your reply has been sent.")
        return super(ReplyPM, self).form_valid(form)
