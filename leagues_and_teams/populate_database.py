import os
import json
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_football_life.settings')
import django

django.setup()
from leagues_and_teams.models import Championship, Team, TeamStanding


uri = 'https://api.football-data.org/v4/competitions/PD/standings'
headers = {'X-Auth-Token': '81866e2c8ae342a2921bcf1a4753e22d'}


def populate_db():
    headers = {'X-Auth-Token': '81866e2c8ae342a2921bcf1a4753e22d'}
    leagues = ['PD', 'BL1']
    for liga in leagues:
        uri = f'https://api.football-data.org/v4/competitions/{liga}/standings'

        response = requests.get(uri, headers=headers)
        data = response.json()
        # create Championship object
        championship_name = data['competition']['name']
        championship_emblem = data['competition']['emblem']
        championship, created = Championship.objects.get_or_create(name=championship_name, emblem=championship_emblem)

        # create Team and TeamStading objects
        for team_data in data['standings'][0]['table']:
            team_info = team_data['team']
            team_id = team_info['id']
            team_name = team_info['name']
            team_short_name = team_info['shortName']
            team_crest_url = team_info['crest']

            team, created = Team.objects.get_or_create(
                id=team_id,
                defaults={'name': team_name, 'short_name': team_short_name, 'crest_url': team_crest_url, 'championship': championship}
            )
            print(team)
            TeamStanding.objects.get_or_create(
                team=team,
                defaults={
                    'position': team_data['position'],
                    'played_games': team_data['playedGames'],
                    'wins': team_data['won'],
                    'draws': team_data['draw'],
                    'losses': team_data['lost'],
                    'points': team_data['points'],
                    'goals_for': team_data['goalsFor'],
                    'goals_against': team_data['goalsAgainst'],
                    'goal_difference': team_data['goalDifference']
                }
            )


populate_db()
