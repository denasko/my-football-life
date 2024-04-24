from datetime import timezone

from django.contrib.auth.models import User
from django.db import models


class FootballField(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f' {self.name} , {self.address}'


class Event(models.Model):
    football_field = models.ForeignKey(FootballField, related_name='events', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=False)
    start_time = models.TimeField(blank=True, null=True)
    max_players = models.IntegerField(blank=True, null=True)
    players = models.ManyToManyField('Players', related_name='events')

    def __str__(self):
        return f' {self.football_field} , {self.title}, {self.players.count()} {self.date}'

    @property
    def formatted_date(self):
        return self.date.strftime("%d %B %Y")


class Players(models.Model):
    STATUS_CHOICES = [
        ('заявлен', 'Заявлен'),
        ('принят', 'Принят'),
        ('отклонен', 'Отклонен'),
    ]

    event = models.ForeignKey(Event, related_name='event_players', on_delete=models.CASCADE, verbose_name='Событие')
    user = models.ForeignKey(User, related_name='player', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='заявлен')


