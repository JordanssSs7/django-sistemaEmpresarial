"""
Models de la App "Gestión de Citas Médicas" (Semana 3).

A partir de este punto los datos se persisten en SQLite mediante Django ORM
(models.Model + migraciones), reemplazando las listas en memoria que se
usaban en la Semana 2.
"""

from django.db import models


DIAS_SEMANA = [
    ("Lunes", "Lunes"),
    ("Martes", "Martes"),
    ("Miércoles", "Miércoles"),
    ("Jueves", "Jueves"),
    ("Viernes", "Viernes"),
    ("Sábado", "Sábado"),
    ("Domingo", "Domingo"),
]

ESTADOS = [
    ("Programada", "Programada"),
    ("Atendida", "Atendida"),
    ("Cancelada", "Cancelada"),
]


class Especialidad(models.Model):
    """Catálogo de especialidades médicas y su costo de consulta."""

    nombre = models.CharField(max_length=100, unique=True)
    costo = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = "Especialidades"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Profesional(models.Model):
    """Profesional de la salud que atiende citas médicas."""

    nombre = models.CharField(max_length=100)
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name="profesionales",
    )
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} — {self.especialidad}"


class Horario(models.Model):
    """Bloque de atención semanal de un profesional (día + rango de horas)."""

    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.CASCADE,
        related_name="horarios",
    )
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        ordering = ["profesional", "dia_semana", "hora_inicio"]

    def __str__(self):
        return f"{self.profesional.nombre} — {self.dia_semana} {self.hora_inicio}-{self.hora_fin}"


class Cita(models.Model):
    """Cita médica agendada para un paciente con un profesional."""

    paciente = models.CharField(max_length=100)
    documento = models.CharField(max_length=8)
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.PROTECT,
        related_name="citas",
    )
    # Se copia la especialidad del profesional al momento de agendar, para
    # conservar el dato histórico aunque el profesional cambie de especialidad.
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name="citas",
    )
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=12, choices=ESTADOS, default="Programada")
    prioritaria = models.BooleanField(default=False)
    consultorio = models.CharField(max_length=20)
    observaciones = models.TextField(blank=True)
    # Calculado a partir de la especialidad del profesional, no lo ingresa el usuario.
    costo_estimado = models.DecimalField(max_digits=6, decimal_places=2)
    # Trazabilidad: fecha/hora exacta en que se registró la cita.
    agendado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha", "hora"]
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"{self.paciente} — {self.fecha} {self.hora} ({self.estado})"
