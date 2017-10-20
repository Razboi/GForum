from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


# Change image form
class ProfileImageForm(forms.ModelForm):
    image = forms.ImageField(label="")

    class Meta:
        model = User
        fields = [
            "image",
        ]


# login form
class UserLoginForm(forms.Form):
    username = forms.CharField(label="", max_length=25, widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    # if the user/password combination does not exists raise an error
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)  # not login, only checking if it exists
        if not user:
            raise forms.ValidationError("Incorrect username or password.")

        return super(UserLoginForm, self).clean(*args, **kwargs)


# register form
class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label="", max_length=25, widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Password Confirmation"}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={"placeholder": "Email"}))

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2"
        ]

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get("password")  # password
        password2 = self.cleaned_data.get("password2")  # password confirmation
        # if the password and the password confirmation are not the same raise an error
        if password != password2:
            raise forms.ValidationError("Passwords must match")

        # if there is a user with that username raise an error
        username = self.cleaned_data.get("username")
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("This username has already been registered")

        email = self.cleaned_data.get("email")
        email_qs = User.objects.filter(email=email)
        # if the email is already registered raise an error
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")

        return super(UserRegisterForm, self).clean(*args, **kwargs)
