# ===========================================================================
# VISTAS (VIEWS) de la App "Gestión de Matrículas y Pensiones" (Semana 3)
# ---------------------------------------------------------------------------
# Una vista es una función que recibe `request` (la petición HTTP) y devuelve
# una respuesta: HTML con render(), o una redirección con redirect().
# `urls.py` decide qué vista se ejecuta para cada URL.
#
# Por cada entidad hay 4 vistas -> listar (READ), crear (CREATE),
# editar (UPDATE) y eliminar (DELETE). Todas repiten el mismo patrón.
#
# Equivalencia ORM -> SQL:
#   Modelo.objects.all()              -> SELECT * FROM ...
#   .filter(campo=valor)              -> ... WHERE campo = valor
#   .order_by("campo")                -> ... ORDER BY campo
#   form.save()  (objeto nuevo)       -> INSERT INTO ...
#   form.save()  (con instance=obj)   -> UPDATE ... WHERE id = ?
#   objeto.delete()                   -> DELETE FROM ... WHERE id = ?
# ===========================================================================

import calendar                # calendar.monthrange(anio, mes) -> (dia_semana_del_1, nro_de_dias)
from datetime import date      # para construir fechas: date(2026, 3, 1)
from decimal import Decimal    # aritmética exacta de dinero (float da errores de redondeo)

from django.contrib import messages                     # avisos "flash": se ven en la página siguiente
from django.db.models import Q                          # permite combinar condiciones con OR en filter()
from django.db.models.deletion import ProtectedError    # excepción al borrar un objeto con on_delete=PROTECT
from django.shortcuts import get_object_or_404, redirect, render
#   render(request, plantilla, contexto) -> combina HTML + datos y devuelve la respuesta
#   redirect("app:name")                 -> HTTP 302 hacia otra URL
#   get_object_or_404(Modelo, pk=pk)     -> Modelo.objects.get(pk=pk); si no existe -> página 404

# Formularios (uno por entidad): construyen el formulario web a partir del modelo.
from .forms import (
    AnioLectivoForm,
    ApoderadoForm,
    EstudianteForm,
    GradoForm,
    MatriculaForm,
    MetodoPagoForm,
    NivelEducativoForm,
    PagoForm,
    PensionForm,
    TipoDescuentoForm,
)
# Modelos (las 10 tablas) + las clases de estado (opciones de los campos `estado`).
from .models import (
    AnioLectivo,
    Apoderado,
    Curso,
    EstadoEstudiante,
    EstadoMatricula,
    EstadoPago,
    EstadoPension,
    Estudiante,
    Grado,
    Matricula,
    MetodoPago,
    NivelEducativo,
    Pago,
    Pension,
    TipoDescuento,
)


# ---------------------------------------------------------------------------
# FUNCIONES AUXILIARES  (el prefijo "_" indica "uso interno del archivo")
# ---------------------------------------------------------------------------

def _sumar_meses(fecha, n):
    """Devuelve `fecha` desplazada `n` meses hacia adelante.

    Se usa para el vencimiento de cada cuota: cuota 1 = mes de inicio,
    cuota 2 = +1 mes, ... , cuota 10 = +9 meses.
    """
    mes = fecha.month - 1 + n                       # mes en base 0 (enero=0) + n meses
    anio = fecha.year + mes // 12                   # cada 12 meses acumulados = +1 año
    mes = mes % 12 + 1                              # vuelve a base 1 (rango 1..12)
    ultimo_dia = calendar.monthrange(anio, mes)[1]  # cuántos días tiene ese mes (28/29/30/31)
    # min(...): si el día original no cabe (ej. 31 -> febrero), lo recorta al último válido
    return date(anio, mes, min(fecha.day, ultimo_dia))


