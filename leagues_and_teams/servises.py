import os

import requests
from django.db.models import Min

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_football_life.settings')
import django

django.setup()
from leagues_and_teams.models import TeamStanding, Championship, Team, Match


def get_match_day(championship_name: Championship.name) -> int:
    championship: Championship = Championship.objects.get(name=championship_name)
    min_played_games: int = TeamStanding.objects.filter(team__championship=championship).aggregate(
        min_played_games=Min('played_games'))['min_played_games']

    #print(f'match_day {min_played_games} - {championship_name}')
    return min_played_games + 1




