"""
RUTAS DE LA API (Semana 8) de la App semana3.

`config/urls.py` incluye este archivo bajo el prefijo "/api/":
    path("api/", include("semana3.api_urls"))
"""

from rest_framework.routers import DefaultRouter

from . import api_views

# Ejercicio 5: el router genera solo las URLs de list/create/retrieve/
# update/partial_update/destroy para cada ViewSet registrado.
router = DefaultRouter()
router.register("cursos", api_views.CursoViewSet, basename="curso")
router.register("estudiantes", api_views.EstudianteViewSet, basename="estudiante")  # Ejercicio 7

urlpatterns = router.urls
