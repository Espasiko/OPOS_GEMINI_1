#!/usr/bin/env python3
"""
Verificador automático de URLs para Q&A
Detecta URLs inventadas y las marca para revisión
"""

import requests
import re
import json
import time
from urllib.parse import urlparse
from typing import List, Dict, Any, Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table

console = Console()

class URLVerifier:
    """Verificador automático de URLs en Q&A"""
    
    def __init__(self, timeout: int = 10, max_retries: int = 2):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Dominios confiables
        self.trusted_domains = {
            'boe.es': 'BOE - Boletín Oficial del Estado',
            'seg-social.es': 'Seguridad Social',
            'inss.es': 'Instituto Nacional de la Seguridad Social',
            'mites.gob.es': 'Ministerio de Trabajo',
            'hacienda.gob.es': 'Ministerio de Hacienda',
            'administracion.gob.es': 'Administración General del Estado',
            'poderjudicial.es': 'Poder Judicial',
            'congreso.es': 'Congreso de los Diputados',
            'senado.es': 'Senado'
        }
        
        # Estadísticas
        self.stats = {
            'total_urls': 0,
            'valid_urls': 0,
            'invalid_urls': 0,
            'timeout_urls': 0,
            'trusted_domains': 0
        }
    
    def extract_urls(self, text: str) -> List[str]:
        """Extrae todas las URLs de un texto"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(url_pattern, text)
    
    def is_trusted_domain(self, url: str) -> Tuple[bool, str]:
        """Verifica si la URL es de un dominio confiable"""
        try:
            domain = urlparse(url).netloc.lower()
            for trusted, name in self.trusted_domains.items():
                if trusted in domain:
                    return True, name
            return False, ""
        except:
            return False, ""
    
    def verify_url(self, url: str) -> Dict[str, Any]:
        """Verifica una URL individual"""
        result = {
            'url': url,
            'valid': False,
            'status_code': None,
            'error': None,
            'trusted': False,
            'trusted_source': None,
            'response_time': None
        }
        
        # Verificar dominio confiable
        is_trusted, source = self.is_trusted_domain(url)
        result['trusted'] = is_trusted
        result['trusted_source'] = source
        
        # Intentar verificar la URL
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                response = self.session.head(
                    url, 
                    timeout=self.timeout, 
                    allow_redirects=True
                )
                result['response_time'] = time.time() - start_time
                result['status_code'] = response.status_code
                
                if response.status_code == 200:
                    result['valid'] = True
                    self.stats['valid_urls'] += 1
                    if is_trusted:
                        self.stats['trusted_domains'] += 1
                    return result
                elif response.status_code == 404:
                    result['error'] = 'NOT_FOUND'
                    self.stats['invalid_urls'] += 1
                    return result
                else:
                    result['error'] = f'HTTP_{response.status_code}'
                    self.stats['invalid_urls'] += 1
                    return result
                    
            except requests.Timeout:
                if attempt == self.max_retries - 1:
                    result['error'] = 'TIMEOUT'
                    self.stats['timeout_urls'] += 1
                    return result
                time.sleep(1)
                
            except requests.RequestException as e:
                result['error'] = f'REQUEST_ERROR: {str(e)}'
                self.stats['invalid_urls'] += 1
                return result
            
            except Exception as e:
                result['error'] = f'UNKNOWN_ERROR: {str(e)}'
                self.stats['invalid_urls'] += 1
                return result
        
        return result
    
    def verify_qa_urls(self, qa_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica todas las URLs en una Q&A"""
        # Extraer URLs del contenido completo
        full_text = json.dumps(qa_data, ensure_ascii=False)
        urls = self.extract_urls(full_text)
        
        if not urls:
            qa_data['url_verification'] = {
                'urls_found': 0,
                'urls_valid': 0,
                'urls_invalid': 0,
                'verification_status': 'NO_URLS',
                'confidence_penalty': 0.0
            }
            return qa_data
        
        # Verificar cada URL
        verification_results = []
        for url in urls:
            self.stats['total_urls'] += 1
            result = self.verify_url(url)
            verification_results.append(result)
        
        # Calcular estadísticas
        valid_count = sum(1 for r in verification_results if r['valid'])
        invalid_count = len(verification_results) - valid_count
        
        # Calcular penalización de confianza
        confidence_penalty = 0.0
        if invalid_count > 0:
            # Penalizar más si son URLs de dominios confiables pero inválidas
            trusted_invalid = sum(
                1 for r in verification_results 
                if r['trusted'] and not r['valid']
            )
            confidence_penalty = (invalid_count * 0.15) + (trusted_invalid * 0.10)
        
        # Agregar metadata de verificación
        qa_data['url_verification'] = {
            'urls_found': len(urls),
            'urls_valid': valid_count,
            'urls_invalid': invalid_count,
            'verification_status': 'PASS' if invalid_count == 0 else 'FAIL',
            'confidence_penalty': min(confidence_penalty, 0.5),  # Max 50% penalty
            'details': verification_results
        }
        
        # Ajustar confianza si existe
        if 'confidence' in qa_data:
            qa_data['confidence'] = max(
                0.0, 
                qa_data['confidence'] - confidence_penalty
            )
        
        # Marcar para revisión si hay URLs inválidas
        if invalid_count > 0:
            if 'flags' not in qa_data:
                qa_data['flags'] = []
            qa_data['flags'].append('INVALID_URLS')
            
            if 'review_priority' in qa_data:
                # Aumentar prioridad si hay URLs inválidas
                if qa_data['review_priority'] == 'low':
                    qa_data['review_priority'] = 'medium'
                elif qa_data['review_priority'] == 'medium':
                    qa_data['review_priority'] = 'high'
        
        return qa_data
    
    def verify_dataset(self, input_file: str, output_file: str = None) -> Dict[str, Any]:
        """Verifica todas las URLs en un dataset JSONL"""
        console.print("\n[bold cyan]🔗 Verificando URLs en dataset...[/bold cyan]\n")
        
        if output_file is None:
            output_file = input_file.replace('.jsonl', '_verified.jsonl')
        
        verified_data = []
        
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("Verificando URLs...", total=len(lines))
            
            for line in lines:
                qa_data = json.loads(line)
                verified_qa = self.verify_qa_urls(qa_data)
                verified_data.append(verified_qa)
                progress.advance(task)
        
        # Guardar dataset verificado
        with open(output_file, 'w', encoding='utf-8') as f:
            for qa in verified_data:
                f.write(json.dumps(qa, ensure_ascii=False) + '\n')
        
        # Mostrar estadísticas
        self.print_stats(len(verified_data))
        
        console.print(f"\n✅ Dataset verificado guardado en: [green]{output_file}[/green]\n")
        
        return {
            'input_file': input_file,
            'output_file': output_file,
            'total_qa': len(verified_data),
            'stats': self.stats
        }
    
    def print_stats(self, total_qa: int):
        """Imprime estadísticas de verificación"""
        table = Table(title="📊 Estadísticas de Verificación de URLs")
        
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="magenta", justify="right")
        table.add_column("Porcentaje", style="green", justify="right")
        
        table.add_row(
            "Total Q&A procesadas",
            str(total_qa),
            "100%"
        )
        
        table.add_row(
            "Total URLs encontradas",
            str(self.stats['total_urls']),
            f"{self.stats['total_urls']/total_qa:.1f} por Q&A"
        )
        
        if self.stats['total_urls'] > 0:
            valid_pct = (self.stats['valid_urls'] / self.stats['total_urls']) * 100
            invalid_pct = (self.stats['invalid_urls'] / self.stats['total_urls']) * 100
            timeout_pct = (self.stats['timeout_urls'] / self.stats['total_urls']) * 100
            trusted_pct = (self.stats['trusted_domains'] / self.stats['total_urls']) * 100
            
            table.add_row(
                "URLs válidas ✅",
                str(self.stats['valid_urls']),
                f"{valid_pct:.1f}%"
            )
            
            table.add_row(
                "URLs inválidas ❌",
                str(self.stats['invalid_urls']),
                f"{invalid_pct:.1f}%"
            )
            
            table.add_row(
                "URLs timeout ⏱️",
                str(self.stats['timeout_urls']),
                f"{timeout_pct:.1f}%"
            )
            
            table.add_row(
                "Dominios confiables 🔒",
                str(self.stats['trusted_domains']),
                f"{trusted_pct:.1f}%"
            )
        
        console.print("\n")
        console.print(table)
        console.print("\n")


def main():
    """Función principal para uso standalone"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Verificador automático de URLs en datasets Q&A'
    )
    parser.add_argument(
        'input_file',
        help='Archivo JSONL de entrada'
    )
    parser.add_argument(
        '-o', '--output',
        help='Archivo JSONL de salida (default: input_verified.jsonl)'
    )
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=10,
        help='Timeout en segundos para verificación (default: 10)'
    )
    parser.add_argument(
        '-r', '--retries',
        type=int,
        default=2,
        help='Número de reintentos (default: 2)'
    )
    
    args = parser.parse_args()
    
    verifier = URLVerifier(timeout=args.timeout, max_retries=args.retries)
    result = verifier.verify_dataset(args.input_file, args.output)
    
    console.print(f"\n[bold green]✅ Verificación completada![/bold green]")
    console.print(f"Total Q&A: {result['total_qa']}")
    console.print(f"Total URLs: {result['stats']['total_urls']}")
    console.print(f"URLs válidas: {result['stats']['valid_urls']}")
    console.print(f"URLs inválidas: {result['stats']['invalid_urls']}\n")


if __name__ == '__main__':
    main()
