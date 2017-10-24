from django import forms

from .models import Post


class PostCreateForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=160, widget=forms.TextInput(
                            attrs={"class": "form-control post-title-form", "placeholder": "Title"}))
    content = forms.CharField(label="", widget=forms.Textarea(
                                attrs={"class": "form-control message-form", "placeholder": "Post content"}))

    class Meta:
        model = Post
        fields = [
            "name",
            "content",

        ]
