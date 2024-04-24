from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from leagues_and_teams.models import Championship, Team
from .models import News, Like, Comment, NewsTags
from .servises import filter_news


def get_news(request):
    championships = Championship.objects.all()
    tags = NewsTags.objects.all()
    news = News.objects.all()
    print(request.GET.get)
    news = filter_news(request, news)

    paginator = Paginator(news, 5)
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    context = {
        'news': news,
        'championships': championships,
        'tags': tags,
        'selected_championship': request.GET.get('championship'),
        'selected_tag': request.GET.get('tag'),
        'selected_date': request.GET.get('date'),
    }

    return render(request, 'news/news.html', context)


def news_detail(request, news_id: News.pk):
    news = News.objects.get(pk=news_id)
    return render(request, template_name='news/news_detail.html', context={'news': news})


def like_news(request, news_id: News.pk):
    if request.method == 'POST':
        news = News.objects.get(pk=news_id)
        like, created = Like.objects.get_or_create(user=request.user, news=news)
        if not created:
            like.delete()
    return redirect('news:news_detail', news_id=news_id)


@login_required
def add_comment(request, news_id: News.pk):
    if request.method == 'POST':
        news = News.objects.get(pk=news_id)
        print(request.user.username)
        comment = Comment(user=request.user, news=news, text=request.POST.get('text'))
        comment.save()
    return redirect('news:news_detail', news_id=news_id)


def delete_comment(request, comment_id: Comment.pk, news_id: News.pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_id)
        if request.user == comment.user:
            comment.delete()
    return redirect('news:news_detail', news_id=news_id)



