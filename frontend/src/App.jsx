import './App.css'

// Ejercicio 4: primer JSX con expresiones entre llaves { }
const nombreApp = 'Gestión de Matrículas y Pensiones'

// Función que se llama dentro del JSX: pensión con descuento, con 2 decimales
function pensionConDescuento(monto, porcentaje) {
  return (monto - (monto * porcentaje) / 100).toFixed(2)
}

// Ejercicio 5: datos escritos a mano con la MISMA forma que la respuesta de
// GET /api/cursos/ (Semana 8): id, nombre, creditos, cupos_disponibles.
const cursos = [
  { id: 1, nombre: 'Matemática', creditos: 4, cupos_disponibles: 12 },
  { id: 2, nombre: 'Comunicación', creditos: 4, cupos_disponibles: 0 },
  { id: 3, nombre: 'Ciencia y Tecnología', creditos: 3, cupos_disponibles: 2 },
  { id: 4, nombre: 'Historia', creditos: 2, cupos_disponibles: 25 },
  { id: 5, nombre: 'Educación Física', creditos: 1, cupos_disponibles: 30 },
]

// Ejercicio 7: relación 1:N. Forma de GET /api/estudiantes/ (Semana 8): cada
// estudiante trae su arreglo `observaciones`. Se agrega además `inscripciones`
// (modelo intermedio CursoEstudiante) para usar nota_final, que es un decimal
// y llega como TEXTO ("15.50"); no forma parte de la API actual.
const estudiantes = [
  {
    id: 1,
    codigo_alumno: 'A-001',
    nombres: 'Lucía',
    apellidos: 'Ramírez Soto',
    estado: 'ACTIVO',
    observaciones: [
      { id: 1, fecha: '2026-03-10', tipo: 'ACADEMICA', descripcion: 'Destaca en Matemática' },
      { id: 2, fecha: '2026-04-02', tipo: 'CONDUCTUAL', descripcion: 'Llegó tarde dos veces' },
    ],
    inscripciones: [
      { id: 1, curso: 'Matemática', nota_final: '16.50' },
      { id: 2, curso: 'Historia', nota_final: '14.00' },
    ],
  },
  {
    id: 2,
    codigo_alumno: 'A-002',
    nombres: 'Diego',
    apellidos: 'Torres Vega',
    estado: 'ACTIVO',
    observaciones: [
      { id: 3, fecha: '2026-03-15', tipo: 'ADMINISTRATIVA', descripcion: 'Documentos pendientes' },
    ],
    inscripciones: [
      { id: 3, curso: 'Comunicación', nota_final: '12.75' },
      { id: 4, curso: 'Educación Física', nota_final: '18.00' },
      { id: 5, curso: 'Matemática', nota_final: '11.25' },
    ],
  },
  {
    id: 3,
    codigo_alumno: 'A-003',
    nombres: 'Camila',
    apellidos: 'Flores Díaz',
    estado: 'RETIRADO',
    observaciones: [],
    inscripciones: [],
  },
]

// Total por registro calculado con JavaScript: promedio de notas (texto -> número)
function promedioNotas(inscripciones) {
  if (inscripciones.length === 0) return null
  const suma = inscripciones.reduce((acc, i) => acc + Number(i.nota_final), 0)
  return (suma / inscripciones.length).toFixed(2)
}


// Ejercicio 8: color del borde según el estado (se aplica con style={{ }})
const colorEstado = {
  ACTIVO: '#27ae60',
  INACTIVO: '#f39c12',
  RETIRADO: '#c0392b',
}

// ===========================================================================
// PARTE 2 — Investigación propia (Ejercicios 10 al 12)
// Entidades: AnioLectivo y Apoderado. Relación 1:N Apoderado -> Estudiantes.
// Los hijos tienen la forma de GET /api/estudiantes/ (Semana 8); los decimales
// de AnioLectivo van como TEXTO, igual que los entrega DRF.
// ===========================================================================
const aniosLectivos = [
  { id: 1, anio: 2026, costo_matricula: '250.00', monto_pension: '420.00', estado: 'ACTIVO' },
  { id: 2, anio: 2025, costo_matricula: '230.00', monto_pension: '380.00', estado: 'CERRADO' },
  { id: 3, anio: 2024, costo_matricula: '210.00', monto_pension: '350.00', estado: 'CERRADO' },
]

