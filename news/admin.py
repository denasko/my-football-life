from django.contrib import admin

from .models import News


@admin.register(News)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('title_first', 'title_second', 'title_third', 'title_fourth', 'main_image', 'second_image',
                    'championship', 'team', 'date', 'is_published')
    list_filter = ('championship', 'team', 'date', 'is_published')
    search_fields = ('title_first', 'content_firth', 'championship', 'team', 'is_published')
    list_per_page = 10
