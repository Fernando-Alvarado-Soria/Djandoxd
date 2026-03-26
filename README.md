# Patios - Gestión de Viajes de Trailers

Sistema web para la gestión y seguimiento de viajes de transporte de carga, desarrollado con Django.

## Funcionalidades

- CRUD completo de viajes (agregar, listar, editar, eliminar)
- Registro de gastos por viaje (casetas, diesel, otros)
- Control de estado de pago
- Cálculo de ganancias
- Autenticación de usuarios (login/logout)
- Creación de usuarios (solo administradores)
- Panel de administración de Django

## Requisitos

- Python 3.11+
- Django 5.2.12

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Fernando-Alvarado-Soria/Djandoxd.git
cd Djandoxd

# Crear entorno virtual
python -m venv env

# Activar entorno virtual
# Windows:
env\Scripts\activate
# Linux/Mac:
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor de desarrollo
python manage.py runserver
```

## Estructura del proyecto

```
Djandoxd/
├── manage.py
├── requirements.txt
├── patios/              # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── trailers/            # App principal
    ├── models.py        # Modelo Viaje
    ├── views.py         # Vistas CRUD + registro
    ├── forms.py         # Formularios
    ├── urls.py          # Rutas de la app
    ├── admin.py         # Configuración del admin
    ├── templates/       # Templates HTML
    └── migrations/      # Migraciones de BD
```