def _calcular_monto_final(pension):
    """Requisito 8: monto_final = monto_base menos el descuento (si aplica).

    Está en una función aparte porque la usan pension_crear y pension_editar
    (así la fórmula no se duplica y no se puede desincronizar).
    """
    if pension.tipo_descuento:                                  # ¿la pensión tiene un descuento asociado?
        # factor = 1 - (porcentaje/100). Ej. 15% -> 1 - 0.15 = 0.85
        factor = Decimal("1") - (pension.tipo_descuento.porcentaje / Decimal("100"))
        # monto_base * factor, redondeado a 2 decimales. Ej. 280 * 0.85 = 238.00
        return (pension.monto_base * factor).quantize(Decimal("0.01"))
    return pension.monto_base                                   # sin descuento -> igual al base


def _eliminar(request, objeto, ruta_lista, nombre):
    """Flujo común de DELETE, reutilizado por las 10 entidades.

    GET  -> muestra la confirmación (no borra).
    POST -> ejecuta objeto.delete(). Si el objeto está protegido
            (on_delete=PROTECT con hijos), captura ProtectedError y avisa.
    Nunca se borra con un GET (regla de seguridad y del enunciado).
    """
    if request.method == "POST":                    # el usuario confirmó el borrado
        try:
            objeto.delete()                         # -> DELETE FROM semana3_<tabla> WHERE id = ?
            messages.success(request, f"{nombre} eliminado correctamente.")
        except ProtectedError:                      # tiene registros hijos con on_delete=PROTECT
            messages.error(
                request,
                f"No se puede eliminar: {nombre.lower()} tiene registros asociados.",
            )
        return redirect(ruta_lista)                 # en ambos casos, vuelve al listado
    # GET -> pinta la página "¿está seguro de eliminar X?"
    return render(request, "semana3/confirm_delete.html", {
        "objeto": objeto,                           # el registro a borrar (se muestra en la confirmación)
        "nombre": nombre,                           # etiqueta legible ("Estudiante", "Pensión", ...)
        "volver": ruta_lista,                       # a dónde apunta el botón "Cancelar"
    })


def index(request):
    """Página de inicio del módulo (/semana3/): solo el menú, no consulta la BD."""
    return render(request, "semana3/index.html")


# ---------------------------------------------------------------------------
# Nivel educativo  (entidad independiente, sin ForeignKey)
# ---------------------------------------------------------------------------

def nivel_list(request):
    """READ: lista todos los niveles educativos."""
    niveles = NivelEducativo.objects.all()   # QuerySet -> SELECT * FROM semana3_niveleducativo
    #                                          (perezoso: la consulta corre al recorrerlo en la plantilla)
    return render(request, "semana3/nivel_list.html", {"niveles": niveles})   # pasa los datos al HTML


def nivel_crear(request):
    """CREATE: GET muestra el formulario vacío; POST valida y hace INSERT."""
    if request.method == "POST":                      # (2) el usuario envió el formulario
        form = NivelEducativoForm(request.POST)       # (3) form con los datos recibidos
        if form.is_valid():                           # (4) valida tipos, max_length, unique, obligatorios
            form.save()                               # (5) -> INSERT INTO semana3_niveleducativo (...)
            messages.success(request, "Nivel educativo registrado correctamente.")  # (6) aviso
            return redirect("semana3:nivel_list")     # (7) Post/Redirect/Get: evita duplicar al recargar
        # si NO es válido: no entra al if, cae al render y muestra los errores
    else:                                             # (1) primera visita a la página (GET)
        form = NivelEducativoForm()                   #     formulario en blanco
    return render(request, "semana3/form.html", {     # (8) pinta el formulario
        "form": form,
        "titulo": "Nuevo nivel educativo",            # texto del <h2>
        "volver": "semana3:nivel_list",               # ruta del botón "Cancelar"
    })


def nivel_editar(request, pk):
    """UPDATE: recupera el objeto por su pk, precarga el form y hace UPDATE."""
    nivel = get_object_or_404(NivelEducativo, pk=pk)      # (A) SELECT ... WHERE id = pk (o 404)
    if request.method == "POST":
        # instance=nivel -> el form aplica los cambios SOBRE ese objeto (no crea uno nuevo)
        form = NivelEducativoForm(request.POST, instance=nivel)
        if form.is_valid():
            form.save()                                  # (C) -> UPDATE ... SET ... WHERE id = pk
            messages.success(request, "Nivel educativo actualizado correctamente.")
            return redirect("semana3:nivel_list")
    else:
        form = NivelEducativoForm(instance=nivel)         # (D) form PRECARGADO con los valores actuales
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": f"Editar nivel: {nivel}",
        "volver": "semana3:nivel_list",
    })


