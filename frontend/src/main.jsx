import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import ListaPractica from './practica/ListaPractica.jsx'
import Practica from './practica/Practica.jsx'

// Rutas de las prácticas:
//   /practica/cursos -> Semana 12, Parte 1 (Ajax con la API de cursos)
//   /practica        -> Semana 11, Parte 1 (comunicación entre componentes)
//   cualquier otra   -> interfaz de la Semana 9 (App)
const ruta = window.location.pathname

let pagina = <App />
if (ruta.startsWith('/practica/cursos')) pagina = <ListaPractica />
else if (ruta.startsWith('/practica')) pagina = <Practica />

createRoot(document.getElementById('root')).render(<StrictMode>{pagina}</StrictMode>)
