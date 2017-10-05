from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control comment-form comment_richtext"}))

    class Meta:
        model = Comment
        fields = [
            "content"
        ]
