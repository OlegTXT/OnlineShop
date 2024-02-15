from django.contrib import auth
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from user.forms import RegisterForm, AuthForm


# Create your views here.
def login(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(request=request,
                                     username=username,
                                     password=password)
            if user:
                auth.login(request=request, user=user)
                return redirect('/')
    context = {
        'form': form
    }
    return render(request,
                  'user/login.html', context)


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


def logout_1(request):
    logout(request)
    return redirect('product-list')
