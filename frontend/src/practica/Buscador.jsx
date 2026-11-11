// Ejercicio 7: campo de texto CONTROLADO. El texto no vive aquí sino en
// Practica: llega por `valor` y cada tecla se avisa al padre con onCambiar.
function Buscador({ valor, onCambiar }) {
  return (
    <input
      type="text"
      className="buscador"
      placeholder="Buscar grado o nivel..."
      value={valor}
      onChange={(e) => onCambiar(e.target.value)}
    />
  )
}

export default Buscador
