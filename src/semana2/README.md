# 🏥 Semana 2 — Gestión de Citas Médicas

App Django **sin base de datos**: los datos viven en listas de `models.py`. Conectada al mismo
Project (`config`) que `semana1`, en su propio espacio de rutas.

> Autor: **Jhoselin**

## 1. Problemática

En clínicas comunitarias, las citas se asignan por teléfono o presencialmente sin un registro
centralizado, generando colas y cruces de horarios. Esta app centraliza profesionales,
especialidades, horarios y citas.

**Usuarios:** recepcionistas (registran citas) y pacientes (consultan disponibilidad).

## 2. Requisitos funcionales

| # | Requisito |
|---|---|
| 1 | Consultar el listado de citas con sus datos principales |
| 2 | Registrar una nueva cita vía formulario |
| 3 | Validar documento (8 dígitos) y fecha antes de guardar |
| 4 | Marcar una cita como prioritaria (bool) |
| 5 | Elegir estado inicial: Programada / Atendida / Cancelada |
| 6 | Calcular el costo estimado según la especialidad |
| 7 | Registrar fecha/hora exacta de agendamiento |
| 8 | Filtrar citas por estado, profesional, especialidad o fecha |
| 9 | Registrar profesionales con su especialidad y disponibilidad |
| 10 | Registrar horarios de atención por profesional (día + rango) |
| 11 | Rechazar horarios que se solapen para un mismo profesional |
| 12 | Rechazar citas fuera de horario u ocupadas por otra cita |
| 13 | Ver el detalle completo de una cita |
| 14 | Cambiar el estado de una cita, liberando el horario al cancelar |
| 15 | Notificar en pantalla cada acción exitosa |

## 3. Modelo de datos (estático, sin BD)

**Profesional** — `id`, `nombre`, `especialidad`, `disponible` (bool)

**Horario** — `id`, `profesional_id` (FK), `dia_semana`, `hora_inicio`, `hora_fin`

**Cita** — `id`, `paciente`, `documento`, `profesional_id` (FK), `especialidad` *(derivado)*,
`fecha`, `hora`, `estado`, `prioritaria`, `consultorio`, `observaciones` *(opcional)*,
`costo_estimado` *(calculado)*, `agendado_en` *(automático)*

Todos los campos son obligatorios salvo `observaciones`; los marcados *(derivado/calculado/automático)*
los asigna la vista, no el usuario.

## 4. Puesta en marcha

```powershell
venv\Scripts\python.exe -m pip install -r src\requirements.txt
venv\Scripts\python.exe src\manage.py migrate
venv\Scripts\python.exe src\manage.py runserver
```

| Ruta | Descripción |
|---|---|
| `/` | Listado de citas (filtros) |
| `/nueva/` | Registrar cita |
| `/citas/<id>/` | Detalle / cambiar estado |
| `/profesionales/` · `/profesionales/nuevo/` | Profesionales |
| `/horarios/` · `/horarios/nuevo/` | Horarios de atención |

## 5. Flujo MVT — caso "registrar cita"

| Etapa | Dónde ocurre |
|---|---|
| Request | `POST /nueva/` con los datos del formulario |
| URL | `config/urls.py` → `semana2/urls.py` → `views.crear` |
| View | `crear()` valida con `CitaForm` (documento, fecha, horario disponible y libre) |
| Model | `models.CITAS.append(...)` — lista en memoria, sin BD |
| Template | Redirige a `listado`, que renderiza `citas_list.html` con la cita ya incluida |
| Response | HTML con el listado actualizado + mensaje de confirmación |

**Convivencia con `semana1`:** ambas apps están en `INSTALLED_APPS` y comparten `base.html`, pero
son independientes — `config/urls.py` reparte rutas (`/` para citas, `/semana1/` para la otra),
`semana1` usa SQLite con migraciones y esta app no toca esa base de datos. Se puede quitar
cualquiera de las dos sin romper la otra.

## 6. Nota sobre datos estáticos

No hay base de datos ni migraciones. Todo vive en listas de Python en `models.py` — los registros
agregados desde los formularios se pierden al reiniciar el servidor. Es el comportamiento esperado
del laboratorio.

## 7. Casos de prueba

| Caso | Entrada | Resultado esperado |
|---|---|---|
| Cita en horario válido | Profesional disponible en esa fecha/hora | Se agenda |
| Cita fuera de horario | Fecha/hora sin bloque asociado | Rechazada |
| Cita en horario ocupado | Choca con otra cita activa | Rechazada |
| Horario solapado | Mismo profesional/día, rango cruzado | Rechazado |
| Documento inválido | No numérico o ≠ 8 dígitos | Rechazado |
| Fecha pasada | Anterior a hoy | Rechazada |
