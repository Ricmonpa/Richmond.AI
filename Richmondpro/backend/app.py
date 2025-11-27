"""
Backend API para el Richmond AI Co-Pilot
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import requests

# Importaciones opcionales de LLMs
try:
    import openai
except ImportError:
    openai = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from rag import get_rag
from rag_embeddings import get_scraped_rag
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE

# Cargar variables de entorno (buscar .env en la raíz del proyecto)
import pathlib
# Obtener la ruta del archivo actual
current_file = pathlib.Path(__file__).resolve()
project_root = current_file.parent.parent
env_path = project_root / ".env"

# Cargar .env
load_dotenv(dotenv_path=env_path)

# Debug: verificar que se cargó
if os.getenv("GOOGLE_API_KEY"):
    print(f"✅ .env cargado desde: {env_path}")
else:
    print(f"⚠️ .env no encontrado o GOOGLE_API_KEY no configurada en: {env_path}")

app = FastAPI(title="Richmond AI Co-Pilot API")

# Configurar CORS
# En producción, permitir dominios de Vercel
cors_origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:8080",
    "https://richmond-ai.vercel.app",
    "https://*.vercel.app",  # Para todos los subdominios de Vercel
]

# Agregar dominio de producción si está definido
if os.getenv("FRONTEND_URL"):
    cors_origins.append(os.getenv("FRONTEND_URL"))

# En desarrollo, permitir todo. En producción, solo los orígenes permitidos
allow_all = os.getenv("ENVIRONMENT") != "production"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Inicializar clientes de LLM
openai_client = None
anthropic_client = None
google_api_key = None
# Modelos de Gemini a probar en orden de preferencia
GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]

if os.getenv("OPENAI_API_KEY") and openai:
    openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
else:
    openai_client = None

if os.getenv("ANTHROPIC_API_KEY") and Anthropic:
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
else:
    anthropic_client = None

google_api_key_env = os.getenv("GOOGLE_API_KEY")
if google_api_key_env:
    google_api_key = google_api_key_env
    # Intentar configurar genai si está disponible (para compatibilidad)
    if genai:
        try:
            genai.configure(api_key=google_api_key)
        except Exception:
            pass  # No crítico, usaremos API REST directamente
    print(f"✅ Google Gemini API key configurada")
else:
    google_api_key = None
    print("⚠️ GOOGLE_API_KEY no encontrada en variables de entorno")


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []


class ChatResponse(BaseModel):
    response: str
    context_used: Optional[str] = None


def get_llm_response(user_message: str, context: str, conversation_history: List[Message]) -> str:
    """
    Obtiene respuesta del LLM usando el contexto RAG
    
    Args:
        user_message: Mensaje del usuario
        context: Contexto relevante de la base de conocimiento
        conversation_history: Historial de conversación
        
    Returns:
        Respuesta del LLM
    """
    # Construir mensajes para el LLM
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + f"\n\nCONTEXTO RELEVANTE DE RICHMONDPRO:\n{context}"}
    ]
    
    # Agregar historial de conversación (últimos 5 mensajes para no exceder tokens)
    for msg in conversation_history[-5:]:
        messages.append({"role": msg.role, "content": msg.content})
    
    # Agregar mensaje actual del usuario
    messages.append({"role": "user", "content": user_message})
    
    # Intentar Google Gemini primero (si está configurado), luego OpenAI, luego Claude
    if google_api_key:
        try:
            # Construir el prompt completo con contexto
            full_prompt = SYSTEM_PROMPT + f"\n\nCONTEXTO RELEVANTE DE RICHMONDPRO:\n{context}\n\n"
            
            # Agregar historial de conversación
            for msg in conversation_history[-5:]:
                if msg.role == "user":
                    full_prompt += f"Usuario: {msg.content}\n"
                else:
                    full_prompt += f"Assistant: {msg.content}\n"
            
            # Agregar mensaje actual
            full_prompt += f"Usuario: {user_message}\nAssistant:"
            
            # Usar API REST directamente con modelo correcto
            # Intentar con diferentes modelos en orden de preferencia
            last_error = None
            for model_name in GEMINI_MODELS:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={google_api_key}"
                    
                    payload = {
                        "contents": [{
                            "parts": [{
                                "text": full_prompt
                            }]
                        }],
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 2048,  # Aumentado para evitar MAX_TOKENS
                        }
                    }
                    
                    response = requests.post(url, json=payload, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        candidates = result.get("candidates", [])
                        
                        if not candidates:
                            raise Exception("No se recibieron candidatos de Gemini")
                        
                        candidate = candidates[0]
                        finish_reason = candidate.get("finishReason", "")
                        content = candidate.get("content", {})
                        parts = content.get("parts", [])
                        
                        # Verificar si hay texto en parts
                        if parts:
                            text = parts[0].get("text", "")
                            if text:
                                # Si finishReason es MAX_TOKENS, la respuesta puede estar truncada pero es válida
                                if finish_reason == "MAX_TOKENS":
                                    print(f"⚠️ Respuesta truncada por límite de tokens, pero se retorna lo disponible")
                                return text
                        
                        # Si no hay parts o texto, verificar finishReason
                        if finish_reason == "MAX_TOKENS":
                            raise Exception("Respuesta truncada: el modelo alcanzó el límite de tokens. Intenta con una pregunta más corta.")
                        elif finish_reason == "SAFETY":
                            raise Exception("Respuesta bloqueada por filtros de seguridad de Gemini.")
                        elif finish_reason:
                            raise Exception(f"Respuesta incompleta. Finish reason: {finish_reason}")
                        else:
                            raise Exception("Respuesta vacía de Gemini - no se pudo extraer texto")
                    elif response.status_code == 404:
                        # Modelo no disponible, probar siguiente
                        last_error = f"Modelo {model_name} no disponible"
                        continue
                    else:
                        error_msg = response.text
                        last_error = f"Error API Gemini con {model_name} (status {response.status_code}): {error_msg[:200]}"
                        # Si es error de API key, no seguir probando
                        if "API key not valid" in error_msg or "API_KEY_INVALID" in error_msg:
                            raise Exception("API key de Google no válida. Verifica que la API key sea correcta y que la API de Gemini esté habilitada en Google Cloud Console.")
                        # Si es otro error, probar siguiente modelo
                        continue
                except requests.exceptions.RequestException as e:
                    last_error = f"Error de conexión con {model_name}: {e}"
                    continue
            
            # Si llegamos aquí, ningún modelo funcionó
            raise Exception(f"No se pudo generar respuesta con ningún modelo de Gemini. Último error: {last_error}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión con Google Gemini: {e}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"❌ Error con Google Gemini: {e}")
            import traceback
            traceback.print_exc()
    
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",  # o "gpt-4" para mejor calidad
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error con OpenAI: {e}")
    
    if anthropic_client:
        try:
            # Convertir formato de mensajes para Claude
            claude_messages = []
            for msg in messages[1:]:  # Saltar system message
                claude_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            response = anthropic_client.messages.create(
                model="claude-3-haiku-20240307",  # o "claude-3-opus-20240229" para mejor calidad
                max_tokens=1000,
                system=SYSTEM_PROMPT + f"\n\nCONTEXTO RELEVANTE DE RICHMONDPRO:\n{context}",
                messages=claude_messages
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error con Claude: {e}")
    
    # Fallback: respuesta básica sin LLM
    return "Lo siento, no pude procesar tu consulta en este momento. Por favor, intenta nuevamente o contacta directamente a RichmondPro."


@app.get("/")
def root():
    """Endpoint de salud"""
    return {
        "status": "ok",
        "service": "Richmond AI Co-Pilot API",
        "version": "1.0.0"
    }


@app.get("/welcome")
def get_welcome():
    """Retorna el mensaje de bienvenida"""
    return {"message": WELCOME_MESSAGE}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal para el chat con el Co-Pilot
    
    Args:
        request: Request con mensaje del usuario e historial
        
    Returns:
        Respuesta del Co-Pilot con contexto usado (opcional)
    """
    try:
        # Intentar usar RAG con embeddings del contenido scraped primero
        # Si no está disponible, usar el RAG básico
        try:
            scraped_rag = get_scraped_rag()
            if scraped_rag and scraped_rag.chunks:
                # Usar RAG con embeddings del sitio scraped
                context = scraped_rag.get_context(request.message, max_chars=3000)
                print(f"✅ Usando contenido scraped del sitio web ({len(scraped_rag.chunks)} chunks)")
            else:
                raise Exception("RAG scraped no disponible")
        except Exception as e:
            # Fallback al RAG básico
            print(f"⚠️ RAG scraped no disponible, usando RAG básico: {e}")
            rag = get_rag()
            context = rag.get_context(request.message, max_chars=2000)
        
        # Convertir historial a formato Message
        # El historial puede venir como objetos Message (Pydantic) o como diccionarios
        history = []
        for msg in request.conversation_history:
            if isinstance(msg, Message):
                # Ya es un objeto Message
                history.append(msg)
            elif isinstance(msg, dict):
                # Es un diccionario, convertirlo a Message
                history.append(Message(role=msg.get("role", "user"), content=msg.get("content", "")))
            else:
                # Fallback
                history.append(Message(role="user", content=str(msg)))
        
        # Obtener respuesta del LLM
        response = get_llm_response(
            user_message=request.message,
            context=context,
            conversation_history=history
        )
        
        return ChatResponse(
            response=response,
            context_used=context[:500] + "..." if len(context) > 500 else context  # Solo primeros 500 chars para debug
        )
    
    except Exception as e:
        print(f"Error en /chat: {e}")
        raise HTTPException(status_code=500, detail=f"Error procesando la consulta: {str(e)}")


@app.get("/health")
def health():
    """Health check endpoint"""
    rag = get_rag()
    kb_loaded = len(rag.knowledge_base) > 0
    
    llm_available = False
    llm_provider = None
    
    if google_api_key:
        llm_available = True
        llm_provider = "Google Gemini"
    elif openai_client:
        llm_available = True
        llm_provider = "OpenAI"
    elif anthropic_client:
        llm_available = True
        llm_provider = "Anthropic"
    
    return {
        "status": "healthy" if (kb_loaded and llm_available) else "degraded",
        "knowledge_base_loaded": kb_loaded,
        "llm_available": llm_available,
        "llm_provider": llm_provider
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

