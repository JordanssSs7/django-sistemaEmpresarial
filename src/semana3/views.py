from django.shortcuts import render


def index(request):
    """Página de inicio del módulo de gestión escolar (Semana 3)."""
    return render(request, "semana3/index.html")
