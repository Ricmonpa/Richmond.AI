# 🔧 Corrección de Puerto en Railway

## ⚠️ Problema Detectado

En Railway, el puerto configurado es **8080**, pero el backend FastAPI está configurado para usar el puerto **8000**.

## ✅ Solución

### Paso 1: Cambiar el Puerto en Railway

En la pantalla de "Generate Service Domain":

1. **Cambia el puerto de `8080` a `8000`**
   - El campo dice: "Enter the port your app is listening on"
   - Cambia el valor a: `8000`

2. **Click en "Generate Domain"** (botón morado)

3. **Railway generará una URL pública** como:
   - `https://richmond-ai-production.up.railway.app`
   - O similar

### Paso 2: Copiar la URL

Una vez generado, copia la URL completa que Railway te da.

### Paso 3: Actualizar Frontend

1. Edita `frontend/js/copilot.js` línea 16
2. Reemplaza `TU-BACKEND-RAILWAY-URL` con la URL real
3. Commit y push

---

## 📋 Resumen

- ❌ Puerto actual en Railway: `8080`
- ✅ Puerto correcto: `8000`
- 🔄 Cambiar a `8000` y generar dominio

