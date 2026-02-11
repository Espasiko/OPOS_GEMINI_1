import os
import sys
import json
import logging
import pdfplumber
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directories
PDF_DIR = os.path.join(os.path.dirname(__file__), '../../data/boe_pdf')
JSON_DIR = os.path.join(os.path.dirname(__file__), '../../data/boe_xml')

def clean_text(text):
    """Basic text cleaning."""
    if not text: return ""
    text = re.sub(r'\s+', ' ', text) # Merge whitespaces
    return text.strip()

def pdf_to_json(pdf_path, boe_id):
    """Extracts text from PDF and wraps in BOE JSON structure."""
    full_text = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(clean_text(text))
        
        combined_text = "\n\n".join(full_text)
        
        # Create JSON structure compatible with process_and_chunk.py
        # Expected: data.metadatos and data.texto.bloque[].version.p[]._text
        
        law_json = {
            "data": {
                "metadatos": {
                    "identificador": {"_text": boe_id},
                    "titulo": {"_text": f"Ley {boe_id} (PDF Import)"}, # Fallback title
                    "numero_oficial": {"_text": boe_id},
                    "departamento": {"_text": "PDF Import"},
                    "url_html_consolidada": {"_text": f"PDF File: {os.path.basename(pdf_path)}"}
                },
                "texto": {
                    "bloque": [
                        {
                            "id": "pdf_content",
                            "version": {
                                "p": [
                                    {"_text": combined_text, "class": "parrafo"}
                                ]
                            }
                        }
                    ]
                }
            }
        }
        
        return law_json

    except Exception as e:
        logger.error(f"Error processing PDF {pdf_path}: {e}")
        return None

def main():
    if not os.path.exists(PDF_DIR):
        logger.error(f"PDF directory not found: {PDF_DIR}")
        return

    logger.info(f"🔄 Converting PDFs in {PDF_DIR} to JSON...")
    
    files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]
    count = 0
    
    for filename in files:
        boe_id = filename.replace(".pdf", "")
        pdf_path = os.path.join(PDF_DIR, filename)
        json_path = os.path.join(JSON_DIR, f"{boe_id}.json")
        
        logger.info(f"   Processing {filename}...")
        
        law_data = pdf_to_json(pdf_path, boe_id)
        
        if law_data:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(law_data, f, ensure_ascii=False, indent=2)
            logger.info(f"   ✅ Created {json_path}")
            count += 1
            
    logger.info(f"🎉 Conversion Complete. Converted {count} files.")

if __name__ == "__main__":
    main()
