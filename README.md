# Patios - Gestión de Viajes de Trailers

Sistema web para la gestión y seguimiento de viajes de transporte de carga, desarrollado con Django.

## 🐳 Desarrollo con Docker (Recomendado)

**¿Por qué Docker?** 
- ✅ Entorno consistente en desarrollo y producción
- ✅ Instalación rápida sin configurar dependencias manualmente
- ✅ Aislamiento y seguridad mejorada
- ✅ Fácil despliegue en Digital Ocean

### Inicio Rápido con Docker

```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. Iniciar aplicación (incluye base de datos PostgreSQL)
docker-compose up --build

# 3. Acceder a http://localhost:8000
```

📖 **Documentación completa:**
- [README-DOCKER.md](README-DOCKER.md) - Guía de desarrollo con Docker
- [DEPLOY-DIGITALOCEAN.md](DEPLOY-DIGITALOCEAN.md) - Guía de despliegue en producción

---

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
- Docker y Docker Compose (opcional, para desarrollo con Docker)

## Instalación Tradicional (Sin Docker)

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
├── Dockerfile                  # Imagen Docker multi-stage
├── docker-compose.yml          # Configuración Docker desarrollo
├── docker-compose.prod.yml     # Configuración Docker producción
├── docker-entrypoint.sh        # Script de inicialización
├── nginx.conf                  # Configuración Nginx
├── .dockerignore              # Archivos excluidos de Docker
├── .env.example               # Ejemplo de variables de entorno
├── patios/                    # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── trailers/                  # App principal
    ├── models.py              # Modelo Viaje
    ├── views.py               # Vistas CRUD + registro
    ├── forms.py               # Formularios
    ├── urls.py                # Rutas de la app
    ├── admin.py               # Configuración del admin
    ├── templates/             # Templates HTML
    └── migrations/            # Migraciones de BD
```

## 🚢 Despliegue en Producción (Digital Ocean)

Este proyecto está completamente dockerizado y listo para desplegarse en Digital Ocean.

### Setup automático:

```bash
# En tu servidor Digital Ocean (Ubuntu)
curl -fsSL https://raw.githubusercontent.com/Fernando-Alvarado-Soria/Djandoxd/main/setup-digitalocean.sh -o setup.sh
chmod +x setup.sh
sudo bash setup.sh
```

### Despliegue manual:

```bash
# 1. Clonar repositorio en el servidor
cd /var/www
git clone https://github.com/Fernando-Alvarado-Soria/Djandoxd.git djandoxd
cd djandoxd

# 2. Configurar variables de entorno
cp .env.example .env
nano .env  # Editar con tus configuraciones

# 3. Desplegar con Docker
docker-compose -f docker-compose.prod.yml up -d --build

# 4. Configurar SSL (opcional)
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

📖 **Guía completa**: [DEPLOY-DIGITALOCEAN.md](DEPLOY-DIGITALOCEAN.md)

## 🛠️ Comandos Útiles Docker

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ejecutar comandos de Django
docker-compose exec web python manage.py <comando>

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Detener servicios
docker-compose down
```

## 🔐 Seguridad

- ✅ Variables de entorno para configuración sensible
- ✅ Contenedores Docker con usuarios no-root
- ✅ HTTPS/SSL ready con Let's Encrypt
- ✅ Headers de seguridad configurados
- ✅ CSRF y XSS protection habilitados
- ✅ WhiteNoise para archivos estáticos seguros

## 🚀 Tecnologías

**Backend**: Django 5.2.12, Python 3.11 | **Base de datos**: PostgreSQL/SQLite | **Servidor**: Gunicorn + Nginx | **Containerización**: Docker & Docker Compose

## 📚 Documentación

- [README-DOCKER.md](README-DOCKER.md) - Guía de Docker para desarrollo
- [DEPLOY-DIGITALOCEAN.md](DEPLOY-DIGITALOCEAN.md) - Guía de despliegue

## 👤 Autor

**Fernando Alvarado Soria** - [@Fernando-Alvarado-Soria](https://github.com/Fernando-Alvarado-Soria)
