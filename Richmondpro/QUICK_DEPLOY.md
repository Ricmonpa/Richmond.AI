# ⚡ Deploy Rápido - 5 Minutos

## 🎯 Estrategia: Frontend (Vercel) + Backend (Railway)

### Paso 1: Subir a GitHub (2 min)

```bash
# Si ya tienes git configurado:
git add .
git commit -m "Richmond AI Co-Pilot - Ready for deploy"
git push

# Si no tienes git configurado:
./deploy.sh
```

### Paso 2: Deploy Frontend en Vercel (2 min)

1. Ve a **https://vercel.com** → Login con GitHub
2. Click **"Add New Project"**
3. Selecciona tu repositorio
4. Configuración:
   ```
   Root Directory: frontend
   Framework Preset: Other
   Build Command: (dejar vacío)
   Output Directory: .
   ```
5. Click **"Deploy"**
6. ✅ Obtendrás una URL como: `https://richmond-copilot.vercel.app`

### Paso 3: Deploy Backend en Railway (2 min)

1. Ve a **https://railway.app** → Login con GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Selecciona tu repositorio
4. En Settings → Variables:
   ```
   GOOGLE_API_KEY = AIzaSyDsgTclU3NaNeGWRrFpFPuFcH27cLc2WJ8
   ```
5. En Settings → Deploy:
   ```
   Root Directory: backend
   Start Command: python app.py
   ```
6. ✅ Obtendrás una URL como: `https://richmond-copilot-production.up.railway.app`

### Paso 4: Conectar Frontend con Backend (1 min)

Edita `frontend/js/copilot.js` línea 8:

```javascript
API_URL: window.location.hostname === 'localhost' 
    ? 'http://localhost:8000'
    : 'https://TU-URL-DE-RAILWAY.app',  // ← Pega aquí la URL de Railway
```

Luego:

```bash
git add frontend/js/copilot.js
git commit -m "Connect frontend to Railway backend"
git push
```

Vercel redeployará automáticamente.

---

## ✅ ¡Listo!

Tu demo estará en: `https://tu-proyecto.vercel.app`

---

## 🔧 Troubleshooting

**CORS Error?**
- Edita `backend/app.py` línea 50
- Agrega tu dominio de Vercel a `cors_origins`

**Backend no responde?**
- Verifica variables de entorno en Railway
- Revisa logs en Railway dashboard

**Frontend no carga?**
- Verifica que el build en Vercel fue exitoso
- Revisa console del navegador (F12)

