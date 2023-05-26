from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from . import forms
from .models import *
from delivery.models import Customer
from delivery.models import Order

def sign_up(request):
    form = forms.SignUpForm(request.POST)
    form2 = forms.TypeChoise(request.POST)
    if form.is_valid() and request.method == 'POST':
        user = form.save()
        user.save()
        if form2.is_valid():
            a = request.POST.get('a')
            if a == 'admin':
                type = UserType.objects.create(
                    user=user,
                    establishment=True
                )
                login(request, user)
                return redirect('delivery:create_establishment')
            if a == 'user':
                type = UserType.objects.create(
                    user=user,
                    establishment=False
                )
                login(request, user)
                return redirect('delivery:customer_create')
    form = forms.SignUpForm()
    return render(request, 'sign_up.html', {'form': form, 'form2': form2})


def sign_in(request):
    form = forms.SignInForm(data=request.POST)
    if form.is_valid() and request.method == 'POST':
        user = form.get_user()
        login(request, user)
        return redirect('delivery:home')
    form = forms.SignInForm()
    return render(request, 'sign_in.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('users:sign_in')


def profile(request):
    customer = Customer.objects.get(user=request.user)
    orders_list = Order.objects.filter(customer=customer)
    return render(request, 'profile.html', {'a': customer, 'orders': orders_list})
