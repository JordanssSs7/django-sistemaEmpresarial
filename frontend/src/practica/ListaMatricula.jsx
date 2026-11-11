import { useEffect } from 'react'

// Hermano de CatalogoGrados (cumple el papel del "carrito"): recibe por props
// las matrículas por registrar y avisa al padre para quitar una línea
// (onQuitar) o vaciar la lista (onVaciar).
function ListaMatricula({ lineas, onQuitar, onVaciar }) {
  // Ejercicio 5: datos DERIVADOS. Se calculan en cada render a partir de las
  // props con reduce(); no necesitan useState porque dependen de `lineas`.
  const total = lineas.reduce((suma, l) => suma + Number(l.costo_matricula) * l.cantidad, 0)
  const estudiantes = lineas.reduce((suma, l) => suma + l.cantidad, 0)

  // Ejercicio 8: el efecto se ejecuta al montar y cada vez que cambia `estudiantes`.
  useEffect(() => {
    console.log('Efecto de la lista de matrícula, estudiantes =', estudiantes)
    document.title = `Matrículas (${estudiantes}) — Gestión escolar`
  }, [estudiantes])

  return (
    <aside className="carrito">
      <h2>📝 Matrículas por registrar</h2>

      {/* Ejercicio 6: mensaje con && cuando no hay líneas */}
      {lineas.length === 0 && <p className="vacio">No hay matrículas por registrar</p>}

      <ul>
        {lineas.map((l) => (
          <li key={l.id}>
            <span>
              {l.nombre_grado} × {l.cantidad}
              <small>S/ {(Number(l.costo_matricula) * l.cantidad).toFixed(2)}</small>
            </span>
            <button type="button" className="btn btn-quitar" onClick={() => onQuitar(l.id)}>
              Quitar
            </button>
          </li>
        ))}
      </ul>

      <p className="unidades">Estudiantes: {estudiantes}</p>
      <p className="total">Total: S/ {total.toFixed(2)}</p>

      {lineas.length > 0 && (
        <button type="button" className="btn btn-secundario" onClick={onVaciar}>
          Vaciar lista
        </button>
      )}
    </aside>
  )
}

export default ListaMatricula
