"""
Formularios de la App "Gestión de Citas Médicas".

Todos son `forms.Form` (NO `ModelForm`) porque esta App no tiene un modelo
de base de datos: los datos se guardan en las listas de models.py.
"""

from datetime import date

from django import forms

from . import models


class CitaForm(forms.Form):
    """Registro de una nueva cita.

    Solo incluye los campos que ingresa el usuario. La especialidad se
    deriva del profesional elegido, y el costo estimado y la fecha/hora de
    agendamiento los calcula la vista al procesar el formulario.
    """

    paciente = forms.CharField(
        label="Nombre del paciente",
        max_length=100,
    )
    documento = forms.CharField(
        label="Documento de identidad",
        max_length=8,
        help_text="8 dígitos.",
    )
    profesional = forms.ChoiceField(
        label="Profesional asignado",
        help_text="Solo se listan profesionales disponibles.",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profesional"].choices = [
            (p["id"], f'{p["nombre"]} — {p["especialidad"]}')
            for p in models.profesionales_disponibles()
        ]

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

    def clean(self):
        """Valida que el profesional atienda ese día/hora y que el horario
        no esté ya ocupado por otra cita activa."""
        cleaned_data = super().clean()
        profesional_id = cleaned_data.get("profesional")
        fecha = cleaned_data.get("fecha")
        hora = cleaned_data.get("hora")

        if profesional_id and fecha and hora:
            profesional_id = int(profesional_id)
            if not models.horario_cubre_fecha_hora(profesional_id, fecha, hora):
                raise forms.ValidationError(
                    "El profesional seleccionado no tiene horario de atención "
                    "en ese día y hora. Revisa sus horarios disponibles."
                )
            if models.horario_ocupado(profesional_id, fecha, hora):
                raise forms.ValidationError(
                    "Ese horario ya está ocupado por otra cita activa con el "
                    "mismo profesional. Elige otra fecha u hora."
                )
        return cleaned_data


class ProfesionalForm(forms.Form):
    """Registro de un nuevo profesional de la salud."""

    nombre = forms.CharField(
        label="Nombre completo",
        max_length=100,
    )
    especialidad = forms.ChoiceField(
        label="Especialidad",
        choices=[(e["nombre"], e["nombre"]) for e in models.ESPECIALIDADES],
    )
    disponible = forms.BooleanField(
        label="Disponible para agendar citas",
        required=False,
        initial=True,
    )


class HorarioForm(forms.Form):
    """Registro de un bloque de horario de atención para un profesional."""

    profesional = forms.ChoiceField(label="Profesional")
    dia_semana = forms.ChoiceField(
        label="Día de atención",
        choices=[(d, d) for d in models.DIAS_SEMANA],
    )
    hora_inicio = forms.TimeField(
        label="Hora de inicio",
        widget=forms.TimeInput(attrs={"type": "time"}),
    )
    hora_fin = forms.TimeField(
        label="Hora de fin",
        widget=forms.TimeInput(attrs={"type": "time"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profesional"].choices = [
            (p["id"], p["nombre"]) for p in models.PROFESIONALES
        ]

    def clean(self):
        """Valida que el rango de horas sea válido y que no se solape con
        otro horario ya registrado para el mismo profesional y día."""
        cleaned_data = super().clean()
        profesional_id = cleaned_data.get("profesional")
        dia_semana = cleaned_data.get("dia_semana")
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

        if profesional_id and dia_semana and hora_inicio and hora_fin and hora_inicio < hora_fin:
            if models.hay_solapamiento_horario(int(profesional_id), dia_semana, hora_inicio, hora_fin):
                raise forms.ValidationError(
                    "Ese profesional ya tiene un horario registrado que se cruza "
                    "con este rango en el mismo día."
                )
        return cleaned_data
