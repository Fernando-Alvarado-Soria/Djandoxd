#!/bin/bash

# Script para actualizar la aplicación en producción
# Uso: ./update-script.sh o update-djandoxd (si lo instalaste globalmente)

set -e

PROJECT_DIR="/var/www/djandoxd"
COMPOSE_FILE="docker-compose.prod.yml"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔄 Actualizando Djandoxd...${NC}"

# Ir al directorio del proyecto
cd $PROJECT_DIR

# Pull de los últimos cambios
echo -e "${YELLOW}📥 Descargando código...${NC}"
git pull origin main

# Backup de la base de datos (si usas PostgreSQL en Docker)
if docker-compose -f $COMPOSE_FILE ps | grep -q "db"; then
    echo -e "${YELLOW}💾 Haciendo backup de base de datos...${NC}"
    BACKUP_FILE="backup-$(date +%Y%m%d-%H%M%S).sql"
    docker-compose -f $COMPOSE_FILE exec -T db pg_dump -U postgres djandoxd > "/var/backups/$BACKUP_FILE"
    echo -e "${GREEN}✓ Backup guardado en /var/backups/$BACKUP_FILE${NC}"
fi

# Construir nueva imagen
echo -e "${YELLOW}🔨 Construyendo imagen Docker...${NC}"
docker-compose -f $COMPOSE_FILE build --no-cache web

# Detener contenedores
echo -e "${YELLOW}⏸️  Deteniendo contenedores...${NC}"
docker-compose -f $COMPOSE_FILE down

# Iniciar contenedores
echo -e "${YELLOW}🚀 Iniciando contenedores...${NC}"
docker-compose -f $COMPOSE_FILE up -d

# Esperar a que la aplicación esté lista
echo -e "${YELLOW}⏳ Esperando a que la aplicación esté lista...${NC}"
sleep 10

# Verificar que está corriendo
if docker-compose -f $COMPOSE_FILE ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Actualización completa!${NC}"
    
    # Mostrar logs
    echo -e "${YELLOW}📋 Últimos logs:${NC}"
    docker-compose -f $COMPOSE_FILE logs --tail=30 web
else
    echo -e "${RED}❌ Error: Los contenedores no están corriendo${NC}"
    docker-compose -f $COMPOSE_FILE logs --tail=50 web
    exit 1
fi

echo -e "${GREEN}✨ Djandoxd actualizado exitosamente${NC}"