# ---------------------------------------------------------------------------
# Año lectivo  (entidad independiente)
# ---------------------------------------------------------------------------

def anio_list(request):
    """READ: lista los años lectivos (orden por año desc. según Meta.ordering)."""
    anios = AnioLectivo.objects.all()                 # SELECT * FROM semana3_aniolectivo
    return render(request, "semana3/anio_list.html", {"anios": anios})


def anio_crear(request):
    """CREATE de año lectivo (Requisito 5). Mismo patrón que nivel_crear."""
    if request.method == "POST":
        form = AnioLectivoForm(request.POST)          # form con los datos enviados
        if form.is_valid():
            form.save()                               # INSERT
            messages.success(request, "Año lectivo registrado correctamente.")
            return redirect("semana3:anio_list")
    else:
        form = AnioLectivoForm()                      # form vacío
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo año lectivo",
        "volver": "semana3:anio_list",
    })


def anio_editar(request, pk):
    """UPDATE de año lectivo."""
    anio = get_object_or_404(AnioLectivo, pk=pk)      # trae el registro existente
    if request.method == "POST":
        form = AnioLectivoForm(request.POST, instance=anio)   # aplica cambios sobre ese objeto
        if form.is_valid():
            form.save()                               # UPDATE
            messages.success(request, "Año lectivo actualizado correctamente.")
            return redirect("semana3:anio_list")
    else:
        form = AnioLectivoForm(instance=anio)         # form precargado
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": f"Editar año lectivo {anio}",
        "volver": "semana3:anio_list",
    })


# ---------------------------------------------------------------------------
# Tipo de descuento  (entidad independiente)
# ---------------------------------------------------------------------------

def descuento_list(request):
    """READ con filtro opcional por el campo `activo` (Requisito 9).

    El filtro llega por la URL: /descuentos/?activo=1
    """
    activo = request.GET.get("activo", "")            # lee ?activo=...  ("" si no viene)
    descuentos = TipoDescuento.objects.all()          # base: todos los descuentos
    if activo == "1":
        descuentos = descuentos.filter(activo=True)   # -> WHERE activo = 1
    elif activo == "0":
        descuentos = descuentos.filter(activo=False)  # -> WHERE activo = 0
    descuentos = descuentos.order_by("nombre")        # -> ORDER BY nombre
    return render(request, "semana3/descuento_list.html", {
        "descuentos": descuentos,
        "f_activo": activo,                           # se devuelve para marcar el filtro activo en el HTML
    })


def descuento_crear(request):
    """CREATE de tipo de descuento (Requisito 8)."""
    if request.method == "POST":
        form = TipoDescuentoForm(request.POST)
        if form.is_valid():
            form.save()                               # INSERT
            messages.success(request, "Tipo de descuento registrado correctamente.")
            return redirect("semana3:descuento_list")
    else:
        form = TipoDescuentoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo tipo de descuento",
        "volver": "semana3:descuento_list",
    })


def descuento_editar(request, pk):
    """UPDATE de tipo de descuento: cambiar porcentaje o desactivarlo (Requisito 8)."""
    descuento = get_object_or_404(TipoDescuento, pk=pk)
    if request.method == "POST":
        form = TipoDescuentoForm(request.POST, instance=descuento)
        if form.is_valid():
            form.save()                               # UPDATE
            messages.success(request, "Tipo de descuento actualizado correctamente.")
            return redirect("semana3:descuento_list")
    else:
        form = TipoDescuentoForm(instance=descuento)
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": f"Editar descuento: {descuento.nombre}",
        "volver": "semana3:descuento_list",
    })


# ---------------------------------------------------------------------------
# Método de pago  (entidad independiente)
# ---------------------------------------------------------------------------

