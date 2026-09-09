"""
MODELS de la App "Gestión de Matrículas y Pensiones" (Semana 3).

Un "model" es una clase de Python que Django convierte en una TABLA de la BD:
  - la clase       -> la tabla  (se llama  semana3_<modelo en minúscula>)
  - cada atributo  -> una columna
  - cada instancia -> una fila
  - obj.save()     -> INSERT (si es nuevo) o UPDATE (si ya tiene id)
  - obj.delete()   -> DELETE

A diferencia de la Semana 2 (datos en listas de Python que se perdían al
reiniciar), aquí todo se guarda en SQLite mediante el ORM y persiste.

Estructura: 5 entidades independientes + 5 relacionadas por ForeignKey.
La clave primaria `id` NO se escribe: Django la agrega sola (autoincremental).
"""

from django.db import models  # trae models.Model, los tipos de campo y TextChoices


# ---------------------------------------------------------------------------
# OPCIONES PARA LOS CAMPOS DE ESTADO  (clases TextChoices)
# ---------------------------------------------------------------------------
# Formato de cada línea:   NOMBRE = "valor_guardado_en_BD", "Etiqueta visible"
# - el 1er string se guarda en la base de datos (corto, estable)
# - el 2do string es lo que ve el usuario en el <select> y en las tablas
# Se usan porque: (1) impiden guardar un valor inválido, (2) Django arma el
# <select> solo, (3) {{ obj.get_<campo>_display }} devuelve la etiqueta bonita.

