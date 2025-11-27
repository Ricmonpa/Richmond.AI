# 🚀 Pasos para Deploy - Richmond AI Co-Pilot

## ✅ Checklist Pre-Deploy

- [x] Código listo y funcionando localmente
- [x] Archivos de configuración creados (vercel.json, railway.json)
- [x] .gitignore configurado
- [ ] Repositorio en GitHub creado
- [ ] Código subido a GitHub
- [ ] Frontend deployado en Vercel
- [ ] Backend deployado en Railway
- [ ] URL del backend actualizada en frontend
- [ ] CORS configurado en backend

---

## 📋 Paso a Paso

### 1. Preparar y Subir a GitHub

```bash
# Verificar estado
git status

# Agregar todos los archivos (excepto los ignorados)
git add .

# Commit
git commit -m "Richmond AI Co-Pilot - Ready for production deploy"

# Si no tienes remote, crear repo en GitHub y luego:
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
git branch -M main
git push -u origin main
```

### 2. Deploy Frontend en Vercel

1. **Ir a Vercel**: https://vercel.com
2. **Login** con GitHub
3. **"Add New Project"**
4. **Importar repositorio** de GitHub
5. **Configuración del proyecto**:
   - **Framework Preset:** `Other`
   - **Root Directory:** `frontend` ⚠️ IMPORTANTE
   - **Build Command:** (dejar vacío)
   - **Output Directory:** `.` (punto)
   - **Install Command:** (dejar vacío)
6. **Environment Variables:** (no necesarias para frontend)
7. **Click "Deploy"**
8. ✅ **Esperar deploy** (1-2 minutos)
9. **Copiar la URL** que te da Vercel (ej: `https://richmond-copilot.vercel.app`)

### 3. Deploy Backend en Railway

1. **Ir a Railway**: https://railway.app
2. **Login** con GitHub
3. **"New Project"** → **"Deploy from GitHub repo"**
4. **Seleccionar tu repositorio**
5. **Configurar el servicio**:
   - Click en el servicio recién creado
   - **Settings** → **Root Directory:** `backend`
   - **Settings** → **Start Command:** `python app.py`
6. **Variables de entorno** (Settings → Variables):
   ```
   GOOGLE_API_KEY = YOUR_GOOGLE_API_KEY_HERE
   ```
7. **Deploy automático** comenzará
8. ✅ **Esperar deploy** (2-3 minutos)
9. **Copiar la URL** del servicio (ej: `https://richmond-copilot-production.up.railway.app`)
   - En Railway: Settings → Domains → Generate Domain

### 4. Conectar Frontend con Backend

1. **Editar** `frontend/js/copilot.js` línea 10:
   ```javascript
   return 'https://TU-URL-DE-RAILWAY.railway.app';
   ```
   Reemplazar `TU-URL-DE-RAILWAY` con la URL real de Railway

2. **Commit y push**:
   ```bash
   git add frontend/js/copilot.js
   git commit -m "Update backend URL for production"
   git push
   ```

3. **Vercel redeployará automáticamente** (1-2 minutos)

### 5. Actualizar CORS en Backend (si es necesario)

Si hay errores de CORS, editar `backend/app.py` línea ~50:

```python
cors_origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "https://*.vercel.app",
    "https://TU-PROYECTO.vercel.app",  # ← Agregar tu URL de Vercel
]
```

Luego:
```bash
git add backend/app.py
git commit -m "Update CORS for production domain"
git push
```

Railway redeployará automáticamente.

---

## 🎉 ¡Listo!

Tu demo estará disponible en:
- **Frontend:** `https://tu-proyecto.vercel.app`
- **Backend:** `https://tu-proyecto.railway.app`

---

## 🔍 Verificar que Funciona

1. Abre la URL de Vercel en el navegador
2. El Co-Pilot debería aparecer automáticamente
3. Prueba una pregunta: "¿Qué es RichmondPro?"
4. Debería responder usando el contenido del sitio web

---

## 🐛 Troubleshooting

### Error: CORS
- Verifica que agregaste tu dominio de Vercel en `backend/app.py`
- Verifica que Railway está corriendo

### Error: Backend no responde
- Revisa logs en Railway dashboard
- Verifica que `GOOGLE_API_KEY` está configurada
- Verifica que el puerto está correcto

### Error: Frontend no carga
- Revisa build logs en Vercel
- Verifica que `Root Directory` es `frontend`
- Revisa console del navegador (F12)

---

## 📝 Notas

- **Railway** tiene un plan gratuito generoso
- **Vercel** tiene un plan gratuito excelente
- Ambos servicios hacen **auto-deploy** cuando haces push a GitHub
- Los **logs** están disponibles en los dashboards de cada servicio

