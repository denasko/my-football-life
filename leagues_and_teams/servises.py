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
    match_day_next = min_played_games + 1
    print(f'match_day {match_day_next} - {championship_name}')
    return match_day_next


def create_match_objects():
    leagues = {'PD': 'Primera Division', 'BL1': 'Bundesliga', 'PL': 'Premier League', 'SA': 'Serie A', 'FL1': 'Ligue 1'}
    headers = {'X-Auth-Token': '81866e2c8ae342a2921bcf1a4753e22d'}

    for league_pars, league_name in leagues.items():

        match_day = get_match_day(championship_name=league_name)
        uri = f'https://api.football-data.org/v4/competitions/{league_pars}/matches?matchday={match_day}'

        response = requests.get(uri, headers=headers)
        data = response.json()

        championship = Championship.objects.get(name=league_name)

        for match_data in data['matches']:

            home_team_data = match_data['homeTeam']
            away_team_data = match_data['awayTeam']

            home_team, _ = Team.objects.get_or_create(
                id=home_team_data['id'],
                defaults={'name': home_team_data['name'], 'short_name': home_team_data['shortName'],
                          'crest_url': home_team_data['crest']}
            )
            away_team, _ = Team.objects.get_or_create(
                id=away_team_data['id'],
                defaults={'name': away_team_data['name'], 'short_name': away_team_data['shortName'],
                          'crest_url': away_team_data['crest']}
            )

            match, created = Match.objects.get_or_create(
                home_team=home_team,
                away_team=away_team,
                date=match_data['utcDate'],
                championship=championship,
                defaults={
                    'status': match_data['status'],
                    'matchday': match_data['matchday'],
                    'home_goals': match_data['score']['fullTime']['home'],
                    'away_goals': match_data['score']['fullTime']['away'],
                }
            )

            if not created:
                match.status = match_data['status']
                match.matchday = match_data['matchday']
                match.home_goals = match_data['score']['fullTime']['home']
                match.away_goals = match_data['score']['fullTime']['away']
                match.save()

    print('uspeh1')


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

    print('uspeh2')


# create_championships_team_teamstanding()
# create_match_objects()



