from celery import shared_task
from .pars_matches import create_matches_async
from  .pars_teamstadings import create_championships_team_teamstanding_async


@shared_task
def parse_match_objects():
    create_matches_async.apply_async()


@shared_task
def parse_championships_team_teamstanding():
    create_championships_team_teamstanding_async.apply_async()


