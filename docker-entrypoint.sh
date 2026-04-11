#!/bin/bash
set -e

echo "🚀 Iniciando aplicación Django..."

# Esperar a que la base de datos esté lista (si usa PostgreSQL)
echo "⏳ Esperando base de datos..."
python << END
import sys
import time
import os
import psycopg2
from urllib.parse import urlparse

max_attempts = 30
attempt = 0

database_url = os.environ.get('DATABASE_URL', '')

if database_url and database_url.startswith('postgres'):
    result = urlparse(database_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    while attempt < max_attempts:
        try:
            conn = psycopg2.connect(
                dbname=database,
                user=username,
                password=password,
                host=hostname,
                port=port
            )
            conn.close()
            print("✅ Base de datos lista!")
            sys.exit(0)
        except psycopg2.OperationalError:
            attempt += 1
            print(f"⏳ Intento {attempt}/{max_attempts} - Base de datos no disponible, esperando...")
            time.sleep(2)
    
    print("❌ No se pudo conectar a la base de datos")
    sys.exit(1)
else:
    print("ℹ️  Usando SQLite o base de datos ya disponible")
END

# Ejecutar migraciones
echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

# Crear superusuario si no existe (opcional)
echo "👤 Verificando superusuario..."
python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')

if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superusuario '{username}' creado")
else:
    print("ℹ️  Superusuario ya existe o no se proporcionó password")
END

echo "✅ Inicialización completa. Iniciando servidor..."

# Ejecutar el comando proporcionado (gunicorn)
exec "$@"
