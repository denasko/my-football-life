from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('football_map/', views.football_map, name='football_map'),
    path('<str:football_field_name>', views.football_field, name='football_field'),
    path('<str:football_field_name>/create_event', views.create_event, name='create_event'),

]
