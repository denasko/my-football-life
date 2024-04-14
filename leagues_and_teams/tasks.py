from celery import shared_task
from .servises import create_match_objects, create_championships_team_teamstanding


@shared_task
def parse_match_objects():
    create_match_objects()


@shared_task
def parse_championships_team_teamstanding():
    create_championships_team_teamstanding()