const apoderados = [
  {
    id: 1,
    nombres: 'Marta',
    apellidos: 'Escobar Ruiz',
    telefono: '987654321',
    correo: 'marta.escobar@correo.com',
    estudiantes: [
      { id: 3, codigo_alumno: 'AL-003', nombres: 'Juanito', apellidos: 'Escobar', estado: 'INACTIVO' },
      { id: 5, codigo_alumno: 'AL-005', nombres: 'Sofía', apellidos: 'Escobar', estado: 'ACTIVO' },
    ],
  },
  {
    id: 2,
    nombres: 'Carlos',
    apellidos: 'Polo Díaz',
    telefono: '',
    correo: '',
    estudiantes: [
      { id: 4, codigo_alumno: 'AL-004', nombres: 'Pablo', apellidos: 'Polo', estado: 'ACTIVO' },
    ],
  },
  {
    id: 3,
    nombres: 'Rosa',
    apellidos: 'Vega Soto',
    telefono: '912345678',
    correo: 'rosa.vega@correo.com',
    estudiantes: [],
  },
]

// Pensión mensual de la familia: solo cuentan los hijos ACTIVOS (texto -> número)
function pensionFamiliar(apoderado, pensionMensual) {
  const activos = apoderado.estudiantes.filter((e) => e.estado === 'ACTIVO').length
  return (activos * Number(pensionMensual)).toFixed(2)
}

