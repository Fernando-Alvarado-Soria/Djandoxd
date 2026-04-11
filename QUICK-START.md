# ⚡ Guía de Inicio Rápido

## 🐳 Opción 1: Docker (Recomendado - 3 minutos)

### Requisitos:
- Docker Desktop instalado
- Git

### Pasos:

```bash
# 1. Clonar
git clone https://github.com/Fernando-Alvarado-Soria/Djandoxd.git
cd Djandoxd

# 2. Configurar
cp .env.example .env

# 3. Iniciar (incluye base de datos automáticamente)
docker-compose up --build
```

✅ **Listo!** Ve a http://localhost:8000

---

## 💻 Opción 2: Desarrollo Tradicional (5 minutos)

### Requisitos:
- Python 3.11+
- Git

### Pasos:

```bash
# 1. Clonar
git clone https://github.com/Fernando-Alvarado-Soria/Djandoxd.git
cd Djandoxd

# 2. Crear entorno virtual
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
python manage.py migrate

# 5. Crear superusuario (opcional)
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver
```

✅ **Listo!** Ve a http://localhost:8000

---

## 🚀 Desplegar en Digital Ocean (10 minutos)

### Requisitos:
- Cuenta de Digital Ocean
- Droplet Ubuntu 22.04

### Pasos:

```bash
# 1. Conectar al servidor
ssh root@tu-ip-servidor

# 2. Ejecutar script de setup
curl -fsSL https://raw.githubusercontent.com/Fernando-Alvarado-Soria/Djandoxd/main/setup-digitalocean.sh -o setup.sh
chmod +x setup.sh
sudo bash setup.sh

# 3. Configurar .env
cd /var/www/djandoxd
nano .env  # Editar variables de entorno

# 4. Desplegar
docker-compose -f docker-compose.prod.yml up -d --build
```

✅ **Listo!** Tu app está en línea

### SSL (Opcional pero recomendado):

```bash
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

---

## 📖 Siguientes Pasos

Después de iniciar la aplicación:

1. **Acceder al admin**: http://localhost:8000/admin
   - Usa las credenciales del superusuario que creaste

2. **Crear tu primer viaje**: http://localhost:8000/agregar_viaje

3. **Ver la lista de viajes**: http://localhost:8000/

---

## 🆘 ¿Problemas?

### Docker no inicia:
```bash
docker-compose logs -f
```

### Puerto 8000 ocupado:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
sudo lsof -ti:8000 | xargs kill -9
```

### Error de base de datos:
```bash
# Con Docker
docker-compose down -v
docker-compose up --build

# Sin Docker
rm db.sqlite3
python manage.py migrate
```

---

## 📚 Más Documentación

- **Desarrollo con Docker**: [README-DOCKER.md](README-DOCKER.md)
- **Despliegue completo**: [DEPLOY-DIGITALOCEAN.md](DEPLOY-DIGITALOCEAN.md)
- **README principal**: [README.md](README.md)

---

**¿Todo funcionó?** ⭐ Dale una estrella al proyecto en GitHub!
