"""
Models de la App "Gestión de Matrículas y Pensiones" (Semana 3).

A diferencia de la Semana 2 (datos en memoria), aquí toda la información se
guarda de forma persistente en SQLite mediante el ORM de Django.

Estructura:
- 5 entidades independientes: NivelEducativo, AnioLectivo, TipoDescuento,
  MetodoPago, Apoderado.
- 5 entidades relacionadas por ForeignKey: Grado, Estudiante, Matricula,
  Pension, Pago.
"""

from django.db import models


# ---------------------------------------------------------------------------
# Opciones para los campos de estado
# ---------------------------------------------------------------------------

class EstadoAnio(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"
    CERRADO = "CERRADO", "Cerrado"


class EstadoEstudiante(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"
    INACTIVO = "INACTIVO", "Inactivo"
    RETIRADO = "RETIRADO", "Retirado"


class EstadoMatricula(models.TextChoices):
    VIGENTE = "VIGENTE", "Vigente"
    ANULADA = "ANULADA", "Anulada"
    TRASLADADA = "TRASLADADA", "Trasladada"


class EstadoPension(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    PAGADA = "PAGADA", "Pagada"
    VENCIDA = "VENCIDA", "Vencida"
    ANULADA = "ANULADA", "Anulada"


class EstadoPago(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    APROBADO = "APROBADO", "Aprobado"
    RECHAZADO = "RECHAZADO", "Rechazado"
    ANULADO = "ANULADO", "Anulado"


# ===========================================================================
# ENTIDADES INDEPENDIENTES (sin ForeignKey)
# ===========================================================================

class NivelEducativo(models.Model):
    """Etapa pedagógica del colegio (Inicial, Primaria, Secundaria)."""

    nombre_nivel = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Nivel educativo"
        verbose_name_plural = "Niveles educativos"
        ordering = ["nombre_nivel"]

    def __str__(self):
        return self.nombre_nivel


class AnioLectivo(models.Model):
    """Periodo escolar con sus fechas y costos parametrizados."""

    anio = models.PositiveIntegerField(unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    costo_matricula = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pension = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=10,
        choices=EstadoAnio.choices,
        default=EstadoAnio.ACTIVO,
    )

    class Meta:
        verbose_name = "Año lectivo"
        verbose_name_plural = "Años lectivos"
        ordering = ["-anio"]

    def __str__(self):
        return str(self.anio)


class TipoDescuento(models.Model):
    """Política de descuento sobre la pensión (beca, segundo hermano, etc.)."""

    nombre = models.CharField(max_length=100)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tipo de descuento"
        verbose_name_plural = "Tipos de descuento"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"


class MetodoPago(models.Model):
    """Medio de pago aceptado por la institución."""

    nombre_metodo = models.CharField(max_length=50, unique=True)
    requiere_voucher = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Método de pago"
        verbose_name_plural = "Métodos de pago"
        ordering = ["nombre_metodo"]

    def __str__(self):
        return self.nombre_metodo


class Apoderado(models.Model):
    """Responsable legal y financiero del pago de las pensiones."""

    num_documento = models.CharField(max_length=15, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Apoderado"
        verbose_name_plural = "Apoderados"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


# ===========================================================================
# ENTIDADES RELACIONADAS (con ForeignKey)
# ===========================================================================

class Grado(models.Model):
    """Grado de estudio (1ro, 2do, ...) que pertenece a un nivel educativo."""

    nombre_grado = models.CharField(max_length=50)
    nivel = models.ForeignKey(
        NivelEducativo,
        on_delete=models.PROTECT,
        related_name="grados",
    )

    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
        ordering = ["nivel__nombre_nivel", "nombre_grado"]

    def __str__(self):
        return f"{self.nombre_grado} - {self.nivel.nombre_nivel}"


class Estudiante(models.Model):
    """Expediente del alumno, vinculado a su apoderado."""

    codigo_alumno = models.CharField(max_length=20, unique=True)
    num_documento = models.CharField(max_length=15, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(
        max_length=10,
        choices=EstadoEstudiante.choices,
        default=EstadoEstudiante.ACTIVO,
    )
    apoderado = models.ForeignKey(
        Apoderado,
        on_delete=models.PROTECT,
        related_name="estudiantes",
    )

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.codigo_alumno} - {self.nombres} {self.apellidos}"


class Matricula(models.Model):
    """Inscripción de un estudiante en un año lectivo y grado."""

    fecha_registro = models.DateTimeField(auto_now_add=True)
    costo_matricula = models.DecimalField(max_digits=10, decimal_places=2)
    estado_matricula = models.CharField(
        max_length=12,
        choices=EstadoMatricula.choices,
        default=EstadoMatricula.VIGENTE,
    )
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.PROTECT,
        related_name="matriculas",
    )
    anio_lectivo = models.ForeignKey(
        AnioLectivo,
        on_delete=models.PROTECT,
        related_name="matriculas",
    )
    grado = models.ForeignKey(
        Grado,
        on_delete=models.PROTECT,
        related_name="matriculas",
    )

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        ordering = ["-fecha_registro"]
        unique_together = ("estudiante", "anio_lectivo")

    def __str__(self):
        return f"{self.estudiante} / {self.anio_lectivo}"


class Pension(models.Model):
    """Cuota mensual de pensión asociada a una matrícula."""

    num_cuota = models.PositiveSmallIntegerField()
    monto_base = models.DecimalField(max_digits=10, decimal_places=2)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    estado_pago = models.CharField(
        max_length=10,
        choices=EstadoPension.choices,
        default=EstadoPension.PENDIENTE,
    )
    matricula = models.ForeignKey(
        Matricula,
        on_delete=models.CASCADE,
        related_name="pensiones",
    )
    tipo_descuento = models.ForeignKey(
        TipoDescuento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pensiones",
    )

    class Meta:
        verbose_name = "Pensión"
        verbose_name_plural = "Pensiones"
        ordering = ["matricula", "num_cuota"]
        unique_together = ("matricula", "num_cuota")

    def __str__(self):
        return f"Cuota {self.num_cuota} - {self.matricula}"


class Pago(models.Model):
    """Abono registrado contra una cuota de pensión."""

    fecha_operacion = models.DateTimeField()
    num_operacion = models.CharField(max_length=50, unique=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    comprobante_url = models.URLField(blank=True)
    estado_validacion = models.CharField(
        max_length=10,
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE,
    )
    pension = models.ForeignKey(
        Pension,
        on_delete=models.PROTECT,
        related_name="pagos",
    )
    metodo_pago = models.ForeignKey(
        MetodoPago,
        on_delete=models.PROTECT,
        related_name="pagos",
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ["-fecha_operacion"]

    def __str__(self):
        return f"Pago {self.num_operacion} - S/ {self.monto_pagado}"