def metodo_list(request):
    """READ: lista los métodos de pago."""
    metodos = MetodoPago.objects.all()               # SELECT * FROM semana3_metodopago
    return render(request, "semana3/metodo_list.html", {"metodos": metodos})


def metodo_crear(request):
    """CREATE de método de pago."""
    if request.method == "POST":
        form = MetodoPagoForm(request.POST)
        if form.is_valid():
            form.save()                               # INSERT
            messages.success(request, "Método de pago registrado correctamente.")
            return redirect("semana3:metodo_list")
    else:
        form = MetodoPagoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo método de pago",
        "volver": "semana3:metodo_list",
    })


def metodo_editar(request, pk):
    """UPDATE de método de pago."""
    metodo = get_object_or_404(MetodoPago, pk=pk)
    if request.method == "POST":
        form = MetodoPagoForm(request.POST, instance=metodo)
        if form.is_valid():
            form.save()                               # UPDATE
            messages.success(request, "Método de pago actualizado correctamente.")
            return redirect("semana3:metodo_list")
    else:
        form = MetodoPagoForm(instance=metodo)
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": f"Editar método: {metodo.nombre_metodo}",
        "volver": "semana3:metodo_list",
    })


# ---------------------------------------------------------------------------
# Apoderado  (entidad independiente; es el "1" de la relación con Estudiante)
# ---------------------------------------------------------------------------

def apoderado_list(request):
    """READ: lista los apoderados."""
    apoderados = Apoderado.objects.all()             # SELECT * FROM semana3_apoderado
    return render(request, "semana3/apoderado_list.html", {"apoderados": apoderados})


def apoderado_crear(request):
    """CREATE de apoderado (Requisito 1)."""
    if request.method == "POST":
        form = ApoderadoForm(request.POST)
        if form.is_valid():
            form.save()                               # INSERT
            messages.success(request, "Apoderado registrado correctamente.")
            return redirect("semana3:apoderado_list")
    else:
        form = ApoderadoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo apoderado",
        "volver": "semana3:apoderado_list",
    })


def apoderado_editar(request, pk):
    """UPDATE de apoderado: actualizar datos de contacto (Requisito 3)."""
    apoderado = get_object_or_404(Apoderado, pk=pk)
    if request.method == "POST":
        form = ApoderadoForm(request.POST, instance=apoderado)
        if form.is_valid():
            form.save()                               # UPDATE
            messages.success(request, "Apoderado actualizado correctamente.")
            return redirect("semana3:apoderado_list")
    else:
        form = ApoderadoForm(instance=apoderado)
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": f"Editar apoderado: {apoderado}",
        "volver": "semana3:apoderado_list",
    })


# ---------------------------------------------------------------------------
# Grado  (entidad relacionada: ForeignKey -> NivelEducativo)
# ---------------------------------------------------------------------------

def grado_list(request):
    """READ: lista los grados junto con su nivel.

    select_related("nivel") trae el nivel en el MISMO SELECT (con JOIN); sin
    esto, la plantilla haría un SELECT extra por cada grado (problema N+1).
    """
    grados = Grado.objects.select_related("nivel").all()   # SELECT ... JOIN semana3_niveleducativo
    return render(request, "semana3/grado_list.html", {"grados": grados})


def grado_crear(request):
    """CREATE de grado. El campo `nivel` (FK) se muestra como un <select> automático."""
    if request.method == "POST":
        form = GradoForm(request.POST)
        if form.is_valid():
            form.save()                               # INSERT (guarda nivel_id con el nivel elegido)
            messages.success(request, "Grado registrado correctamente.")
            return redirect("semana3:grado_list")
    else:
        form = GradoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo grado",
        "volver": "semana3:grado_list",
    })


def grado_editar(request, pk):
    """UPDATE de grado."""
    grado = get_object_or_404(Grado, pk=pk)
    if request.method == "POST":
        form = GradoForm(request.POST, instance=grado)
        if form.is_valid():
            form.save()                               # UPDATE
            messages.success(request, "Grado actualizado correctamente.")
            return redirect("semana3:grado_list")
    else:
        form = GradoForm(instance=grado)
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": f"Editar grado: {grado.nombre_grado}",
        "volver": "semana3:grado_list",
    })


