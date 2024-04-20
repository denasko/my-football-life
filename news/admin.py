from django.contrib import admin, messages

from .models import News, Comment, NewsTags, NewsSection


class NewsSectionInline(admin.TabularInline):
    model = NewsSection
    extra = 1


class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsSectionInline]
    filter_horizontal = ('tags',)
    list_display = ('title', 'display_tags', 'championship', 'team', 'date', 'is_published')
    list_filter = ('tags', 'championship', 'team', 'date', 'is_published')
    search_fields = ('title', 'championship__name', 'team__name', 'is_published')
    list_per_page = 10
    actions = ['set_published', 'set_not_published']

    def display_tags(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())

    display_tags.short_description = 'Tags'

    @admin.action(description="Опубликовать")
    def set_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} новостей опубликованы")

    @admin.action(description="Запретить")
    def set_not_published(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} новостей заблокированы", messages.WARNING)


admin.site.register(News, NewsAdmin)
admin.site.register(NewsTags)
admin.site.register(Comment)
