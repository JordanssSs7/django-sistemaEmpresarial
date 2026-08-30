from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from . import models
from .forms import CitaForm


def listado(request):
    """Muestra todas las citas registradas, con filtro opcional por estado."""
    estado = request.GET.get("estado", "")

    citas = models.CITAS
    if estado:
        citas = [cita for cita in citas if cita["estado"] == estado]

    contexto = {
        "citas": citas,
        "estados": models.ESTADOS,
        "estado_activo": estado,
        "total": len(citas),
    }
    return render(request, "semana2/citas_list.html", contexto)


def crear(request):
    """Muestra y procesa el formulario de registro de una nueva cita."""
    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            nueva_cita = {
                "id": models.siguiente_id(),
                "paciente": datos["paciente"],
                "documento": datos["documento"],
                "medico": datos["medico"],
                "especialidad": datos["especialidad"],
                "fecha": datos["fecha"],
                "hora": datos["hora"],
                "estado": datos["estado"],
                "prioritaria": datos["prioritaria"],
                "consultorio": datos["consultorio"],
                "observaciones": datos["observaciones"],
                # Calculado automáticamente segun la especialidad elegida.
                "costo_estimado": models.costo_de_especialidad(datos["especialidad"]),
                # Trazabilidad: momento exacto del agendamiento.
                "agendado_en": timezone.now(),
            }
            # Se agrega a la MISMA lista en memoria (no se reasigna la variable).
            models.CITAS.append(nueva_cita)
            messages.success(
                request,
                f"Cita agendada correctamente para {nueva_cita['paciente']} "
                f"({nueva_cita['especialidad']}).",
            )
            return redirect("semana2_listado")
    else:
        form = CitaForm()

    return render(request, "semana2/cita_form.html", {"form": form})
