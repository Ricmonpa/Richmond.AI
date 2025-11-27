# 🚀 Guía Rápida de Deploy

## Opción Recomendada: Frontend (Vercel) + Backend (Railway)

### 1️⃣ Preparar Git

```bash
git init
git add .
git commit -m "Initial commit: Richmond AI Co-Pilot"
```

### 2️⃣ Crear Repositorio en GitHub

1. Ve a GitHub y crea un nuevo repositorio
2. Conecta tu repositorio local:

```bash
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
git branch -M main
git push -u origin main
```

### 3️⃣ Deploy Frontend en Vercel

1. Ve a [vercel.com](https://vercel.com)
2. "Add New Project" → Importa tu repo de GitHub
3. Configuración:
   - **Root Directory:** `frontend`
   - **Framework:** Other
   - **Build Command:** (vacío)
   - **Output Directory:** `.`
4. Deploy

### 4️⃣ Deploy Backend en Railway

1. Ve a [railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Selecciona tu repo
4. Configuración:
   - **Root Directory:** `backend`
   - **Start Command:** `python app.py`
5. Variables de entorno:
   - `GOOGLE_API_KEY`: `YOUR_GOOGLE_API_KEY_HERE`
6. Railway te dará una URL (ej: `https://richmond-copilot-production.up.railway.app`)

### 5️⃣ Actualizar Frontend con URL del Backend

Edita `frontend/js/copilot.js` línea 7:

```javascript
API_URL: window.location.hostname === 'localhost' 
    ? 'http://localhost:8000'
    : 'https://TU-URL-DE-RAILWAY.app',  // ← Cambiar esto
```

Commit y push:

```bash
git add frontend/js/copilot.js
git commit -m "Update API URL for production"
git push
```

Vercel redeployará automáticamente.

### 6️⃣ Actualizar CORS en Backend

Edita `backend/app.py` y agrega tu dominio de Vercel a `cors_origins`.

---

## ✅ Listo!

Tu demo estará disponible en:
- Frontend: `https://tu-proyecto.vercel.app`
- Backend: `https://tu-proyecto.railway.app`

