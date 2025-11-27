"""
Sistema RAG básico para el Richmond AI Co-Pilot
"""

import os
from typing import List, Dict
import re


class SimpleRAG:
    """Sistema RAG simple basado en búsqueda de texto"""
    
    def __init__(self, knowledge_base_path: str):
        """
        Inicializa el sistema RAG con la base de conocimiento
        
        Args:
            knowledge_base_path: Ruta al archivo markdown con la base de conocimiento
        """
        self.knowledge_base_path = knowledge_base_path
        self.knowledge_base = self._load_knowledge_base()
        self.chunks = self._chunk_knowledge_base()
    
    def _load_knowledge_base(self) -> str:
        """Carga la base de conocimiento desde el archivo"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: Knowledge base not found at {self.knowledge_base_path}")
            return ""
    
    def _chunk_knowledge_base(self) -> List[Dict[str, str]]:
        """
        Divide la base de conocimiento en chunks semánticos
        Usa headers de markdown como delimitadores
        """
        chunks = []
        current_chunk = {"title": "", "content": ""}
        
        lines = self.knowledge_base.split('\n')
        
        for line in lines:
            # Detectar headers de markdown
            if line.startswith('#'):
                # Guardar chunk anterior si tiene contenido
                if current_chunk["content"].strip():
                    chunks.append(current_chunk)
                
                # Iniciar nuevo chunk
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                current_chunk = {
                    "title": title,
                    "content": line + "\n",
                    "level": level
                }
            else:
                current_chunk["content"] += line + "\n"
        
        # Agregar último chunk
        if current_chunk["content"].strip():
            chunks.append(current_chunk)
        
        return chunks
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        """
        Busca chunks relevantes basado en palabras clave
        
        Args:
            query: Consulta del usuario
            top_k: Número de chunks a retornar
            
        Returns:
            Lista de chunks relevantes con título y contenido
        """
        query_lower = query.lower()
        query_words = set(re.findall(r'\b\w+\b', query_lower))
        
        scored_chunks = []
        
        for chunk in self.chunks:
            content_lower = chunk["content"].lower()
            title_lower = chunk["title"].lower()
            
            # Calcular score simple basado en coincidencias
            title_matches = sum(1 for word in query_words if word in title_lower)
            content_matches = sum(1 for word in query_words if word in content_lower)
            
            # Peso mayor para matches en título
            score = (title_matches * 3) + content_matches
            
            if score > 0:
                scored_chunks.append({
                    "chunk": chunk,
                    "score": score
                })
        
        # Ordenar por score y retornar top_k
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        
        return [item["chunk"] for item in scored_chunks[:top_k]]
    
    def get_context(self, query: str, max_chars: int = 2000) -> str:
        """
        Obtiene contexto relevante para una consulta
        
        Args:
            query: Consulta del usuario
            max_chars: Máximo de caracteres en el contexto
            
        Returns:
            String con contexto relevante formateado
        """
        relevant_chunks = self.search(query, top_k=5)
        
        context_parts = []
        current_length = 0
        
        for chunk in relevant_chunks:
            chunk_text = f"## {chunk['title']}\n{chunk['content']}\n\n"
            
            if current_length + len(chunk_text) <= max_chars:
                context_parts.append(chunk_text)
                current_length += len(chunk_text)
            else:
                # Agregar parcialmente si hay espacio
                remaining = max_chars - current_length
                if remaining > 100:  # Solo si hay espacio significativo
                    context_parts.append(chunk_text[:remaining] + "...")
                break
        
        return "\n".join(context_parts)
    
    def get_full_knowledge_base(self) -> str:
        """Retorna la base de conocimiento completa"""
        return self.knowledge_base


# Instancia global del RAG
_rag_instance = None


def get_rag() -> SimpleRAG:
    """Obtiene la instancia singleton del RAG"""
    global _rag_instance
    
    if _rag_instance is None:
        # Ruta absoluta desde el archivo actual
        current_file = os.path.abspath(__file__)
        backend_dir = os.path.dirname(current_file)
        project_root = os.path.dirname(backend_dir)
        kb_path = os.path.join(project_root, "knowledge", "richmondpro_kb.md")
        
        # Verificar que el archivo existe
        if not os.path.exists(kb_path):
            raise FileNotFoundError(
                f"Base de conocimiento no encontrada en: {kb_path}\n"
                f"Verifica que el archivo knowledge/richmondpro_kb.md existe."
            )
        
        _rag_instance = SimpleRAG(kb_path)
    
    return _rag_instance

