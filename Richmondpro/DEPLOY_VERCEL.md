# 🚀 Deploy a Vercel - Richmond AI Co-Pilot

## Opción 1: Frontend en Vercel + Backend en Railway/Render (Recomendado)

### Paso 1: Preparar el Repositorio

```bash
# Inicializar git (si no está)
git init

# Agregar todos los archivos
git add .

# Commit inicial
git commit -m "Initial commit: Richmond AI Co-Pilot Demo"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/tu-usuario/richmond-copilot.git
git branch -M main
git push -u origin main
```

### Paso 2: Deploy Frontend en Vercel

1. Ve a [vercel.com](https://vercel.com) e inicia sesión
2. Click en "Add New Project"
3. Importa tu repositorio de GitHub
4. Configuración:
   - **Framework Preset:** Other
   - **Root Directory:** `frontend`
   - **Build Command:** (dejar vacío)
   - **Output Directory:** `.` (punto)
5. Variables de entorno (no necesarias para frontend)
6. Click "Deploy"

### Paso 3: Deploy Backend en Railway

1. Ve a [railway.app](https://railway.app) e inicia sesión
2. "New Project" → "Deploy from GitHub repo"
3. Selecciona tu repositorio
4. Configuración:
   - **Root Directory:** `backend`
   - **Start Command:** `python app.py`
5. Variables de entorno:
   - `GOOGLE_API_KEY`: Tu API key de Google
   - `PORT`: `8000` (Railway lo asigna automáticamente)
6. Railway te dará una URL como: `https://tu-proyecto.railway.app`

### Paso 4: Actualizar Frontend con URL del Backend

Edita `frontend/js/copilot.js`:

```javascript
const CONFIG = {
    API_URL: 'https://tu-proyecto.railway.app',  // URL de Railway
    DEBOUNCE_DELAY: 300
};
```

Haz commit y push:

```bash
git add frontend/js/copilot.js
git commit -m "Update API URL for production"
git push
```

Vercel redeployará automáticamente.

---

## Opción 2: Todo en Vercel (Serverless Functions)

### Configuración para Vercel Serverless

1. **Crear `vercel.json`** (ya creado)

2. **Mover backend a `/api`**:

```bash
# Crear estructura para Vercel
mkdir -p api
cp backend/app.py api/index.py
```

3. **Actualizar imports en `api/index.py`** para que funcionen en Vercel

4. **Variables de entorno en Vercel**:
   - `GOOGLE_API_KEY`: Tu API key
   - Agregar en Settings → Environment Variables

5. **Deploy**:
   - Push a GitHub
   - Vercel detectará automáticamente y desplegará

---

## 🔧 Configuración de Variables de Entorno

### En Vercel (Frontend):
No se necesitan variables de entorno para el frontend.

### En Railway/Render (Backend):
```bash
GOOGLE_API_KEY=AIzaSyDsgTclU3NaNeGWRrFpFPuFcH27cLc2WJ8
PORT=8000
```

---

## 📝 Checklist Pre-Deploy

- [ ] `.env` está en `.gitignore` (no subir API keys)
- [ ] `frontend/js/copilot.js` tiene la URL correcta del backend
- [ ] Backend tiene CORS configurado para el dominio de Vercel
- [ ] Archivos de conocimiento están en el repositorio
- [ ] `requirements.txt` está actualizado

---

## 🐛 Troubleshooting

### CORS Errors
Actualizar `backend/app.py`:
```python
allow_origins=[
    "https://tu-proyecto.vercel.app",
    "https://*.vercel.app"  # Para previews
]
```

### Backend no responde
- Verificar que Railway/Render está corriendo
- Verificar variables de entorno
- Revisar logs en Railway/Render dashboard

### Frontend no carga
- Verificar que el build en Vercel fue exitoso
- Revisar console del navegador para errores
- Verificar que la URL del backend es correcta

---

## 🔄 Actualizar Contenido del Sitio

Para actualizar el contenido scraped:

```bash
cd backend
python3 scraper.py
git add knowledge/richmondpro_scraped.json
git commit -m "Update scraped content"
git push
```

El backend se actualizará automáticamente.

