from django.contrib.auth.models import User
from django.db import models

from leagues_and_teams.models import Championship, Team


class News(models.Model):
    title_first = models.CharField(max_length=100, null=True, blank=True)
    content_first = models.TextField(null=True, blank=True)
    title_second = models.CharField(max_length=100, null=True, blank=True)
    content_second = models.TextField(null=True, blank=True)
    title_third = models.CharField(max_length=100, null=True, blank=True)
    content_third = models.TextField(null=True)
    title_fourth = models.CharField(max_length=100, null=True, blank=True)
    content_fourth = models.TextField(null=True, blank=True)
    main_image = models.ImageField(upload_to='news_images/', null=True, blank=True, verbose_name='Главное изображение')
    second_image = models.ImageField(upload_to='news_images/', null=True, blank=True, verbose_name='Второе изображение')
    championship = models.ForeignKey(Championship, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='championship_news')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='team_news')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title_first
