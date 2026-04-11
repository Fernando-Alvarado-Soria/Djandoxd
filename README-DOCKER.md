# 🐳 Docker - Desarrollo Local

Este archivo contiene instrucciones rápidas para trabajar con Docker en tu entorno local.

## 🚀 Inicio Rápido

### 1. Preparar el entorno

```bash
# Copiar el archivo de ejemplo de variables de entorno
cp .env.example .env

# Editar el archivo .env con tus configuraciones locales
# (Puedes dejar los valores por defecto para desarrollo)
```

### 2. Iniciar la aplicación

```bash
# Construir e iniciar todos los servicios (web + base de datos)
docker-compose up --build

# O en modo background (segundo plano)
docker-compose up -d --build
```

La aplicación estará disponible en: http://localhost:8000

### 3. Crear superusuario (primera vez)

```bash
# Si no configuraste DJANGO_SUPERUSER_PASSWORD en .env
docker-compose exec web python manage.py createsuperuser
```

## 📋 Comandos Útiles

### Gestión de Contenedores

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver solo logs de Django
docker-compose logs -f web

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver servicios corriendo
docker-compose ps
```

### Django Management Commands

```bash
# Ejecutar cualquier comando de Django
docker-compose exec web python manage.py <comando>

# Ejemplos:
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py createsuperuser
```

### Acceso a la Base de Datos

```bash
# Acceder al shell de PostgreSQL
docker-compose exec db psql -U postgres -d djandoxd

# Ejecutar comandos SQL directamente
docker-compose exec db psql -U postgres -d djandoxd -c "SELECT * FROM auth_user;"
```

### Limpieza

```bash
# Detener y eliminar contenedores
docker-compose down

# Detener, eliminar contenedores Y volúmenes (¡BORRA LA BASE DE DATOS!)
docker-compose down -v

# Limpiar imágenes no utilizadas
docker system prune -a
```

## 🔧 Desarrollo con Hot Reload

El archivo `docker-compose.yml` está configurado para desarrollo con hot-reload:
- Los cambios en el código Python se reflejan automáticamente
- No necesitas reconstruir la imagen para cada cambio
- Solo cuando agregues nuevas dependencias a `requirements.txt` necesitas reconstruir:

```bash
docker-compose up -d --build web
```

## 📦 Agregar Nuevas Dependencias

```bash
# 1. Agregar la dependencia a requirements.txt

# 2. Reconstruir la imagen
docker-compose up -d --build web

# 3. Verificar que se instaló correctamente
docker-compose exec web pip list
```

## 🐛 Debugging

### Verificar que todo funciona

```bash
# Test de conexión a base de datos
docker-compose exec web python manage.py check --database default

# Ver configuración de Django
docker-compose exec web python manage.py diffsettings
```

### Problemas Comunes

**Error: Puerto 8000 ya en uso**
```bash
# En Windows PowerShell, encontrar el proceso:
netstat -ano | findstr :8000

# Matar el proceso (usa el PID de la salida anterior)
taskkill /PID <PID> /F
```

**Error: Puerto 5432 ya en uso (PostgreSQL)**
```bash
# Detener PostgreSQL local si está corriendo
# O cambiar el puerto en docker-compose.yml: "5433:5432"
```

**Contenedor se reinicia constantemente**
```bash
# Ver los logs
docker-compose logs web

# Verificar que .env tiene las configuraciones correctas
```

## 🧪 Testing

```bash
# Ejecutar tests
docker-compose exec web python manage.py test

# Con cobertura (si tienes coverage instalado)
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

## 📝 Notas

- **Base de datos**: Los datos persisten en un volumen Docker (`postgres_data`)
- **Archivos estáticos**: Se recolectan automáticamente al iniciar
- **Migraciones**: Se ejecutan automáticamente al iniciar el contenedor
- **Hot reload**: Gunicorn está configurado con `--reload` en desarrollo

## 🚢 Pasar a Producción

Cuando estés listo para producción, revisa [DEPLOY-DIGITALOCEAN.md](DEPLOY-DIGITALOCEAN.md) para instrucciones completas de despliegue.

Principales cambios necesarios:
1. `DEBUG=False`
2. SECRET_KEY única y segura
3. Configurar ALLOWED_HOSTS
4. Usar base de datos managed
5. Configurar SSL/HTTPS
6. Eliminar `--reload` de gunicorn
