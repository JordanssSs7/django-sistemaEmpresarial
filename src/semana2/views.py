from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone

from . import models
from .forms import CitaForm, HorarioForm, ProfesionalForm


# ---------------------------------------------------------------------------
# Citas médicas
# ---------------------------------------------------------------------------

def listado(request):
    """Muestra las citas registradas, con filtros por estado, profesional,
    especialidad y fecha."""
    estado = request.GET.get("estado", "")
    profesional_id = request.GET.get("profesional", "")
    especialidad = request.GET.get("especialidad", "")
    fecha = request.GET.get("fecha", "")

    citas = models.CITAS
    if estado:
        citas = [cita for cita in citas if cita["estado"] == estado]
    if profesional_id:
        citas = [cita for cita in citas if cita["profesional_id"] == int(profesional_id)]
    if especialidad:
        citas = [cita for cita in citas if cita["especialidad"] == especialidad]
    if fecha:
        citas = [cita for cita in citas if cita["fecha"].isoformat() == fecha]

    citas = sorted(citas, key=lambda cita: (cita["fecha"], cita["hora"]))
    citas = [
        {**cita, "profesional_nombre": models.nombre_profesional(cita["profesional_id"])}
        for cita in citas
    ]

    contexto = {
        "citas": citas,
        "estados": models.ESTADOS,
        "estado_activo": estado,
        "profesionales": models.PROFESIONALES,
        "profesional_activo": profesional_id,
        "especialidades": models.ESPECIALIDADES,
        "especialidad_activa": especialidad,
        "fecha_activa": fecha,
        "total": len(citas),
    }
    return render(request, "semana2/citas_list.html", contexto)


def crear(request):
    """Muestra y procesa el formulario de registro de una nueva cita."""
    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            profesional_id = int(datos["profesional"])
            profesional = models.profesional_por_id(profesional_id)
            nueva_cita = {
                "id": models.siguiente_id_cita(),
                "paciente": datos["paciente"],
                "documento": datos["documento"],
                "profesional_id": profesional_id,
                # Se deriva del profesional elegido, no la ingresa el usuario.
                "especialidad": profesional["especialidad"],
                "fecha": datos["fecha"],
                "hora": datos["hora"],
                "estado": datos["estado"],
                "prioritaria": datos["prioritaria"],
                "consultorio": datos["consultorio"],
                "observaciones": datos["observaciones"],
                "costo_estimado": models.costo_de_especialidad(profesional["especialidad"]),
                "agendado_en": timezone.now(),
            }
            models.CITAS.append(nueva_cita)
            messages.success(
                request,
                f"Cita agendada correctamente para {nueva_cita['paciente']} "
                f"con {profesional['nombre']} ({profesional['especialidad']}).",
            )
            return redirect("semana2_listado")
    else:
        form = CitaForm()

    return render(request, "semana2/cita_form.html", {"form": form})


def detalle(request, cita_id):
    """Muestra el detalle completo de una cita registrada."""
    cita = models.cita_por_id(cita_id)
    if cita is None:
        raise Http404("Cita no encontrada")

    contexto = {
        "cita": cita,
        "profesional": models.profesional_por_id(cita["profesional_id"]),
    }
    return render(request, "semana2/cita_detail.html", contexto)


def actualizar_estado(request, cita_id):
    """Cambia el estado de una cita (por ejemplo, para atenderla o
    cancelarla, liberando el horario para otro paciente)."""
    cita = models.cita_por_id(cita_id)
    if cita is None:
        raise Http404("Cita no encontrada")

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        if nuevo_estado in models.ESTADOS:
            cita["estado"] = nuevo_estado
            messages.success(
                request,
                f'La cita de {cita["paciente"]} ahora está "{nuevo_estado}".',
            )

    return redirect("semana2_listado")


# ---------------------------------------------------------------------------
# Profesionales de la salud
# ---------------------------------------------------------------------------

def listado_profesionales(request):
    """Muestra los profesionales registrados, su especialidad y disponibilidad."""
    return render(request, "semana2/profesionales_list.html", {"profesionales": models.PROFESIONALES})


def crear_profesional(request):
    """Muestra y procesa el formulario de registro de un nuevo profesional."""
    if request.method == "POST":
        form = ProfesionalForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            nuevo_profesional = {
                "id": models.siguiente_id_profesional(),
                "nombre": datos["nombre"],
                "especialidad": datos["especialidad"],
                "disponible": datos["disponible"],
            }
            models.PROFESIONALES.append(nuevo_profesional)
            messages.success(request, f"Profesional {nuevo_profesional['nombre']} registrado correctamente.")
            return redirect("semana2_profesionales")
    else:
        form = ProfesionalForm()

    return render(request, "semana2/profesional_form.html", {"form": form})


# ---------------------------------------------------------------------------
# Horarios de atención
# ---------------------------------------------------------------------------

def listado_horarios(request):
    """Muestra los horarios de atención registrados por profesional."""
    horarios = sorted(
        models.HORARIOS,
        key=lambda h: (h["profesional_id"], models.DIAS_SEMANA.index(h["dia_semana"]), h["hora_inicio"]),
    )
    horarios = [
        {**h, "profesional_nombre": models.nombre_profesional(h["profesional_id"])}
        for h in horarios
    ]
    return render(request, "semana2/horarios_list.html", {"horarios": horarios})


def crear_horario(request):
    """Muestra y procesa el formulario de registro de un horario de atención."""
    if request.method == "POST":
        form = HorarioForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            nuevo_horario = {
                "id": models.siguiente_id_horario(),
                "profesional_id": int(datos["profesional"]),
                "dia_semana": datos["dia_semana"],
                "hora_inicio": datos["hora_inicio"],
                "hora_fin": datos["hora_fin"],
            }
            models.HORARIOS.append(nuevo_horario)
            messages.success(request, "Horario de atención registrado correctamente.")
            return redirect("semana2_horarios")
    else:
        form = HorarioForm()

    return render(request, "semana2/horario_form.html", {"form": form})