class EstadoAnio(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"      # año escolar abierto, se puede matricular
    CERRADO = "CERRADO", "Cerrado"   # año finalizado, solo lectura


class EstadoEstudiante(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"          # estudia normalmente
    INACTIVO = "INACTIVO", "Inactivo"    # suspendido temporalmente
    RETIRADO = "RETIRADO", "Retirado"    # se fue del colegio (baja lógica, no se borra)


class EstadoMatricula(models.TextChoices):
    VIGENTE = "VIGENTE", "Vigente"           # matrícula activa este año
    ANULADA = "ANULADA", "Anulada"           # se dejó sin efecto
    TRASLADADA = "TRASLADADA", "Trasladada"  # el alumno pasó a otra sección/colegio


class EstadoPension(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"  # cuota aún no pagada
    PAGADA = "PAGADA", "Pagada"           # cuota cancelada y validada
    VENCIDA = "VENCIDA", "Vencida"        # pasó su fecha de vencimiento sin pago
    ANULADA = "ANULADA", "Anulada"        # cuota dejada sin efecto


class EstadoPago(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"    # tesorería aún no revisa el voucher
    APROBADO = "APROBADO", "Aprobado"       # voucher válido -> la pensión pasa a "Pagada"
    RECHAZADO = "RECHAZADO", "Rechazado"    # voucher inválido -> la pensión vuelve a "Pendiente"
    ANULADO = "ANULADO", "Anulado"          # pago registrado por error


# ===========================================================================
# ENTIDADES INDEPENDIENTES  (no tienen ForeignKey a ninguna otra entidad)
# ===========================================================================

class NivelEducativo(models.Model):
    """Etapa pedagógica del colegio (Inicial, Primaria, Secundaria)."""

    # CharField = texto corto (VARCHAR). max_length es obligatorio.
    # unique=True -> la BD rechaza dos niveles con el mismo nombre.
    nombre_nivel = models.CharField(max_length=50, unique=True)
    # TextField = texto largo sin límite. blank=True -> el formulario lo permite vacío.
    descripcion = models.TextField(blank=True)

    class Meta:                                  # configuración del modelo (no son columnas)
        verbose_name = "Nivel educativo"         # nombre en singular para el /admin/
        verbose_name_plural = "Niveles educativos"  # nombre en plural (sin esto diría "Niveleducativos")
        ordering = ["nombre_nivel"]              # orden por defecto: alfabético por nombre

    def __str__(self):                           # cómo se muestra el objeto (admin, <select>, plantillas)
        return self.nombre_nivel


class AnioLectivo(models.Model):
    """Periodo escolar con sus fechas y costos parametrizados (Requisito 5)."""

    anio = models.PositiveIntegerField(unique=True)   # entero >= 0; no puede repetirse el año
    fecha_inicio = models.DateField()                 # DATE: día de inicio de clases
    fecha_fin = models.DateField()                    # DATE: día de fin de clases
    # DecimalField para dinero: exacto (float tendría errores de redondeo).
    # max_digits=10, decimal_places=2 -> hasta 99 999 999.99
    costo_matricula = models.DecimalField(max_digits=10, decimal_places=2)  # se paga una vez
    monto_pension = models.DecimalField(max_digits=10, decimal_places=2)    # base de cada cuota mensual
    estado = models.CharField(
        max_length=10,
        choices=EstadoAnio.choices,   # solo acepta ACTIVO / CERRADO
        default=EstadoAnio.ACTIVO,    # valor por defecto si no se indica
    )

    class Meta:
        verbose_name = "Año lectivo"
        verbose_name_plural = "Años lectivos"
        ordering = ["-anio"]          # el "-" = descendente: 2026 aparece antes que 2025

    def __str__(self):
        return str(self.anio)        # se muestra solo el número del año


class TipoDescuento(models.Model):
    """Política de descuento sobre la pensión (beca, segundo hermano, pronto pago)."""

    nombre = models.CharField(max_length=100)                          # nombre de la política
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)   # ej. 15.00 (%)
    activo = models.BooleanField(default=True)                         # se desactiva sin borrar (Requisito 9)

    class Meta:
        verbose_name = "Tipo de descuento"
        verbose_name_plural = "Tipos de descuento"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"   # ej. "Segundo hermano (15.00%)"


class MetodoPago(models.Model):
    """Medio de pago aceptado por la institución (transferencia, ventanilla, etc.)."""

    nombre_metodo = models.CharField(max_length=50, unique=True)   # no repetir métodos
    requiere_voucher = models.BooleanField(default=False)          # True -> exige subir comprobante

    class Meta:
        verbose_name = "Método de pago"
        verbose_name_plural = "Métodos de pago"
        ordering = ["nombre_metodo"]

    def __str__(self):
        return self.nombre_metodo


class Apoderado(models.Model):
    """Responsable legal y financiero del pago de las pensiones.

    Es el lado "1" de la relación 1:N con Estudiante (una familia, varios hijos).
    """

    num_documento = models.CharField(max_length=15, unique=True)   # DNI/CE: identifica al apoderado
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)         # opcional
    correo = models.EmailField(blank=True)                         # EmailField valida el formato "algo@algo"

    class Meta:
        verbose_name = "Apoderado"
        verbose_name_plural = "Apoderados"
        ordering = ["apellidos", "nombres"]   # orden tipo lista de asistencia

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


# ===========================================================================
# ENTIDADES RELACIONADAS  (tienen ForeignKey)
# ---------------------------------------------------------------------------
# ForeignKey(Otro, ...) crea físicamente una columna "<campo>_id" que guarda
# el id de una fila de la tabla "Otro". Es una relación muchos-a-uno.
#
# on_delete = qué hacer con los "hijos" cuando se borra el "padre":
#     PROTECT   -> impide borrar el padre si tiene hijos (lanza ProtectedError)
#     CASCADE   -> al borrar el padre, se borran también los hijos
#     SET_NULL  -> al borrar el padre, la columna del hijo queda en NULL
#
# related_name = "camino de vuelta": desde el padre se llega a los hijos, p. ej.
#     apoderado.estudiantes.all()   /   matricula.pensiones.all()
# ===========================================================================

class Grado(models.Model):
    """Grado de estudio (1ro, 2do, ...) que pertenece a un nivel educativo."""

    nombre_grado = models.CharField(max_length=50)   # ej. "1ro de Primaria"
    nivel = models.ForeignKey(
        NivelEducativo,               # apunta a la tabla NivelEducativo (crea columna nivel_id)
        on_delete=models.PROTECT,     # no dejar borrar un nivel que tiene grados
        related_name="grados",        # permite hacer  nivel.grados.all()
    )

    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
        # "__" navega la relación: ordena por el nombre del nivel y luego por el del grado
        ordering = ["nivel__nombre_nivel", "nombre_grado"]

    def __str__(self):
        return f"{self.nombre_grado} - {self.nivel.nombre_nivel}"   # "1ro de Primaria - Primaria"


class Estudiante(models.Model):
    """Expediente del alumno, vinculado a su apoderado."""

    codigo_alumno = models.CharField(max_length=20, unique=True)   # código interno del colegio
    num_documento = models.CharField(max_length=15, unique=True)   # DNI del alumno
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(
        max_length=10,
        choices=EstadoEstudiante.choices,     # ACTIVO / INACTIVO / RETIRADO
        default=EstadoEstudiante.ACTIVO,      # al crearlo, entra como "Activo"
    )
    apoderado = models.ForeignKey(
        Apoderado,                   # cada estudiante pertenece a un apoderado (columna apoderado_id)
        on_delete=models.PROTECT,    # Requisito 4: conservar historial, no borrar en cascada
        related_name="estudiantes",  # apoderado.estudiantes.all() -> los hijos de esa familia
    )

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.codigo_alumno} - {self.nombres} {self.apellidos}"


# ---------------------------------------------------------------------------
# RELACIÓN 1:1 (Semana 4, Ejercicio 2)
# ---------------------------------------------------------------------------
# OneToOneField = un ForeignKey con unique=True agregado por Django: como
# máximo un FichaMedica por Estudiante. Es la "ficha complementaria": datos
# de salud que no todo Estudiante necesariamente tiene llenos, y que no
# tendría sentido guardar como columnas sueltas en la tabla principal.

class FichaMedica(models.Model):
    """Información médica complementaria de un estudiante (a lo sumo una)."""

    estudiante = models.OneToOneField( #<---------
        Estudiante,
        on_delete=models.CASCADE,       # es una extensión de Estudiante: si se borra
                                         # el estudiante, su ficha médica no tiene
                                         # razón de existir por separado.
        related_name="ficha_medica",    # acceso inverso: estudiante.ficha_medica
    )
    tipo_sangre = models.CharField(max_length=5, blank=True)     # ej. "O+"
    alergias = models.TextField(blank=True)
    contacto_emergencia_nombre = models.CharField(max_length=150)
    contacto_emergencia_telefono = models.CharField(max_length=20)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Ficha médica"
        verbose_name_plural = "Fichas médicas"

    def __str__(self):
        return f"Ficha médica de {self.estudiante}"


class TipoObservacion(models.TextChoices):
    ACADEMICA = "ACADEMICA", "Académica"
    CONDUCTUAL = "CONDUCTUAL", "Conductual"
    ADMINISTRATIVA = "ADMINISTRATIVA", "Administrativa"


# ---------------------------------------------------------------------------
# RELACIÓN 1:N (Semana 4, Ejercicio 3)
# ---------------------------------------------------------------------------
# Un Estudiante puede tener muchas Observaciones a lo largo del tiempo, pero
# cada Observacion pertenece a un único Estudiante. Por eso:
#   - Estudiante  = lado "1"  (el que es referenciado)
#   - Observacion = lado "N"  (el que tiene muchos registros por cada Estudiante)
# La ForeignKey se declara en el lado "N" (Observacion) porque es ahí donde
# físicamente se necesita la columna extra (estudiante_id) para poder repetir
# el mismo estudiante en varias filas; el lado "1" no necesita ninguna columna
# nueva, solo gana el acceso inverso a través del related_name.

class Observacion(models.Model):
    """Nota académica, conductual o administrativa registrada sobre un
    estudiante. Un mismo estudiante puede acumular muchas a lo largo del año."""

    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,      # son notas internas del expediente, sin valor
                                        # legal/financiero propio: si se borra el
                                        # estudiante, sus observaciones no tienen
                                        # ningún sentido guardadas por separado.
        related_name="observaciones",  # acceso inverso: estudiante.observaciones.all()
    )
    fecha = models.DateField(auto_now_add=True)
    tipo = models.CharField(
        max_length=15,
        choices=TipoObservacion.choices,
        default=TipoObservacion.ACADEMICA,
    )
    descripcion = models.TextField()

    class Meta:
        verbose_name = "Observación"
        verbose_name_plural = "Observaciones"
        ordering = ["-fecha"]

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.estudiante} — {self.fecha}"


