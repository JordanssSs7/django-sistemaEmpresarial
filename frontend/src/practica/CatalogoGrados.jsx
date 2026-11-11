import GradoCard from './GradoCard.jsx'

// Hijo de Practica: recibe la lista de grados ya filtrada y dibuja una tarjeta
// por grado con map() y key. Solo reenvía onAgregar a cada GradoCard.
function CatalogoGrados({ grados, onAgregar }) {
  if (grados.length === 0) {
    return <p className="vacio">No hay grados que coincidan</p>
  }

  return (
    <div className="grid">
      {grados.map((grado) => (
        <GradoCard key={grado.id} grado={grado} onAgregar={onAgregar} />
      ))}
    </div>
  )
}

export default CatalogoGrados
