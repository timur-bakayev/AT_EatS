from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ChoiceField

from .models import *


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Create any username'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Create any password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


Choises = [
    ('user', 'Покупатель'),
    ('admin', 'Заведение'),
]


class TypeChoise(forms.Form):
    a = forms.ChoiceField(widget=forms.RadioSelect, choices=Choises , label='Выберите ')


class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Имя пользователя'}) , label='Имя пользователя')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Введите пароль'}), label='Пароль')

    class Meta:
        model = User
        fields = ['username', 'password']