# ---------------------------------------------------------------------------
# Estudiante  (entidad relacionada: ForeignKey -> Apoderado)
# ---------------------------------------------------------------------------

def estudiante_list(request):
    """READ con filtros (Requisito 2): estado, año lectivo, grado y búsqueda de texto."""
    estado = request.GET.get("estado", "")           # filtro por campo directo del estudiante
    anio = request.GET.get("anio", "")               # filtro a través de la matrícula
    grado = request.GET.get("grado", "")             # filtro a través de la matrícula
    q = request.GET.get("q", "").strip()             # texto libre de búsqueda (.strip() quita espacios)

    # select_related("apoderado"): JOIN para traer el apoderado y evitar el problema N+1.
    estudiantes = Estudiante.objects.select_related("apoderado").all()
    if estado:
        estudiantes = estudiantes.filter(estado=estado)                    # WHERE estado = ?
    if anio:
        # "matriculas" es el related_name; "__" navega la relación hasta la FK de la matrícula
        estudiantes = estudiantes.filter(matriculas__anio_lectivo_id=anio) # JOIN matricula + WHERE
    if grado:
        estudiantes = estudiantes.filter(matriculas__grado_id=grado)
    if q:
        # Q(...) | Q(...): el "|" significa OR. __icontains -> LIKE '%q%' sin distinguir mayúsculas.
        estudiantes = estudiantes.filter(
            Q(nombres__icontains=q)
            | Q(apellidos__icontains=q)
            | Q(num_documento__icontains=q)
            | Q(codigo_alumno__icontains=q)
        )
    # .distinct(): el JOIN con matrículas podría repetir un estudiante con varias matrículas
    estudiantes = estudiantes.distinct().order_by("apellidos", "nombres")

    return render(request, "semana3/estudiante_list.html", {
        "estudiantes": estudiantes,
        "estados": EstadoEstudiante.choices,         # opciones para el <select> de estado en el HTML
        "anios": AnioLectivo.objects.all(),          # opciones para el <select> de año
        "grados": Grado.objects.select_related("nivel").all(),  # opciones para el <select> de grado
        "f_estado": estado,                          # valores activos -> para dejar el filtro marcado
        "f_anio": anio,
        "f_grado": grado,
        "q": q,
    })


def estudiante_crear(request):
    """CREATE de estudiante (Requisito 1). El campo `apoderado` es un <select>."""
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()                               # INSERT (guarda apoderado_id)
            messages.success(request, "Estudiante registrado correctamente.")
            return redirect("semana3:estudiante_list")
    else:
        form = EstudianteForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo estudiante",
        "volver": "semana3:estudiante_list",
    })


def estudiante_editar(request, pk):
    """UPDATE de estudiante (Requisitos 3 y 4).

    Sirve para actualizar datos y también para cambiar el `estado` a
    "Inactivo"/"Retirado" (baja lógica: no se borra el registro, se marca).
    """
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == "POST":
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()                               # UPDATE
            messages.success(request, "Estudiante actualizado correctamente.")
            return redirect("semana3:estudiante_list")
    else:
        form = EstudianteForm(instance=estudiante)
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": f"Editar estudiante: {estudiante.nombres} {estudiante.apellidos}",
        "volver": "semana3:estudiante_list",
    })


# ---------------------------------------------------------------------------
# Semana 4, Ejercicio 6 — consultar las relaciones nuevas desde la View
# ---------------------------------------------------------------------------

