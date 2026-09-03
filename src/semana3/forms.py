"""
Formularios de la App "Gestión de Matrículas y Pensiones" (Semana 3).

Se usan ModelForm: Django construye los campos a partir del modelo y, al
llamar form.save(), ejecuta el INSERT / UPDATE mediante el ORM.
"""

from django import forms

from .models import (
    AnioLectivo,
    Apoderado,
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
    class Meta:
        model = NivelEducativo
        fields = ["nombre_nivel", "descripcion"]


class AnioLectivoForm(forms.ModelForm):
    class Meta:
        model = AnioLectivo
        fields = [
            "anio",
            "fecha_inicio",
            "fecha_fin",
            "costo_matricula",
            "monto_pension",
            "estado",
        ]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }


class TipoDescuentoForm(forms.ModelForm):
    class Meta:
        model = TipoDescuento
        fields = ["nombre", "porcentaje", "activo"]


class MetodoPagoForm(forms.ModelForm):
    class Meta:
        model = MetodoPago
        fields = ["nombre_metodo", "requiere_voucher"]


class ApoderadoForm(forms.ModelForm):
    class Meta:
        model = Apoderado
        fields = ["num_documento", "nombres", "apellidos", "telefono", "correo"]


class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        fields = ["nombre_grado", "nivel"]


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = [
            "codigo_alumno",
            "num_documento",
            "nombres",
            "apellidos",
            "fecha_nacimiento",
            "estado",
            "apoderado",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
        }


class MatriculaForm(forms.ModelForm):
    """El costo de matrícula NO se pide: se copia del año lectivo elegido."""

    class Meta:
        model = Matricula
        fields = ["estudiante", "anio_lectivo", "grado", "estado_matricula"]


class PensionForm(forms.ModelForm):
    """El monto_final NO se pide: lo calcula la vista aplicando el descuento."""

    class Meta:
        model = Pension
        fields = [
            "matricula",
            "num_cuota",
            "monto_base",
            "fecha_vencimiento",
            "estado_pago",
            "tipo_descuento",
        ]
        widgets = {
            "fecha_vencimiento": forms.DateInput(attrs={"type": "date"}),
        }


class PagoForm(forms.ModelForm):
    fecha_operacion = forms.DateTimeField(
        label="Fecha y hora de la operación",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"],
    )

    class Meta:
        model = Pago
        fields = [
            "pension",
            "num_operacion",
            "monto_pagado",
            "fecha_operacion",
            "comprobante_url",
            "metodo_pago",
            "estado_validacion",
        ]
