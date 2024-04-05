from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegistrationForm, RefactorProfileForm


def index(request):
    return render(request, 'users/index.html')


def change_profile(request):
    """
    :param request:
    :return: Page with current profile
    """
    if request.method == 'POST':
        form = RefactorProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            return redirect('users:change_profile')

    else:
        form = RefactorProfileForm(instance=request.user.profile)
    return render(request, template_name='users/profile.html', context={'form': form})


def register(request):
    """
    :param request:
    :return: page with registration form
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')
            hashed_password = make_password(user_password)

            # create a new user
            user = User.objects.create(username=user_username, email=user_email, password=hashed_password)

            if user:
                return redirect('users:index')
            else:
                return render(request, template_name='registration/register.html',
                              context={'form': form, 'error_message': 'Ошибка при регистрации пользователя'})
    else:
        form = RegistrationForm()
    return render(request, template_name='registration/register.html', context={'form': form})



