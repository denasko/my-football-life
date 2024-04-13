from django.urls import path
from . import views

app_name = 'leagues_and_teams'

urlpatterns = [
    path('tables/', views.championships_list, name='championships_list'),
    path('tables/<str:championship_name>/', views.championship_table, name='championship_table'),
    path('tables/<str:championship_name>/matches', views.list_championship_games, name='list_championship_games'),
    path('tables/<str:championship_name>/prev', views.preview, name='preview'),

]
