# 🔒 Guía de Seguridad para API Keys de Gemini

## ⚠️ REGLAS CRÍTICAS DE SEGURIDAD

Basado en la [documentación oficial de Google](https://ai.google.dev/gemini-api/docs/api-key?hl=es-419#security):

### ❌ NUNCA HACER:

1. **NUNCA confirmar API keys en control de código fuente**
   - ❌ NO subir API keys a Git/GitHub
   - ❌ NO incluir keys en archivos `.md`, `.py`, `.js`, etc.
   - ❌ NO usar keys reales en documentación

2. **NUNCA exponer API keys en el cliente**
   - ❌ NO usar keys directamente en apps web o móviles en producción
   - ❌ NO incluir keys en código JavaScript del frontend
   - ❌ Las keys en código del cliente pueden ser extraídas

### ✅ SIEMPRE HACER:

1. **Usar variables de entorno**
   ```bash
   # Local (.env - NO en Git)
   GOOGLE_API_KEY=tu-api-key-aqui
   
   # Railway/Vercel: Variables de entorno en el dashboard
   ```

2. **Usar llamadas del servidor**
   - ✅ La forma más segura es llamar a la API desde el backend
   - ✅ Mantener la key confidencial en el servidor
   - ✅ El frontend solo llama al backend, nunca directamente a Gemini

3. **Agregar restricciones a la key**
   - En [Google Cloud Console](https://console.cloud.google.com/)
   - Limitar permisos de la key
   - Restringir por IP, dominio, o API específica

4. **Usar placeholders en documentación**
   ```markdown
   GOOGLE_API_KEY=tu-api-key-aqui
   # O
   GOOGLE_API_KEY=YOUR_API_KEY_HERE
   ```

## 🛡️ Configuración Segura

### Local (.env)

1. Crear archivo `.env` en la raíz del proyecto:
   ```bash
   GOOGLE_API_KEY=tu-api-key-real-aqui
   ```

2. Verificar que `.env` está en `.gitignore`:
   ```
   .env
   .env.local
   .env.production
   ```

3. **NUNCA** hacer commit de `.env`

### Railway (Backend)

1. Ir a **Settings** → **Variables**
2. Agregar variable:
   - Name: `GOOGLE_API_KEY`
   - Value: `tu-api-key-real-aqui`
3. **NO** incluir en código o documentación

### Vercel (Frontend)

1. Ir a **Settings** → **Environment Variables**
2. Agregar variables necesarias
3. **NO** incluir API keys de Gemini (el frontend no debe tenerlas)

## 📋 Checklist de Seguridad

Antes de hacer commit:

- [ ] Verificar que `.env` está en `.gitignore`
- [ ] No hay API keys en archivos `.md`
- [ ] No hay API keys en código fuente (`.py`, `.js`, etc.)
- [ ] Usar solo placeholders en documentación
- [ ] Variables de entorno configuradas en Railway/Vercel
- [ ] API keys solo en variables de entorno del servidor

## 🔍 Cómo Verificar que No Hay Keys Expuestas

```bash
# Buscar posibles API keys en el repositorio
grep -r "AIzaSy" . --exclude-dir=.git

# Si encuentras algo, reemplázalo con un placeholder
```

## 🚨 Si una Key se Expone

1. **Inmediatamente:**
   - Ir a [Google Cloud Console](https://console.cloud.google.com/)
   - Eliminar o rotar la key expuesta
   - Crear una nueva key

2. **Limpiar el repositorio:**
   - Remover la key de todos los archivos
   - Hacer commit y push
   - Considerar usar `git filter-branch` si la key está en el historial

3. **Actualizar variables de entorno:**
   - Railway: Actualizar `GOOGLE_API_KEY`
   - Local: Actualizar `.env`

## 📚 Referencias

- [Documentación oficial de Google sobre seguridad de API keys](https://ai.google.dev/gemini-api/docs/api-key?hl=es-419#security)
- [Google Cloud Console - API Keys](https://console.cloud.google.com/apis/credentials)

---

**Recuerda:** Trata tu API key como una contraseña. Si se ve comprometida, otros pueden usar tu cuota, incurrir en cargos y acceder a tus datos.

