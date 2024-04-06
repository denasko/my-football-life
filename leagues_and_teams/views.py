from django.shortcuts import render, get_object_or_404

from .models import TeamStanding, Championship


def championships_list(request):
    championships = Championship.objects.all()
    return render(request, template_name='leagues_and_teams/championships_list.html',
                  context={'championships': championships})


def championship_table(request, championship_name: Championship):
    """
    :param request:
    :return:
    """
    championship = get_object_or_404(Championship, name=championship_name)
    standings = TeamStanding.objects.filter(team__championship=championship)
    return render(request, template_name='leagues_and_teams/championship_table.html',
                  context={'standings': standings, 'championship': championship})
