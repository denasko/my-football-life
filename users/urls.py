from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_profile/', views.profile, name='profile'),
    path('profile/', views.update_profile, name='update_profile'),
    path('profile/<int:profile_id>', views.another_profile, name='another_profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('all_feedbacks/', views.all_feedbacks, name='all_feedbacks'),

]
