from django import forms
from django.contrib.auth.forms import AuthenticationForm
from geolocation_fields.models import fields
from .models import *


class LocationForm(forms.ModelForm):
    geo = fields.PointField()

    class Meta:
        model = Location
        fields = ['geo']


class CustomerCreationForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='Введите ваш адрес')
    phone = forms.CharField(widget=forms.NumberInput(attrs={'class': 'input'}), label='Введите ваш номер')

    class Meta:
        model = Customer
        fields = ['address', 'phone']


class EstablishmentCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='Введите название заведения')
    bio = forms.CharField(widget=forms.Textarea(), label='Описание заведения')
    phone = forms.CharField(widget=forms.NumberInput(attrs={'class': 'input'}), label='Номер телефона заведения')
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='Адрес заведения')
    type = forms.ModelChoiceField(queryset=Category.objects.all())
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'input'}), label='Фото заведения')
    logo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'input'}), label='Логотип заведения')

    class Meta:
        model = Establishments
        fields = ['name', 'bio', 'phone', 'address', 'type', 'photo', 'logo']


class FoodCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='Название блюда')
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input has-text-centered'}), label='Цена блюда')
    bio = forms.CharField(widget=forms.Textarea(), label='Описание блюда')
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'input'}), label='Фото блюда')
    category = forms.ModelChoiceField(queryset=FoodCategory.objects.all())

    class Meta:
        model = Food
        fields = ['name', 'price', 'bio', 'photo', 'category']


class OrderForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='Напишите адрес')
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='Номер телефона')

    class Meta:
        model = Order
        fields = ['address', 'phone']


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='Введите ваше имя и фамилию')

    class Meta:
        model = Profile
        fields = ['full_name']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='Никнейм')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), label='Пароль')

    class Meta:
        model = User
        fields = ['username', 'password']


