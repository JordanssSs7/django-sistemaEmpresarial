"""
Fuente de datos de la App "Gestión de Citas Médicas" (Semana 2/3).

Esta App NO usa base de datos: toda la información vive en las listas de
este módulo (especialidades, profesionales, horarios y citas). Las vistas
leen y agregan datos sobre estas listas en memoria.

IMPORTANTE: al reiniciar el servidor de desarrollo (o al guardar un archivo
.py con el servidor corriendo, por el auto-reload de Django) las listas
vuelven a este estado inicial y se pierden los cambios hechos desde los
formularios. Esto es esperado en este laboratorio.
"""

from datetime import date, time, datetime


# ---------------------------------------------------------------------------
# Catálogos de opciones (datos estáticos de apoyo)
# ---------------------------------------------------------------------------

# Cada especialidad lleva asociado su costo estimado de consulta.
# Se usa para calcular `costo_estimado` de forma automática al registrar
# una cita, a partir de la especialidad del profesional elegido.
ESPECIALIDADES = [
    {"nombre": "Medicina General", "costo": 30.0},
    {"nombre": "Pediatría", "costo": 45.0},
    {"nombre": "Cardiología", "costo": 90.0},
    {"nombre": "Dermatología", "costo": 70.0},
    {"nombre": "Ginecología", "costo": 80.0},
    {"nombre": "Odontología", "costo": 50.0},
]

# Estados posibles de una cita. Se ofrecen como lista de opciones en el
# formulario y como filtro en el listado.
ESTADOS = ["Programada", "Atendida", "Cancelada"]

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

_DIA_SEMANA_POR_INDICE = dict(enumerate(DIAS_SEMANA))


def costo_de_especialidad(nombre):
    """Devuelve el costo estimado de una especialidad (0.0 si no se encuentra)."""
    for especialidad in ESPECIALIDADES:
        if especialidad["nombre"] == nombre:
            return especialidad["costo"]
    return 0.0


def dia_semana_de_fecha(fecha):
    """Traduce una fecha a su nombre de día de la semana en español."""
    return _DIA_SEMANA_POR_INDICE[fecha.weekday()]


# ---------------------------------------------------------------------------
# Profesionales de la salud
# ---------------------------------------------------------------------------

PROFESIONALES = [
    {"id": 1, "nombre": "Dr. Alberto Ruiz", "especialidad": "Cardiología", "disponible": True},
    {"id": 2, "nombre": "Dra. Lucía Mendoza", "especialidad": "Medicina General", "disponible": True},
    {"id": 3, "nombre": "Dra. Carmen Sánchez", "especialidad": "Ginecología", "disponible": True},
    {"id": 4, "nombre": "Dr. Manuel Ríos", "especialidad": "Pediatría", "disponible": True},
    {"id": 5, "nombre": "Dr. Iván Torres", "especialidad": "Dermatología", "disponible": True},
    {"id": 6, "nombre": "Dra. Rosa Flores", "especialidad": "Odontología", "disponible": False},
]


def siguiente_id_profesional():
    return max((p["id"] for p in PROFESIONALES), default=0) + 1


def profesional_por_id(profesional_id):
    for profesional in PROFESIONALES:
        if profesional["id"] == int(profesional_id):
            return profesional
    return None


def nombre_profesional(profesional_id):
    profesional = profesional_por_id(profesional_id)
    return profesional["nombre"] if profesional else "—"


def profesionales_disponibles(especialidad=None):
    """Profesionales activos, opcionalmente filtrados por especialidad."""
    resultado = [p for p in PROFESIONALES if p["disponible"]]
    if especialidad:
        resultado = [p for p in resultado if p["especialidad"] == especialidad]
    return resultado


# ---------------------------------------------------------------------------
# Horarios de atención por profesional
# ---------------------------------------------------------------------------

HORARIOS = [
    {"id": 1, "profesional_id": 1, "dia_semana": "Lunes", "hora_inicio": time(8, 0), "hora_fin": time(12, 0)},
    {"id": 2, "profesional_id": 1, "dia_semana": "Miércoles", "hora_inicio": time(8, 0), "hora_fin": time(12, 0)},
    {"id": 3, "profesional_id": 2, "dia_semana": "Jueves", "hora_inicio": time(9, 0), "hora_fin": time(13, 0)},
    {"id": 4, "profesional_id": 3, "dia_semana": "Miércoles", "hora_inicio": time(8, 0), "hora_fin": time(12, 0)},
    {"id": 5, "profesional_id": 4, "dia_semana": "Viernes", "hora_inicio": time(10, 0), "hora_fin": time(14, 0)},
    {"id": 6, "profesional_id": 5, "dia_semana": "Martes", "hora_inicio": time(14, 0), "hora_fin": time(18, 0)},
]


def siguiente_id_horario():
    return max((h["id"] for h in HORARIOS), default=0) + 1


def horarios_de_profesional(profesional_id):
    return [h for h in HORARIOS if h["profesional_id"] == int(profesional_id)]


