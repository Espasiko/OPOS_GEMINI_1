import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_boe_rd84():
    url = "https://www.boe.es/buscar/act.php?id=BOE-A-1996-4447&tn=1"
    print(f"Scraping {url}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # El texto consolidado suele estar en un div con id 'textoxslt' o similar, o directamente en el body
    # En la versión web del BOE, el texto está estructurado en parrafos <p> dentro de <div>
    
    content = []
    
    # Buscar título
    titulo = soup.find('h3', class_='documento-titulo')
    if titulo:
        content.append(f"# {titulo.get_text(strip=True)}")
    
    # Buscar bloques de texto
    # Esta es una aproximación básica. La estructura real puede variar.
    texto_div = soup.find('div', id='textoxslt')
    
    if not texto_div:
        # Fallback si no encuentra el div específico
        texto_div = soup.find('div', class_='textoxslt')

    if texto_div:
        for elem in texto_div.find_all(['p', 'h4', 'h5']):
            text = elem.get_text(strip=True)
            if not text:
                continue
                
            if elem.name in ['h4', 'h5']:
                content.append(f"\n## {text}")
            else:
                content.append(text)
    else:
        print("No se encontró el contenedor de texto principal.")
        # Intento de extraer del body general con selectores más amplios
        cnt = soup.select('.para')
        for p in cnt:
             content.append(p.get_text(strip=True))

    output_file = "backend/data/RD_84_1996_scraped.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(content))
        
    print(f"Scraping completado. Guardado en {output_file}")
    print(f"Total líneas extraídas: {len(content)}")
    print("Primeras 5 líneas:")
    for line in content[:5]:
        print(f"- {line[:100]}...")

if __name__ == "__main__":
    scrape_boe_rd84()
