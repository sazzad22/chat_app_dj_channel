# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("2", views.index2, name="index2"),
    path("<str:room_name>/", views.room, name="room"),
]