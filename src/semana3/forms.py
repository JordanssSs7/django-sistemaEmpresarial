"""
FORMULARIOS de la App "Gestión de Matrículas y Pensiones" (Semana 3).

Se usan `ModelForm` (no `forms.Form` como en semana 2): Django construye los
campos LEYENDO el modelo y, al llamar `form.save()`, ejecuta el INSERT (si el
form se creó vacío) o el UPDATE (si se creó con `instance=obj`) vía el ORM.

En cada clase, dentro de `class Meta`:
  - model   -> de qué modelo se sacan los campos
  - fields  -> lista EXPLÍCITA de qué campos aparecen en el formulario
               (los que calcula la vista o son automáticos NO se ponen aquí)
  - widgets -> cambia el control HTML de un campo (ej. selector de fecha)

Los campos ForeignKey se convierten solos en un <select> con las opciones
disponibles (usan el __str__ del modelo relacionado para las etiquetas).
"""

from django import forms   # trae forms.ModelForm, forms.DateInput, forms.DateTimeField, ...

from .models import (      # los modelos sobre los que se construyen los formularios
    AnioLectivo,
    Apoderado,
    CursoEstudiante,       # modelo intermedio de la relación N:M Estudiante<->Curso
    Estudiante,
    Grado,
    Matricula,
    MetodoPago,
    NivelEducativo,
    Pago,
    Pension,
    TipoDescuento,
)


class NivelEducativoForm(forms.ModelForm):
    """Formulario de Nivel educativo: nombre + descripción."""
    class Meta:
        model = NivelEducativo                       # base: el modelo NivelEducativo
        fields = ["nombre_nivel", "descripcion"]     # campos visibles en el formulario


class AnioLectivoForm(forms.ModelForm):
    """Formulario de Año lectivo. Las fechas usan el calendario del navegador."""
    class Meta:
        model = AnioLectivo
        fields = [
            "anio",              # número del año (entero, único)
            "fecha_inicio",      # inicio de clases
            "fecha_fin",         # fin de clases
            "costo_matricula",   # monto de matrícula del año
            "monto_pension",     # monto base de cada cuota mensual
            "estado",            # ACTIVO / CERRADO (llega como <select>)
        ]
        widgets = {
            # type="date" -> input de calendario en vez de caja de texto
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }


class TipoDescuentoForm(forms.ModelForm):
    """Formulario de Tipo de descuento: nombre, porcentaje y si está activo."""
    class Meta:
        model = TipoDescuento
        fields = ["nombre", "porcentaje", "activo"]  # `activo` se muestra como casilla


class MetodoPagoForm(forms.ModelForm):
    """Formulario de Método de pago: nombre y si requiere voucher."""
    class Meta:
        model = MetodoPago
        fields = ["nombre_metodo", "requiere_voucher"]   # `requiere_voucher` -> casilla


class ApoderadoForm(forms.ModelForm):
    """Formulario de Apoderado: documento y datos de contacto."""
    class Meta:
        model = Apoderado
        fields = ["num_documento", "nombres", "apellidos", "telefono", "correo"]


class GradoForm(forms.ModelForm):
    """Formulario de Grado. El campo `nivel` (FK) se muestra como <select>."""
    class Meta:
        model = Grado
        fields = ["nombre_grado", "nivel"]   # `nivel` -> desplegable de niveles educativos


class EstudianteForm(forms.ModelForm):
    """Formulario de Estudiante. El campo `apoderado` (FK) se muestra como <select>."""
    class Meta:
        model = Estudiante
        fields = [
            "codigo_alumno",      # código interno del colegio (único)
            "num_documento",      # DNI del alumno (único)
            "nombres",
            "apellidos",
            "fecha_nacimiento",   # con calendario (ver widgets)
            "estado",             # ACTIVO / INACTIVO / RETIRADO
            "apoderado",          # desplegable de apoderados registrados
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
        }


class EstudianteChoiceField(forms.ModelChoiceField):
    """<select> de estudiantes que muestra también su apoderado en la
    etiqueta, para que al matricular quede claro quién es el responsable
    de pago sin tener que ir a consultarlo aparte."""

    def label_from_instance(self, estudiante):
        return f"{estudiante.nombres} {estudiante.apellidos} — Apoderado: {estudiante.apoderado.nombres} {estudiante.apoderado.apellidos}"


