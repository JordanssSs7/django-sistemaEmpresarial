from django.urls import path

from . import views

urlpatterns = [
    path('', views.listado, name='semana2_listado'),
    path('nueva/', views.crear, name='semana2_crear'),
]
