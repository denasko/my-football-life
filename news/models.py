from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from leagues_and_teams.models import Championship, Team


class News(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='news_images/', null=True, blank=True)
    sections = models.ManyToManyField('NewsSection', related_name='news_sections', blank=True, null=True)
    championship = models.ForeignKey(Championship, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='championship_news')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='team_news')
    tags = models.ManyToManyField('NewsTags', related_name='news', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ('-date',)
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['championship']),
        ]

    def __str__(self):
        return f'{self.title}, championship - {self.championship}, team - {self.team}'

    def count_likes(self):
        return Like.objects.filter(news=self).count()

    def count_comments(self):
        return Comment.objects.filter(news=self).count()


class NewsSection(models.Model):
    title = models.CharField(max_length=100)
    content = CKEditor5Field()
    photo = models.ImageField(upload_to='news_images/', null=True, blank=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='news_sections', null=True, blank=True)

    def __str__(self):
        return self.title


class NewsTags(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f'{self.name}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey('News', on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'{self.user} - {self.news}'