class MatriculaChoiceField(forms.ModelChoiceField):
    """<select> de matrículas que muestra estudiante + año + grado, para
    saber a qué matrícula corresponde una pensión sin adivinar por el id."""

    def label_from_instance(self, matricula):
        return f"{matricula.estudiante.nombres} {matricula.estudiante.apellidos} — {matricula.anio_lectivo} — {matricula.grado}"


class PensionChoiceField(forms.ModelChoiceField):
    """<select> de pensiones que muestra el número de cuota y a quién
    pertenece, para saber contra qué deuda se está registrando un pago."""

    def label_from_instance(self, pension):
        return f"Cuota {pension.num_cuota} — {pension.matricula.estudiante.nombres} {pension.matricula.estudiante.apellidos} (S/ {pension.monto_final or pension.monto_base})"


class MatriculaForm(forms.ModelForm):
    """Formulario de Matrícula.

    `costo_matricula` NO está en `fields`: lo copia la vista `matricula_crear`
    del año lectivo elegido, no lo escribe el usuario.
    """
    estudiante = EstudianteChoiceField(
        queryset=Estudiante.objects.select_related("apoderado").all(),
        label="Estudiante",
    )

    class Meta:
        model = Matricula
        fields = [
            "estudiante",         # desplegable de estudiantes (con su apoderado en la etiqueta)
            "anio_lectivo",       # desplegable de años lectivos
            "grado",              # desplegable de grados
            "estado_matricula",   # VIGENTE / ANULADA / TRASLADADA
        ]


class PensionForm(forms.ModelForm):
    """Formulario de Pensión.

    `monto_final` NO está en `fields`: lo calcula la vista aplicando el
    descuento sobre `monto_base` (Requisito 8).
    """
    matricula = MatriculaChoiceField(
        queryset=Matricula.objects.select_related("estudiante", "anio_lectivo", "grado").all(),
        label="Matrícula",
    )

    class Meta:
        model = Pension
        fields = [
            "matricula",          # desplegable de matrículas (con estudiante/año/grado en la etiqueta)
            "num_cuota",          # número de cuota (1-10)
            "monto_base",         # precio sin descuento
            "fecha_vencimiento",  # con calendario
            "estado_pago",        # PENDIENTE / PAGADA / VENCIDA / ANULADA
            "tipo_descuento",     # desplegable de descuentos (opcional: puede quedar vacío)
        ]
        widgets = {
            "fecha_vencimiento": forms.DateInput(attrs={"type": "date"}),
        }


class PagoForm(forms.ModelForm):
    """Formulario de Pago.

    `fecha_operacion` se redefine a mano (fuera de Meta) para usar el control
    datetime-local del navegador (fecha + hora) y aceptar el formato que este
    envía: "2026-03-10T09:30".
    """
    fecha_operacion = forms.DateTimeField(
        label="Fecha y hora de la operación",
        # widget: input de tipo datetime-local, mostrando el valor en formato AAAA-MM-DDTHH:MM
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        # input_formats: qué formatos de texto acepta Django al recibir el POST
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"],
    )

    pension = PensionChoiceField(
        queryset=Pension.objects.select_related("matricula__estudiante").all(),
        label="Pensión",
    )

    class Meta:
        model = Pago
        fields = [
            "pension",            # desplegable de pensiones (con cuota + estudiante en la etiqueta)
            "num_operacion",      # nro de operación bancaria (único)
            "monto_pagado",
            "fecha_operacion",    # el campo redefinido arriba
            "comprobante_url",    # enlace al voucher (opcional)
            "metodo_pago",        # desplegable de métodos de pago
            "estado_validacion",  # PENDIENTE / APROBADO / RECHAZADO / ANULADO
        ]


class CursoEstudianteForm(forms.ModelForm):
    """Formulario del MODELO INTERMEDIO de la relación N:M Estudiante<->Curso.

    No es un ManyToManyField "de un solo campo": al tener atributos propios
    (nota_final, estado), la inscripción se gestiona como cualquier otra
    entidad con FK, con su propio CRUD. `fecha_inscripcion` no está en
    `fields` porque es `auto_now_add=True` (Django la pone sola al crear).
    """
    class Meta:
        model = CursoEstudiante
        fields = [
            "estudiante",   # desplegable de estudiantes
            "curso",        # desplegable de cursos
            "nota_final",   # opcional: se llena cuando el curso termina
            "estado",       # CURSANDO / APROBADO / DESAPROBADO / RETIRADO
        ]
