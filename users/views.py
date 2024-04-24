from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page

from .forms import RegistrationForm, RefactorProfileForm, FeedbackForm, CustomUserForm
from .models import Profile, Feedback


def index(request):
    return render(request, 'users/index.html')


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
                login(request, user)
                return redirect('users:index')
            else:
                return render(request, template_name='registration/register.html',
                              context={'form': form, 'error_message': 'Ошибка при регистрации пользователя'})
    else:
        form = RegistrationForm()
    return render(request, template_name='registration/register.html', context={'form': form})


# _______________________________________________About and Feedback___________________________________________________


#@cache_page(60 * 15)
def about(request):
    return render(request, template_name='users/about.html')


@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_instance = form.save(commit=False)
            feedback_instance.profile = request.user.profile
            feedback_instance.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('users:index')
    else:
        form = FeedbackForm()
    return render(request, 'users/feedback.html', {'form': form})


def all_feedbacks(request):
    feedbacks = Feedback.objects.filter(is_published=True)
    paginator = Paginator(feedbacks, 5)
    page = request.GET.get('page')
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        feedbacks = paginator.page(1)
    except EmptyPage:
        feedbacks = paginator.page(paginator.num_pages)
    return render(request, template_name='users/all_feedbacks.html', context={'feedbacks': feedbacks})


# _______________________________________________Profile___________________________________________________


@login_required
def profile(request):
    profile: Profile = request.user.profile
    return render(request, template_name='users/profile.html', context={'profile': profile})


@login_required
def update_profile(request):
    """
    :param request:
    :return: Page with current profile
    """
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=request.user)
        profile_form = RefactorProfileForm(request.POST, instance=request.user.profile)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile')

    else:
        user_form = CustomUserForm(instance=request.user)
        profile_form = RefactorProfileForm(instance=request.user.profile)
    return render(request, template_name='users/update_profile.html', context={'profile_form': profile_form,
                                                                               'user_form': user_form})


def another_profile(request, profile_id: Profile.id):
    user_profile = Profile.objects.get(pk=profile_id)
    another_user = User.objects.get(profile=user_profile)
    return render(request, template_name='users/another_profile.html', context={'profile': user_profile,
                                                                                'another_user': another_user})
