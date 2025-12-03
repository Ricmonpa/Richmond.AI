/**
 * Richmond AI Co-Pilot - Frontend Logic
 */

// Configuración
const CONFIG = {
    // Detectar si estamos en producción (Vercel) o desarrollo
    // IMPORTANTE: Después de deployar en Railway, actualiza la URL del backend aquí
    API_URL: (function() {
        const hostname = window.location.hostname;
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:8000';  // Desarrollo local
        }
        // Producción: URL del backend en Railway
        return 'https://richmondai-production.up.railway.app';
    })(),
    DEBOUNCE_DELAY: 300
};

// Estado del Co-Pilot
const state = {
    isOpen: false,
    conversationHistory: [],
    isTyping: false
};

// Elementos DOM
const elements = {
    panel: document.getElementById('copilot-panel'),
    toggle: document.getElementById('copilot-toggle'),
    close: document.getElementById('copilot-close'),
    messages: document.getElementById('copilot-messages'),
    input: document.getElementById('copilot-input'),
    send: document.getElementById('copilot-send')
};

/**
 * Inicialización
 */
function init() {
    // Event listeners
    elements.toggle.addEventListener('click', openCopilot);
    elements.close.addEventListener('click', closeCopilot);
    elements.send.addEventListener('click', sendMessage);
    elements.input.addEventListener('keydown', handleInputKeydown);
    
    // Inicializar manejo de teclado en móvil
    initMobileKeyboardHandler();
    
    // Abrir automáticamente al cargar (para demo)
    setTimeout(() => {
        openCopilot();
        loadWelcomeMessage();
    }, 500);
}

/**
 * Abre el panel del Co-Pilot
 */
function openCopilot() {
    state.isOpen = true;
    elements.panel.classList.add('open');
    elements.toggle.classList.add('hidden');
    elements.input.focus();
}

/**
 * Cierra el panel del Co-Pilot
 */
function closeCopilot() {
    state.isOpen = false;
    elements.panel.classList.remove('open');
    elements.toggle.classList.remove('hidden');
}

/**
 * Carga el mensaje de bienvenida
 */
async function loadWelcomeMessage() {
    try {
        console.log('🔗 Intentando conectar a:', CONFIG.API_URL);
        const response = await fetch(`${CONFIG.API_URL}/welcome`);
        console.log('📡 Respuesta del servidor:', response.status, response.statusText);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        addMessage('ai', data.message);
    } catch (error) {
        console.error('❌ Error cargando mensaje de bienvenida:', error);
        console.error('🔍 URL intentada:', CONFIG.API_URL);
        addMessage('ai', '¡Bienvenido! Soy el Richmond AI Co-Pilot. ¿Cómo puedo ayudarte hoy?');
    }
}

/**
 * Maneja el envío de mensajes
 */
