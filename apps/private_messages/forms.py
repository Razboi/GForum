from django import forms
from django.contrib.auth import get_user_model

from .models import PrivateMessage

User = get_user_model()


class PMCreateForm(forms.ModelForm):
    contact_username = forms.CharField(label="", max_length=120, widget=forms.TextInput(attrs={"placeholder": "to... (username)"}))
    subject = forms.CharField(label="", max_length=120, widget=forms.TextInput(attrs={"placeholder": "Subject"}))
    content = forms.CharField(label="", widget=forms.Textarea(
    attrs={"class": "form-control message-form richtext", "placeholder": "Write your message here.."}))

    class Meta:
        model = PrivateMessage
        fields = [
        "contact_username",
        "subject",
        "content"
        ]

    def clean(self, *args, **kwargs):
        contact = self.cleaned_data.get("contact_username")
        try:
            contact = User.objects.get(username=contact)
        except User.DoesNotExist:
            raise forms.ValidationError("This username does not exist.")

        return super(PMCreateForm, self).clean(*args, **kwargs)


class PMReplyForm(forms.ModelForm):
    subject = forms.CharField(label="", max_length=120, widget=forms.TextInput(attrs={"placeholder": "Subject"}))
    content = forms.CharField(label="", widget=forms.Textarea(
    attrs={"class": "form-control message-form", "placeholder": "Write your message here.."}))

    class Meta:
        model = PrivateMessage
        fields = [
        "subject",
        "content"
        ]
