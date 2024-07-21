from django.urls import path

from game import views


app_name='game'

urlpatterns = [
    path('choose/<int:game_id>/', views.Choose.as_view(), name='choose'),
    path('play/', views.PlayGame.as_view(), name='play'),
]
