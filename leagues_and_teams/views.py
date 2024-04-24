from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page

from .models import TeamStanding, Championship, Match, NextMatchPreview
from .servises import get_match_day


# _________________________________________________Championships________________________________________________________


def championships_list(request):
    """
    :param request:
    :return: page with list of Championships
    """
    championships = Championship.objects.all()
    return render(request, template_name='leagues_and_teams/championships_list.html',
                  context={'championships': championships})


def championship_table(request, championship_name: 'Championship.name'):
    """
    :param request:
    :param championship_name: Championship.name
    :return: page with championship table
    """
    try:
        championship: Championship = get_object_or_404(Championship, name=championship_name)
        standings: TeamStanding = TeamStanding.objects.filter(team__championship=championship).order_by('position')
        return render(request, template_name='leagues_and_teams/championship_table.html',
                      context={'standings': standings, 'championship': championship})

    except Championship.DoesNotExist:
        messages.error(request, f'Чемпионат {championship_name} не найден :с')
        return redirect('leagues_and_teams:championship_list')


# _________________________________________________Matches________________________________________________________


@cache_page(60 * 1)
def list_championship_games(request, championship_name: 'Championship.name'):
    """
    :param request:
    :param championship_name: Championship.name
    :return: page with games in championship
    """
    championship: Championship = get_object_or_404(Championship, name=championship_name)
    match_days = (Match.objects.filter(championship=championship).order_by('matchday').
                  values_list('matchday', flat=True).distinct())

    if request.method == 'POST':
        match_day = request.POST.get('matchday')
        matches = championship.matches.filter(matchday=match_day)
    else:
        match_day: int = get_match_day(championship_name=championship_name)
        matches = championship.matches.filter(matchday=match_day)
    return render(request, template_name='leagues_and_teams/list_championship_games.html',
                  context={'matches': matches, 'match_days': match_days, 'championship_name': championship_name})


def upcoming_matches(request):
    """
    :param request:
    :return: Page with upcoming matches
    """
    all_matches = Match.objects.filter(status='TIMED').order_by('date')[:20]
    paginator = Paginator(all_matches, 5)
    page = request.GET.get('page')

    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)

    return render(request, template_name='leagues_and_teams/upcoming_matches.html', context={'matches': matches})


# _________________________________________________Preview________________________________________________________


def preview(request, championship_name: 'Championship.name'):
    """
    :param request:
    :param championship_name: Championship.name
    :return: page with preview of next match
    """
    next_match_day: int = get_match_day(championship_name=championship_name)
    print(next_match_day)
    previews = NextMatchPreview.objects.filter(match__matchday=next_match_day)
    championship: Championship = get_object_or_404(Championship, name=championship_name)
    return render(request, template_name='leagues_and_teams/preview.html',
                  context={'previews': previews, 'championship': championship, 'next_match_day': next_match_day})
