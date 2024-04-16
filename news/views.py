from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from leagues_and_teams.models import Championship
from .models import News


def get_news(request):
    championships = Championship.objects.all()

    if request.method == 'POST':
        championship_name = request.POST.get('championship')
        if championship_name:
            try:
                championship = Championship.objects.get(name=championship_name)
                news = News.objects.filter(championship=championship)
            except Championship.DoesNotExist:
                news = News.objects.all()
        else:
            news = News.objects.all()
    else:
        news = News.objects.all()

    paginator = Paginator(news, 5)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, template_name='news/news.html', context={'news': news, 'championships': championships})


def news_detail(request, news_id: News.pk):
    news = News.objects.get(pk=news_id)
    return render(request, template_name='news/news_detail.html', context={'news': news})
