"""
Formulario de registro de citas médicas.

Se usa `forms.Form` (NO `ModelForm`) porque esta App no tiene un modelo de
base de datos: los datos se guardan en la lista `CITAS` de models.py.

Solo se incluyen los campos que ingresa el usuario. El costo estimado y la
fecha/hora de agendamiento los calcula la vista al procesar el formulario.
"""

from datetime import date

from django import forms

from . import models


class CitaForm(forms.Form):
    paciente = forms.CharField(
        label="Nombre del paciente",
        max_length=100,
    )
    documento = forms.CharField(
        label="Documento de identidad",
        max_length=8,
        help_text="8 dígitos.",
    )
    medico = forms.CharField(
        label="Médico asignado",
        max_length=100,
    )
    especialidad = forms.ChoiceField(
        label="Especialidad",
        choices=[(e["nombre"], e["nombre"]) for e in models.ESPECIALIDADES],
    )
    fecha = forms.DateField(
        label="Fecha de la cita",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    hora = forms.TimeField(
        label="Hora de la cita",
        widget=forms.TimeInput(attrs={"type": "time"}),
    )
    estado = forms.ChoiceField(
        label="Estado inicial",
        choices=[(e, e) for e in models.ESTADOS],
    )
    prioritaria = forms.BooleanField(
        label="¿Requiere atención prioritaria? (adulto mayor, gestante, emergencia)",
        required=False,
    )
    consultorio = forms.CharField(
        label="Consultorio / ambiente",
        max_length=20,
    )
    observaciones = forms.CharField(
        label="Observaciones / motivo de consulta",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    def clean_documento(self):
        """El documento debe tener exactamente 8 dígitos numéricos."""
        documento = self.cleaned_data["documento"].strip()
        if not documento.isdigit():
            raise forms.ValidationError("El documento debe contener solo números.")
        if len(documento) != 8:
            raise forms.ValidationError("El documento debe tener 8 dígitos.")
        return documento

    def clean_fecha(self):
        """No se permite agendar una cita en una fecha ya pasada."""
        fecha = self.cleaned_data["fecha"]
        if fecha < date.today():
            raise forms.ValidationError("La fecha de la cita no puede estar en el pasado.")
        return fecha