def hay_solapamiento_horario(profesional_id, dia_semana, hora_inicio, hora_fin, excluir_id=None):
    """True si [hora_inicio, hora_fin) se cruza con otro horario ya
    registrado para el mismo profesional y día."""
    for horario in horarios_de_profesional(profesional_id):
        if horario["id"] == excluir_id:
            continue
        if horario["dia_semana"] != dia_semana:
            continue
        if hora_inicio < horario["hora_fin"] and horario["hora_inicio"] < hora_fin:
            return True
    return False


def horario_cubre_fecha_hora(profesional_id, fecha, hora):
    """True si algún bloque de horario del profesional cubre ese día/hora."""
    dia = dia_semana_de_fecha(fecha)
    for horario in horarios_de_profesional(profesional_id):
        if horario["dia_semana"] == dia and horario["hora_inicio"] <= hora < horario["hora_fin"]:
            return True
    return False


# ---------------------------------------------------------------------------
# Fuente de datos principal: listado de citas médicas
# ---------------------------------------------------------------------------

CITAS = [
    {
        "id": 1,
        "paciente": "María Fernández Rojas",
        "documento": "45872103",
        "profesional_id": 1,
        "especialidad": "Cardiología",
        "fecha": date(2026, 9, 2),
        "hora": time(9, 0),
        "estado": "Programada",
        "prioritaria": True,
        "consultorio": "C-201",
        "observaciones": "Control de presión arterial. Paciente adulto mayor.",
        "costo_estimado": 90.0,
        "agendado_en": datetime(2026, 8, 27, 10, 15),
    },
    {
        "id": 2,
        "paciente": "Jorge Castillo Núñez",
        "documento": "40218765",
        "profesional_id": 2,
        "especialidad": "Medicina General",
        "fecha": date(2026, 9, 3),
        "hora": time(11, 30),
        "estado": "Programada",
        "prioritaria": False,
        "consultorio": "C-104",
        "observaciones": "Chequeo de rutina anual.",
        "costo_estimado": 30.0,
        "agendado_en": datetime(2026, 8, 27, 12, 40),
    },
    {
        "id": 3,
        "paciente": "Ana Beatriz Salinas",
        "documento": "72659481",
        "profesional_id": 3,
        "especialidad": "Ginecología",
        "fecha": date(2026, 8, 26),
        "hora": time(8, 15),
        "estado": "Atendida",
        "prioritaria": True,
        "consultorio": "C-210",
        "observaciones": "Control de gestación, semana 30.",
        "costo_estimado": 80.0,
        "agendado_en": datetime(2026, 8, 20, 9, 5),
    },
    {
        "id": 4,
        "paciente": "Luis Alberto Tapia",
        "documento": "48120937",
        "profesional_id": 5,
        "especialidad": "Dermatología",
        "fecha": date(2026, 8, 25),
        "hora": time(16, 0),
        "estado": "Cancelada",
        "prioritaria": False,
        "consultorio": "C-108",
        "observaciones": "Revisión de lunares. Paciente reprogramará.",
        "costo_estimado": 70.0,
        "agendado_en": datetime(2026, 8, 19, 15, 20),
    },
    {
        "id": 5,
        "paciente": "Carmen Rosa Villalobos",
        "documento": "09873214",
        "profesional_id": 4,
        "especialidad": "Pediatría",
        "fecha": date(2026, 9, 4),
        "hora": time(10, 45),
        "estado": "Programada",
        "prioritaria": False,
        "consultorio": "C-115",
        "observaciones": "Vacunación y control de peso del menor.",
        "costo_estimado": 45.0,
        "agendado_en": datetime(2026, 8, 28, 8, 30),
    },
    {
        "id": 6,
        "paciente": "Pedro Gonzáles Ramírez",
        "documento": "41567890",
        "profesional_id": 6,
        "especialidad": "Odontología",
        "fecha": date(2026, 9, 5),
        "hora": time(13, 0),
        "estado": "Atendida",
        "prioritaria": False,
        "consultorio": "C-120",
        "observaciones": "Limpieza dental y evaluación de caries.",
        "costo_estimado": 50.0,
        "agendado_en": datetime(2026, 8, 28, 14, 10),
    },
]


def siguiente_id_cita():
    return max((cita["id"] for cita in CITAS), default=0) + 1


def cita_por_id(cita_id):
    for cita in CITAS:
        if cita["id"] == int(cita_id):
            return cita
    return None


def horario_ocupado(profesional_id, fecha, hora, excluir_id=None):
    """True si ya existe una cita activa (no cancelada) con ese profesional,
    en esa fecha y hora exactas."""
    for cita in CITAS:
        if cita["id"] == excluir_id:
            continue
        if (
            cita["profesional_id"] == int(profesional_id)
            and cita["fecha"] == fecha
            and cita["hora"] == hora
            and cita["estado"] != "Cancelada"
        ):
            return True
    return False
