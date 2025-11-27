# 🚀 Deploy Ahora - Richmond AI Co-Pilot

## ✅ Código ya está en GitHub
**Repositorio:** https://github.com/Ricmonpa/Richmond.AI.git

---

## 📋 Pasos para Deploy (5 minutos)

### 1️⃣ Deploy Frontend en Vercel

1. Ve a **https://vercel.com**
2. **Login** con GitHub
3. Click **"Add New Project"**
4. **Importa** el repositorio: `Ricmonpa/Richmond.AI`
5. **Configuración**:
   ```
   Framework Preset: Other
   Root Directory: frontend          ⚠️ IMPORTANTE
   Build Command: (dejar vacío)
   Output Directory: .               (punto)
   Install Command: (dejar vacío)
   ```
6. **Environment Variables:** (no necesarias)
7. Click **"Deploy"**
8. ⏱️ Espera 1-2 minutos
9. ✅ **Copia la URL** que te da Vercel (ej: `https://richmond-ai.vercel.app`)

---

### 2️⃣ Deploy Backend en Railway

1. Ve a **https://railway.app**
2. **Login** con GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. **Selecciona** el repositorio: `Ricmonpa/Richmond.AI`
5. **Configurar el servicio**:
   - Click en el servicio recién creado
   - **Settings** → **Root Directory:** `backend`
   - **Settings** → **Start Command:** `python app.py`
6. **Variables de entorno** (Settings → Variables → Add Variable):
   ```
   Name: GOOGLE_API_KEY
   Value: YOUR_GOOGLE_API_KEY_HERE
   ```
7. **Generar dominio** (Settings → Domains → Generate Domain)
8. ⏱️ Espera 2-3 minutos para el deploy
9. ✅ **Copia la URL** de Railway (ej: `https://richmond-ai-production.up.railway.app`)

---

### 3️⃣ Conectar Frontend con Backend

1. **Editar** `frontend/js/copilot.js` línea 10:
   ```javascript
   return 'https://TU-URL-DE-RAILWAY.railway.app';
   ```
   Reemplaza `TU-URL-DE-RAILWAY` con la URL real de Railway

2. **Commit y push**:
   ```bash
   git add frontend/js/copilot.js
   git commit -m "Connect frontend to Railway backend"
   git push
   ```

3. ⏱️ Vercel redeployará automáticamente (1-2 minutos)

---

### 4️⃣ Actualizar CORS (si hay errores)

Si ves errores de CORS en la consola del navegador:

1. **Editar** `backend/app.py` línea ~50
2. **Agregar** tu URL de Vercel:
   ```python
   cors_origins = [
       "http://localhost:8080",
       "http://localhost:3000",
       "https://*.vercel.app",
       "https://TU-PROYECTO.vercel.app",  # ← Agregar aquí
   ]
   ```
3. **Commit y push**:
   ```bash
   git add backend/app.py
   git commit -m "Update CORS for production"
   git push
   ```

---

## 🎉 ¡Listo!

Tu demo estará en: **https://tu-proyecto.vercel.app**

---

## 🔍 Verificar

1. Abre la URL de Vercel
2. El Co-Pilot debería aparecer automáticamente
3. Prueba: "¿Qué es RichmondPro?"
4. Debería responder usando el contenido del sitio web

---

## 📝 URLs Importantes

- **GitHub:** https://github.com/Ricmonpa/Richmond.AI
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Railway Dashboard:** https://railway.app/dashboard

---

## 🆘 Si algo falla

**CORS Error?**
- Verifica que agregaste tu dominio de Vercel en `backend/app.py`
- Verifica que Railway está corriendo

**Backend no responde?**
- Revisa logs en Railway (View Logs)
- Verifica que `GOOGLE_API_KEY` está configurada
- Verifica que el Root Directory es `backend`

**Frontend no carga?**
- Revisa build logs en Vercel
- Verifica que Root Directory es `frontend`
- Abre console del navegador (F12) para ver errores

