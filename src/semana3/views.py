import calendar
from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render

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
from .models import (
    AnioLectivo,
    Apoderado,
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


def _sumar_meses(fecha, n):
    """Devuelve `fecha` desplazada n meses hacia adelante."""
    mes = fecha.month - 1 + n
    anio = fecha.year + mes // 12
    mes = mes % 12 + 1
    ultimo_dia = calendar.monthrange(anio, mes)[1]
    return date(anio, mes, min(fecha.day, ultimo_dia))


def index(request):
    """Menú del módulo de gestión escolar (Semana 3)."""
    return render(request, "semana3/index.html")


# ---------------------------------------------------------------------------
# Nivel educativo
# ---------------------------------------------------------------------------

def nivel_list(request):
    niveles = NivelEducativo.objects.all()
    return render(request, "semana3/nivel_list.html", {"niveles": niveles})


def nivel_crear(request):
    if request.method == "POST":
        form = NivelEducativoForm(request.POST)
        if form.is_valid():
            form.save()  # INSERT
            messages.success(request, "Nivel educativo registrado correctamente.")
            return redirect("semana3:nivel_list")
    else:
        form = NivelEducativoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo nivel educativo",
        "volver": "semana3:nivel_list",
    })


# ---------------------------------------------------------------------------
# Año lectivo
# ---------------------------------------------------------------------------

def anio_list(request):
    anios = AnioLectivo.objects.all()
    return render(request, "semana3/anio_list.html", {"anios": anios})


def anio_crear(request):
    if request.method == "POST":
        form = AnioLectivoForm(request.POST)
        if form.is_valid():
            form.save()  # INSERT
            messages.success(request, "Año lectivo registrado correctamente.")
            return redirect("semana3:anio_list")
    else:
        form = AnioLectivoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo año lectivo",
        "volver": "semana3:anio_list",
    })


# ---------------------------------------------------------------------------
# Tipo de descuento
# ---------------------------------------------------------------------------

def descuento_list(request):
    activo = request.GET.get("activo", "")
    descuentos = TipoDescuento.objects.all()
    if activo == "1":
        descuentos = descuentos.filter(activo=True)      # WHERE activo = 1
    elif activo == "0":
        descuentos = descuentos.filter(activo=False)     # WHERE activo = 0
    descuentos = descuentos.order_by("nombre")           # ORDER BY nombre
    return render(request, "semana3/descuento_list.html", {
        "descuentos": descuentos,
        "f_activo": activo,
    })


def descuento_crear(request):
    if request.method == "POST":
        form = TipoDescuentoForm(request.POST)
        if form.is_valid():
            form.save()  # INSERT
            messages.success(request, "Tipo de descuento registrado correctamente.")
            return redirect("semana3:descuento_list")
    else:
        form = TipoDescuentoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo tipo de descuento",
        "volver": "semana3:descuento_list",
    })


# ---------------------------------------------------------------------------
# Método de pago
# ---------------------------------------------------------------------------

def metodo_list(request):
    metodos = MetodoPago.objects.all()
    return render(request, "semana3/metodo_list.html", {"metodos": metodos})


def metodo_crear(request):
    if request.method == "POST":
        form = MetodoPagoForm(request.POST)
        if form.is_valid():
            form.save()  # INSERT
            messages.success(request, "Método de pago registrado correctamente.")
            return redirect("semana3:metodo_list")
    else:
        form = MetodoPagoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo método de pago",
        "volver": "semana3:metodo_list",
    })


# ---------------------------------------------------------------------------
# Apoderado
# ---------------------------------------------------------------------------

def apoderado_list(request):
    apoderados = Apoderado.objects.all()
    return render(request, "semana3/apoderado_list.html", {"apoderados": apoderados})


def apoderado_crear(request):
    if request.method == "POST":
        form = ApoderadoForm(request.POST)
        if form.is_valid():
            form.save()  # INSERT
            messages.success(request, "Apoderado registrado correctamente.")
            return redirect("semana3:apoderado_list")
    else:
        form = ApoderadoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo apoderado",
        "volver": "semana3:apoderado_list",
    })


# ---------------------------------------------------------------------------
# Grado  (ForeignKey -> NivelEducativo)
# ---------------------------------------------------------------------------

def grado_list(request):
    grados = Grado.objects.select_related("nivel").all()
    return render(request, "semana3/grado_list.html", {"grados": grados})


def grado_crear(request):
    if request.method == "POST":
        form = GradoForm(request.POST)
        if form.is_valid():
            form.save()  # INSERT
            messages.success(request, "Grado registrado correctamente.")
            return redirect("semana3:grado_list")
    else:
        form = GradoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo grado",
        "volver": "semana3:grado_list",
    })


# ---------------------------------------------------------------------------
# Estudiante  (ForeignKey -> Apoderado)
# ---------------------------------------------------------------------------

