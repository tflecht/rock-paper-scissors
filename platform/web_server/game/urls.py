from django.urls import path

from game import views


app_name='game'

urlpatterns = [
    path('choose/<int:game_id>/', views.Choose.as_view(), name='choose'),
    path('complete/', views.CompleteGame.as_view(), name='complete'),
    path('pending/', views.PendingGame.as_view(), name='pending'),
    path('play/', views.PlayGame.as_view(), name='play'),
    path('status/<int:game_id>/', views.Status.as_view(), name='status'),
]
