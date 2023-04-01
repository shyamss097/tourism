from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Manager, User


class UserSignupForm(UserCreationForm):
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'address')


class ManagerSignupForm(UserCreationForm):
    phone = forms.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone')


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ManagerLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
