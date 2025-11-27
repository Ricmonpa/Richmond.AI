# 🧪 Instrucciones para Probar el Demo

## Paso 1: Instalar Dependencias

Abre una terminal y ejecuta:

```bash
cd /Users/ricardomoncadapalafox/Richmondpro
pip3 install -r requirements.txt
```

Esto instalará:
- fastapi
- uvicorn
- python-dotenv
- openai
- anthropic
- python-multipart

## Paso 2: Configurar API Key

Necesitas una API key de OpenAI o Anthropic:

### Opción A: OpenAI (Recomendado para empezar)
1. Ve a https://platform.openai.com/api-keys
2. Crea una nueva API key
3. Crea el archivo `.env` en la raíz del proyecto:

```bash
echo "OPENAI_API_KEY=sk-tu-api-key-aqui" > .env
```

### Opción B: Anthropic (Claude)
1. Ve a https://console.anthropic.com/
2. Crea una API key
3. Crea el archivo `.env`:

```bash
echo "ANTHROPIC_API_KEY=sk-ant-tu-api-key-aqui" > .env
```

## Paso 3: Iniciar el Backend

En una terminal:

```bash
cd /Users/ricardomoncadapalafox/Richmondpro/backend
python3 app.py
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**¡No cierres esta terminal!** El servidor debe seguir corriendo.

## Paso 4: Abrir el Frontend

### Opción A: Abrir directamente (más simple)
1. Abre tu navegador
2. Presiona `Cmd + O` (o File > Open)
3. Navega a: `/Users/ricardomoncadapalafox/Richmondpro/frontend/index.html`
4. Abre el archivo

### Opción B: Con servidor local (recomendado)
Abre **otra terminal** y ejecuta:

```bash
cd /Users/ricardomoncadapalafox/Richmondpro/frontend
python3 -m http.server 8080
```

Luego abre en tu navegador: `http://localhost:8080`

## Paso 5: ¡Probar el Co-Pilot!

1. El panel del Co-Pilot debería aparecer automáticamente a la derecha
2. Verás un mensaje de bienvenida
3. Prueba preguntas como:
   - "¿Cómo funciona el Assessment Center?"
   - "¿Qué resultados han tenido otras universidades?"
   - "Necesito mejorar la empleabilidad de mis estudiantes"
   - "¿Cómo se integra RichmondPro con nuestro plan curricular?"

## 🔍 Verificar que Todo Funciona

### Backend funcionando:
Abre en tu navegador: `http://localhost:8000/health`

Deberías ver un JSON con:
```json
{
  "status": "healthy",
  "knowledge_base_loaded": true,
  "llm_available": true,
  "llm_provider": "OpenAI" (o "Anthropic")
}
```

### Frontend conectado:
1. Abre la consola del navegador (F12 o Cmd+Option+I)
2. No deberías ver errores en rojo
3. Si ves errores de CORS, verifica que el backend esté corriendo

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
pip3 install -r requirements.txt
```

### Error: "API key invalid"
- Verifica que el archivo `.env` existe en la raíz del proyecto
- Verifica que la API key es correcta (sin espacios)
- Para OpenAI: debe empezar con `sk-`
- Para Anthropic: debe empezar con `sk-ant-`

### Error: "Connection refused" o CORS
- Verifica que el backend está corriendo en `http://localhost:8000`
- Abre `http://localhost:8000/health` para verificar
- Si usas la Opción A (abrir HTML directamente), puede haber problemas de CORS. Usa la Opción B (servidor local)

### El Co-Pilot no aparece
- Abre la consola del navegador (F12)
- Revisa si hay errores
- Verifica que `copilot.js` se está cargando

### Respuestas lentas o errores
- Verifica tu conexión a internet
- Verifica que tienes créditos en tu cuenta de OpenAI/Anthropic
- Revisa los logs en la terminal donde corre el backend

## ✅ Checklist Rápido

- [ ] Dependencias instaladas (`pip3 install -r requirements.txt`)
- [ ] Archivo `.env` creado con API key válida
- [ ] Backend corriendo en `http://localhost:8000`
- [ ] Frontend abierto en el navegador
- [ ] Co-Pilot visible en el panel derecho
- [ ] Mensaje de bienvenida aparece
- [ ] Puedo enviar mensajes y recibir respuestas

## 🎯 Próximos Pasos

Una vez que funcione:
- Personaliza los colores en `frontend/styles/copilot.css`
- Actualiza la base de conocimiento en `knowledge/richmondpro_kb.md`
- Ajusta el comportamiento en `backend/prompts.py`
- Revisa `DEPLOY.md` para integrarlo con richmondpro.global

