#!/usr/bin/env python3
"""
Verificador Automático de URLs para Dataset Q&A
- Extrae URLs de respuestas LLM
- Verifica validez de cada URL
- Marca URLs inventadas
- Reduce score de confianza
"""

import requests
import re
import json
from typing import Dict, List, Tuple
from urllib.parse import urlparse

class URLVerifier:
    """Verificador automático de URLs"""
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_urls(self, text: str) -> List[str]:
        """Extrae todas las URLs de un texto"""
        # Patrón para URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+[^\s<>"{}|\\^`\[\].,;:!?)]'
        urls = re.findall(url_pattern, text)
        
        # Limpiar URLs
        cleaned_urls = []
        for url in urls:
            # Remover caracteres finales problemáticos
            url = url.rstrip('.,;:!?)')
            cleaned_urls.append(url)
        
        return list(set(cleaned_urls))  # Eliminar duplicados
    
    def verify_url(self, url: str) -> Dict:
        """
        Verifica una URL individual
        
        Returns:
            {
                "url": str,
                "valid": bool,
                "status_code": int,
                "status": str,
                "reason": str,
                "domain": str
            }
        """
        result = {
            "url": url,
            "valid": False,
            "status_code": 0,
            "status": "unknown",
            "reason": "",
            "domain": ""
        }
        
        try:
            # Parsear URL
            parsed = urlparse(url)
            result["domain"] = parsed.netloc
            
            # Verificar URL
            response = self.session.head(
                url,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            result["status_code"] = response.status_code
            
            if response.status_code == 200:
                result["valid"] = True
                result["status"] = "valid"
                result["reason"] = "URL accesible"
            elif response.status_code == 404:
                result["status"] = "not_found"
                result["reason"] = "URL no existe (404)"
            elif response.status_code == 403:
                result["status"] = "forbidden"
                result["reason"] = "Acceso bloqueado (403) - posiblemente inventada"
            elif response.status_code >= 400:
                result["status"] = "error"
                result["reason"] = f"Error HTTP {response.status_code}"
            else:
                result["status"] = "redirect"
                result["reason"] = f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            result["status"] = "timeout"
            result["reason"] = f"Timeout (>{self.timeout}s)"
            
        except requests.exceptions.ConnectionError:
            result["status"] = "connection_error"
            result["reason"] = "No se puede conectar - URL probablemente inventada"
            
        except requests.exceptions.InvalidURL:
            result["status"] = "invalid"
            result["reason"] = "URL mal formada"
            
        except Exception as e:
            result["status"] = "error"
            result["reason"] = f"Error: {str(e)[:100]}"
        
        return result
    
    def verify_all_urls(self, text: str) -> Dict:
        """
        Verifica todas las URLs en un texto
        
        Returns:
            {
                "urls_found": int,
                "urls_valid": int,
                "urls_invalid": int,
                "validity_rate": float,
                "results": List[Dict]
            }
        """
        urls = self.extract_urls(text)
        
        if not urls:
            return {
                "urls_found": 0,
                "urls_valid": 0,
                "urls_invalid": 0,
                "validity_rate": 1.0,  # Sin URLs = 100% válido
                "results": []
            }
        
        results = []
        for url in urls:
            result = self.verify_url(url)
            results.append(result)
        
        valid_count = sum(1 for r in results if r["valid"])
        invalid_count = len(results) - valid_count
        
        return {
            "urls_found": len(urls),
            "urls_valid": valid_count,
            "urls_invalid": invalid_count,
            "validity_rate": valid_count / len(urls) if urls else 1.0,
            "results": results
        }
    
    def verify_qa_pair(self, qa_data: Dict) -> Dict:
        """
        Verifica URLs en un par Q&A y ajusta confianza
        
        Args:
            qa_data: {
                "question": str,
                "answer": str,
                "explanation": str,
                "sources": List[str],  # opcional
                "confidence": float,   # opcional
                ...
            }
        
        Returns:
            qa_data actualizado con:
                - url_verification: Dict con resultados
                - confidence: ajustado según URLs
                - warnings: lista de advertencias
        """
        # Extraer todo el texto
        text_parts = [
            qa_data.get("question", ""),
            qa_data.get("answer", ""),
            qa_data.get("explanation", ""),
        ]
        
        # Añadir sources si existen
        if "sources" in qa_data and isinstance(qa_data["sources"], list):
            text_parts.extend(qa_data["sources"])
        
        full_text = " ".join(str(p) for p in text_parts)
        
        # Verificar URLs
        verification = self.verify_all_urls(full_text)
        qa_data["url_verification"] = verification
        
        # Inicializar warnings si no existe
        if "warnings" not in qa_data:
            qa_data["warnings"] = []
        
        # Ajustar confianza según URLs
        if "confidence" not in qa_data:
            qa_data["confidence"] = 1.0
        
        if verification["urls_found"] > 0:
            validity_rate = verification["validity_rate"]
            
            if validity_rate < 1.0:
                # Reducir confianza proporcionalmente
                original_confidence = qa_data["confidence"]
                
                # Penalización: 0.1 por cada URL inválida
                penalty = verification["urls_invalid"] * 0.1
                qa_data["confidence"] = max(0.0, original_confidence - penalty)
                
                # Añadir warning
                qa_data["warnings"].append(
                    f"{verification['urls_invalid']}/{verification['urls_found']} "
                    f"URLs inválidas o inventadas"
                )
                
                # Listar URLs problemáticas
                for result in verification["results"]:
                    if not result["valid"]:
                        qa_data["warnings"].append(
                            f"URL inválida: {result['url']} - {result['reason']}"
                        )
        
        return qa_data


def test_verifier():
    """Prueba el verificador con ejemplos"""
    print("="*80)
    print("🧪 PRUEBA: Verificador Automático de URLs")
    print("="*80)
    
    verifier = URLVerifier()
    
    # Ejemplo 1: URLs válidas del BOE
    print("\n1️⃣ Probando URLs del BOE (válidas):")
    text1 = """
    Según el artículo 205 LGSS:
    https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724
    https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a205
    """
    
    result1 = verifier.verify_all_urls(text1)
    print(f"   URLs encontradas: {result1['urls_found']}")
    print(f"   URLs válidas: {result1['urls_valid']}")
    print(f"   Tasa validez: {result1['validity_rate']*100:.0f}%")
    
    for r in result1['results']:
        status_icon = "✅" if r['valid'] else "❌"
        print(f"   {status_icon} {r['url'][:60]}... - {r['reason']}")
    
    # Ejemplo 2: URLs inventadas
    print("\n2️⃣ Probando URLs inventadas:")
    text2 = """
    Más información en:
    https://www.seg-social.es/wps/portal/wss/internet/fake/12345
    https://www.boe.es/buscar/act.php?id=FAKE-123
    """
    
    result2 = verifier.verify_all_urls(text2)
    print(f"   URLs encontradas: {result2['urls_found']}")
    print(f"   URLs válidas: {result2['urls_valid']}")
    print(f"   Tasa validez: {result2['validity_rate']*100:.0f}%")
    
    for r in result2['results']:
        status_icon = "✅" if r['valid'] else "❌"
        print(f"   {status_icon} {r['url'][:60]}... - {r['reason']}")
    
    # Ejemplo 3: Q&A completo
    print("\n3️⃣ Probando Q&A completo:")
    qa = {
        "question": "¿Cuál es la edad de jubilación?",
        "answer": "67 años",
        "explanation": "Según artículo 205 LGSS",
        "sources": [
            "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
            "https://www.fake-url-inventada.com/fake"
        ],
        "confidence": 1.0
    }
    
    qa_verified = verifier.verify_qa_pair(qa)
    
    print(f"   Confianza original: 1.0")
    print(f"   Confianza ajustada: {qa_verified['confidence']:.2f}")
    print(f"   URLs válidas: {qa_verified['url_verification']['urls_valid']}/{qa_verified['url_verification']['urls_found']}")
    
    if qa_verified['warnings']:
        print(f"   Warnings:")
        for w in qa_verified['warnings']:
            print(f"      ⚠️ {w}")
    
    # Guardar ejemplo
    with open("url_verification_example.json", "w", encoding="utf-8") as f:
        json.dump(qa_verified, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("✅ Prueba completada")
    print("📄 Ejemplo guardado en: url_verification_example.json")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_verifier()
