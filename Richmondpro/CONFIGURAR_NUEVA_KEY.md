# ✅ Configuración de Nueva API Key

## Configuración Recomendada

### ✅ MARCAR:
- **Nombre:** "api richmond" (o el que prefieras)
- **Restricciones de API:** 
  - ✅ Cambiar a **"Restringir clave"**
  - ✅ Seleccionar **SOLO**: "Generative Language API"

### ❌ NO MARCAR:
- **Autenticar las llamadas a la API a través de una cuenta de servicio:** ❌ NO marcar (no necesario para Gemini API REST)

### ⚠️ OPCIONAL:
- **Restricciones de aplicaciones:** 
  - "Ninguno" está bien por ahora
  - O "Direcciones IP" si conoces las IPs de Railway

## Después de Crear:

1. **Copiar la nueva key** que se muestra
2. **Actualizar Railway:**
   - Settings → Variables → `GOOGLE_API_KEY`
   - Pegar la nueva key
   - Guardar
3. **Actualizar .env local** (si lo usas)

---

**⚠️ CRÍTICO:** Asegúrate de marcar "Restringir clave" y seleccionar "Generative Language API" para seguridad.

