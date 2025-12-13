import requests
from bs4 import BeautifulSoup
import sys
import os
import argparse

def scrape_boe(boe_id):
    url = f"https://www.boe.es/buscar/act.php?id={boe_id}&tn=1"
    print(f"🌍 Scraping {url}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    content = []
    
    # 1. Extract Title
    titulo = soup.find('h3', class_='documento-titulo')
    if titulo:
        title_text = titulo.get_text(strip=True)
        content.append(f"# {title_text}")
        print(f"✅ Found Title: {title_text[:50]}...")
    else:
        print("⚠️ Warning: Title not found")
        content.append(f"# {boe_id}")

    # 2. Extract Text Content
    # Strategy: Find main container. 
    # 'textoxslt' is standard for consolidation view.
    texto_div = soup.find('div', id='textoxslt') or soup.find('div', class_='textoxslt')
    
    if texto_div:
        # Iterate relevant elements, preserving structure
        for elem in texto_div.find_all(['p', 'h4', 'h5', 'div']): # 'div' sometimes wraps articles
            # Check for common structural classes
            if elem.get('class') and 'bloque' in elem.get('class'):
                 # Sometimes blocks are divs
                 pass

            text = elem.get_text(strip=True)
            if not text:
                continue
                
            # Headers detection (h4, h5 or specific classes)
            if elem.name in ['h4', 'h5'] or (elem.name == 'p' and (text.startswith('Artículo') or text.startswith('Disposición')) and len(text) < 200):
                content.append(f"\n## {text}")
            else:
                 # Standard paragraph
                content.append(text)
                
        print(f"✅ Extracted content from 'textoxslt' container")
    else:
        print("⚠️ 'textoxslt' container not found. Attempting fallback parse...")
        # Fallback: Scrape all paragraphs in the document body (risky but better than nothing)
        cnt = soup.select('.para')
        if cnt:
             for p in cnt:
                content.append(p.get_text(strip=True))
             print(f"✅ Extracted content using fallback '.para' selector")
        else:
            print("❌ Critical: No content found via standard or fallback selectors.")
            return

    # 3. Save to File
    output_dir = "backend/data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{boe_id}_scraped.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(content))
        
    print(f"💾 Saved to: {output_file}")
    print(f"📊 Total chunks/paragraphs extracted: {len(content)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal BOE Scraper")
    parser.add_argument("boe_id", help="BOE Identifier (e.g., BOE-A-2015-10438)")
    args = parser.parse_args()
    
    scrape_boe(args.boe_id)
