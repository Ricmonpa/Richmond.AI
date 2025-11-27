# 🚨 Fix Urgente - Railway Root Directory

## ❌ Problema Detectado

Railway está analizando el directorio **raíz** del repo y ve:
```
./
├── knowledge/
├── app.py
├── prompts.py
...
```

Pero **NO encuentra `requirements.txt`** porque está en `Richmondpro/backend/requirements.txt`

## ✅ Solución INMEDIATA

### En Railway Dashboard:

1. **Ve a tu servicio "Richmond.AI"**
2. **Settings** → **Source** (o busca "Root Directory" en el sidebar)
3. **Verifica el campo "Root Directory"**

### Debe ser EXACTAMENTE:

```
Richmondpro/backend
```

**NO:**
- ❌ `Richmondpro` (solo)
- ❌ `backend` (solo)
- ❌ `/Richmondpro/backend` (con slash inicial)
- ❌ `.` (raíz)

**SÍ:**
- ✅ `Richmondpro/backend` (exactamente así)

### Si está mal:

1. **Edita el campo "Root Directory"**
2. **Escribe:** `Richmondpro/backend`
3. **Guarda**
4. **Railway redeployará automáticamente**

---

## 🔍 Cómo Verificar que Funcionó:

Después de cambiar, en los logs deberías ver:

```
[inf] Detected Python
[inf] Installing dependencies from requirements.txt
[inf] Starting app...
```

En lugar de:
```
[inf] ✖ Railpack could not determine how to build the app
```

---

## ⏱️ Tiempo Estimado:

- Cambiar Root Directory: 30 segundos
- Railway redeploy: 2-3 minutos
- Total: ~3 minutos

---

## 📋 Checklist:

- [ ] Root Directory = `Richmondpro/backend`
- [ ] Guardar cambios
- [ ] Esperar redeploy
- [ ] Verificar logs (debe detectar Python)
- [ ] Probar backend: `curl https://richmondai-production.up.railway.app/health`

