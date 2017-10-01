from django import forms
from .models import Post
from apps.forum.models import Forum


class PostCreateForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=120, widget=forms.TextInput(attrs={"placeholder": "Title"}))
    content = forms.CharField(label="", widget=forms.Textarea(
    attrs={"class": "form-control message-form", "placeholder": "Post content"}))

    class Meta:
        model = Post
        fields = [
            "name",
            "content",
            
        ]
