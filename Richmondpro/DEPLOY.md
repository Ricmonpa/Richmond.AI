# Guía de Despliegue - Richmond AI Co-Pilot

## 🚀 Despliegue Local (Demo)

### Paso 1: Configurar el Entorno

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Configurar API Key

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key
# Usa OPENAI_API_KEY o ANTHROPIC_API_KEY
```

### Paso 3: Iniciar el Backend

```bash
cd backend
python app.py
```

El servidor estará disponible en `http://localhost:8000`

### Paso 4: Abrir el Frontend

**Opción A: Archivo directo**
- Abrir `frontend/index.html` en el navegador
- ⚠️ Nota: Puede haber problemas de CORS si el backend está en otro puerto

**Opción B: Servidor local (recomendado)**
```bash
cd frontend
python -m http.server 8080
# O con Node.js:
# npx http-server -p 8080
```

Luego abrir `http://localhost:8080` en el navegador.

**Opción C: Ajustar URL en el código**
- Editar `frontend/js/copilot.js` y cambiar `API_URL` a la URL correcta del backend

## 🌐 Integración con richmondpro.global

### Opción 1: Inyección de Script (Recomendado para Demo)

1. **Hostear los archivos del Co-Pilot** en un servidor (ej: Netlify, Vercel, AWS S3)

2. **Agregar al final del `<body>` de richmondpro.global:**

```html
<!-- Richmond AI Co-Pilot -->
<link rel="stylesheet" href="https://tu-servidor.com/copilot.css">
<div id="richmond-copilot-root"></div>
<script>
  window.RICHMOND_COPILOT_CONFIG = {
    apiUrl: 'https://tu-backend.com'
  };
</script>
<script src="https://tu-servidor.com/copilot.js"></script>
```

3. **Modificar `copilot.js`** para inyectar el panel en `#richmond-copilot-root` en lugar de usar el HTML completo.

### Opción 2: Iframe

1. Crear una página standalone con el Co-Pilot
2. Insertar en richmondpro.global:

```html
<iframe 
  src="https://tu-servidor.com/copilot.html" 
  style="position: fixed; right: 0; top: 0; width: 30%; height: 100vh; border: none; z-index: 1000;"
></iframe>
```

### Opción 3: Widget Embeddable

Crear una versión del Co-Pilot como widget que se puede incrustar fácilmente.

## 🔧 Configuración de Producción

### Backend

1. **Variables de entorno:**
   - Configurar `OPENAI_API_KEY` o `ANTHROPIC_API_KEY`
   - Ajustar `PORT` si es necesario

2. **CORS:**
   - En `backend/app.py`, actualizar `allow_origins` con los dominios permitidos:
   ```python
   allow_origins=["https://richmondpro.global", "https://www.richmondpro.global"]
   ```

3. **Despliegue del backend:**
   - **Opción A: Railway/Render/Fly.io**
     - Conectar repositorio
     - Configurar variables de entorno
     - Deploy automático
   
   - **Opción B: VPS (DigitalOcean, AWS EC2)**
     ```bash
     # Instalar dependencias
     pip install -r requirements.txt
     
     # Usar gunicorn para producción
     pip install gunicorn
     gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
     ```

### Frontend

1. **Actualizar URL de API:**
   - En `frontend/js/copilot.js`, cambiar `API_URL` a la URL de producción

2. **Despliegue:**
   - **Netlify/Vercel:** Arrastrar carpeta `frontend/` o conectar repositorio
   - **AWS S3 + CloudFront:** Subir archivos estáticos
   - **CDN:** Cualquier servicio de hosting estático

## 📝 Checklist de Producción

- [ ] API keys configuradas y seguras
- [ ] CORS configurado correctamente
- [ ] URLs de API actualizadas en frontend
- [ ] Base de conocimiento actualizada
- [ ] System prompt revisado y ajustado
- [ ] Pruebas de funcionalidad completadas
- [ ] Monitoreo y logging configurado (opcional)
- [ ] Rate limiting implementado (opcional, recomendado)

## 🐛 Troubleshooting

### Error: CORS
- Verificar que `allow_origins` en `app.py` incluya el dominio del frontend
- En desarrollo, usar `allow_origins=["*"]` (no recomendado para producción)

### Error: API Key no válida
- Verificar que el archivo `.env` existe y tiene la key correcta
- Verificar que el backend está leyendo el `.env` (usar `python-dotenv`)

### El Co-Pilot no aparece
- Verificar que `copilot.js` se está cargando (consola del navegador)
- Verificar que la URL de la API es correcta
- Verificar conexión con el backend (endpoint `/health`)

### Respuestas lentas
- Considerar usar modelos más rápidos (gpt-4o-mini, claude-3-haiku)
- Implementar caching de respuestas comunes
- Optimizar el sistema RAG (reducir tamaño de chunks)

