# Web Scraper y RAG para RichmondPro

## 📋 Descripción

Sistema completo de web scraping y RAG (Retrieval-Augmented Generation) que extrae contenido del sitio web oficial de RichmondPro y lo usa para alimentar el Co-Pilot con información real y actualizada.

## 🚀 Uso

### Ejecutar el Scraper

```bash
cd backend
python3 scraper.py
```

Esto:
1. Extrae contenido de `https://richmondpro.global/`
2. Procesa y limpia el texto
3. Divide el contenido en chunks semánticos
4. Guarda en `knowledge/richmondpro_scraped.json`

### Actualizar el Contenido

Para actualizar el contenido del sitio:

```bash
cd backend
python3 scraper.py
```

El sistema automáticamente usará el contenido más reciente.

## 🔧 Componentes

### 1. `scraper.py`
- Extrae HTML del sitio web
- Limpia y procesa el texto
- Divide en chunks semánticos
- Guarda en formato JSON

### 2. `rag_embeddings.py`
- Sistema RAG con TF-IDF y similitud de coseno
- Búsqueda semántica de chunks relevantes
- No requiere librerías de ML externas

### 3. Integración en `app.py`
- Usa automáticamente el contenido scraped si está disponible
- Fallback al RAG básico si no hay contenido scraped
- Contexto dinámico basado en la pregunta del usuario

## 📊 Estructura de Datos

El archivo `richmondpro_scraped.json` contiene:

```json
[
  {
    "url": "https://richmondpro.global",
    "title": "Richmond Pro - Three Pillars",
    "content": "Contenido del chunk...",
    "chunk_id": 0
  }
]
```

## 🎯 System Prompt

El system prompt ha sido actualizado para:
- **Solo usar información del sitio web** proporcionada en el contexto
- **No inventar información** (evitar alucinaciones)
- **Reconocer cuando no tiene información** sobre un tema
- Mantener el tono de consultor estratégico

## ✅ Verificación

Para verificar que el RAG scraped funciona:

```bash
cd backend
python3 -c "from rag_embeddings import get_scraped_rag; rag = get_scraped_rag(); print(f'Chunks: {len(rag.chunks) if rag else 0}')"
```

## 🔄 Flujo de Datos

1. **Usuario hace pregunta** → Frontend envía a `/chat`
2. **Backend busca contexto** → RAG scraped busca chunks relevantes
3. **Contexto + Pregunta** → Se envía a Gemini con el contexto
4. **Gemini responde** → Basándose SOLO en el contexto proporcionado
5. **Respuesta al usuario** → Con información real del sitio web

## 📝 Notas

- El scraper respeta los tiempos de espera (1 segundo entre requests)
- El contenido se divide en chunks de ~800 palabras con overlap de 150
- El sistema de embeddings usa TF-IDF (no requiere modelos externos)
- Si el contenido scraped no está disponible, usa el RAG básico como fallback