class Matricula(models.Model):
    """Inscripción de un estudiante en un año lectivo y grado."""

    # auto_now_add=True -> pone la fecha/hora del momento de CREAR y nunca la vuelve a cambiar
    fecha_registro = models.DateTimeField(auto_now_add=True)
    # "Foto" del costo al momento de matricular (la vista lo copia del año lectivo,
    # así aunque el año cambie de precio, la matrícula guarda el que se cobró).
    costo_matricula = models.DecimalField(max_digits=10, decimal_places=2)
    estado_matricula = models.CharField(
        max_length=12,
        choices=EstadoMatricula.choices,       # VIGENTE / ANULADA / TRASLADADA
        default=EstadoMatricula.VIGENTE,
    )
    # Tres ForeignKey: una matrícula relaciona un estudiante + un año + un grado.
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.PROTECT, related_name="matriculas",
    )
    anio_lectivo = models.ForeignKey(
        AnioLectivo, on_delete=models.PROTECT, related_name="matriculas",
    )
    grado = models.ForeignKey(
        Grado, on_delete=models.PROTECT, related_name="matriculas",
    )

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        ordering = ["-fecha_registro"]     # las más recientes primero
        # unique_together: la COMBINACIÓN de esas dos columnas debe ser única
        # -> un estudiante no puede matricularse dos veces en el mismo año.
        unique_together = ("estudiante", "anio_lectivo")

    def __str__(self):
        return f"{self.estudiante} / {self.anio_lectivo}"


