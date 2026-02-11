import os
import sys
import logging
from time import sleep

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agents.boe_api_client import BOEApiClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory setup
PDF_DIR = os.path.join(os.path.dirname(__file__), '../../data/boe_pdf')
os.makedirs(PDF_DIR, exist_ok=True)

# Missing laws to download as PDF
MISSING_LAWS_PDF = {
    "RDL 11/2024 Mejora Pensiones": "BOE-A-2024-26917",
    "Ley 9/2009 Ampliación Paternidad": "BOE-A-2009-15931", # Corrected (original failed ID)
    "RD 1415/2001 Catalogación Defensa": "BOE-A-2002-58"
}

def main():
    logger.info(f"⬇️ Starting PDF download for {len(MISSING_LAWS_PDF)} laws...")
    
    with BOEApiClient() as client:
        success_count = 0
        
        for name, boe_id in MISSING_LAWS_PDF.items():
            try:
                filepath = os.path.join(PDF_DIR, f"{boe_id}.pdf")
                if os.path.exists(filepath):
                    logger.info(f"✅ Exists: {name} ({boe_id})")
                    success_count += 1
                    continue
                
                logger.info(f"📥 Downloading PDF: {name} ({boe_id})...")
                
                # Fetch PDF bytes using the API client
                pdf_content = client.get_documento_boe(boe_id, formato="pdf")
                
                with open(filepath, "wb") as f:
                    f.write(pdf_content)
                
                logger.info(f"   Saved to {filepath}")
                success_count += 1
                sleep(1) # Be polite
                
            except Exception as e:
                logger.error(f"❌ Failed {name} ({boe_id}): {str(e)}")

        logger.info(f"🎉 PDF Download Complete. Success: {success_count}/{len(MISSING_LAWS_PDF)}")

if __name__ == "__main__":
    main()
