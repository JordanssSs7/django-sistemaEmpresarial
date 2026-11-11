import { useCallback, useState } from 'react'
import { grados } from './datos.js'
import Aviso from './Aviso.jsx'
import Buscador from './Buscador.jsx'
import CatalogoGrados from './CatalogoGrados.jsx'
import ListaMatricula from './ListaMatricula.jsx'
import '../App.css'
import './practica.css'

// Componente PADRE: guarda el estado compartido (matrículas por registrar,
// texto de búsqueda y aviso) y lo reparte a los hijos por props. Los hijos le
// avisan con funciones.
function Practica() {
  // Ejercicio 4: estado elevado. CatalogoGrados y ListaMatricula son hermanos
  // y ambos dependen de este arreglo, por eso vive en el padre común.
  const [matriculas, setMatriculas] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState(null)

  // Ejercicios 3 y 4: si el grado ya está en la lista, se aumenta su cantidad
  // con map(); si no, se agrega una línea nueva con spread. Nunca push.
  function agregarMatricula(grado) {
    console.log('Agregar matrícula en:', grado.nombre_grado)
    const existe = matriculas.some((l) => l.id === grado.id)
    if (existe) {
      setMatriculas(
        matriculas.map((l) => (l.id === grado.id ? { ...l, cantidad: l.cantidad + 1 } : l)),
      )
    } else {
      const linea = {
        id: grado.id,
        nombre_grado: grado.nombre_grado,
        costo_matricula: grado.costo_matricula,
        cantidad: 1,
      }
      setMatriculas([...matriculas, linea])
    }
    // Objeto nuevo en cada clic: así el efecto de Aviso se reinicia aunque se
    // agregue el mismo grado dos veces seguidas.
    setAviso({ nombre_grado: grado.nombre_grado, hora: Date.now() })
  }

  // Ejercicio 6: quitar con filter() y vaciar con un arreglo vacío (sin splice).
  function quitarMatricula(id) {
    setMatriculas(matriculas.filter((l) => l.id !== id))
  }

  function vaciarMatriculas() {
    setMatriculas([])
  }

  // useCallback mantiene la misma función entre renders; si cambiara en cada
  // render, el efecto de Aviso reiniciaría el temporizador al escribir en el buscador.
  const cerrarAviso = useCallback(() => setAviso(null), [])

  // Ejercicio 7: lista filtrada (dato derivado) por grado o nivel, sin
  // distinguir mayúsculas.
  const texto = busqueda.trim().toLowerCase()
  const gradosFiltrados = grados.filter(
    (g) =>
      g.nombre_grado.toLowerCase().includes(texto) || g.nivel_nombre.toLowerCase().includes(texto),
  )

  return (
    <>
      <header className="cabecera">
        <h1>Gestión de Matrículas y Pensiones</h1>
        <p className="tagline">Semana 11 · Parte 1: comunicación entre componentes</p>
      </header>

      <main className="contenido">
        {aviso && <Aviso aviso={aviso} onCerrar={cerrarAviso} />}

        <div className="practica-layout">
          <section>
            <h2>Grados del año lectivo 2026</h2>
            <Buscador valor={busqueda} onCambiar={setBusqueda} />
            <CatalogoGrados grados={gradosFiltrados} onAgregar={agregarMatricula} />
          </section>

          <ListaMatricula
            lineas={matriculas}
            onQuitar={quitarMatricula}
            onVaciar={vaciarMatriculas}
          />
        </div>
      </main>
    </>
  )
}

export default Practica
