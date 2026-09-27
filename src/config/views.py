from django.shortcuts import render


def hub(request):
    """Menú principal: elegir a cuál de los 3 proyectos del curso entrar."""
    proyectos = [
        {
            "titulo": "Semana 1",
            "subtitulo": "Catálogo de Ítems",
            "descripcion": "Primer proyecto del curso: modelo, vista y template básicos con base de datos.",
            "url_name": "item_list",
            "icono": "bi-box-seam-fill",
            "color": "#3498db",
        },
        {
            "titulo": "Semana 2",
            "subtitulo": "Gestión de Citas Médicas",
            "descripcion": "Sistema de citas médicas con profesionales y horarios, persistido con Django ORM.",
            "url_name": "semana2_listado",
            "icono": "bi-heart-pulse-fill",
            "color": "#16a085",
        },
        {
            "titulo": "Semana 3",
            "subtitulo": "Sistema de Matrículas",
            "descripcion": "Sistema escolar con matrículas, pensiones y pagos.",
            "url_name": "semana3:index",
            "icono": "bi-mortarboard-fill",
            "color": "#8e44ad",
        },
    ]
    return render(request, "hub.html", {"proyectos": proyectos})
