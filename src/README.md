# 🏢 Sistema Empresarial — Gestión de Ítems con Django

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/uso-académico-lightgrey)

Laboratorio del curso **Desarrollo de Aplicaciones Empresariales** — unidad de *Clases,
atributos y métodos*. Implementa la primera versión de un sistema empresarial capaz de
registrar y listar un catálogo de ítems (productos), aplicando el patrón **MVT** de Django
a través de un modelo `Item`, una vista de listado y un panel administrativo.

> Autor: **Jordan Reyes** · Repositorio del laboratorio, no afiliado a otros proyectos similares.

## Índice

- [Requisitos y stack técnico](#-requisitos-y-stack-técnico)
- [Organización de carpetas](#️-organización-de-carpetas)
- [Instalación](#️-instalación)
- [Puesta en marcha](#️-puesta-en-marcha)
- [Modelo Item](#-modelo-item)

## 🧩 Requisitos y stack técnico

**Antes de empezar necesitas**

| Herramienta | Notas |
|---|---|
| Python 3.10+ | Marcar **"Add Python to PATH"** durante la instalación |
| Git | Para control de versiones |
| Visual Studio Code | Editor recomendado |

**Con qué está construido**

| Capa | Tecnología |
|---|---|
| Framework web | Django 5.2 |
| Frontend | HTML5 & CSS3 |
| Base de datos | SQLite3 |

## 🗂️ Organización de carpetas

```text
django_project/
├── .gitignore              # Ignora el entorno virtual venv/ y archivos temporales
│
├── venv/                    # Entorno virtual de Python (no se sube a Git)
│
└── src/                      # Código fuente del proyecto
    ├── manage.py              # Script principal (servidor y migraciones)
    ├── requirements.txt       # Dependencias del proyecto
    ├── README.md               # Este documento
    │
    ├── config/                 # Configuración global de Django
    │   ├── settings.py          # Apps, base de datos, plantillas
    │   ├── urls.py               # Enrutador principal de URLs
    │   ├── asgi.py                # Configuración ASGI
    │   └── wsgi.py                # Configuración WSGI / despliegue
    │
    └── core/                    # Aplicación principal del catálogo
        ├── models.py             # Modelo Item
        ├── views.py               # Vista item_list
        ├── urls.py                 # Rutas del catálogo
        ├── admin.py                 # Registro de Item en el admin
        ├── migrations/               # Migraciones de la base de datos
        └── templates/
            ├── base.html             # Estructura base, navegación y footer
            └── core/
                └── item_list.html      # Listado de ítems (for / empty)
```

## ⚙️ Instalación

**1. Clonar el repositorio**

```powershell
git clone <URL-del-repositorio>
cd django_project
```

**2. Crear y activar el entorno virtual**

```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**3. Instalar las dependencias**

```powershell
pip install --upgrade pip
pip install -r src/requirements.txt
```

## ▶️ Puesta en marcha

**1. Aplicar las migraciones de la base de datos**

```powershell
cd src
python manage.py migrate
```

**2. Crear un superusuario (para acceder al admin)**

```powershell
python manage.py createsuperuser
```

**3. Iniciar el servidor de desarrollo**

```powershell
python manage.py runserver
```

**4. Abrir la aplicación en el navegador**

| Ruta | URL |
|---|---|
| Catálogo Principal (Inicio) | http://127.0.0.1:8000/ |
| Panel Administrativo | http://127.0.0.1:8000/admin/ |

## 📦 Modelo Item

| Campo | Tipo | Detalle |
|---|---|---|
| `name` | `CharField` | Nombre del ítem |
| `description` | `TextField` | Descripción larga, opcional (`blank`, `null`) |
| `created_at` | `DateTimeField` | Fecha/hora de creación automática (`auto_now_add`) |

## 🔒 Nota sobre seguridad

- No usar `DEBUG = True` en producción.
- No subir la carpeta `venv/`, `db.sqlite3` ni ningún secreto/credencial al repositorio.
