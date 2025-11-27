# 🚀 Próximos Pasos - Deploy Backend

## ✅ Lo que ya está hecho:
- ✅ Frontend deployado en Vercel: `https://richmond-ai.vercel.app`
- ✅ CORS corregido en backend (permitir todos los orígenes)
- ✅ Código actualizado en GitHub

## ⏳ Lo que falta:

### Deploy Backend en Railway

1. **Ve a Railway**: https://railway.app
2. **Login** con GitHub
3. **"New Project"** → **"Deploy from GitHub repo"**
4. **Selecciona**: `Ricmonpa/Richmond.AI`
5. **Configurar**:
   - Click en el servicio
   - **Settings** → **Root Directory:** `backend`
   - **Settings** → **Start Command:** `python app.py`
6. **Variables de entorno** (Settings → Variables):
   ```
   GOOGLE_API_KEY = YOUR_GOOGLE_API_KEY_HERE
   ```
7. **Generar dominio**:
   - Settings → Domains → Generate Domain
   - Copia la URL (ej: `https://richmond-ai-production.up.railway.app`)

### Actualizar URL en Frontend

Una vez que tengas la URL de Railway:

1. **Edita** `frontend/js/copilot.js` línea 16:
   ```javascript
   return 'https://TU-URL-REAL-DE-RAILWAY.railway.app';
   ```
   Reemplaza `TU-URL-REAL-DE-RAILWAY` con tu URL real

2. **Commit y push**:
   ```bash
   git add frontend/js/copilot.js
   git commit -m "Update backend URL to Railway"
   git push
   ```

3. **Vercel redeployará automáticamente**

---

## 🎯 Después de esto

El Co-Pilot funcionará completamente:
- ✅ Frontend en Vercel
- ✅ Backend en Railway
- ✅ Conectados correctamente
- ✅ CORS resuelto

