#!/usr/bin/env python3
"""
Descarga leyes directamente del BOE web (scraping)
Código Civil + búsqueda info Tratados UE
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json
import time

def download_codigo_civil_boe():
    """
    Descarga Código Civil del BOE (versión consolidada)
    """
    print("\n📥 Descargando Código Civil del BOE...")
    
    # URL consolidado BOE
    boe_id = "BOE-A-1889-4763"
    url =f"https://www.boe.es/buscar/act.php?id={boe_id}"
    
    print(f"   URL: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Guardar HTML completo
        output_dir = Path("/home/spas/OPOS_GEMINI_1/backend/data/leyes_extra")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        html_file = output_dir / f"codigo_civil_{boe_id}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"   ✅ HTML guardado: {html_file}")
        
        # Parsear para extraer texto
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar contenedor principal
        content = soup.find('div', class_='documento') or soup.find('div', id='textoLegislacion')
        
        if content:
            # Extraer artículos
            articulos = content.find_all(['p', 'div'], class_=lambda x: x and 'articulo' in x.lower()) if content else []
            
            text_content = content.get_text(separator='\n\n', strip=True)
            
            # Guardar texto plano
            txt_file = output_dir / f"codigo_civil_{boe_id}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(text_content)
            
            print(f"   ✅ Texto guardado: {txt_file}")
            print(f"   📊 Tamaño: {len(text_content):,} caracteres")
            
            # Metadata
            metadata = {
                'boe_id': boe_id,
                'titulo': 'Código Civil',
                'url_oficial': url,
                'caracteres': len(text_content),
                'descargado': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            metadata_file = output_dir / f"codigo_civil_{boe_id}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Metadata: {metadata_file}")
            
            return txt_file
        else:
            print("   ⚠️ No se encontró contenido principal")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def download_from_eurlex_direct():
    """
    Descarga Tratados UE directamente de EUR-Lex
    """
    print("\n📥 Descargando Tratados UE de EUR-Lex...")
    
    output_dir = Path("/home/spas/OPOS_GEMINI_1/backend/data/leyes_extra")
    
    tratados = {
        "TUE": {
            "celex": "12012M/TXT",
            "url": "https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:12012M/TXT",
            "nombre": "Tratado de la Unión Europea"
        },
        "TFUE": {
            "celex": "12012E/TXT",
            "url": "https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:12012E/TXT",
            "nombre": "Tratado de Funcionamiento UE"
        }
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }
    
    for key, tratado in tratados.items():
        print(f"\n   Descargando {tratado['nombre']}...")
        print(f"   URL: {tratado['url']}")
        
        try:
            response = requests.get(tratado['url'], headers=headers, timeout=30)
            response.raise_for_status()
            
            # Guardar HTML
            html_file = output_dir / f"{key}_eurlex.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"   ✅ HTML: {html_file}")
            
            # Parsear texto
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # EUR-Lex usa divs específicos
            content = soup.find('div', id='document') or soup.find('div', class_='text')
            
            if content:
                text = content.get_text(separator='\n\n', strip=True)
                
                txt_file = output_dir / f"{key}_eurlex.txt"
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                print(f"   ✅ Texto: {txt_file}")
                print(f"   📊 Tamaño: {len(text):,} caracteres")
            else:
                print(f"   ⚠️ Contenido no encontrado")
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    print("=" * 70)
    print("DESCARGA LEYES - BOE + EUR-LEX (Web Scraping)")
    print("=" * 70)
    
    # 1. Código Civil
    codigo_civil = download_codigo_civil_boe()
    
    # 2. Tratados UE
    download_from_eurlex_direct()
    
    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    
    output_dir = Path("/home/spas/OPOS_GEMINI_1/backend/data/leyes_extra")
    files = list(output_dir.glob("*"))
    
    print(f"\n📂 Archivos descargados ({len(files)}):")
    for f in files:
        size = f.stat().st_size
        print(f"   - {f.name} ({size:,} bytes)")
    
    print("\n✅ Descarga completada")
    print("\nPróximos pasos:")
    print("1. Parsear archivos TXT")
    print("2. Crear script ingesta para estos archivos")
    print("3. Ingestar en Qdrant local")

if __name__ == "__main__":
    main()
