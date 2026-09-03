from django.urls import path

from . import views

app_name = "semana3"

urlpatterns = [
    path("", views.index, name="index"),
]
