#!/bin/bash

# Script de deploy para Richmond AI Co-Pilot

echo "🚀 Preparando deploy de Richmond AI Co-Pilot..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/app.py" ]; then
    echo "❌ Error: No se encuentra backend/app.py"
    echo "   Asegúrate de estar en el directorio raíz del proyecto"
    exit 1
fi

# Verificar git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "📦 Inicializando Git..."
    git init
    git branch -M main
fi

# Verificar que no hay cambios sin commitear
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Cambios detectados. ¿Deseas hacer commit? (s/n)"
    read -r response
    if [[ "$response" =~ ^[Ss]$ ]]; then
        echo "📝 Agregando archivos..."
        git add .
        echo "💬 Mensaje del commit:"
        read -r commit_message
        git commit -m "${commit_message:-Update Richmond AI Co-Pilot}"
    fi
fi

# Verificar remote
if ! git remote | grep -q origin; then
    echo ""
    echo "🔗 No hay remote configurado."
    echo "   Por favor, crea un repositorio en GitHub y luego ejecuta:"
    echo "   git remote add origin https://github.com/TU-USUARIO/TU-REPO.git"
    echo ""
    echo "   O proporciona la URL ahora:"
    read -r repo_url
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
    fi
fi

# Push a GitHub
echo ""
echo "📤 Haciendo push a GitHub..."
git push -u origin main || git push origin main

echo ""
echo "✅ Código subido a GitHub"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1️⃣  DEPLOY FRONTEND EN VERCEL:"
echo "   - Ve a https://vercel.com"
echo "   - 'Add New Project' → Importa tu repo"
echo "   - Root Directory: frontend"
echo "   - Framework: Other"
echo "   - Deploy"
echo ""
echo "2️⃣  DEPLOY BACKEND EN RAILWAY:"
echo "   - Ve a https://railway.app"
echo "   - 'New Project' → 'Deploy from GitHub repo'"
echo "   - Root Directory: backend"
echo "   - Start Command: python app.py"
echo "   - Agregar variable: GOOGLE_API_KEY"
echo ""
echo "3️⃣  ACTUALIZAR URL DEL BACKEND:"
echo "   - Edita frontend/js/copilot.js línea 8"
echo "   - Cambia la URL del backend por la de Railway"
echo "   - git add, commit, push"
echo ""
echo "🎉 ¡Listo para deploy!"

