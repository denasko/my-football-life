from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from .servises import get_match_day

from .models import TeamStanding, Championship, Match


@cache_page(60 * 15)
def championships_list(request):
    championships = Championship.objects.all()
    return render(request, template_name='leagues_and_teams/championships_list.html',
                  context={'championships': championships})


@cache_page(60 * 15)
def championship_table(request, championship_name: 'Championship.name'):
    """
    :param request:
    :param championship_name: Championship.name
    :return:
    """
    try:
        championship: Championship = get_object_or_404(Championship, name=championship_name)
        standings: TeamStanding = TeamStanding.objects.filter(team__championship=championship).order_by('position')
        return render(request, template_name='leagues_and_teams/championship_table.html',
                      context={'standings': standings, 'championship': championship})

    except Championship.DoesNotExist:
        messages.error(request, f'Чемпионат {championship_name} не найден :с')
        return redirect('leagues_and_teams:championship_list')


@cache_page(60 * 1)
def list_championship_games(request, championship_name: 'Championship.name'):
    championship: Championship = get_object_or_404(Championship, name=championship_name)
    match_days = (Match.objects.filter(championship=championship).order_by('matchday').
                  values_list('matchday', flat=True).distinct())

    if request.method == 'POST':
        match_day = request.POST.get('matchday')
        matches = championship.matches.filter(matchday=match_day)
    else:
        match_day = get_match_day(championship_name)
        matches = championship.matches.filter(matchday=match_day)
    return render(request, template_name='leagues_and_teams/list_championship_games.html',
                      context={'matches': matches, 'match_days': match_days, 'championship_name': championship_name})


def preview(request, championship_name: 'Championship.name'):
    return render(request, template_name='leagues_and_teams/preview.html',)
