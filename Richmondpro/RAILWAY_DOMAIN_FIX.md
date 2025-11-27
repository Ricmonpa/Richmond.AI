# ⚠️ URL Interna vs URL Pública

## ❌ `richmondai.railway.internal` - NO es la correcta

Esta es una URL **INTERNA** de Railway:
- Solo funciona dentro de la red de Railway
- NO es accesible desde Vercel
- NO es accesible desde el navegador
- Es para comunicación entre servicios dentro de Railway

## ✅ Necesitas una URL PÚBLICA

### Cómo generar el dominio público:

1. **En Railway Dashboard:**
   - Ve a tu servicio "Richmond.AI"
   - Click en **"Settings"**
   - Ve a la sección **"Networking"** (en el sidebar izquierdo)

2. **En "Public Networking":**
   - Verás: "Access to this service publicly through HTTP or TCP"
   - Click en el botón **"Generate Domain"** (con icono de rayo ⚡)
   - Railway generará una URL como: `https://richmond-ai-production.up.railway.app`

3. **Copia esa URL pública** (termina en `.railway.app`, NO `.railway.internal`)

4. **Actualiza el frontend:**
   - Edita `frontend/js/copilot.js` línea 16
   - Reemplaza con la URL pública que acabas de generar

---

## 🔍 Diferencia:

- ❌ `.railway.internal` = Solo dentro de Railway (privada)
- ✅ `.railway.app` = Accesible públicamente (pública)

---

## 📋 Pasos Exactos:

1. Railway → Settings → Networking
2. Public Networking → "Generate Domain"
3. Copia la URL (ej: `https://richmond-ai-production.up.railway.app`)
4. Actualiza `frontend/js/copilot.js` con esa URL
5. Commit y push