class Pension(models.Model):
    """Cuota mensual de pensión asociada a una matrícula.

    Las 10 cuotas se crean automáticamente en la vista `matricula_crear`.
    """

    num_cuota = models.PositiveSmallIntegerField()   # número de cuota: 1 a 10
    monto_base = models.DecimalField(max_digits=10, decimal_places=2)   # precio sin descuento
    # monto_final lo calcula la vista: monto_base menos el descuento (Requisito 8).
    monto_final = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()           # último día para pagar sin mora
    estado_pago = models.CharField(
        max_length=10,
        choices=EstadoPension.choices,    # PENDIENTE / PAGADA / VENCIDA / ANULADA
        default=EstadoPension.PENDIENTE,  # toda cuota nace pendiente
    )
    matricula = models.ForeignKey(
        Matricula,
        on_delete=models.CASCADE,     # si se borra la matrícula, sus 10 cuotas se borran también
        related_name="pensiones",     # matricula.pensiones.all()
    )
    tipo_descuento = models.ForeignKey(
        TipoDescuento,
        on_delete=models.SET_NULL,    # si se borra el descuento, esta columna queda en NULL
        null=True,                    # la columna admite NULL en la base de datos
        blank=True,                   # el formulario permite dejar el campo vacío
        related_name="pensiones",
    )

    class Meta:
        verbose_name = "Pensión"
        verbose_name_plural = "Pensiones"
        ordering = ["matricula", "num_cuota"]        # agrupadas por matrícula, en orden de cuota
        # no puede haber dos cuotas "número 3" para la misma matrícula
        unique_together = ("matricula", "num_cuota")

    def __str__(self):
        return f"Cuota {self.num_cuota} - {self.matricula}"


class Pago(models.Model):
    """Abono registrado contra una cuota de pensión (Requisito 10)."""

    fecha_operacion = models.DateTimeField()                       # cuándo se hizo la transferencia
    num_operacion = models.CharField(max_length=50, unique=True)   # nro de operación del banco (irrepetible)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    comprobante_url = models.URLField(blank=True)                  # enlace al voucher (valida formato URL)
    estado_validacion = models.CharField(
        max_length=10,
        choices=EstadoPago.choices,       # PENDIENTE / APROBADO / RECHAZADO / ANULADO
        default=EstadoPago.PENDIENTE,     # entra pendiente de revisión por tesorería
    )
    pension = models.ForeignKey(
        Pension, on_delete=models.PROTECT, related_name="pagos",   # PROTECT: no perder registros de dinero
    )
    metodo_pago = models.ForeignKey(
        MetodoPago, on_delete=models.PROTECT, related_name="pagos",
    )
    # cuándo se registró en el sistema (distinto de fecha_operacion, que es la del banco)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ["-fecha_operacion"]   # los pagos más recientes primero

    def __str__(self):
        return f"Pago {self.num_operacion} - S/ {self.monto_pagado}"
