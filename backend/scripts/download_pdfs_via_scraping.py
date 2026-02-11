import os
import requests
import re
import logging
from bs4 import BeautifulSoup
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PDF_DIR = os.path.join(os.path.dirname(__file__), '../../data/boe_pdf')
os.makedirs(PDF_DIR, exist_ok=True)

TARGET_LAWS = {
    "RDL 11/2024": "BOE-A-2024-26917",
    "Ley 9/2009": "BOE-A-2009-15931", # Assuming this is the correct ID for Ley 9/2009
    "RD 1415/2001": "BOE-A-2002-58"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

def get_pdf_url(boe_id):
    """Scrapes the BOE document page to find the PDF link."""
    url = f"https://www.boe.es/buscar/doc.php?id={boe_id}"
    logger.info(f"🔎 Inspecting {url}")
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Look for the PDF link class or structure
        # Common selector: a[title="PDF"] or link to .pdf
        # Try finding links containing 'pdfs'
        
        pdf_link = None
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Typical BOE PDF link: /boe/dias/2024/12/24/pdfs/BOE-A-2024-26917.pdf
            if '.pdf' in href and 'boe/dias' in href:
                pdf_link = href
                break
        
        if pdf_link:
            if pdf_link.startswith('/'):
                pdf_link = f"https://www.boe.es{pdf_link}"
            return pdf_link
            
        return None

    except Exception as e:
        logger.error(f"Error scraping {boe_id}: {e}")
        return None

def download_file(url, boe_id):
    try:
        logger.info(f"📥 Downloading {url}...")
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        
        filepath = os.path.join(PDF_DIR, f"{boe_id}.pdf")
        with open(filepath, "wb") as f:
            f.write(resp.content)
        logger.info(f"✅ Saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return False

def main():
    success = 0
    for name, boe_id in TARGET_LAWS.items():
        logger.info(f"Processing {name} ({boe_id})...")
        
        # 1. Try manual override for RDL 11/2024 (known URL)
        if boe_id == "BOE-A-2024-26917":
             # We know this one works via search, but let's test scraping too or just failover
             pass
        
        pdf_url = get_pdf_url(boe_id)
        
        if pdf_url:
            if download_file(pdf_url, boe_id):
                success += 1
        else:
            logger.warning(f"❌ Could not find PDF URL for {boe_id}")
            
        time.sleep(1)

    logger.info(f"Finished. Success: {success}/{len(TARGET_LAWS)}")

if __name__ == "__main__":
    main()
