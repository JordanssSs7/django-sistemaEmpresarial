// Hijo: muestra UN grado que recibe por props. No guarda estado ni puede
// cambiar `grado` (las props son de solo lectura); solo avisa al padre.
function GradoCard({ grado, onAgregar }) {
  const sinVacantes = grado.vacantes === 0

  return (
    <article className="tarjeta">
      <h3>
        {grado.nombre_grado} <small>· {grado.nivel_nombre}</small>
      </h3>
      {/* El costo llega como texto: se convierte a número para mostrar 2 decimales */}
      <p className="meta">Matrícula S/ {Number(grado.costo_matricula).toFixed(2)}</p>
      {sinVacantes ? (
        <span className="badge badge-agotado">Sin vacantes</span>
      ) : (
        <span className="badge badge-ok">Vacantes: {grado.vacantes}</span>
      )}

      {/* Ejercicio 3: se pasa una FUNCIÓN flecha; React la ejecuta solo al hacer clic.
          Escribir onClick={onAgregar(grado)} la ejecutaría al dibujar la tarjeta. */}
      <button
        type="button"
        className="btn btn-primario"
        disabled={sinVacantes}
        onClick={() => onAgregar(grado)}
      >
        Agregar
      </button>
    </article>
  )
}

export default GradoCard
