from django import forms
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']



class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']