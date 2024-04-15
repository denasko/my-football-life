import os

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_football_life.settings')
import django

django.setup()
from leagues_and_teams.models import TeamStanding, Championship, Team


def create_championships_team_teamstanding():
    headers = {'X-Auth-Token': '81866e2c8ae342a2921bcf1a4753e22d'}
    leagues = ['PD', 'BL1', 'PL', 'SA', 'FL1']
    for liga in leagues:
        uri = f'https://api.football-data.org/v4/competitions/{liga}/standings'

        response = requests.get(uri, headers=headers)
        data = response.json()

        # create or get Championship object
        championship_name = data['competition']['name']
        championship_emblem = data['competition']['emblem']
        championship, created = Championship.objects.get_or_create(name=championship_name, emblem=championship_emblem)

        # Update or create Team and TeamStading objects
        for team_data in data['standings'][0]['table']:
            team_info = team_data['team']
            team_id = team_info['id']
            team_name = team_info['name']
            team_short_name = team_info['shortName']
            team_crest_url = team_info['crest']

            team, created = Team.objects.get_or_create(
                id=team_id,
                defaults={'name': team_name, 'short_name': team_short_name, 'crest_url': team_crest_url,
                          'championship': championship}
            )

            # Get or create TeamStanding object
            team_standing, created = TeamStanding.objects.get_or_create(team=team)
            # Update TeamStanding fields
            team_standing.position = team_data['position']
            team_standing.played_games = team_data['playedGames']
            team_standing.wins = team_data['won']
            team_standing.draws = team_data['draw']
            team_standing.losses = team_data['lost']
            team_standing.points = team_data['points']
            team_standing.goals_for = team_data['goalsFor']
            team_standing.goals_against = team_data['goalsAgainst']
            team_standing.goal_difference = team_data['goalDifference']
            team_standing.save()

        print('Parsed standings for league: %s', championship_name)

