import axios from 'axios'

// Semana 12, Ejercicio 3: única instancia de Axios para todo el front-end.
// La dirección del servidor de Django se escribe solo aquí; los componentes
// usan rutas relativas como api.get('/cursos/').
// Semana 13: la matrícula en línea usará esta misma instancia, por ejemplo
// api.get('/grados/') desde pages/GradosPage.jsx.
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 5000, // si Django no responde en 5 s, la petición falla y cae en el catch
})

export default api