def estudiante_list(request):
    estado = request.GET.get("estado", "")
    anio = request.GET.get("anio", "")
    grado = request.GET.get("grado", "")
    q = request.GET.get("q", "").strip()

    estudiantes = Estudiante.objects.select_related("apoderado").all()
    if estado:
        estudiantes = estudiantes.filter(estado=estado)
    if anio:
        estudiantes = estudiantes.filter(matriculas__anio_lectivo_id=anio)
    if grado:
        estudiantes = estudiantes.filter(matriculas__grado_id=grado)
    if q:
        estudiantes = estudiantes.filter(
            Q(nombres__icontains=q)
            | Q(apellidos__icontains=q)
            | Q(num_documento__icontains=q)
            | Q(codigo_alumno__icontains=q)
        )
    estudiantes = estudiantes.distinct().order_by("apellidos", "nombres")

    return render(request, "semana3/estudiante_list.html", {
        "estudiantes": estudiantes,
        "estados": EstadoEstudiante.choices,
        "anios": AnioLectivo.objects.all(),
        "grados": Grado.objects.select_related("nivel").all(),
        "f_estado": estado,
        "f_anio": anio,
        "f_grado": grado,
        "q": q,
    })


def estudiante_crear(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()  # INSERT
            messages.success(request, "Estudiante registrado correctamente.")
            return redirect("semana3:estudiante_list")
    else:
        form = EstudianteForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo estudiante",
        "volver": "semana3:estudiante_list",
    })


# ---------------------------------------------------------------------------
# Matrícula  (FK -> Estudiante, AnioLectivo, Grado)
# ---------------------------------------------------------------------------

def matricula_list(request):
    anio = request.GET.get("anio", "")
    estado = request.GET.get("estado", "")

    matriculas = Matricula.objects.select_related(
        "estudiante", "anio_lectivo", "grado", "grado__nivel"
    ).all()
    if anio:
        matriculas = matriculas.filter(anio_lectivo_id=anio)
    if estado:
        matriculas = matriculas.filter(estado_matricula=estado)
    matriculas = matriculas.order_by("-fecha_registro")

    return render(request, "semana3/matricula_list.html", {
        "matriculas": matriculas,
        "anios": AnioLectivo.objects.all(),
        "estados": EstadoMatricula.choices,
        "f_anio": anio,
        "f_estado": estado,
    })


def matricula_crear(request):
    if request.method == "POST":
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save(commit=False)
            # El costo de matrícula se copia del año lectivo (Requisito 5/6).
            matricula.costo_matricula = matricula.anio_lectivo.costo_matricula
            matricula.save()  # INSERT matrícula

            # Requisito 7: generar automáticamente las 10 cuotas de pensión.
            monto = matricula.anio_lectivo.monto_pension
            inicio = matricula.anio_lectivo.fecha_inicio
            cuotas = [
                Pension(
                    matricula=matricula,
                    num_cuota=numero,
                    monto_base=monto,
                    monto_final=monto,
                    fecha_vencimiento=_sumar_meses(inicio, numero - 1),
                    estado_pago=EstadoPension.PENDIENTE,
                )
                for numero in range(1, 11)
            ]
            Pension.objects.bulk_create(cuotas)  # 10 INSERT

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


# ---------------------------------------------------------------------------
# Pensión  (FK -> Matricula, TipoDescuento opcional)
# ---------------------------------------------------------------------------

def pension_list(request):
    estado = request.GET.get("estado", "")

    pensiones = Pension.objects.select_related(
        "matricula", "matricula__estudiante", "tipo_descuento"
    ).all()
    if estado:
        pensiones = pensiones.filter(estado_pago=estado)     # WHERE estado_pago = ?
    pensiones = pensiones.order_by("fecha_vencimiento", "num_cuota")  # ORDER BY

    return render(request, "semana3/pension_list.html", {
        "pensiones": pensiones,
        "estados": EstadoPension.choices,
        "f_estado": estado,
    })


def pension_crear(request):
    if request.method == "POST":
        form = PensionForm(request.POST)
        if form.is_valid():
            pension = form.save(commit=False)
            # Requisito 8: monto_final = monto_base menos el descuento (si aplica).
            if pension.tipo_descuento:
                factor = Decimal("1") - (pension.tipo_descuento.porcentaje / Decimal("100"))
                pension.monto_final = (pension.monto_base * factor).quantize(Decimal("0.01"))
            else:
                pension.monto_final = pension.monto_base
            pension.save()  # INSERT
            messages.success(request, "Pensión registrada correctamente.")
            return redirect("semana3:pension_list")
    else:
        form = PensionForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nueva pensión",
        "volver": "semana3:pension_list",
    })


# ---------------------------------------------------------------------------
# Pago  (FK -> Pension, MetodoPago)
# ---------------------------------------------------------------------------

def pago_list(request):
    estado = request.GET.get("estado", "")

    pagos = Pago.objects.select_related(
        "pension", "pension__matricula__estudiante", "metodo_pago"
    ).all()
    if estado:
        pagos = pagos.filter(estado_validacion=estado)
    pagos = pagos.order_by("-fecha_operacion")

    return render(request, "semana3/pago_list.html", {
        "pagos": pagos,
        "estados": EstadoPago.choices,
        "f_estado": estado,
    })


def pago_crear(request):
    if request.method == "POST":
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()  # INSERT
            messages.success(request, "Pago registrado correctamente.")
            return redirect("semana3:pago_list")
    else:
        form = PagoForm()
    return render(request, "semana3/form.html", {
        "form": form,
        "titulo": "Nuevo pago",
        "volver": "semana3:pago_list",
    })
