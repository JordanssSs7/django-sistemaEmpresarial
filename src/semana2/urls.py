from django.urls import path

from . import views

urlpatterns = [
    path('', views.listado, name='semana2_listado'),
    path('nueva/', views.crear, name='semana2_crear'),
    path('citas/<int:cita_id>/', views.detalle, name='semana2_detalle'),
    path('citas/<int:cita_id>/estado/', views.actualizar_estado, name='semana2_actualizar_estado'),

    path('profesionales/', views.listado_profesionales, name='semana2_profesionales'),
    path('profesionales/nuevo/', views.crear_profesional, name='semana2_crear_profesional'),

    path('horarios/', views.listado_horarios, name='semana2_horarios'),
    path('horarios/nuevo/', views.crear_horario, name='semana2_crear_horario'),
]
