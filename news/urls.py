from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.get_news, name='get_news'),
    path('<int:news_id>', views.news_detail, name='news_detail'),

]