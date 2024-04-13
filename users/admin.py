from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Feedback


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Профиль"


class FeedbackInline(admin.StackedInline):
    model = Feedback
    can_delete = False
    verbose_name_plural = "Отзывы"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birthday', 'phone_number', 'bio']
    inlines = [FeedbackInline, ]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['profile', 'rating', 'header', 'comment', 'date']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
