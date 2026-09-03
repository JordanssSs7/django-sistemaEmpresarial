from django.urls import path

from . import views

app_name = "semana3"

urlpatterns = [
    path("", views.index, name="index"),

    # Nivel educativo
    path("niveles/", views.nivel_list, name="nivel_list"),
    path("niveles/nuevo/", views.nivel_crear, name="nivel_crear"),
    path("niveles/<int:pk>/editar/", views.nivel_editar, name="nivel_editar"),
    path("niveles/<int:pk>/eliminar/", views.nivel_eliminar, name="nivel_eliminar"),

    # Año lectivo
    path("anios/", views.anio_list, name="anio_list"),
    path("anios/nuevo/", views.anio_crear, name="anio_crear"),
    path("anios/<int:pk>/editar/", views.anio_editar, name="anio_editar"),
    path("anios/<int:pk>/eliminar/", views.anio_eliminar, name="anio_eliminar"),

    # Tipo de descuento
    path("descuentos/", views.descuento_list, name="descuento_list"),
    path("descuentos/nuevo/", views.descuento_crear, name="descuento_crear"),
    path("descuentos/<int:pk>/editar/", views.descuento_editar, name="descuento_editar"),
    path("descuentos/<int:pk>/eliminar/", views.descuento_eliminar, name="descuento_eliminar"),

    # Método de pago
    path("metodos-pago/", views.metodo_list, name="metodo_list"),
    path("metodos-pago/nuevo/", views.metodo_crear, name="metodo_crear"),
    path("metodos-pago/<int:pk>/editar/", views.metodo_editar, name="metodo_editar"),
    path("metodos-pago/<int:pk>/eliminar/", views.metodo_eliminar, name="metodo_eliminar"),

    # Apoderado
    path("apoderados/", views.apoderado_list, name="apoderado_list"),
    path("apoderados/nuevo/", views.apoderado_crear, name="apoderado_crear"),
    path("apoderados/<int:pk>/editar/", views.apoderado_editar, name="apoderado_editar"),
    path("apoderados/<int:pk>/eliminar/", views.apoderado_eliminar, name="apoderado_eliminar"),

    # Grado (FK -> NivelEducativo)
    path("grados/", views.grado_list, name="grado_list"),
    path("grados/nuevo/", views.grado_crear, name="grado_crear"),
    path("grados/<int:pk>/editar/", views.grado_editar, name="grado_editar"),
    path("grados/<int:pk>/eliminar/", views.grado_eliminar, name="grado_eliminar"),

    # Estudiante (FK -> Apoderado)
    path("estudiantes/", views.estudiante_list, name="estudiante_list"),
    path("estudiantes/nuevo/", views.estudiante_crear, name="estudiante_crear"),
    path("estudiantes/<int:pk>/editar/", views.estudiante_editar, name="estudiante_editar"),
    path("estudiantes/<int:pk>/eliminar/", views.estudiante_eliminar, name="estudiante_eliminar"),

    # Matrícula (FK -> Estudiante, AnioLectivo, Grado)
    path("matriculas/", views.matricula_list, name="matricula_list"),
    path("matriculas/nueva/", views.matricula_crear, name="matricula_crear"),
    path("matriculas/<int:pk>/editar/", views.matricula_editar, name="matricula_editar"),
    path("matriculas/<int:pk>/eliminar/", views.matricula_eliminar, name="matricula_eliminar"),

    # Pensión (FK -> Matricula, TipoDescuento)
    path("pensiones/", views.pension_list, name="pension_list"),
    path("pensiones/nueva/", views.pension_crear, name="pension_crear"),
    path("pensiones/<int:pk>/editar/", views.pension_editar, name="pension_editar"),
    path("pensiones/<int:pk>/eliminar/", views.pension_eliminar, name="pension_eliminar"),

    # Pago (FK -> Pension, MetodoPago)
    path("pagos/", views.pago_list, name="pago_list"),
    path("pagos/nuevo/", views.pago_crear, name="pago_crear"),
    path("pagos/<int:pk>/editar/", views.pago_editar, name="pago_editar"),
    path("pagos/<int:pk>/eliminar/", views.pago_eliminar, name="pago_eliminar"),
]