def estudiante_detalle(request, pk):
    """Usa select_related() para la relación 1:1: trae en una sola consulta
    (con JOIN) al estudiante junto con su apoderado (FK) y su ficha médica
    (OneToOne inverso) - select_related() sirve para relaciones "a lo sumo
    un objeto" (FK y OneToOne), tanto hacia adelante como hacia atrás.

    Las observaciones (1:N) son "a lo sumo muchos objetos", así que se
    resuelven aparte con el manager inverso (Django las trae en su propia
    consulta, no con JOIN).
    """
    estudiante = get_object_or_404(
        Estudiante.objects.select_related("apoderado", "ficha_medica"),
        pk=pk,
    )
    observaciones = estudiante.observaciones.all()   # related_name de Observacion (1:N)
    return render(request, "semana3/estudiante_detalle.html", {
        "estudiante": estudiante,
        "observaciones": observaciones,
    })


def curso_list(request):
    """Usa prefetch_related() para recorrer el modelo intermedio
    CursoEstudiante (N:M Estudiante<->Curso) sin caer en el problema N+1:
    sin esto, por cada curso se dispararía una consulta aparte para traer
    a sus estudiantes inscritos; con prefetch_related(), Django hace UNA
    sola consulta extra para TODAS las inscripciones y las reparte en
    memoria entre los cursos.
    """
    cursos = Curso.objects.prefetch_related("inscripciones_curso__estudiante")
    return render(request, "semana3/curso_list.html", {"cursos": cursos})


# ---------------------------------------------------------------------------
# Matrícula  (entidad relacionada: ForeignKey -> Estudiante, AnioLectivo, Grado)
# ---------------------------------------------------------------------------

def matricula_list(request):
    """READ con filtros por año lectivo y por estado de matrícula."""
    anio = request.GET.get("anio", "")
    estado = request.GET.get("estado", "")

    # select_related con "__" encadena varias relaciones en un solo SELECT con JOINs
    matriculas = Matricula.objects.select_related(
        "estudiante", "anio_lectivo", "grado", "grado__nivel"
    ).all()
    if anio:
        matriculas = matriculas.filter(anio_lectivo_id=anio)      # WHERE anio_lectivo_id = ?
    if estado:
        matriculas = matriculas.filter(estado_matricula=estado)   # WHERE estado_matricula = ?
    matriculas = matriculas.order_by("-fecha_registro")           # ORDER BY fecha_registro DESC

    return render(request, "semana3/matricula_list.html", {
        "matriculas": matriculas,
        "anios": AnioLectivo.objects.all(),
        "estados": EstadoMatricula.choices,
        "f_anio": anio,
        "f_estado": estado,
    })


def matricula_crear(request):
    """CREATE con lógica de negocio (Requisitos 6 y 7).

    Además de guardar la matrícula:
      1. copia `costo_matricula` del año lectivo elegido;
      2. genera automáticamente las 10 cuotas de pensión (vencimiento mensual).
    """
    if request.method == "POST":
        form = MatriculaForm(request.POST)
        if form.is_valid():
            # commit=False -> crea el objeto EN MEMORIA, todavía sin INSERT,
            # para poder ajustarle campos antes de guardarlo.
            matricula = form.save(commit=False)
            # copia el costo actual del año lectivo (así queda "congelado" en la matrícula)
            matricula.costo_matricula = matricula.anio_lectivo.costo_matricula
            matricula.save()                                       # ahora sí: INSERT de la matrícula

            # --- Requisito 7: generar las 10 cuotas de pensión ---
            monto = matricula.anio_lectivo.monto_pension           # base de cada cuota
            inicio = matricula.anio_lectivo.fecha_inicio           # fecha del 1er vencimiento
            cuotas = [                                             # arma 10 objetos Pension en memoria
                Pension(
                    matricula=matricula,                          # todas apuntan a esta matrícula
                    num_cuota=numero,                             # 1, 2, ..., 10
                    monto_base=monto,
                    monto_final=monto,                            # sin descuento por defecto
                    fecha_vencimiento=_sumar_meses(inicio, numero - 1),  # +0, +1, ..., +9 meses
                    estado_pago=EstadoPension.PENDIENTE,
                )
                for numero in range(1, 11)                        # range(1, 11) -> 1..10
            ]
            Pension.objects.bulk_create(cuotas)                   # 10 INSERT en UNA sola consulta

            messages.success(
                request,
                f"Matrícula registrada. Se generaron 10 cuotas de pensión de S/ {monto}.",
            )
            return redirect("semana3:matricula_list")
    else:
        form = MatriculaForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nueva matrícula",
        "volver": "semana3:matricula_list",
    })


