from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label="", max_length=25, widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)  # not login, only checking if it exists
        if not user:
            raise forms.ValidationError("Incorrect username or password.")
        if not user.is_active:
            raise forms.ValidationError("This user is not longer active.")
        
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label="", max_length=25, widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Password Confirmation"}))

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2"
        ]

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords must match")

        username = self.cleaned_data.get("username")
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("This username has already been registered")

        return super(UserRegisterForm, self).clean(*args, **kwargs)
