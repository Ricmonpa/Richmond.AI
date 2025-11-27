# Richmond AI Co-Pilot Demo

Demo de concepto para RichmondPro: un asistente de IA contextual que actúa como consultor de ventas integrado en el sitio web.

## 🚀 Características

- Panel lateral fijo (25-30% ancho) siempre visible
- Chat interactivo con IA contextual
- Integración con base de conocimiento (RAG) sobre RichmondPro
- Diseño profesional tipo IDE/Herramienta empresarial
- Respuestas proactivas y consultivas

## 📁 Estructura del Proyecto

```
Richmondpro/
├── frontend/
│   ├── index.html          # Página principal con el Co-Pilot
│   ├── styles/
│   │   └── copilot.css     # Estilos del Co-Pilot
│   └── js/
│       └── copilot.js      # Lógica del frontend
├── backend/
│   ├── app.py              # API FastAPI
│   ├── rag.py              # Sistema RAG básico
│   └── prompts.py          # System prompts
├── knowledge/
│   └── richmondpro_kb.md   # Base de conocimiento
├── requirements.txt        # Dependencias Python
└── README.md              # Este archivo
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8+
- Node.js (opcional, solo para desarrollo)

### Pasos

1. **Clonar/Descargar el proyecto**

2. **Instalar dependencias del backend:**
```bash
cd backend
pip install -r ../requirements.txt
```

3. **Configurar variables de entorno:**
```bash
# Crear archivo .env en la raíz del proyecto
echo "OPENAI_API_KEY=tu_api_key_aqui" > .env
# O usar ANTHROPIC_API_KEY para Claude
```

4. **Iniciar el servidor backend:**
```bash
cd backend
python app.py
```

5. **Abrir el frontend:**
   - Abrir `frontend/index.html` en el navegador
   - O usar un servidor local: `python -m http.server 8000` en la carpeta frontend

## 🎯 Uso

### Modo Demo Standalone

1. Iniciar el backend (puerto 8000)
2. Abrir `frontend/index.html` en el navegador
3. El Co-Pilot aparecerá automáticamente en el panel derecho

### Integración con richmondpro.global

Para integrar el Co-Pilot en el sitio real:

1. **Opción 1: Inyección de script**
   - Agregar al final del `<body>` de richmondpro.global:
   ```html
   <script src="https://tu-servidor.com/copilot.js"></script>
   <link rel="stylesheet" href="https://tu-servidor.com/copilot.css">
   ```

2. **Opción 2: Iframe (para demo rápido)**
   - El Co-Pilot puede cargarse en un iframe que apunte a tu servidor

## 🔧 Configuración

### Cambiar el LLM

En `backend/app.py`, modificar:
- `OPENAI_API_KEY` para usar GPT-4
- `ANTHROPIC_API_KEY` para usar Claude

### Personalizar el System Prompt

Editar `backend/prompts.py` para ajustar el comportamiento del Co-Pilot.

### Actualizar Base de Conocimiento

Editar `knowledge/richmondpro_kb.md` con nueva información sobre RichmondPro.

## 📝 Notas

- Este es un **demo de concepto** (MVP)
- La base de conocimiento está hardcoded en `richmondpro_kb.md`
- Para producción, considerar implementar un sistema RAG más robusto con embeddings y vector DB

## 🎨 Personalización

- Colores: Editar variables CSS en `frontend/styles/copilot.css`
- Mensaje inicial: Modificar en `frontend/js/copilot.js`
- Ancho del panel: Ajustar en `copilot.css` (variable `--copilot-width`)

