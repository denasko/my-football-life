import json

import requests


def pars_matches():
    leagues = ['PD', 'BL1', 'PL', 'SA', 'FL1']
    headers = {'X-Auth-Token': '81866e2c8ae342a2921bcf1a4753e22d'}

    for league in leagues:
        uri = f'https://api.football-data.org/v4/competitions/{league}/matches?status=SCHEDULED&limit=1'
        response = requests.get(uri, headers=headers)
        data = response.json()

        with open(f'league_{league}.json', 'w') as file:
            json.dump(data, file)
        print('uspeh')


def print_matches(league: str) -> dict:
    with open(f'league_{league}.json', 'r') as file:
        matches = json.load(file)
    return matches['matches']


pars_matches()
