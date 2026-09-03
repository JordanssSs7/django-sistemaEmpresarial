from django.urls import path

from . import views

app_name = "semana3"

urlpatterns = [
    path("", views.index, name="index"),

    # Nivel educativo
    path("niveles/", views.nivel_list, name="nivel_list"),
    path("niveles/nuevo/", views.nivel_crear, name="nivel_crear"),

    # Año lectivo
    path("anios/", views.anio_list, name="anio_list"),
    path("anios/nuevo/", views.anio_crear, name="anio_crear"),

    # Tipo de descuento
    path("descuentos/", views.descuento_list, name="descuento_list"),
    path("descuentos/nuevo/", views.descuento_crear, name="descuento_crear"),

    # Método de pago
    path("metodos-pago/", views.metodo_list, name="metodo_list"),
    path("metodos-pago/nuevo/", views.metodo_crear, name="metodo_crear"),

    # Apoderado
    path("apoderados/", views.apoderado_list, name="apoderado_list"),
    path("apoderados/nuevo/", views.apoderado_crear, name="apoderado_crear"),

    # Grado (FK -> NivelEducativo)
    path("grados/", views.grado_list, name="grado_list"),
    path("grados/nuevo/", views.grado_crear, name="grado_crear"),

    # Estudiante (FK -> Apoderado)
    path("estudiantes/", views.estudiante_list, name="estudiante_list"),
    path("estudiantes/nuevo/", views.estudiante_crear, name="estudiante_crear"),

    # Matrícula (FK -> Estudiante, AnioLectivo, Grado)
    path("matriculas/", views.matricula_list, name="matricula_list"),
    path("matriculas/nueva/", views.matricula_crear, name="matricula_crear"),

    # Pensión (FK -> Matricula, TipoDescuento)
    path("pensiones/", views.pension_list, name="pension_list"),
    path("pensiones/nueva/", views.pension_crear, name="pension_crear"),

    # Pago (FK -> Pension, MetodoPago)
    path("pagos/", views.pago_list, name="pago_list"),
    path("pagos/nuevo/", views.pago_crear, name="pago_crear"),
]
