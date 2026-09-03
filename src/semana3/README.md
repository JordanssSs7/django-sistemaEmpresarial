# 🎓 Semana 3 — Gestión de Matrículas y Pensiones

App Django **con base de datos** (SQLite + ORM + migraciones). Conectada al mismo Project
(`config`) que `semana1` y `semana2`, bajo el prefijo de rutas `/semana3/`.

A diferencia de la Semana 2 (datos en memoria), aquí toda la información se guarda de forma
persistente: los registros se mantienen aunque se reinicie el servidor.

## 1. Problemática

Los colegios enfrentan cuellos de botella y pérdidas financieras al gestionar matrículas,
documentos y el cobro mensual de pensiones mediante procesos manuales como hojas de Excel. Esta
falta de automatización genera errores en el cálculo de descuentos por hermanos, demoras al
validar comprobantes bancarios y una alta morosidad difícil de rastrear.

**Usuarios:**
- Personal administrativo / secretaría: registra estudiantes y apoderados, realiza matrículas.
- Personal de tesorería / caja: configura años lectivos y pensiones, valida los comprobantes.
- Apoderados: consultan el estado de las cuotas y registran pagos con su voucher.

**Proceso que se mejora:** el ciclo de cobranza escolar — apertura del año lectivo → matrícula →
generación automática de las 10 cuotas → registro del pago → validación del comprobante →
actualización del estado de la cuota.

## 2. Requisitos funcionales

| # | Requisito | Operación |
|---|---|---|
| 1 | Registrar estudiantes y apoderados, asociándolos bajo una misma estructura familiar | CREATE |
| 2 | Buscar, filtrar y listar estudiantes por año lectivo, grado y estado | READ |
| 3 | Actualizar los datos personales y de contacto del estudiante o apoderado | UPDATE |
| 4 | Cambiar el estado de un estudiante a "Inactivo" o "Retirado" sin eliminar su historial | UPDATE |
| 5 | Aperturar un nuevo año escolar definiendo costo de matrícula y monto de pensiones | CREATE |
| 6 | Matricular a un estudiante asignándole un grado dentro del año lectivo vigente | CREATE |
| 7 | Generar automáticamente las 10 cuotas de pensión al confirmar la matrícula | CREATE |
| 8 | Crear y modificar tipos de descuento (segundo hermano, pronto pago, beca) | CREATE + UPDATE |
| 9 | Eliminar o desactivar una regla de descuento del catálogo | DELETE |
| 10 | Registrar un pago con su comprobante y validarlo (Aprobado/Rechazado), actualizando la pensión | CREATE + UPDATE |

## 3. Modelo de datos (10 entidades)

### Independientes (sin ForeignKey)

| Entidad | Campos |
|---|---|
| **NivelEducativo** | `nombre_nivel` (único), `descripcion` |
| **AnioLectivo** | `anio` (único), `fecha_inicio`, `fecha_fin`, `costo_matricula`, `monto_pension`, `estado` |
| **TipoDescuento** | `nombre`, `porcentaje`, `activo` (bool) |
| **MetodoPago** | `nombre_metodo` (único), `requiere_voucher` (bool) |
| **Apoderado** | `num_documento` (único), `nombres`, `apellidos`, `telefono`, `correo` |

### Relacionadas (con ForeignKey)

| Entidad | Campos | ForeignKey → `on_delete` |
|---|---|---|
| **Grado** | `nombre_grado` | `nivel` → NivelEducativo (`PROTECT`) |
| **Estudiante** | `codigo_alumno` (único), `num_documento` (único), `nombres`, `apellidos`, `fecha_nacimiento`, `estado` | `apoderado` → Apoderado (`PROTECT`) |
| **Matricula** | `fecha_registro` (auto), `costo_matricula`, `estado_matricula` | `estudiante`, `anio_lectivo`, `grado` (`PROTECT`) |
| **Pension** | `num_cuota`, `monto_base`, `monto_final` *(calculado)*, `fecha_vencimiento`, `estado_pago` | `matricula` (`CASCADE`), `tipo_descuento` (`SET_NULL`, opcional) |
| **Pago** | `fecha_operacion`, `num_operacion` (único), `monto_pagado`, `comprobante_url`, `estado_validacion`, `fecha_registro` (auto) | `pension`, `metodo_pago` (`PROTECT`) |