def matricula_editar(request, pk):
    """UPDATE de matrícula: permite cambiar el grado/sección (Requisito 7).

    IMPORTANTE: al editar NO se regeneran las cuotas; eso solo ocurre al crear.
    """
    matricula = get_object_or_404(Matricula, pk=pk)
    if request.method == "POST":
        form = MatriculaForm(request.POST, instance=matricula)
        if form.is_valid():
            form.save()                               # UPDATE (solo los campos de la matrícula)
            messages.success(request, "Matrícula actualizada correctamente.")
            return redirect("semana3:matricula_list")
    else:
        form = MatriculaForm(instance=matricula)
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": f"Editar matrícula: {matricula}",
        "volver": "semana3:matricula_list",
    })


# ---------------------------------------------------------------------------
# Pensión  (FK -> Matricula [CASCADE]; FK opcional -> TipoDescuento [SET_NULL])
# ---------------------------------------------------------------------------

def pension_list(request):
    """READ con filtro por estado_pago (Requisito 9: pagadas / pendientes / vencidas)."""
    estado = request.GET.get("estado", "")

    pensiones = Pension.objects.select_related(
        "matricula", "matricula__estudiante", "tipo_descuento"    # JOINs para mostrar datos relacionados
    ).all()
    if estado:
        pensiones = pensiones.filter(estado_pago=estado)                # WHERE estado_pago = ?
    pensiones = pensiones.order_by("fecha_vencimiento", "num_cuota")    # ORDER BY vencimiento, cuota

    return render(request, "semana3/pension_list.html", {
        "pensiones": pensiones,
        "estados": EstadoPension.choices,
        "f_estado": estado,
    })


def pension_crear(request):
    """CREATE de pensión con lógica: calcula `monto_final` con el descuento (Requisito 8)."""
    if request.method == "POST":
        form = PensionForm(request.POST)
        if form.is_valid():
            pension = form.save(commit=False)                     # objeto en memoria, sin INSERT
            pension.monto_final = _calcular_monto_final(pension)  # aplica el descuento
            pension.save()                                        # INSERT (ya con monto_final calculado)
            messages.success(request, "Pensión registrada correctamente.")
            return redirect("semana3:pension_list")
    else:
        form = PensionForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nueva pensión",
        "volver": "semana3:pension_list",
    })


def pension_editar(request, pk):
    """UPDATE de pensión: si cambia `monto_base` o el descuento, recalcula `monto_final`."""
    pension = get_object_or_404(Pension, pk=pk)
    if request.method == "POST":
        form = PensionForm(request.POST, instance=pension)
        if form.is_valid():
            pension = form.save(commit=False)                    # aplica cambios en memoria
            pension.monto_final = _calcular_monto_final(pension) # recalcula con los nuevos datos
            pension.save()                                       # UPDATE
            messages.success(request, "Pensión actualizada correctamente.")
            return redirect("semana3:pension_list")
    else:
        form = PensionForm(instance=pension)
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": f"Editar pensión: {pension}",
        "volver": "semana3:pension_list",
    })


# ---------------------------------------------------------------------------
# Pago  (entidad relacionada: FK -> Pension, MetodoPago)
# ---------------------------------------------------------------------------

def pago_list(request):
    """READ con filtro por estado_validacion (tesorería revisa los pendientes)."""
    estado = request.GET.get("estado", "")

    pagos = Pago.objects.select_related(
        "pension", "pension__matricula__estudiante", "metodo_pago"
    ).all()
    if estado:
        pagos = pagos.filter(estado_validacion=estado)     # WHERE estado_validacion = ?
    pagos = pagos.order_by("-fecha_operacion")             # ORDER BY fecha_operacion DESC

    return render(request, "semana3/pago_list.html", {
        "pagos": pagos,
        "estados": EstadoPago.choices,
        "f_estado": estado,
    })