async function sendMessage() {
    const message = elements.input.value.trim();
    
    if (!message || state.isTyping) {
        return;
    }
    
    // Agregar mensaje del usuario a la UI
    addMessage('user', message);
    
    // Agregar al historial
    state.conversationHistory.push({
        role: 'user',
        content: message
    });
    
    // Limpiar input
    elements.input.value = '';
    elements.input.style.height = 'auto';
    
    // Deshabilitar input mientras se procesa
    setTyping(true);
    
    try {
        console.log('📤 Enviando mensaje a:', `${CONFIG.API_URL}/chat`);
        // Llamar a la API
        const response = await fetch(`${CONFIG.API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                conversation_history: state.conversationHistory
            })
        });
        
        console.log('📡 Respuesta del servidor:', response.status, response.statusText);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Error del servidor:', errorText);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('✅ Respuesta recibida:', data);
        
        // Agregar respuesta de la IA
        addMessage('ai', data.response);
        
        // Agregar al historial
        state.conversationHistory.push({
            role: 'assistant',
            content: data.response
        });
        
    } catch (error) {
        console.error('❌ Error enviando mensaje:', error);
        console.error('🔍 URL intentada:', `${CONFIG.API_URL}/chat`);
        addMessage('ai', `Lo siento, hubo un error al procesar tu consulta. ${error.message || 'Por favor, intenta nuevamente.'}`);
    } finally {
        setTyping(false);
    }
}

/**
 * Agrega un mensaje al chat
 */
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const header = document.createElement('div');
    header.className = 'message-header';
    header.textContent = role === 'user' ? '👤 Tú' : '🤖 Richmond AI';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Procesar contenido (soporte básico para markdown y widgets)
    contentDiv.innerHTML = formatMessageContent(content);
    
    messageDiv.appendChild(header);
    messageDiv.appendChild(contentDiv);
    
    elements.messages.appendChild(messageDiv);
    
    // Scroll al final
    scrollToBottom();
}

/**
 * Formatea el contenido del mensaje
 * Soporta markdown básico y widgets
 */
function formatMessageContent(content) {
    // Convertir markdown básico a HTML
    let html = content
        // Negritas
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Listas con bullets
        .replace(/^•\s(.+)$/gm, '<li>$1</li>')
        // Listas numeradas
        .replace(/^\d+\.\s(.+)$/gm, '<li>$1</li>')
        // Saltos de línea
        .replace(/\n/g, '<br>');
    
    // Detectar y formatear widgets/tarjetas
    // Ejemplo: [Widget: Plan de Acción] ... [/Widget]
    html = html.replace(
        /\[Widget:\s*([^\]]+)\]([\s\S]*?)\[\/Widget\]/g,
        (match, title, body) => {
            return `
                <div class="message-card">
                    <h4>${title}</h4>
                    <div>${formatMessageContent(body)}</div>
                </div>
            `;
        }
    );
    
    // Detectar botones de acción
    // Ejemplo: [Button: Texto|Acción]
    html = html.replace(
        /\[Button:\s*([^|]+)\|([^\]]+)\]/g,
        (match, text, action) => {
            return `<button class="message-card-button" onclick="handleAction('${action}')">${text}</button>`;
        }
    );
    
    // Si hay listas, envolverlas en <ul>
    if (html.includes('<li>')) {
        html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }
    
    return html;
}

/**
 * Maneja acciones de botones en mensajes
 */
function handleAction(action) {
    switch(action) {
        case 'schedule_demo':
            addMessage('user', 'Me gustaría agendar una demo personalizada');
            setTimeout(() => sendMessage(), 100);
            break;
        case 'view_report':
            addMessage('user', 'Quisiera ver un ejemplo de reporte de competencias');
            setTimeout(() => sendMessage(), 100);
            break;
        case 'analyze_gaps':
            addMessage('user', 'Necesito analizar las brechas en nuestro plan curricular');
            setTimeout(() => sendMessage(), 100);
            break;
        default:
            console.log('Acción no reconocida:', action);
    }
}

/**
 * Maneja teclas en el input
 */
function handleInputKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
    
    // Auto-resize del textarea
    if (event.key === 'Enter' || event.key === 'Backspace') {
        setTimeout(() => {
            elements.input.style.height = 'auto';
            elements.input.style.height = elements.input.scrollHeight + 'px';
        }, 0);
    }
}

/**
 * Muestra/oculta indicador de escritura
 */
function setTyping(typing) {
    state.isTyping = typing;
    elements.send.disabled = typing;
    elements.input.disabled = typing;
    
    if (typing) {
        showTypingIndicator();
    } else {
        hideTypingIndicator();
    }
}

/**
 * Muestra indicador de escritura
 */
function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    elements.messages.appendChild(indicator);
    scrollToBottom();
}

/**
 * Oculta indicador de escritura
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

/**
 * Scroll al final del chat
 */
function scrollToBottom() {
    const messagesContainer = elements.messages.parentElement;
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Manejo de teclado en móvil - comportamiento tipo WhatsApp
 */
function initMobileKeyboardHandler() {
    // Solo en dispositivos móviles
    if (!('visualViewport' in window)) {
        return;
    }
    
    const viewport = window.visualViewport;
    let lastHeight = viewport.height;
    
    function handleViewportResize() {
        const currentHeight = viewport.height;
        const heightDiff = lastHeight - currentHeight;
        
        // Si la altura disminuyó significativamente, el teclado apareció
        if (heightDiff > 100) {
            // Actualizar variable CSS con la nueva altura del viewport
            document.documentElement.style.setProperty('--viewport-height', `${currentHeight}px`);
            
            // Scroll al input cuando el teclado aparece
            setTimeout(() => {
                elements.input.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
        } 
        // Si la altura aumentó, el teclado desapareció
        else if (heightDiff < -100) {
            // Restaurar altura completa
            document.documentElement.style.setProperty('--viewport-height', `${viewport.height}px`);
        }
        
        lastHeight = currentHeight;
    }
    
    // Escuchar cambios en el viewport (cuando aparece/desaparece el teclado)
    viewport.addEventListener('resize', handleViewportResize);
    viewport.addEventListener('scroll', handleViewportResize);
    
    // Configuración inicial
    document.documentElement.style.setProperty('--viewport-height', `${viewport.height}px`);
    
    // Manejar focus en el input
    elements.input.addEventListener('focus', () => {
        // Pequeño delay para que el teclado aparezca primero
        setTimeout(() => {
            handleViewportResize();
        }, 300);
    });
    
    // Prevenir comportamiento problemático en iOS
    if (/iPhone|iPad|iPod/.test(navigator.userAgent)) {
        elements.input.addEventListener('blur', () => {
            // Prevenir que el scroll quede en posición incorrecta
            window.scrollTo(0, 0);
        });
    }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

