#!/bin/bash

# Script de setup inicial para Digital Ocean
# Ejecutar como root: bash setup-digitalocean.sh

set -e

echo "🚀 Setup de Djandoxd en Digital Ocean"
echo "======================================"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Verificar que se ejecuta como root
if [[ $EUID -ne 0 ]]; then
   print_error "Este script debe ejecutarse como root (usar sudo)"
   exit 1
fi

# 1. Actualizar sistema
print_message "Actualizando sistema..."
apt update && apt upgrade -y

# 2. Instalar Docker
if ! command -v docker &> /dev/null; then
    print_message "Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    print_message "Docker ya está instalado"
fi

# 3. Instalar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_message "Instalando Docker Compose..."
    apt install docker-compose -y
else
    print_message "Docker Compose ya está instalado"
fi

# 4. Instalar herramientas adicionales
print_message "Instalando herramientas adicionales..."
apt install -y git curl nano ufw certbot python3-certbot-nginx

# 5. Configurar Firewall
print_message "Configurando firewall..."
ufw --force enable
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
print_message "Firewall configurado"

# 6. Crear directorio del proyecto
PROJECT_DIR="/var/www/djandoxd"
print_message "Creando directorio del proyecto en $PROJECT_DIR..."
mkdir -p $PROJECT_DIR

# 7. Preguntar por el repositorio
echo ""
print_warning "Configuración del repositorio"
read -p "URL del repositorio Git (ej: https://github.com/usuario/Djandoxd.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    print_error "URL del repositorio es requerida"
    exit 1
fi

# 8. Clonar repositorio
print_message "Clonando repositorio..."
cd $PROJECT_DIR
if [ -d ".git" ]; then
    print_warning "El proyecto ya existe. Actualizando..."
    git pull
else
    git clone $REPO_URL .
fi

# 9. Configurar archivo .env
print_message "Configurando archivo .env..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warning "Se creó .env desde .env.example. ¡DEBES EDITARLO!"
    else
        print_error "No existe .env.example. Debes crear .env manualmente"
    fi
else
    print_warning ".env ya existe"
fi

# 10. Generar SECRET_KEY si no existe
if [ -f ".env" ]; then
    if ! grep -q "SECRET_KEY=" .env || grep -q "SECRET_KEY=tu-secret-key-super-segura-aqui-cambiar-en-produccion" .env; then
        print_message "Generando SECRET_KEY..."
        SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
        print_message "SECRET_KEY generada"
    fi
fi

# 11. Preguntar si quiere configurar SSL
echo ""
read -p "¿Deseas configurar SSL con Let's Encrypt ahora? (s/N): " SETUP_SSL
read -p "Tu dominio (ej: ejemplo.com): " DOMAIN

if [ ! -z "$DOMAIN" ] && [ -f ".env" ]; then
    print_message "Actualizando ALLOWED_HOSTS en .env..."
    sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=localhost,127.0.0.1,$DOMAIN,www.$DOMAIN/" .env
fi

# 12. Instrucciones finales
echo ""
echo "======================================"
print_message "Setup inicial completado!"
echo "======================================"
echo ""
print_warning "PRÓXIMOS PASOS:"
echo ""
echo "1. Editar el archivo .env con tus configuraciones:"
echo "   nano $PROJECT_DIR/.env"
echo ""
echo "2. Especialmente configurar:"
echo "   - DEBUG=False"
echo "   - SECRET_KEY (ya generada)"
echo "   - DATABASE_URL (tu base de datos de Digital Ocean)"
echo "   - ALLOWED_HOSTS (tu dominio)"
echo ""
echo "3. Construir e iniciar la aplicación:"
echo "   cd $PROJECT_DIR"
echo "   docker-compose -f docker-compose.prod.yml up -d --build"
echo ""
echo "4. Ver logs:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""

if [[ $SETUP_SSL =~ ^[Ss]$ ]] && [ ! -z "$DOMAIN" ]; then
    echo "5. Configurar SSL (después de que la app esté corriendo):"
    echo "   certbot --nginx -d $DOMAIN -d www.$DOMAIN"
    echo ""
fi

echo "6. Crear script de actualización:"
echo "   cp $PROJECT_DIR/update-script.sh /usr/local/bin/update-djandoxd"
echo "   chmod +x /usr/local/bin/update-djandoxd"
echo ""
print_message "¡Listo para desplegar! 🚀"
