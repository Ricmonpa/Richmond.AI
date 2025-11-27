"""
Web Scraper para extraer contenido de richmondpro.global
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import os
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set
import time


class RichmondProScraper:
    """Scraper para extraer contenido de RichmondPro"""
    
    def __init__(self, base_url: str = "https://richmondpro.global"):
        self.base_url = base_url
        self.visited_urls: Set[str] = set()
        self.content_chunks: List[Dict[str, str]] = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def clean_text(self, text: str) -> str:
        """Limpia y normaliza el texto"""
        if not text:
            return ""
        
        # Remover espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        # Remover caracteres especiales problemáticos
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        # Remover saltos de línea múltiples
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def extract_text_from_element(self, element) -> str:
        """Extrae texto de un elemento HTML, removiendo scripts y estilos"""
        # Clonar el elemento para no modificar el original
        clone = BeautifulSoup(str(element), 'html.parser')
        
        # Remover scripts y estilos
        for script in clone(['script', 'style', 'noscript']):
            script.decompose()
        
        # Obtener texto
        text = clone.get_text(separator=' ', strip=True)
        return self.clean_text(text)
    
    def extract_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """Extrae enlaces relevantes de la página"""
        links = []
        base_domain = urlparse(self.base_url).netloc
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            parsed = urlparse(full_url)
            
            # Solo enlaces del mismo dominio
            if parsed.netloc == base_domain or not parsed.netloc:
                # Normalizar URL
                if not parsed.netloc:
                    full_url = urljoin(self.base_url, href)
                
                # Solo URLs válidas (no javascript:, mailto:, etc.)
                if parsed.scheme in ['http', 'https', '']:
                    # Remover fragmentos y parámetros de tracking
                    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                    # Remover trailing slash para normalizar
                    if clean_url.endswith('/') and clean_url != self.base_url + '/':
                        clean_url = clean_url[:-1]
                    
                    # Filtrar URLs no deseadas
                    skip_patterns = [
                        '/wp-admin', '/wp-content/uploads', '/feed', '/xmlrpc',
                        '/tag/', '/category/', '/author/', '.pdf', '.jpg', '.png',
                        '/search', '/login', '/register', '#'
                    ]
                    
                    should_skip = any(pattern in clean_url for pattern in skip_patterns)
                    
                    if (clean_url.startswith(self.base_url) and 
                        clean_url not in self.visited_urls and 
                        not should_skip):
                        links.append(clean_url)
        
        return list(set(links))
    
    def scrape_page(self, url: str) -> Dict[str, any]:
        """Extrae contenido de una página específica"""
        try:
            print(f"📄 Scrapeando: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer título
            title = ""
            if soup.title:
                title = self.clean_text(soup.title.get_text())
            elif soup.find('h1'):
                title = self.extract_text_from_element(soup.find('h1'))
            
            # Extraer contenido principal
            content_parts = []
            
            # Buscar en diferentes secciones comunes
            main_selectors = [
                'main', 'article', '.entry-content', '.post-content',
                '.content', '#content', '.main-content', 'section'
            ]
            
            main_content = None
            for selector in main_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break
            
            if not main_content:
                main_content = soup.find('body')
            
            if main_content:
                # Extraer headings y párrafos de forma más exhaustiva
                # Primero headings (estructura)
                for heading in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                    text = self.extract_text_from_element(heading)
                    if text and len(text) > 5:
                        content_parts.append(f"## {text}")
                
                # Luego párrafos y listas
                for element in main_content.find_all(['p', 'li', 'span', 'div']):
                    text = self.extract_text_from_element(element)
                    # Filtrar textos muy cortos o que son solo números/símbolos
                    if (text and len(text) > 30 and 
                        not re.match(r'^[\d\s\W]+$', text) and
                        text not in content_parts[-10:]):  # Evitar duplicados recientes
                        content_parts.append(text)
            
            # Si no encontramos mucho contenido, intentar extraer todo el body
            if len(content_parts) < 5:
                body_text = self.extract_text_from_element(soup.find('body'))
                if body_text and len(body_text) > 100:
                    # Dividir en párrafos lógicos
                    paragraphs = re.split(r'\n\s*\n', body_text)
                    for para in paragraphs:
                        para = self.clean_text(para)
                        if para and len(para) > 50:
                            content_parts.append(para)
            
            # Combinar contenido
            full_content = '\n\n'.join(content_parts)
            full_content = self.clean_text(full_content)
            
            # Extraer enlaces
            links = self.extract_links(soup, url)
            
            return {
                'url': url,
                'title': title,
                'content': full_content,
                'links': links
            }
        
        except Exception as e:
            print(f"❌ Error scrapeando {url}: {e}")
            return None
    
    def scrape_site(self, max_pages: int = 20) -> List[Dict[str, str]]:
        """Scrapea el sitio completo"""
        print(f"🚀 Iniciando scraping de {self.base_url}")
        
        # URLs conocidas comunes de RichmondPro
        common_urls = [
            self.base_url,
            f"{self.base_url}/about",
            f"{self.base_url}/about-us",
            f"{self.base_url}/solutions",
            f"{self.base_url}/our-solutions",
            f"{self.base_url}/services",
            f"{self.base_url}/contact",
            f"{self.base_url}/contact-us",
            f"{self.base_url}/content-curriculum",
            f"{self.base_url}/assessment-center",
            f"{self.base_url}/professional-preparation",
            f"{self.base_url}/employability",
        ]
        
        # Empezar con URLs conocidas + página principal
        urls_to_visit = list(set(common_urls))
        all_content = []
        
        while urls_to_visit and len(self.visited_urls) < max_pages:
            url = urls_to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
            
            self.visited_urls.add(url)
            
            # Scrapear página
            page_data = self.scrape_page(url)
            
            if page_data and page_data['content']:
                all_content.append(page_data)
                
                # Agregar nuevos enlaces a la cola
                for link in page_data.get('links', []):
                    if link not in self.visited_urls and link not in urls_to_visit:
                        urls_to_visit.append(link)
            
            # Pausa para no sobrecargar el servidor
            time.sleep(1)
        
        print(f"✅ Scraping completado: {len(all_content)} páginas")
        return all_content
    
    def chunk_content(self, content_list: List[Dict], chunk_size: int = 800, overlap: int = 150) -> List[Dict[str, str]]:
        """Divide el contenido en chunks para RAG, priorizando secciones semánticas"""
        chunks = []
        
        for page in content_list:
            url = page['url']
            title = page['title']
            content = page['content']
            
            # Intentar dividir por secciones (headings, párrafos largos)
            # Primero buscar patrones de secciones
            sections = re.split(r'(##\s+[^\n]+|Three Pillars|Assessment Center|Professional Development|Institutional Benefits)', content, flags=re.IGNORECASE)
            
            current_section = ""
            section_title = title
            
            for i, section in enumerate(sections):
                section = section.strip()
                if not section:
                    continue
                
                # Si es un título de sección
                if section.startswith('##') or any(keyword in section for keyword in ['Three Pillars', 'Assessment Center', 'Professional Development', 'Institutional Benefits']):
                    # Guardar sección anterior si tiene contenido
                    if current_section and len(current_section.strip()) > 50:
                        words = current_section.split()
                        for j in range(0, len(words), chunk_size - overlap):
                            chunk_words = words[j:j + chunk_size]
                            chunk_text = ' '.join(chunk_words)
                            if len(chunk_text.strip()) > 100:
                                chunks.append({
                                    'url': url,
                                    'title': f"{title} - {section_title}",
                                    'content': chunk_text,
                                    'chunk_id': len(chunks)
                                })
                    
                    # Nueva sección
                    section_title = section[:100] if len(section) < 100 else section[:100] + "..."
                    current_section = section + " "
                else:
                    current_section += section + " "
            
            # Guardar última sección
            if current_section and len(current_section.strip()) > 50:
                words = current_section.split()
                for j in range(0, len(words), chunk_size - overlap):
                    chunk_words = words[j:j + chunk_size]
                    chunk_text = ' '.join(chunk_words)
                    if len(chunk_text.strip()) > 100:
                        chunks.append({
                            'url': url,
                            'title': f"{title} - {section_title}",
                            'content': chunk_text,
                            'chunk_id': len(chunks)
                        })
            
            # Si no se encontraron secciones, dividir normalmente
            if not chunks:
                words = content.split()
                for i in range(0, len(words), chunk_size - overlap):
                    chunk_words = words[i:i + chunk_size]
                    chunk_text = ' '.join(chunk_words)
                    if len(chunk_text.strip()) > 100:
                        chunks.append({
                            'url': url,
                            'title': title,
                            'content': chunk_text,
                            'chunk_id': len(chunks)
                        })
        
        print(f"✅ Contenido dividido en {len(chunks)} chunks")
        return chunks
    
    def save_to_file(self, chunks: List[Dict], filename: str = "richmondpro_scraped.json"):
        """Guarda los chunks en un archivo JSON"""
        # Intentar guardar en knowledge/ primero, luego en backend/knowledge/
        paths_to_try = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge", filename),
            os.path.join(os.path.dirname(__file__), "knowledge", filename)
        ]
        
        for filepath in paths_to_try:
            try:
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(chunks, f, ensure_ascii=False, indent=2)
                print(f"✅ Contenido guardado en: {filepath}")
                return filepath
            except Exception as e:
                continue
        
        raise Exception(f"No se pudo guardar el archivo en ninguna ubicación")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Contenido guardado en: {filepath}")
        return filepath


def main():
    """Función principal para ejecutar el scraper"""
    scraper = RichmondProScraper()
    
    # Scrapear sitio
    content = scraper.scrape_site(max_pages=15)
    
    # Dividir en chunks
    chunks = scraper.chunk_content(content)
    
    # Guardar
    scraper.save_to_file(chunks)
    
    print(f"\n📊 Resumen:")
    print(f"   - Páginas scrapeadas: {len(content)}")
    print(f"   - Chunks creados: {len(chunks)}")
    print(f"   - Total de caracteres: {sum(len(c['content']) for c in chunks)}")


if __name__ == "__main__":
    main()