La clave primaria (`id`) la gestiona Django automáticamente en todas las entidades.
`monto_final` y `costo_matricula` (de Matricula) los calcula la vista, no el usuario.

## 4. Puesta en marcha

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r src\requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

| Ruta | Descripción |
|---|---|
| `/semana3/` | Menú del módulo |
| `/semana3/niveles/` · `/anios/` · `/descuentos/` · `/metodos-pago/` · `/apoderados/` | Catálogos (CRUD) |
| `/semana3/grados/` · `/estudiantes/` · `/matriculas/` · `/pensiones/` · `/pagos/` | Entidades relacionadas (CRUD) |
| `<entidad>/nuevo/` · `<entidad>/<id>/editar/` · `<entidad>/<id>/eliminar/` | Crear / editar / eliminar |

## 5. Flujo de persistencia (ORM ↔ SQL)

**Caso CREATE — registrar una matrícula:**

| Etapa | Dónde ocurre |
|---|---|
| Request | `POST /semana3/matriculas/nueva/` con los datos del formulario |
| URL | `config/urls.py` → `semana3/urls.py` → `views.matricula_crear` |
| View | `MatriculaForm` valida; se copia `costo_matricula` del año lectivo |
| Model / ORM | `matricula.save()` → `INSERT`; `Pension.objects.bulk_create([...])` → 10 `INSERT` |
| SQLite | Se persisten la matrícula y sus 10 cuotas |
| Response | `redirect` al listado, que muestra la matrícula ya guardada |

**Equivalencia ORM → SQL:**

| ORM | SQL |
|---|---|
| `Model.objects.all()` | `SELECT * FROM ...` |
| `.filter(campo=valor)` | `... WHERE campo = valor` |
| `.order_by("campo")` | `... ORDER BY campo` |
| `form.save()` (nuevo) | `INSERT INTO ...` |
| `form.save()` (con `instance=`) | `UPDATE ... WHERE id = ?` |
| `objeto.delete()` | `DELETE FROM ... WHERE id = ?` |

## 6. Convivencia con `semana1` y `semana2`

Las tres apps están en `INSTALLED_APPS` del mismo Project `config` y comparten `templates/base.html`.
`config/urls.py` reparte las rutas: `/` para semana2, `/semana1/`, `/semana3/`. Cada app tiene su
propio `urls.py`, `models.py` y migraciones. `semana3` y `semana1` comparten `db.sqlite3` pero con
tablas distintas (`semana3_*`, `semana1_*`); `semana2` no usa base de datos.

## 7. Casos de prueba

| Caso | Entrada | Resultado esperado |
|---|---|---|
| CREATE simple | Nivel educativo con nombre válido | Se guarda, aparece en el listado |
| CREATE con lógica | Confirmar una matrícula | Se generan automáticamente 10 cuotas de pensión |
| CREATE — descuento | Pensión con `tipo_descuento` de 15% sobre 280 | `monto_final` = 238.00 |
| READ — filtro | `/pensiones/?estado=PENDIENTE` | Solo cuotas pendientes |
| UPDATE — baja lógica | Estudiante: estado → "Retirado" | Cambia el estado, no se borra el registro |
| UPDATE — validación | Pago: estado → "Aprobado" | La pensión asociada pasa a "Pagada" |
| DELETE real | Eliminar un método de pago sin uso | Desaparece de SQLite |
| DELETE — PROTECT | Eliminar un apoderado con estudiantes | Se rechaza con mensaje de error |
| DELETE — CASCADE | Eliminar una matrícula | Se eliminan también sus 10 cuotas |
| Validación unique | Año lectivo con `anio` duplicado | Rechazado por el formulario |
