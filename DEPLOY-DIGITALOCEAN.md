# 🚀 Guía de Despliegue en Digital Ocean con Docker

Esta guía te ayudará a desplegar tu aplicación Django usando Docker en Digital Ocean.

## 📋 Requisitos Previos

1. Cuenta de Digital Ocean
2. Docker instalado localmente (para pruebas)
3. Git configurado
4. Acceso SSH a tu Droplet

## 🏗️ Opción 1: Despliegue en Droplet (Servidor Virtual)

### Paso 1: Crear y Configurar Droplet

1. **Crear un Droplet en Digital Ocean:**
   - Imagen: Ubuntu 22.04 LTS
   - Plan: Basic ($6-12/mes recomendado)
   - Región: Más cercana a tus usuarios
   - Autenticación: SSH keys (recomendado)
   - Nombre: `djandoxd-production`

2. **Conectarse al Droplet:**
   ```bash
   ssh root@tu-ip-del-droplet
   ```

### Paso 2: Instalar Docker en el Droplet

```bash
# Actualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt install docker-compose -y

# Verificar instalación
docker --version
docker-compose --version

# Instalar git y otras herramientas
apt install git curl nano -y
```

### Paso 3: Configurar el Proyecto

```bash
# Crear directorio para la aplicación
mkdir -p /var/www/djandoxd
cd /var/www/djandoxd

# Clonar el repositorio
git clone https://github.com/tu-usuario/Djandoxd.git .

# Crear archivo .env de producción
nano .env
```

**Configuración del archivo `.env` de producción:**
```env
# Django Configuration
DEBUG=False
SECRET_KEY=genera-una-clave-segura-aqui-usa-comando-abajo
ALLOWED_HOSTS=tu-ip-o-dominio.com,www.tu-dominio.com

# Database Configuration (Managed PostgreSQL de Digital Ocean)
DATABASE_URL=postgresql://usuario:password@host:25060/database?sslmode=require

# Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@tudominio.com
DJANGO_SUPERUSER_PASSWORD=password-seguro-aqui
```

**Generar SECRET_KEY segura:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Paso 4: Configurar Base de Datos PostgreSQL

**Opción A: PostgreSQL en Managed Database (Recomendado)**

1. En el panel de Digital Ocean, crear un Managed PostgreSQL
2. Copiar la cadena de conexión `DATABASE_URL`
3. Agregar IP del Droplet a "Trusted Sources"
4. Usar la cadena en tu archivo `.env`

**Opción B: PostgreSQL en Docker (usando docker-compose.yml)**

Si prefieres usar PostgreSQL en el mismo droplet, solo necesitas configurar las variables en `.env`:
```env
POSTGRES_DB=djandoxd
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password-muy-seguro
DATABASE_URL=postgresql://postgres:password-muy-seguro@db:5432/djandoxd
```

### Paso 5: Construir y Ejecutar Contenedores

```bash
# Para producción con base de datos externa (Managed Database)
docker-compose up -d --build web

# Para producción con PostgreSQL en Docker
docker-compose up -d --build web db

# Para producción con Nginx (recomendado)
docker-compose --profile production up -d --build
```

### Paso 6: Verificar Despliegue

```bash
# Ver logs
docker-compose logs -f web

# Ver contenedores corriendo
docker ps

# Verificar salud de la aplicación
curl http://localhost:8000/admin/login/
```

### Paso 7: Configurar Firewall

```bash
# Configurar UFW (Firewall)
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# Verificar estado
ufw status
```

### Paso 8: Configurar Dominio (Opcional pero Recomendado)

1. **En tu proveedor de dominio:**
   - Crear registro A: `@` → IP del Droplet
   - Crear registro A: `www` → IP del Droplet

2. **Actualizar ALLOWED_HOSTS:**
   ```bash
   nano .env
   # Agregar: ALLOWED_HOSTS=tudominio.com,www.tudominio.com,tu-ip
   docker-compose restart web
   ```

3. **Configurar SSL con Let's Encrypt:**
   ```bash
   # Instalar Certbot
   apt install certbot python3-certbot-nginx -y
   
   # Obtener certificado SSL
   certbot --nginx -d tudominio.com -d www.tudominio.com
   
   # Renovación automática (se configura automáticamente)
   certbot renew --dry-run
   ```

## 🏢 Opción 2: Despliegue en App Platform (PaaS)

Digital Ocean App Platform es más simple pero un poco más costoso.

### Pasos:

1. **En el panel de Digital Ocean:**
   - Apps → Create App
   - Seleccionar repositorio de GitHub
   - Detectará automáticamente Dockerfile

2. **Configurar variables de entorno:**
   - Agregar todas las variables del `.env.example`
   - Configurar DATABASE_URL desde Managed Database

