#!/bin/bash

# Script de inicio rápido para Richmond AI Co-Pilot

echo "🚀 Iniciando Richmond AI Co-Pilot Demo..."
echo ""

# Verificar que existe .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "📝 Creando .env desde .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Archivo .env creado. Por favor, edítalo y agrega tu API key."
        echo ""
        echo "Presiona Enter cuando hayas configurado tu API key..."
        read
    else
        echo "❌ Error: .env.example no encontrado"
        exit 1
    fi
fi

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Verificar dependencias
echo "📦 Verificando dependencias..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📥 Instalando dependencias..."
    pip install -r requirements.txt
fi

# Iniciar backend
echo ""
echo "🔧 Iniciando backend en http://localhost:8000..."
echo "📖 Abre frontend/index.html en tu navegador"
echo "   O ejecuta: cd frontend && python3 -m http.server 8080"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

cd backend
python3 app.py

