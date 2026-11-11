import { useEffect } from 'react'

// Ejercicio 8: muestra "Agregado: <grado>" y a los 3 segundos pide al padre
// que lo oculte. La función que devuelve el efecto limpia el temporizador si
// llega un aviso nuevo antes de tiempo o si el componente se desmonta.
function Aviso({ aviso, onCerrar }) {
  useEffect(() => {
    const temporizador = setTimeout(onCerrar, 3000)
    return () => clearTimeout(temporizador)
  }, [aviso, onCerrar])

  return <p className="aviso">Agregado: {aviso.nombre_grado}</p>
}

export default Aviso