3. **Configurar recursos:**
   - Basic: $5-12/mes
   - Professional: $12-50/mes

4. **Deploy:**
   - Click en "Deploy"
   - Esperar a que termine

## 🔄 Actualización del Código

### En Droplet:

```bash
# Conectarse al servidor
ssh root@tu-ip-del-droplet

# Ir al directorio del proyecto
cd /var/www/djandoxd

# Pull últimos cambios
git pull origin main

# Reconstruir y reiniciar contenedores
docker-compose up -d --build

# Verificar logs
docker-compose logs -f web
```

### Crear un script de actualización:

```bash
# Crear script
nano /usr/local/bin/update-djandoxd.sh
```

Contenido del script:
```bash
#!/bin/bash
set -e

echo "🔄 Actualizando Djandoxd..."

cd /var/www/djandoxd

echo "📥 Descargando código..."
git pull origin main

echo "🔨 Construyendo imagen Docker..."
docker-compose build web

echo "🚀 Reiniciando contenedores..."
docker-compose up -d

echo "📋 Ejecutando migraciones..."
docker-compose exec -T web python manage.py migrate

echo "📦 Recolectando archivos estáticos..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo "✅ Actualización completa!"
docker-compose logs --tail=50 web
```

```bash
# Dar permisos de ejecución
chmod +x /usr/local/bin/update-djandoxd.sh

# Usar el script
update-djandoxd.sh
```

## 🛠️ Comandos Útiles

### Gestión de Contenedores:

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f web

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (¡CUIDADO!)
docker-compose down -v

# Ver estado de servicios
docker-compose ps
```

### Django Management Commands:

```bash
# Ejecutar comando de Django
docker-compose exec web python manage.py <comando>

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Shell de Django
docker-compose exec web python manage.py shell

# Recolectar archivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

### Backup de Base de Datos:

```bash
# Backup PostgreSQL (Docker)
docker-compose exec db pg_dump -U postgres djandoxd > backup-$(date +%Y%m%d-%H%M%S).sql

# Restaurar backup
docker-compose exec -T db psql -U postgres djandoxd < backup.sql

# Backup Managed Database
pg_dump "postgresql://usuario:password@host:25060/database?sslmode=require" > backup.sql
```

## 🔒 Seguridad

### Checklist de Seguridad:

- [ ] `DEBUG=False` en producción
- [ ] SECRET_KEY única y segura
- [ ] Firewall configurado (UFW)
- [ ] SSL/HTTPS habilitado
- [ ] Base de datos con contraseñas seguras
- [ ] Backups automáticos configurados
- [ ] Actualizar sistema regularmente: `apt update && apt upgrade`
- [ ] Variables sensibles en `.env` (no en código)
- [ ] `.env` en `.gitignore`
- [ ] Configurar límites de rate limiting (opcional)

## 📊 Monitoreo

### Instalar herramientas de monitoreo:

```bash
# Instalar ctop (monitor de contenedores)
wget https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-amd64 -O /usr/local/bin/ctop
chmod +x /usr/local/bin/ctop
ctop

# Ver uso de recursos
docker stats

# Logs de sistema
journalctl -u docker -f
```

## 🆘 Troubleshooting

### Problema: Contenedor no inicia

```bash
# Ver logs detallados
docker-compose logs web

# Ver últimas 100 líneas
docker-compose logs --tail=100 web

# Reconstruir sin cache
docker-compose build --no-cache web
```

### Problema: No conecta a base de datos

```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps db

# Verificar logs de base de datos
docker-compose logs db

# Test de conexión
docker-compose exec web python -c "from django.db import connection; connection.ensure_connection(); print('✅ Conectado')"
```

### Problema: Error 502 Bad Gateway

```bash
# Verificar que web está corriendo
docker-compose ps web

# Reiniciar nginx
docker-compose restart nginx

# Verificar logs
docker-compose logs nginx web
```

## 📚 Recursos Adicionales

- [Documentación de Docker](https://docs.docker.com/)
- [Digital Ocean Tutorials](https://www.digitalocean.com/community/tutorials)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)

## 💡 Mejores Prácticas

1. **Usar Managed Database** para producción (mejor rendimiento y backups automáticos)
2. **Configurar SSL/HTTPS** siempre en producción
3. **Backups regulares** de base de datos y archivos media
4. **Monitorear logs** regularmente
5. **Actualizar** dependencias y sistema operativo
6. **Usar secrets** para información sensible (Docker Secrets o variables de entorno)
7. **Implementar CI/CD** para deploys automáticos (GitHub Actions)

---

¿Necesitas ayuda? Revisa los logs con `docker-compose logs -f` 🔍
