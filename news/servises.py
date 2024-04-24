from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from leagues_and_teams.models import Championship
from news.models import NewsTags, News


def filter_news(request, news):
    championship_name = request.GET.get('championship')
    tag_name = request.GET.get('tag')
    date = request.GET.get('date')

    print(championship_name, tag_name, date, sep='\n')

    if championship_name:
        try:
            championship = Championship.objects.get(name=championship_name)
            news = news.filter(championship=championship)
        except Championship.DoesNotExist:
            pass

    if tag_name:
        news = news.filter(tags__name=tag_name)

    if date:
        # Assuming 'date' is in YYYY-MM-DD format
        news = news.filter(date=date)

    return news




