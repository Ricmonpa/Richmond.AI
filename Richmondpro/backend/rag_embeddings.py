"""
Sistema RAG mejorado con búsqueda semántica usando embeddings simples
"""

import os
import json
import re
from typing import List, Dict, Tuple
from collections import Counter
import math


class SimpleEmbeddingRAG:
    """
    Sistema RAG simple usando TF-IDF y similitud de coseno
    No requiere librerías externas de ML
    """
    
    def __init__(self, knowledge_base_path: str):
        """
        Inicializa el RAG con la base de conocimiento
        
        Args:
            knowledge_base_path: Ruta al archivo JSON con chunks scraped
        """
        self.knowledge_base_path = knowledge_base_path
        self.chunks = self._load_knowledge_base()
        self.vocabulary = self._build_vocabulary()
        self.tf_idf_vectors = self._compute_tf_idf()
    
    def _load_knowledge_base(self) -> List[Dict]:
        """Carga la base de conocimiento desde el archivo JSON"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            print(f"✅ Base de conocimiento cargada: {len(chunks)} chunks")
            return chunks
        except FileNotFoundError:
            print(f"⚠️ Archivo no encontrado: {self.knowledge_base_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Error parseando JSON: {e}")
            return []
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokeniza el texto en palabras"""
        # Convertir a minúsculas y extraer palabras
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def _build_vocabulary(self) -> Dict[str, int]:
        """Construye el vocabulario de todos los chunks"""
        vocabulary = {}
        word_id = 0
        
        for chunk in self.chunks:
            words = self._tokenize(chunk['content'])
            for word in words:
                if word not in vocabulary:
                    vocabulary[word] = word_id
                    word_id += 1
        
        return vocabulary
    
    def _compute_tf(self, words: List[str]) -> Dict[str, float]:
        """Calcula Term Frequency"""
        word_count = Counter(words)
        total_words = len(words)
        
        if total_words == 0:
            return {}
        
        tf = {}
        for word, count in word_count.items():
            tf[word] = count / total_words
        
        return tf
    
    def _compute_idf(self) -> Dict[str, float]:
        """Calcula Inverse Document Frequency"""
        idf = {}
        total_docs = len(self.chunks)
        
        for word in self.vocabulary:
            # Contar en cuántos documentos aparece la palabra
            doc_count = sum(1 for chunk in self.chunks 
                          if word in self._tokenize(chunk['content']))
            
            if doc_count > 0:
                idf[word] = math.log(total_docs / doc_count)
            else:
                idf[word] = 0
        
        return idf
    
    def _compute_tf_idf(self) -> List[Dict[str, float]]:
        """Calcula vectores TF-IDF para cada chunk"""
        idf = self._compute_idf()
        tf_idf_vectors = []
        
        for chunk in self.chunks:
            words = self._tokenize(chunk['content'])
            tf = self._compute_tf(words)
            
            tf_idf = {}
            for word, tf_value in tf.items():
                if word in idf:
                    tf_idf[word] = tf_value * idf[word]
            
            tf_idf_vectors.append(tf_idf)
        
        return tf_idf_vectors
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calcula similitud de coseno entre dos vectores"""
        # Obtener todas las palabras únicas
        all_words = set(vec1.keys()) | set(vec2.keys())
        
        if not all_words:
            return 0.0
        
        # Calcular producto punto y magnitudes
        dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in all_words)
        magnitude1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        magnitude2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _query_to_vector(self, query: str) -> Dict[str, float]:
        """Convierte una consulta en un vector TF-IDF"""
        words = self._tokenize(query)
        tf = self._compute_tf(words)
        
        # Calcular IDF para la consulta (usar IDF del corpus)
        idf = self._compute_idf()
        
        query_vector = {}
        for word, tf_value in tf.items():
            if word in self.vocabulary and word in idf:
                query_vector[word] = tf_value * idf[word]
        
        return query_vector
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Busca los chunks más relevantes para una consulta
        
        Args:
            query: Consulta del usuario
            top_k: Número de chunks a retornar
            
        Returns:
            Lista de tuplas (chunk, score) ordenadas por relevancia
        """
        if not self.chunks:
            return []
        
        query_vector = self._query_to_vector(query)
        
        # Calcular similitud con cada chunk
        scores = []
        for i, chunk in enumerate(self.chunks):
            chunk_vector = self.tf_idf_vectors[i]
            similarity = self._cosine_similarity(query_vector, chunk_vector)
            scores.append((chunk, similarity))
        
        # Ordenar por score descendente
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Retornar top_k
        return scores[:top_k]
    
    def get_context(self, query: str, max_chars: int = 3000) -> str:
        """
        Obtiene contexto relevante para una consulta
        
        Args:
            query: Consulta del usuario
            max_chars: Máximo de caracteres en el contexto
            
        Returns:
            String con contexto relevante formateado
        """
        relevant_chunks = self.search(query, top_k=10)
        
        context_parts = []
        current_length = 0
        
        for chunk, score in relevant_chunks:
            if score < 0.01:  # Filtrar chunks con muy baja relevancia
                continue
            
            chunk_text = f"## {chunk.get('title', 'Contenido')}\n"
            chunk_text += f"**Fuente:** {chunk.get('url', 'N/A')}\n\n"
            chunk_text += f"{chunk.get('content', '')}\n\n"
            
            if current_length + len(chunk_text) <= max_chars:
                context_parts.append(chunk_text)
                current_length += len(chunk_text)
            else:
                # Agregar parcialmente si hay espacio
                remaining = max_chars - current_length
                if remaining > 100:
                    context_parts.append(chunk_text[:remaining] + "...")
                break
        
        return "\n".join(context_parts) if context_parts else "No se encontró información relevante en el sitio web."


# Instancia global del RAG scraped
_scraped_rag_instance = None

def get_scraped_rag():
    """Obtiene instancia del RAG con contenido scraped"""
    global _scraped_rag_instance
    
    if _scraped_rag_instance is None:
        # Intentar múltiples ubicaciones
        paths_to_try = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge", "richmondpro_scraped.json"),
            os.path.join(os.path.dirname(__file__), "knowledge", "richmondpro_scraped.json")
        ]
        
        for knowledge_path in paths_to_try:
            if os.path.exists(knowledge_path):
                try:
                    _scraped_rag_instance = SimpleEmbeddingRAG(knowledge_path)
                    return _scraped_rag_instance
                except Exception as e:
                    print(f"⚠️ Error cargando RAG scraped desde {knowledge_path}: {e}")
                    continue
        
        # Si no se encontró, retornar None
        print("⚠️ No se encontró archivo richmondpro_scraped.json")
        return None
    
    return _scraped_rag_instance

