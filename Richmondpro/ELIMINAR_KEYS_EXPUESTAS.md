# 🚨 ELIMINAR AMBAS API KEYS EXPUESTAS

## ⚠️ SITUACIÓN CRÍTICA

**AMBAS** API keys están expuestas en el historial de Git:

1. ❌ `AIzaSyAV3QQ6mPpiMwCVyCfpZ1bsM2PLln-m3Ug` ("richmond api")
2. ❌ `AIzaSyDsgTclU3NaNeGWRrFpFPuFcH27cLc2WJ8` ("NUEVA API RICHMOND")

## ✅ ACCIÓN INMEDIATA (3 pasos)

### Paso 1: Eliminar "richmond api"
1. En Google Cloud Console, haz clic en los **3 puntos (⋮)** de "richmond api"
2. Selecciona **"Borrar"** (Delete)
3. Confirma la eliminación

### Paso 2: Eliminar "NUEVA API RICHMOND"
1. Haz clic en los **3 puntos (⋮)** de "NUEVA API RICHMOND"
2. Selecciona **"Borrar"** (Delete)
3. Confirma la eliminación

### Paso 3: Crear UNA NUEVA API Key (completamente nueva)
1. Clic en **"+ Crear credenciales"** → **"Clave de API"**
2. **Copiar la nueva key** que se genera
3. **Configurar restricciones:**
   - **Restricciones de API:** 
     - Seleccionar "Restringir clave"
     - Marcar **SOLO**: "Generative Language API"
   - **Restricciones de aplicaciones:** 
     - Por ahora dejar "Ninguno" (o configurar IPs de Railway si las conoces)
4. **Guardar**

### Paso 4: Actualizar Railway
1. Ir a Railway Dashboard → Tu proyecto → Settings → Variables
2. Editar `GOOGLE_API_KEY`
3. Pegar la **NUEVA key** (la que acabas de crear)
4. Guardar

### Paso 5: Actualizar .env local (si lo usas)
```bash
GOOGLE_API_KEY=tu-nueva-key-aqui
```

## ⏱️ TIEMPO: ~3 minutos

---

**IMPORTANTE:** No uses ninguna de las dos keys actuales. Ambas están comprometidas.

