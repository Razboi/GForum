from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    content = forms.CharField(label="", max_length=5000, widget=forms.Textarea(
        attrs={"class": "form-control comment-form richtext"}))

    class Meta:
        model = Comment
        fields = [
            "content"
        ]
