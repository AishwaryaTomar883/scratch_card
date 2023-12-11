from django.urls import path
from . import views

app_name = "myapp"


urlpatterns = [
    path("index/", views.index, name="index"),
    #path("home/", views.home, name="home"),
    path("games/", views.games, name="games"),
    path("games/<int:id>/", views.games, name="games"),
    path("scratch-details/", views.scratch_details, name="scratch-details"),
    path("game-history/", views.game_history, name="game_history"),
]