def pago_crear(request):
    """CREATE de pago: registrar el abono con su comprobante (Requisito 10)."""
    if request.method == "POST":
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()                               # INSERT
            messages.success(request, "Pago registrado correctamente.")
            return redirect("semana3:pago_list")
    else:
        form = PagoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo pago",
        "volver": "semana3:pago_list",
    })


def pago_editar(request, pk):
    """UPDATE de pago con lógica de negocio (Requisito 10).

    Al validar el comprobante, además de guardar el pago se sincroniza la cuota:
      - "Aprobado"              -> la pensión pasa a "Pagada".
      - "Rechazado" / "Anulado" -> la pensión vuelve a "Pendiente".
    Se modifican DOS filas: el pago y su pensión.
    """
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == "POST":
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            pago = form.save()                                  # UPDATE del pago

            pension = pago.pension                              # navega la FK hasta la cuota asociada
            if pago.estado_validacion == EstadoPago.APROBADO:
                pension.estado_pago = EstadoPension.PAGADA
                pension.save()                                  # UPDATE de la pensión
            elif pago.estado_validacion in (EstadoPago.RECHAZADO, EstadoPago.ANULADO):
                pension.estado_pago = EstadoPension.PENDIENTE
                pension.save()                                  # UPDATE de la pensión

            messages.success(request, "Pago actualizado correctamente.")
            return redirect("semana3:pago_list")
    else:
        form = PagoForm(instance=pago)
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": f"Editar pago: {pago.num_operacion}",
        "volver": "semana3:pago_list",
    })


# ===========================================================================
# DELETE (Ejercicio 17) — una vista de una línea por entidad.
# Cada una: (1) busca el registro con get_object_or_404, (2) delega en el
# helper _eliminar(), que hace la confirmación (GET) y el borrado (POST).
# ===========================================================================

def nivel_eliminar(request, pk):
    """DELETE de nivel educativo."""
    return _eliminar(request, get_object_or_404(NivelEducativo, pk=pk),
                     "semana3:nivel_list", "Nivel educativo")


def anio_eliminar(request, pk):
    """DELETE de año lectivo."""
    return _eliminar(request, get_object_or_404(AnioLectivo, pk=pk),
                     "semana3:anio_list", "Año lectivo")


def descuento_eliminar(request, pk):
    """DELETE de tipo de descuento (Requisito 9)."""
    return _eliminar(request, get_object_or_404(TipoDescuento, pk=pk),
                     "semana3:descuento_list", "Tipo de descuento")


def metodo_eliminar(request, pk):
    """DELETE de método de pago."""
    return _eliminar(request, get_object_or_404(MetodoPago, pk=pk),
                     "semana3:metodo_list", "Método de pago")


def apoderado_eliminar(request, pk):
    """DELETE de apoderado (falla con PROTECT si tiene estudiantes)."""
    return _eliminar(request, get_object_or_404(Apoderado, pk=pk),
                     "semana3:apoderado_list", "Apoderado")


def grado_eliminar(request, pk):
    """DELETE de grado."""
    return _eliminar(request, get_object_or_404(Grado, pk=pk),
                     "semana3:grado_list", "Grado")


def estudiante_eliminar(request, pk):
    """DELETE de estudiante."""
    return _eliminar(request, get_object_or_404(Estudiante, pk=pk),
                     "semana3:estudiante_list", "Estudiante")


def matricula_eliminar(request, pk):
    """DELETE de matrícula (CASCADE: borra también sus 10 cuotas de pensión)."""
    return _eliminar(request, get_object_or_404(Matricula, pk=pk),
                     "semana3:matricula_list", "Matrícula")


def pension_eliminar(request, pk):
    """DELETE de pensión."""
    return _eliminar(request, get_object_or_404(Pension, pk=pk),
                     "semana3:pension_list", "Pensión")


def pago_eliminar(request, pk):
    """DELETE de pago (anular un abono registrado por error)."""
    return _eliminar(request, get_object_or_404(Pago, pk=pk),
                     "semana3:pago_list", "Pago")
