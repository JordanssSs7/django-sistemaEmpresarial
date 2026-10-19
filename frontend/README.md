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
| `src/main.jsx` | Monta React en `#root` |
| `src/App.jsx` | Componente principal (JSX y datos) |
| `src/App.css`, `src/index.css` | Estilos (`className`) |
| `package.json` | Dependencias y scripts (equivale a `requirements.txt`) |
