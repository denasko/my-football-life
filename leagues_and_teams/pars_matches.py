import os

import requests
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_football_life.settings')
import django

django.setup()
from leagues_and_teams.models import Championship, Team, Match
from .servises import get_match_day


def get_match_data(championship_name, match_day):
    uri = f'https://api.football-data.org/v4/competitions/{championship_name}/matches?matchday={match_day}'
    response = requests.get(uri, headers={'X-Auth-Token': '81866e2c8ae342a2921bcf1a4753e22d'})
    return response.json()


@transaction.atomic
def update_or_create_matches(championship, match_data):
    for match_info in match_data['matches']:
        home_team_data = match_info['homeTeam']
        away_team_data = match_info['awayTeam']

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
            date=match_info['utcDate'],
            championship=championship,
            defaults={
                'status': match_info['status'],
                'matchday': match_info['matchday'],
                'home_goals': match_info['score']['fullTime']['home'],
                'away_goals': match_info['score']['fullTime']['away'],
            }
        )

        if not created:
            match.status = match_info['status']
            match.matchday = match_info['matchday']
            match.home_goals = match_info['score']['fullTime']['home']
            match.away_goals = match_info['score']['fullTime']['away']
            match.save()


def create_matches():
    championships = {
        'PD': 'Primera Division',
        'BL1': 'Bundesliga',
        'PL': 'Premier League',
        'SA': 'Serie A',
        'FL1': 'Ligue 1'
    }

    for league_pars, league_name in championships.items():
        print(f"{league_pars} ready to parse")
        match_day = get_match_day(league_name)
        match_data = get_match_data(league_pars, match_day)
        championship = Championship.objects.get(name=league_name)
        update_or_create_matches(championship, match_data)


def main():
    create_matches()


if __name__ == "__main__":
    main()
