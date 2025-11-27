# Estructura del Proyecto - Richmond AI Co-Pilot

```
Richmondpro/
│
├── 📁 frontend/                    # Frontend del Co-Pilot
│   ├── index.html                  # Página principal con el Co-Pilot embebido
│   ├── 📁 styles/
│   │   └── copilot.css             # Estilos del panel lateral y chat
│   └── 📁 js/
│       └── copilot.js              # Lógica del frontend (chat, UI, API calls)
│
├── 📁 backend/                     # Backend API
│   ├── app.py                      # API FastAPI principal
│   ├── rag.py                      # Sistema RAG básico (búsqueda en KB)
│   └── prompts.py                  # System prompts para el LLM
│
├── 📁 knowledge/                   # Base de conocimiento
│   └── richmondpro_kb.md          # Información sobre RichmondPro (RAG)
│
├── 📄 requirements.txt             # Dependencias Python
├── 📄 .env.example                 # Plantilla de variables de entorno
├── 📄 .gitignore                   # Archivos a ignorar en git
│
├── 📄 README.md                    # Documentación principal
├── 📄 QUICKSTART.md                # Guía de inicio rápido
├── 📄 DEPLOY.md                    # Guía de despliegue
├── 📄 PROJECT_STRUCTURE.md         # Este archivo
│
└── 🚀 start.sh                     # Script de inicio rápido
```

## Flujo de Datos

```
Usuario (Frontend)
    ↓
copilot.js → fetch() → API Request
    ↓
Backend (app.py)
    ↓
rag.py → Busca en richmondpro_kb.md
    ↓
prompts.py → Construye system prompt con contexto
    ↓
LLM (OpenAI/Anthropic) → Genera respuesta
    ↓
Backend → JSON Response
    ↓
Frontend → Renderiza mensaje en chat
```

## Componentes Clave

### Frontend
- **index.html**: Estructura HTML con panel lateral fijo
- **copilot.css**: Estilos profesionales tipo IDE/Herramienta empresarial
- **copilot.js**: 
  - Manejo de UI (abrir/cerrar panel)
  - Comunicación con API
  - Formateo de mensajes (markdown básico, widgets)
  - Historial de conversación

### Backend
- **app.py**: 
  - Endpoints: `/`, `/welcome`, `/chat`, `/health`
  - Integración con LLM (OpenAI/Anthropic)
  - CORS configurado
- **rag.py**: 
  - Carga base de conocimiento
  - Búsqueda por palabras clave
  - Retorna contexto relevante
- **prompts.py**: 
  - System prompt para consultor de ventas EdTech
  - Mensaje de bienvenida

### Base de Conocimiento
- **richmondpro_kb.md**: 
  - Información sobre los 3 pilares
  - Casos de éxito
  - Métricas y beneficios
  - Proceso de implementación

## Personalización

### Cambiar Colores
Editar variables CSS en `frontend/styles/copilot.css`:
```css
:root {
    --copilot-header-bg: #1e3a8a;
    --copilot-accent: #3b82f6;
    /* ... */
}
```

### Actualizar Base de Conocimiento
Editar `knowledge/richmondpro_kb.md` con nueva información.

### Ajustar Comportamiento del LLM
Editar `backend/prompts.py` para modificar el system prompt.

### Cambiar Ancho del Panel
En `frontend/styles/copilot.css`:
```css
:root {
    --copilot-width: 30%;  /* Cambiar aquí */
}
```

## Próximos Pasos (Mejoras Futuras)

1. **RAG Avanzado**: 
   - Usar embeddings (OpenAI/Cohere)
   - Vector database (Pinecone, Weaviate)
   - Búsqueda semántica mejorada

2. **Funcionalidades**:
   - Guardar conversaciones
   - Exportar reportes generados
   - Integración con CRM (captura de leads)

3. **UI/UX**:
   - Modo oscuro
   - Animaciones más suaves
   - Soporte para archivos adjuntos

4. **Backend**:
   - Rate limiting
   - Caching de respuestas
   - Logging y analytics
   - Autenticación (si es necesario)

