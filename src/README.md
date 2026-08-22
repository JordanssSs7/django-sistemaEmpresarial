# Sistema Empresarial — Laboratorio Django (Clases, atributos y métodos)

## Descripción del proyecto
Primera versión de un "Sistema Empresarial" desarrollada como laboratorio del curso
**Desarrollo de Aplicaciones Empresariales**. Es una aplicación web en Django que gestiona
un catálogo simple de ítems (productos) mediante una app `core` con el modelo `Item`,
una vista que lista los ítems y un panel de administración.

## Tecnologías utilizadas
- Windows 11
- Python 3.14
- Django 5.2 (Django 5)
- Visual Studio Code
- Git / GitHub
- Entorno virtual de Python (`venv`)

## Requisitos previos
- Python 3.10 o superior instalado y disponible en el PATH.
- pip funcionando correctamente.
- Git instalado (opcional, para control de versiones).

## Estructura del proyecto
```
django_project/
├── venv/                     # entorno virtual (no se sube a Git)
└── src/
    ├── manage.py
    ├── config/                # configuración del proyecto
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── core/                  # app principal
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── views.py
    │   └── urls.py
    ├── templates/
    │   ├── base.html
    │   └── core/
    │       └── item_list.html
    ├── requirements.txt
    └── README.md
```

## Entorno virtual
El entorno virtual vive en `django_project/venv/`, separado del código fuente en `django_project/src/`.

Crear el entorno virtual (Windows PowerShell), desde `django_project/`:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## Instalación de dependencias
Con el entorno virtual activado, desde `django_project/src/`:
```powershell
pip install -r requirements.txt
```

## Migraciones
```powershell
python manage.py makemigrations
python manage.py migrate
```

## Creación del superusuario
```powershell
python manage.py createsuperuser
```
Se solicitará username, email (opcional) y contraseña de forma interactiva y segura.

## Ejecución del servidor
```powershell
python manage.py runserver
```

## Acceso al sitio
- Página principal (listado de ítems): http://127.0.0.1:8000/

## Acceso al administrador
- Panel de administración: http://127.0.0.1:8000/admin/
- Inicia sesión con las credenciales del superusuario creado anteriormente.
- Desde el admin puedes crear, editar y eliminar objetos `Item`.

## Modelo Item
Campos:
- `name`: texto (CharField).
- `description`: texto largo, opcional (TextField, blank/null).
- `created_at`: fecha/hora de creación automática (DateTimeField auto_now_add).

## Nota sobre seguridad
- No usar `DEBUG = True` en producción.
- No subir la carpeta `venv/`, `db.sqlite3` ni ningún secreto/credencial al repositorio.
