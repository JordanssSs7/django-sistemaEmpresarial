"""
SERIALIZERS de la App "Gestión de Matrículas y Pensiones" (Semana 8).

Un serializer hace lo mismo que un Form, pero para la API: convierte un
objeto de Python/ORM en algo que se puede mandar como JSON (serializar), y
al revés, convierte JSON recibido en datos listos para guardar (deserializar
+ validar).
"""

from rest_framework import serializers

from .models import Curso, Estudiante, Observacion


class CursoSerializer(serializers.ModelSerializer):
    """Serializer del recurso simple (Ejercicio 2)."""

    class Meta:
        model = Curso
        fields = ["id", "nombre", "creditos", "cupos_disponibles"]

    def validate_creditos(self, value):
        """Ejercicio 3: regla de negocio propia, igual que un clean_<campo>
        de un Form, pero del lado del serializer."""
        if value <= 0:
            raise serializers.ValidationError("Los créditos deben ser mayores que 0.")
        return value


class ObservacionSerializer(serializers.ModelSerializer):
    """Serializer "hijo", usado ANIDADO dentro de EstudianteSerializer."""

    class Meta:
        model = Observacion
        fields = ["id", "fecha", "tipo", "descripcion"]


class EstudianteSerializer(serializers.ModelSerializer):
    """Ejercicio 7: recurso con relaciones, de solo lectura.
    `observaciones` es el related_name de la FK en Observacion -> Estudiante
    (relación 1:N). Al declararlo como un serializer anidado, cada estudiante
    sale en el JSON con la LISTA completa de sus observaciones adentro."""

    observaciones = ObservacionSerializer(many=True, read_only=True)

    class Meta:
        model = Estudiante
        fields = [
            "id", "codigo_alumno", "nombres", "apellidos", "estado",
            "observaciones",
        ]
