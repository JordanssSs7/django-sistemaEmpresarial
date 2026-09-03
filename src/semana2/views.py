from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from . import models
from .models import Cita, Especialidad, Horario, Profesional
from .forms import CitaForm, HorarioForm, ProfesionalForm


def listado(request):
    """Ejercicio 4: listado de citas leído mediante Django ORM (QuerySet)
    en vez de la lista en memoria de la Semana 2."""
    estado = request.GET.get("estado", "")
    profesional_id = request.GET.get("profesional", "")
    especialidad = request.GET.get("especialidad", "")
    fecha = request.GET.get("fecha", "")

    citas = Cita.objects.select_related("profesional", "especialidad").all()
    if estado:
        citas = citas.filter(estado=estado)
    if profesional_id:
        citas = citas.filter(profesional_id=profesional_id)
    if especialidad:
        citas = citas.filter(especialidad__nombre=especialidad)
    if fecha:
        citas = citas.filter(fecha=fecha)
    citas = citas.order_by("fecha", "hora")

    contexto = {
        "citas": citas,
        "estados": [valor for valor, _ in models.ESTADOS],
        "estado_activo": estado,
        "profesionales": Profesional.objects.all(),
        "profesional_activo": profesional_id,
        "especialidades": Especialidad.objects.all(),
        "especialidad_activa": especialidad,
        "fecha_activa": fecha,
        "total": citas.count(),
    }
    return render(request, "semana2/citas_list.html", contexto)

def crear(request):
    """Ejercicio 5: registro de una cita persistido mediante Django ORM
    (Cita.objects.create), en vez de un .append() sobre una lista."""
    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            profesional = Profesional.objects.get(pk=datos["profesional"])
            cita = Cita.objects.create(
                paciente=datos["paciente"],
                documento=datos["documento"],
                profesional=profesional,
                # Se copia la especialidad y el costo del profesional elegido.
                especialidad=profesional.especialidad,
                costo_estimado=profesional.especialidad.costo,
                fecha=datos["fecha"],
                hora=datos["hora"],
                estado=datos["estado"],
                prioritaria=datos["prioritaria"],
                consultorio=datos["consultorio"],
                observaciones=datos["observaciones"],
                # "agendado_en" no se pasa: el campo es auto_now_add=True.
            )
            messages.success(
                request,
                f"Cita agendada correctamente para {cita.paciente} "
                f"con {profesional.nombre} ({profesional.especialidad}).",
            )
            return redirect("semana2_listado")
    else:
        form = CitaForm()

    return render(request, "semana2/cita_form.html", {"form": form})


def detalle(request, cita_id):
    cita = Cita.objects.select_related("profesional", "especialidad").filter(pk=cita_id).first()
    if cita is None:
        raise Http404("Cita no encontrada")

    contexto = {
        "cita": cita,
        "profesional": cita.profesional,
    }
    return render(request, "semana2/cita_detail.html", contexto)


def actualizar_estado(request, cita_id):
    cita = Cita.objects.filter(pk=cita_id).first()
    if cita is None:
        raise Http404("Cita no encontrada")

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        if nuevo_estado in [valor for valor, _ in models.ESTADOS]:
            cita.estado = nuevo_estado
            cita.save(update_fields=["estado"])
            messages.success(
                request,
                f'La cita de {cita.paciente} ahora está "{nuevo_estado}".',
            )

    return redirect("semana2_listado")

def listado_profesionales(request):
    profesionales = Profesional.objects.select_related("especialidad").all()
    return render(request, "semana2/profesionales_list.html", {"profesionales": profesionales})


def crear_profesional(request):
    """Ejercicio 5 (extendido): registro de un profesional vía ORM."""
    if request.method == "POST":
        form = ProfesionalForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            especialidad = Especialidad.objects.get(nombre=datos["especialidad"])
            profesional = Profesional.objects.create(
                nombre=datos["nombre"],
                especialidad=especialidad,
                disponible=datos["disponible"],
            )
            messages.success(request, f"Profesional {profesional.nombre} registrado correctamente.")
            return redirect("semana2_profesionales")
    else:
        form = ProfesionalForm()

    return render(request, "semana2/profesional_form.html", {"form": form})

def listado_horarios(request):
    horarios = models.Horario.objects.select_related("profesional").order_by(
        "profesional__nombre", "dia_semana", "hora_inicio"
    )
    return render(request, "semana2/horarios_list.html", {"horarios": horarios})

def crear_horario(request):
    """Ejercicio 5 (extendido): registro de un horario vía ORM."""
    if request.method == "POST":
        form = HorarioForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            Horario.objects.create(
                profesional_id=int(datos["profesional"]),
                dia_semana=datos["dia_semana"],
                hora_inicio=datos["hora_inicio"],
                hora_fin=datos["hora_fin"],
            )
            messages.success(request, "Horario de atención registrado correctamente.")
            return redirect("semana2_horarios")
    else:
        form = HorarioForm()

    return render(request, "semana2/horario_form.html", {"form": form})