function App() {
  const montoPension = 350
  const descuento = 15
  const anioActivo = aniosLectivos.find((a) => a.estado === 'ACTIVO')

  return (
    <>
      <header className="cabecera">
        {/* Expresión 1: una variable */}
        <h1>{nombreApp}</h1>
        <p className="tagline">Interfaz React · datos escritos a mano (Semana 9)</p>
      </header>

      <main className="contenido">
        {/* Expresión 2: un cálculo y una llamada a función */}
        <section className="resumen">
          <div className="dato">
            <span>Pensión base</span>
            <strong>S/ {montoPension.toFixed(2)}</strong>
          </div>
          <div className="dato">
            <span>Con {descuento}% de descuento</span>
            <strong>S/ {pensionConDescuento(montoPension, descuento)}</strong>
          </div>
          <div className="dato">
            <span>Total anual (10 cuotas)</span>
            <strong>S/ {(montoPension * 10).toFixed(2)}</strong>
          </div>
        </section>

        <h2>Cursos</h2>
        {/* map() recorre el arreglo, como {% for curso in cursos %} en Django.
            key={curso.id} permite a React identificar cada tarjeta. */}
        {/* Ejercicio 6: mensaje de lista vacía con && (se prueba vaciando el arreglo) */}
        {cursos.length === 0 && <p className="vacio">No hay registros</p>}
        <div className="grid">
          {cursos.map((curso) => (
            <article className="tarjeta" key={curso.id}>
              <h3>{curso.nombre}</h3>
              <p className="meta">{curso.creditos} créditos</p>
              {/* Ternario: si no quedan cupos muestra "Agotado", si no, el número */}
              {curso.cupos_disponibles === 0 ? (
                <span className="badge badge-agotado">Agotado</span>
              ) : (
                <span className="badge badge-ok">Cupos: {curso.cupos_disponibles}</span>
              )}
              {/* &&: solo se dibuja si quedan entre 1 y 3 cupos */}
              {curso.cupos_disponibles > 0 && curso.cupos_disponibles <= 3 && (
                <span className="badge badge-alerta">¡Últimas plazas!</span>
              )}
            </article>
          ))}
        </div>

        <h2>Estudiantes</h2>
        {estudiantes.length === 0 && <p className="vacio">No hay registros</p>}
        {/* map() EXTERNO: una tarjeta por estudiante, con su propia key */}
        <div className="lista-estudiantes">
          {estudiantes.map((est) => (
            <article
              className="tarjeta estudiante"
              key={est.id}
              style={{ borderLeft: `6px solid ${colorEstado[est.estado]}` }}
            >
              <h3>
                {est.nombres} {est.apellidos}
                <small> · {est.codigo_alumno} · {est.estado}</small>
              </h3>

              <div className="columnas">
                <div>
                  {/* map() INTERNO: observaciones de ESTE estudiante (1:N) */}
                  <h4>Observaciones ({est.observaciones.length})</h4>
                  {est.observaciones.length === 0 && <p className="vacio">Sin observaciones</p>}
                  <ul>
                    {est.observaciones.map((obs) => (
                      <li key={obs.id}>
                        <span className="fecha">{obs.fecha}</span> [{obs.tipo}] {obs.descripcion}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  {/* map() INTERNO: inscripciones (texto -> Number().toFixed(2)) */}
                  <h4>
                    Cursos inscritos ({est.inscripciones.length})
                    {est.inscripciones.length > 0 && (
                      <span className="badge badge-ok">
                        Promedio {promedioNotas(est.inscripciones)}
                      </span>
                    )}
                  </h4>
                  {est.inscripciones.length === 0 && <p className="vacio">Sin inscripciones</p>}
                  <ul>
                    {est.inscripciones.map((ins) => (
                      <li key={ins.id}>
                        {ins.curso}: <strong>{Number(ins.nota_final).toFixed(2)}</strong>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </article>
          ))}
        </div>

        {/* ================= PARTE 2: investigación propia ================= */}
        <h2 className="titulo-parte">Parte 2 · Investigación propia</h2>

        <h2>Años lectivos</h2>
        {/* Ejercicio 11: mensaje de lista vacía */}
        {aniosLectivos.length === 0 && <p className="vacio">No hay registros</p>}
        <div className="grid">
          {aniosLectivos.map((a) => (
            <article className="tarjeta" key={a.id}>
              <h3>Año {a.anio}</h3>
              <p className="meta">
                Matrícula S/ {Number(a.costo_matricula).toFixed(2)} · Pensión S/{' '}
                {Number(a.monto_pension).toFixed(2)}
              </p>
              {/* Ternario sobre el campo estado */}
              {a.estado === 'ACTIVO' ? (
                <span className="badge badge-ok">Matrículas abiertas</span>
              ) : (
                <span className="badge badge-agotado">Año cerrado</span>
              )}
              {/* &&: solo si la pensión supera S/ 400 */}
              {Number(a.monto_pension) > 400 && (
                <span className="badge badge-alerta">Pensión alta</span>
              )}
            </article>
          ))}
        </div>

        <h2>Apoderados y sus hijos</h2>
        {apoderados.length === 0 && <p className="vacio">No hay registros</p>}
        {/* map() EXTERNO: apoderados. map() INTERNO: sus estudiantes (1:N) */}
        <div className="lista-estudiantes">
          {apoderados.map((ap) => (
            <article
              className="tarjeta estudiante"
              key={ap.id}
              style={{ borderLeft: `6px solid ${ap.estudiantes.length > 0 ? '#3498db' : '#9ca3af'}` }}
            >
              <h3>
                {ap.nombres} {ap.apellidos}
                <small> · {ap.correo || 'Sin correo'} · {ap.telefono || 'Sin teléfono'}</small>
              </h3>
              <h4>
                Hijos ({ap.estudiantes.length})
                {anioActivo && ap.estudiantes.length > 0 && (
                  <span className="badge badge-ok">
                    Pensión mensual S/ {pensionFamiliar(ap, anioActivo.monto_pension)}
                  </span>
                )}
              </h4>
              {ap.estudiantes.length === 0 && <p className="vacio">Sin estudiantes registrados</p>}
              <ul>
                {ap.estudiantes.map((e) => (
                  <li key={e.id}>
                    <strong>{e.codigo_alumno}</strong> — {e.nombres} {e.apellidos} ({e.estado})
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </main>
    </>
  )
}

export default App
