from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.get_news, name='get_news'),
    path('<int:news_id>', views.news_detail, name='news_detail'),
    path('like/<int:news_id>/', views.like_news, name='like_news'),
    path('comment/<int:news_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/<int:news_id>', views.delete_comment, name='delete_comment'),

]