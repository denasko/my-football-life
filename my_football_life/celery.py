from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_football_life.settings')

app = Celery('my_football_life')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'parse_match_objects_every_10_minutes': {
        'task': 'leagues_and_teams.tasks.parse_match_objects',
        'schedule': timedelta(minutes=5),
    },
    'parse_championships_team_teamstanding_daily': {
        'task': 'leagues_and_teams.tasks.parse_championships_team_teamstanding',
        'schedule': timedelta(minutes=33),
    },
}