import json
import os

import requests
from django.db.models import Min

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_football_life.settings')
import django

django.setup()
from leagues_and_teams.models import TeamStanding, Championship


def get_matchday(championship_name) -> int:
    championship: Championship = Championship.objects.get(name=championship_name)
    min_played_games: int = TeamStanding.objects.filter(team__championship=championship).aggregate(
        min_played_games=Min('played_games'))['min_played_games']
    match_day_next = min_played_games + 1
    print(championship)
    print(match_day_next)
    return match_day_next


def pars_matches():
    leagues = {'PD': 'Primera Division', 'BL1': 'Bundesliga', 'PL': 'Premier League', 'SA': 'Serie A', 'FL1': 'Ligue 1'}
    headers = {'X-Auth-Token': '81866e2c8ae342a2921bcf1a4753e22d'}

    for league_pars, league_name in leagues.items():

        match_day = get_matchday(championship_name=league_name)
        uri = f'https://api.football-data.org/v4/competitions/{league_pars}/matches?matchday={match_day}'

        response = requests.get(uri, headers=headers)
        data = response.json()

        with open(f'{league_name}.json', 'w') as file:
            json.dump(data, file)


def print_matches(league: str) -> dict:
    with open(f'{league}.json', 'r') as file:
        matches = json.load(file)
    return matches['matches']


pars_matches()



