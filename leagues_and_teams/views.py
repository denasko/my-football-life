from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .servises import print_matches
from .models import TeamStanding, Championship


def championships_list(request):
    championships = Championship.objects.all()
    return render(request, template_name='leagues_and_teams/championships_list.html',
                  context={'championships': championships})


def championship_table(request, championship_name: Championship):
    """
    :param request:
    :param championship_name: Championship.name
    :return:
    """
    try:
        championship: Championship = get_object_or_404(Championship, name=championship_name)
        standings: TeamStanding = TeamStanding.objects.filter(team__championship=championship)
        return render(request, template_name='leagues_and_teams/championship_table.html',
                      context={'standings': standings, 'championship': championship})

    except Championship.DoesNotExist:
        messages.error(request, f'Чемпионат {championship_name} не найден :с')
        return redirect('leagues_and_teams:championship_list')


def list_championship_games(request, championship_name):
    matches = print_matches(league='BL1')
    return render(request, template_name='leagues_and_teams/list_championship_games.html',
                  context={'matches': matches})
