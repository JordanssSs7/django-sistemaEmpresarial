# Frontend — Gestión de Matrículas y Pensiones (React + Vite)

Interfaz de la **Semana 9** del curso *Desarrollo de Aplicaciones Empresariales*.
Vive en `frontend/`, junto al backend Django (`src/`). Por ahora **no consume la API**:
los datos están escritos a mano en `src/App.jsx`, con la misma forma que las respuestas
de la API REST de la Semana 8. La conexión con la API se hace en la Semana 12.

## Requisitos

- Node.js LTS (incluye npm). Probado con Node 24 y npm 11.

## Instalar y ejecutar

```bash
cd frontend
npm install
npm run dev
```

Abrir http://localhost:5173/.

Otros comandos:

```bash
npm run lint    # revisa el código con oxlint
npm run build   # genera la carpeta dist/ (no se sube a Git)
```

## Qué muestra la interfaz

**Parte 1 — Aplicación de las Semanas 4 a 8**
- Resumen de pensión con expresiones `{ }` (`toFixed(2)`, función con descuento).
- Lista de **Cursos** con `map()` y `key`; ternario (`Agotado` / `Cupos: n`), `&&`
  (`¡Últimas plazas!`) y mensaje "No hay registros".
- Lista de **Estudiantes** con listas anidadas (observaciones e inscripciones) y
  promedio de notas calculado con JavaScript.

**Parte 2 — Investigación propia**
- Lista de **Años lectivos** (ternario por `estado`, `&&` para "Pensión alta").
- Lista de **Apoderados** con sus **hijos** anidados (relación 1:N) y la pensión
  mensual familiar calculada con JavaScript.

## Estructura

| Archivo | Papel |
|---|---|
| `index.html` | Única página; contiene `<div id="root">` |
| `src/main.jsx` | Monta React en `#root` (`App`, o `Practica` si la ruta es `/practica`) |
| `src/App.jsx` | Componente principal (JSX y datos) |
| `src/App.css`, `src/index.css` | Estilos (`className`) |
| `package.json` | Dependencias y scripts (equivale a `requirements.txt`) |
| `src/practica/` | Semana 11, Parte 1: mini catálogo con carrito |

## Semana 11 — Parte 1: comunicación entre componentes

Abrir http://localhost:5173/practica. Se aplica el mini catálogo con carrito de la guía
al sistema escolar: la secretaría elige **grados del año lectivo 2026** y arma la lista de
**matrículas por registrar** (por ejemplo, dos hermanos en el mismo grado).

| Componente | Recibe por props | Avisa al padre con |
|---|---|---|
| `Practica.jsx` (padre) | — | guarda `matriculas`, `busqueda` y `aviso` con `useState` |
| `Buscador.jsx` | `valor` | `onCambiar(texto)` |
| `CatalogoGrados.jsx` | `grados` (ya filtrados) | reenvía `onAgregar` |
| `GradoCard.jsx` | `grado` | `onAgregar(grado)` |
| `ListaMatricula.jsx` | `lineas` | `onQuitar(id)`, `onVaciar()` |
| `Aviso.jsx` | `aviso` | `onCerrar()` a los 3 s (`useEffect` + `clearTimeout`) |

- Los grados están en `src/practica/datos.js`, con `costo_matricula` como texto (igual que la API).
- El total y la cantidad de estudiantes se calculan con `reduce()`, sin `useState`.
- El estado se actualiza siempre con un arreglo nuevo (`map`, `filter`, spread); nunca con `push` ni `splice`.
- `ListaMatricula` cambia el título de la pestaña con `useEffect` cada vez que cambia la cantidad de estudiantes.
