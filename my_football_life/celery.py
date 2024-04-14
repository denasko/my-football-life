from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

# Установите переменную окружения 'DJANGO_SETTINGS_MODULE' на ваш файл настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_football_life.settings')

# Создайте экземпляр объекта Celery
app = Celery('my_football_life')

# Загрузите конфигурацию из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически загрузите задачи из всех модулей Django в приложение Celery
app.autodiscover_tasks()




app.conf.beat_schedule = {
    'parse_match_objects_every_10_minutes': {
        'task': 'your_app.tasks.parse_match_objects',
        'schedule': timedelta(minutes=10),
    },
    'parse_championships_team_teamstanding_daily': {
        'task': 'your_app.tasks.parse_championships_team_teamstanding',
        'schedule': timedelta(minutes=25),
    },
}