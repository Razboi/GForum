from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"cols": 50, "rows": 5}))

    class Meta:
        model = Comment
        fields = [
            "content"
        ]
