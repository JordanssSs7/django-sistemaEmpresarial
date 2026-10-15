"""
VISTAS DE LA API (Semana 8) de la App "Gestión de Matrículas y Pensiones".

Las vistas genéricas de DRF (generics.*) ya traen implementado el CRUD
completo: solo hay que decirles qué queryset usar y con qué serializer.
"""

from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Curso, Estudiante
from .serializers import CursoSerializer, EstudianteSerializer


class CursoViewSet(viewsets.ModelViewSet):
    """Ejercicio 5: reemplaza las 2 vistas genéricas del Ejercicio 4
    (ListCreateAPIView + RetrieveUpdateDestroyAPIView) por una sola clase.
    ModelViewSet ya trae list/create/retrieve/update/partial_update/destroy."""
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    # Ejercicio 8: ?search=texto busca en "nombre"; ?ordering=campo ordena
    # (anteponer "-" para descendente, ej. ?ordering=-cupos_disponibles).
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre"]
    ordering_fields = ["nombre", "creditos", "cupos_disponibles"]


class EstudianteViewSet(viewsets.ReadOnlyModelViewSet):
    """Ejercicio 7: recurso con relaciones, de SOLO LECTURA (list + retrieve,
    sin create/update/destroy -> no tiene sentido crear un estudiante desde
    aquí, ya existe su propio CRUD en semana3/views.py)."""
    serializer_class = EstudianteSerializer

    def get_queryset(self):
        # prefetch_related porque la relación es 1:N (un estudiante tiene
        # VARIAS observaciones) -> select_related no sirve para "varios".
        queryset = Estudiante.objects.prefetch_related("observaciones")
        # Ejercicio 8: filtro manual por parámetro ?estado=
        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    @action(detail=False)
    def activos(self, request):
        """Ejercicio 8: acción propia -> /api/estudiantes/activos/.
        Reutiliza .activos() del EstudianteQuerySet personalizado (Semana 7)
        en vez de repetir el mismo .filter(estado=...) a mano."""
        estudiantes = Estudiante.objects.activos().prefetch_related("observaciones")
        serializer = self.get_serializer(estudiantes, many=True)
        return Response(serializer.data)
