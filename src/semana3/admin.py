"""
Registro de los modelos en el panel de administración de Django (/admin/).

`admin.site.register(Modelo)` hace que el modelo aparezca en /admin/ con
formularios automáticos de alta, edición y borrado.

Para qué sirve aquí: cargar datos de prueba rápido sin pasar por los
formularios web de la app. Requiere un superusuario:
    python manage.py createsuperuser
"""

from django.contrib import admin

from . import models

# Entidades independientes
admin.site.register(models.NivelEducativo)
admin.site.register(models.AnioLectivo)
admin.site.register(models.TipoDescuento)
admin.site.register(models.MetodoPago)
admin.site.register(models.Apoderado)

# Entidades relacionadas (con ForeignKey)
admin.site.register(models.Grado)
admin.site.register(models.Matricula)
admin.site.register(models.Pension)
admin.site.register(models.Pago)

# ---------------------------------------------------------------------------
# Semana 5 — entidades de las tres relaciones nuevas: 1:1, 1:N y N:M
# ---------------------------------------------------------------------------
admin.site.register(models.FichaMedica)     # relación 1:1 con Estudiante
admin.site.register(models.Curso)           # lado N:M
admin.site.register(models.CursoEstudiante) # modelo intermedio de la relación N:M


# ---------------------------------------------------------------------------
# Ejercicio 4 sem5 — ModelAdmin personalizado (list_display + search_fields)
# ---------------------------------------------------------------------------
# @admin.register(Modelo) es lo mismo que admin.site.register(Modelo, EstaClase),
# pero como decorador: engancha la clase de abajo con el modelo indicado.

# ---------------------------------------------------------------------------
# Ejercicio 6 — StackedInline para la relación 1:1 (FichaMedica)
# ---------------------------------------------------------------------------
# Un Inline no se registra aparte: se declara y se cuelga de otro ModelAdmin
# (vía `inlines = [...]`) para editarse DENTRO de la pantalla del "padre".
# StackedInline = campos uno debajo del otro (como un mini-formulario aparte),
# ideal para 1:1 porque solo hay UN registro relacionado que mostrar.

class FichaMedicaInline(admin.StackedInline):
    model = models.FichaMedica
    extra = 0     # no ofrecer formularios extra en blanco: 1:1 = a lo sumo 1
    max_num = 1   # refuerza en el propio Admin que no puede haber más de una


@admin.register(models.Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    """Entidad principal: se ve código, nombre completo, estado y apoderado
    de un vistazo, sin entrar a cada registro."""
    list_display = ("codigo_alumno", "nombres", "apellidos", "estado", "apoderado")
    search_fields = ("nombres", "apellidos", "num_documento", "codigo_alumno")
    # Ejercicio 5: panel lateral para filtrar rápido por estado
    # (Activo / Inactivo / Retirado) sin escribir nada.
    list_filter = ("estado",)
    # Ejercicio 6: la ficha médica del estudiante se edita en la misma pantalla.
    inlines = [FichaMedicaInline]


@admin.register(models.Observacion)
class ObservacionAdmin(admin.ModelAdmin):
    """Relación 1:N: se ve a qué estudiante pertenece cada observación,
    su tipo y fecha, sin abrir cada una."""
    list_display = ("estudiante", "tipo", "fecha", "descripcion")
    search_fields = ("descripcion", "estudiante__nombres", "estudiante__apellidos")
    # Ejercicio 5: filtra por tipo (Académica/Conductual/Administrativa) y
    # por fecha (Django genera solo un desglose por año/mes/día/hoy).
    list_filter = ("tipo", "fecha")
