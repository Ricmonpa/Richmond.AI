# 🔄 Rotación de API Key - Pasos Inmediatos

## ⚠️ SITUACIÓN ACTUAL

La API key `AIzaSyDsgTclU3NaNeGWRrFpFPuFcH27cLc2WJ8` fue expuesta en el historial de Git y debe ser **revocada inmediatamente**.

## ✅ PASOS A SEGUIR (5 minutos)

### 1. **Revocar la Key Expuesta** (Google Cloud Console)

1. Ir a: https://console.cloud.google.com/apis/credentials
2. Buscar la key: `AIzaSyDsgTclU3NaNeGWRrFpFPuFcH27cLc2WJ8`
3. Hacer clic en la key
4. Clic en **"DELETE"** o **"RESTRICT"** → **"DELETE"**
5. Confirmar eliminación

### 2. **Crear Nueva API Key**

1. En la misma página: https://console.cloud.google.com/apis/credentials
2. Clic en **"+ CREATE CREDENTIALS"** → **"API Key"**
3. Copiar la nueva key generada
4. **OPCIONAL pero RECOMENDADO:** Configurar restricciones:
   - **Application restrictions:** 
     - Seleccionar "IP addresses"
     - Agregar IPs de Railway (si las conoces) o dejar sin restricción por ahora
   - **API restrictions:**
     - Seleccionar "Restrict key"
     - Marcar solo: **"Generative Language API"**

### 3. **Actualizar Railway**

1. Ir a: https://railway.app/dashboard
2. Seleccionar tu proyecto
3. **Settings** → **Variables**
4. Buscar `GOOGLE_API_KEY`
5. Editar y pegar la **nueva key**
6. Guardar (Railway redeployará automáticamente)

### 4. **Actualizar Local (.env)**

1. Editar `.env` en tu máquina local:
   ```bash
   GOOGLE_API_KEY=tu-nueva-key-aqui
   ```
2. Reiniciar el servidor local si está corriendo

### 5. **Verificar que Funciona**

1. Esperar 1-2 minutos a que Railway redeploye
2. Probar el Co-Pilot en: https://richmond-ai.vercel.app
3. Verificar logs de Railway para confirmar que no hay errores de API key

## 🛡️ PREVENCIÓN FUTURA

✅ **NUNCA** incluir API keys en:
- Archivos `.md`
- Código fuente (`.py`, `.js`)
- Commits de Git

✅ **SIEMPRE** usar:
- Variables de entorno (`.env` local, Railway/Vercel en producción)
- Placeholders en documentación: `YOUR_GOOGLE_API_KEY_HERE`

## ⏱️ TIEMPO ESTIMADO

- Revocar key antigua: 1 minuto
- Crear nueva key: 1 minuto
- Actualizar Railway: 1 minuto
- Actualizar local: 30 segundos
- Verificar: 1 minuto

**Total: ~5 minutos**

---

**IMPORTANTE:** La key antigua debe ser revocada **inmediatamente** para evitar uso no autorizado.

