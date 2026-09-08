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
admin.site.register(models.Estudiante)
admin.site.register(models.Matricula)
admin.site.register(models.Pension)
admin.site.register(models.Pago)
