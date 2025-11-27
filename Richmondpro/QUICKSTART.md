# 🚀 Quick Start - Richmond AI Co-Pilot Demo

Guía rápida para poner en marcha el demo en 5 minutos.

## Requisitos Previos

- Python 3.8 o superior
- Una API key de OpenAI o Anthropic

## Pasos Rápidos

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar API Key

```bash
# Crear archivo .env
echo "OPENAI_API_KEY=tu-api-key-aqui" > .env
```

O edita `.env.example` y renómbralo a `.env`

### 3. Iniciar Backend

```bash
cd backend
python app.py
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Abrir Frontend

**Opción más simple:**
- Abre `frontend/index.html` directamente en tu navegador
- Si hay problemas de CORS, usa la opción siguiente

**Con servidor local:**
```bash
cd frontend
python -m http.server 8080
```

Luego abre: `http://localhost:8080`

### 5. ¡Listo! 🎉

El Co-Pilot debería aparecer automáticamente en el panel derecho.

## Probar el Demo

1. El Co-Pilot se abre automáticamente con un mensaje de bienvenida
2. Prueba preguntas como:
   - "¿Cómo funciona el Assessment Center?"
   - "¿Qué resultados han tenido otras universidades?"
   - "Necesito mejorar la empleabilidad de mis estudiantes"
3. El Co-Pilot responderá usando la base de conocimiento de RichmondPro

## Solución Rápida de Problemas

**Backend no inicia:**
- Verifica que tienes Python 3.8+
- Verifica que instalaste las dependencias: `pip install -r requirements.txt`
- Verifica que el puerto 8000 no está en uso

**No aparece el Co-Pilot:**
- Abre la consola del navegador (F12) y revisa errores
- Verifica que el backend está corriendo en `http://localhost:8000`
- Prueba abrir `http://localhost:8000/health` en el navegador

**Error de API Key:**
- Verifica que el archivo `.env` existe en la raíz del proyecto
- Verifica que la API key es correcta
- Para OpenAI: debe empezar con `sk-`
- Para Anthropic: debe empezar con `sk-ant-`

## Siguiente Paso

Una vez que el demo funciona, revisa:
- `README.md` para documentación completa
- `DEPLOY.md` para guía de despliegue
- `backend/prompts.py` para personalizar el comportamiento del Co-Pilot
- `knowledge/richmondpro_kb.md` para actualizar la base de conocimiento

