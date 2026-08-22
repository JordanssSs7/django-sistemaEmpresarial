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
- [Reto opcional](#-reto-opcional)
- [Implementaciones avanzadas asistidas por IA](#-implementaciones-avanzadas-asistidas-por-ia-agente-claude--vs-code)
- [Resultados de la implementación con el Agente de IA](#-resultados-de-la-implementación-con-el-agente-de-ia)
- [Documentación y publicación del proyecto](#-documentación-y-publicación-del-proyecto)

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
        ├── views.py               # item_list, item_list_api, api_demo
        ├── urls.py                 # Rutas del catálogo y de la API
        ├── admin.py                 # Registro de Item en el admin
        ├── migrations/               # Migraciones de la base de datos
        └── templates/
            ├── base.html             # Estructura base, estilos CSS y navegación
            └── core/
                ├── item_list.html      # Catálogo con tarjetas y buscador JS
                └── api_demo.html         # Página de demostración de la API
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

| Ruta | URL | Descripción |
|---|---|---|
| Catálogo principal | http://127.0.0.1:8000/ | Listado de ítems con buscador en tiempo real |
| API de ítems | http://127.0.0.1:8000/api/items/ | Ítems en formato JSON, ordenados por fecha de creación |
| Demo de la API | http://127.0.0.1:8000/api-demo/ | Consume la API con `fetch` y muestra el resultado |
| Panel administrativo | http://127.0.0.1:8000/admin/ | Alta, edición y borrado de ítems |

## 📦 Modelo Item

| Campo | Tipo | Detalle |
|---|---|---|
| `name` | `CharField` | Nombre del ítem |
| `description` | `TextField` | Descripción larga, opcional (`blank`, `null`) |
| `created_at` | `DateTimeField` | Fecha/hora de creación automática (`auto_now_add`) |

## 🔒 Nota sobre seguridad

- No usar `DEBUG = True` en producción.
- No subir la carpeta `venv/`, `db.sqlite3` ni ningún secreto/credencial al repositorio.

## 🌟 Reto opcional

Además de los ejercicios obligatorios, se completaron las tres funcionalidades complementarias
propuestas como reto:

- ✅ Estilos CSS agregados a la plantilla base para mejorar la presentación del catálogo.
- ✅ Buscador interactivo en JavaScript que filtra los ítems sin recargar la página.
- ✅ Endpoint de API para el modelo `Item`, consumido desde un frontend con HTML, CSS y
  JavaScript vanilla.

## 🤖 Implementaciones avanzadas asistidas por IA (Agente Claude / VS Code)

A partir de este punto, el desarrollo de las funcionalidades complementarias (estilos CSS,
buscador interactivo en JavaScript y creación/consumo de la API REST) se realizó utilizando
un agente de Inteligencia Artificial (Claude, integrado como extensión en Visual Studio Code).
Se redactaron e ingresaron instrucciones detalladas para la generación automatizada y
optimizada del código, revisando y probando cada cambio directamente sobre el proyecto antes
de aceptarlo.

## ✅ Resultados de la implementación con el Agente de IA

1. **Estilos CSS**: se integró un diseño limpio basado en tarjetas (*cards*), sombras suaves y
   una tipografía moderna para la presentación del catálogo de productos.
2. **Interactividad (JavaScript)**: se añadió una barra de búsqueda en tiempo real que filtra
   las tarjetas de los ítems en el navegador sin necesidad de recargar la página.
3. **Consumo de API REST**: se habilitó la ruta `/api/items/` para devolver los ítems en
   formato JSON, junto con el enlace **"Demo API"** en la cabecera del sitio, que consume esos
   datos mediante `fetch` en la página `/api-demo/`.

## 📚 Documentación y publicación del proyecto

En este paso final se generó el archivo `requirements.txt` para congelar las dependencias
instaladas en el entorno virtual. Luego se redactó este `README.md` detallando las
tecnologías usadas, la estructura del proyecto y los pasos de instalación y ejecución.
Finalmente, se inicializó el repositorio local con Git y se subió todo el código fuente a un
repositorio público en GitHub.
