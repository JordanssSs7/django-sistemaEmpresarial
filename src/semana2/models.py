"""
Fuente de datos de la App "Gestión de Citas Médicas" (Semana 2).

Esta App NO usa base de datos: toda la información vive en las listas de
este módulo. Las vistas leen y agregan citas sobre `CITAS` en memoria.

IMPORTANTE: al reiniciar el servidor de desarrollo (o al guardar un archivo
.py con el servidor corriendo, por el auto-reload de Django) las listas
vuelven a este estado inicial y se pierden las citas agregadas desde el
formulario. Esto es esperado en este laboratorio.
"""

from datetime import date, time, datetime


# ---------------------------------------------------------------------------
# Catálogos de opciones (datos estáticos de apoyo)
# ---------------------------------------------------------------------------

# Cada especialidad lleva asociado su costo estimado de consulta.
# Se usa para el ChoiceField del formulario y para calcular `costo_estimado`
# de forma automática al registrar una cita.
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


def costo_de_especialidad(nombre):
    """Devuelve el costo estimado de una especialidad (0.0 si no se encuentra)."""
    for especialidad in ESPECIALIDADES:
        if especialidad["nombre"] == nombre:
            return especialidad["costo"]
    return 0.0


def siguiente_id():
    """Calcula el siguiente id disponible para una cita nueva."""
    return max((cita["id"] for cita in CITAS), default=0) + 1


# ---------------------------------------------------------------------------
# Fuente de datos principal: listado de citas médicas
# ---------------------------------------------------------------------------

CITAS = [
    {
        "id": 1,
        "paciente": "María Fernández Rojas",
        "documento": "45872103",
        "medico": "Dr. Alberto Ruiz",
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
        "medico": "Dra. Lucía Mendoza",
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
        "medico": "Dra. Lucía Mendoza",
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
        "medico": "Dr. Alberto Ruiz",
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
        "medico": "Dr. Manuel Ríos",
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
        "medico": "Dr. Manuel Ríos",
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
