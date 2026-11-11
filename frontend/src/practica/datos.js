// Ejercicio 1: grados del año lectivo 2026 que la secretaría ofrece para
// matricular. Tienen la forma de la API de la Semana 8 (semana3): el costo de
// matrícula es un DecimalField y por eso llega como TEXTO ("250.00").
// `vacantes` cumple el papel del stock: con 0 vacantes el grado está lleno.
export const grados = [
  { id: 1, nombre_grado: '3 años', nivel_nombre: 'Inicial', costo_matricula: '180.00', vacantes: 12 },
  { id: 2, nombre_grado: '1ro de Primaria', nivel_nombre: 'Primaria', costo_matricula: '250.00', vacantes: 20 },
  { id: 3, nombre_grado: '6to de Primaria', nivel_nombre: 'Primaria', costo_matricula: '250.00', vacantes: 3 },
  { id: 4, nombre_grado: '1ro de Secundaria', nivel_nombre: 'Secundaria', costo_matricula: '300.00', vacantes: 0 },
  { id: 5, nombre_grado: '5to de Secundaria', nivel_nombre: 'Secundaria', costo_matricula: '300.00', vacantes: 8 },
]
