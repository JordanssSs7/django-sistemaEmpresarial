import { useEffect, useState } from 'react'
import api from '../api.js'
import '../App.css'
import './practica.css'

// Convierte el JSON de errores del serializer ({"creditos": ["..."]}) en un texto.
function mensajeDeError(datos) {
  if (!datos || typeof datos !== 'object') return 'No se pudo guardar el curso.'
  return Object.entries(datos)
    .map(([campo, mensajes]) => `${campo}: ${[].concat(mensajes).join(' ')}`)
    .join(' · ')
}

// Semana 12, Parte 1: CRUD del recurso Curso (/api/cursos/ de la Semana 8)
// consumido con Ajax (Axios). Los datos ya no están escritos a mano: los
// entrega Django y React solo los pide y los dibuja.
function ListaPractica() {
  const [cursos, setCursos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)
  const [buscar, setBuscar] = useState('')

  // Formulario controlado del Ejercicio 6
  const [nombre, setNombre] = useState('')
  const [creditos, setCreditos] = useState('1')
  const [cupos, setCupos] = useState('30')
  const [errorForm, setErrorForm] = useState(null)

  // Ejercicios 4, 5 y 8: GET dentro de useEffect. La función del efecto no es
  // async (debe devolver nada o una limpieza, no una promesa), por eso se
  // declara una función async adentro y se llama al final.
  useEffect(() => {
    let ignorar = false // si llega otra búsqueda, se descarta la respuesta vieja

    async function cargarCursos() {
      setCargando(true)
      setError(null)
      try {
        const respuesta = await api.get('/cursos/', { params: { search: buscar } })
        if (!ignorar) setCursos(respuesta.data)
      } catch (err) {
        console.error('Error al cargar los cursos:', err.message)
        if (!ignorar) setError('No se pudo cargar la lista')
      } finally {
        if (!ignorar) setCargando(false)
      }
    }

    cargarCursos()
    return () => {
      ignorar = true
    }
  }, [buscar])

  // Ejercicio 6: POST. El curso que devuelve la API (ya con su id) se agrega
  // al estado con un arreglo nuevo.
  async function crearCurso(e) {
    e.preventDefault()
    setErrorForm(null)
    try {
      const respuesta = await api.post('/cursos/', {
        nombre,
        creditos: Number(creditos),
        cupos_disponibles: Number(cupos),
      })
      setCursos([...cursos, respuesta.data])
      setNombre('')
      setCreditos('1')
      setCupos('30')
    } catch (err) {
      // Error 400: err.response.data trae los mensajes del serializer
      setErrorForm(err.response ? mensajeDeError(err.response.data) : 'No hay conexión con el servidor.')
    }
  }

  // Ejercicio 7: PATCH. Solo se envía el campo que cambia; el estado se
  // actualiza con map() usando el curso que devuelve la API.
  async function cambiarCupos(curso, diferencia) {
    try {
      const respuesta = await api.patch(`/cursos/${curso.id}/`, {
        cupos_disponibles: curso.cupos_disponibles + diferencia,
      })
      setCursos(cursos.map((c) => (c.id === curso.id ? respuesta.data : c)))
    } catch (err) {
      setError(err.response ? mensajeDeError(err.response.data) : 'No se pudo actualizar el curso.')
    }
  }

  // Ejercicio 7: DELETE. Recién cuando Django responde 204 se quita del estado.
  async function eliminarCurso(id) {
    try {
      const respuesta = await api.delete(`/cursos/${id}/`)
      if (respuesta.status === 204) {
        setCursos(cursos.filter((c) => c.id !== id))
      }
    } catch (err) {
      setError(err.response?.status === 404 ? 'El curso ya no existe.' : 'No se pudo eliminar el curso.')
    }
  }

  return (
    <>
      <header className="cabecera">
        <h1>Gestión de Matrículas y Pensiones</h1>
        <p className="tagline">Semana 12 · Parte 1: Ajax con la API de cursos (/api/cursos/)</p>
      </header>

      <main className="contenido">
        <h2>Nuevo curso</h2>
        <form className="form-practica" onSubmit={crearCurso}>
          <label>
            Nombre
            <input value={nombre} onChange={(e) => setNombre(e.target.value)} required />
          </label>
          <label>
            Créditos
            <input type="number" value={creditos} onChange={(e) => setCreditos(e.target.value)} />
          </label>
          <label>
            Cupos
            <input type="number" min="0" value={cupos} onChange={(e) => setCupos(e.target.value)} />
          </label>
          <button type="submit" className="btn btn-primario">
            Guardar
          </button>
        </form>
        {errorForm && <p className="error-api">{errorForm}</p>}

        <h2>Cursos</h2>
        {/* Ejercicio 8: el texto viaja a la API como ?search= */}
        <input
          type="text"
          className="buscador"
          placeholder="Buscar curso por nombre..."
          value={buscar}
          onChange={(e) => setBuscar(e.target.value)}
        />

        {/* Ejercicio 5: los tres estados de la pantalla */}
        {cargando && <p className="vacio">Cargando...</p>}
        {!cargando && error && <p className="error-api">{error}</p>}
        {!cargando && !error && cursos.length === 0 && (
          <p className="vacio">{buscar ? 'No hay cursos que coincidan con la búsqueda' : 'No hay cursos registrados'}</p>
        )}

        {!cargando && !error && cursos.length > 0 && (
          <table className="tabla-practica">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Créditos</th>
                <th>Cupos</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {cursos.map((curso) => (
                <tr key={curso.id}>
                  <td>{curso.id}</td>
                  <td>{curso.nombre}</td>
                  <td>{curso.creditos}</td>
                  <td>{curso.cupos_disponibles}</td>
                  <td className="acciones">
                    <button type="button" className="btn btn-secundario" onClick={() => cambiarCupos(curso, 1)}>
                      +1 cupo
                    </button>
                    <button
                      type="button"
                      className="btn btn-secundario"
                      disabled={curso.cupos_disponibles === 0}
                      onClick={() => cambiarCupos(curso, -1)}
                    >
                      −1 cupo
                    </button>
                    <button type="button" className="btn btn-quitar" onClick={() => eliminarCurso(curso.id)}>
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </main>
    </>
  )
}

export default ListaPractica
