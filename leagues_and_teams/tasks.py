from celery import shared_task
from .pars_matches import create_matches
from  .pars_teamstadings import create_championships_team_teamstanding


@shared_task
def parse_match_objects():
    create_matches()


@shared_task
def parse_championships_team_teamstanding():
    create_championships_team_teamstanding()