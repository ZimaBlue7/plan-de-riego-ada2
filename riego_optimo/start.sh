#!/bin/bash

# Navegar al directorio donde se encuentra este script
cd "$(dirname "$0")"

echo "=== Iniciador de Riego Óptimo ==="

# Verificar si existe el ambiente virtual
if [ ! -d "venv" ]; then
    echo "Ambiente virtual no encontrado. Creando venv..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error al crear el ambiente virtual. Asegúrate de tener python3 instalado."
        exit 1
    fi
    echo "Ambiente virtual creado con éxito."
fi

# Activar el ambiente virtual
echo "Activando ambiente virtual..."
source venv/bin/activate

# Instalar requerimientos si existe requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Instalando/actualizando paquetes desde requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "No se encontró requirements.txt. Saltando instalación de paquetes."
fi

# Ejecutar la aplicación principal
echo "Iniciando aplicación..."
python3 main.py

# Desactivar al terminar
deactivate
