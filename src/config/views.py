from django.shortcuts import render


def hub(request):
    """Menú principal: elegir a cuál de los 3 proyectos del curso entrar."""
    proyectos = [
        {
            "titulo": "Semana 1",
            "subtitulo": "Catálogo de Ítems",
            "descripcion": "Primer proyecto del curso: modelo, vista y template básicos con base de datos.",
            "url_name": "item_list",
        },
        {
            "titulo": "Semana 2",
            "subtitulo": "Gestión de Citas Médicas",
            "descripcion": "Sistema de citas médicas con profesionales y horarios, persistido con Django ORM.",
            "url_name": "semana2_listado",
        },
        {
            "titulo": "Semana 3",
            "subtitulo": "Gestión de Matrículas y Pensiones",
            "descripcion": "Sistema escolar con matrículas, pensiones y pagos, con relaciones 1:1, 1:N y N:M.",
            "url_name": "semana3:index",
        },
    ]
    return render(request, "hub.html", {"proyectos": proyectos})
