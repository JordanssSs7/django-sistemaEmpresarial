import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Practica from './practica/Practica.jsx'

// Semana 11, Parte 1: http://localhost:5173/practica muestra la práctica;
// cualquier otra ruta sigue mostrando la interfaz de la Semana 9 (App).
const esPractica = window.location.pathname.startsWith('/practica')

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {esPractica ? <Practica /> : <App />}
  </StrictMode>,
)
