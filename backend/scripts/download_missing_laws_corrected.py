import os
import sys
import json
import logging
import time

# Add backend directory to path to import agents
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agents.boe_api_client import BOEApiClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('download_missing_corrected.log')
    ]
)
logger = logging.getLogger(__name__)

# Directory to save JSON files
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/boe_xml')
os.makedirs(DATA_DIR, exist_ok=True)

# Corrected mapping of Missing Law Name -> Correct BOE ID
CORRECTED_LAWS = {
    "LO 3/1981 Defensor del Pueblo": "BOE-A-1981-10325",
    "LO 2/1982 Tribunal de Cuentas": "BOE-A-1982-11584",
    "Ley 7/1988 Funcionamiento TC": "BOE-A-1988-8678",
    "RD 1971/1999 Procedimiento Incapacidad": "BOE-A-2000-1546",
    "RD 504/2022 Modifica Afiliación": "BOE-A-2022-10677",
    "RD 1430/2009 Incapacidad Temporal": "BOE-A-2009-15442",
    "RD 1369/2006 Desempleo e Incapacidad": "BOE-A-2006-21239",
    "RD 1300/1995 Incapacidades Laborales": "BOE-A-1995-19848",
    "RD 1415/2001 Catalogación Defensa": "BOE-A-2002-58",
    "RD 295/2009 Maternidad Paternidad": "BOE-A-2009-4724",
    "Ley 9/2009 Ampliación Paternidad": "BOE-A-2009-16029",
    "RDL 11/2024 Mejora Pensiones": "BOE-A-2024-26917",
    "RDL 20/2020 Ingreso Mínimo Vital": "BOE-A-2020-5493",
    "RD 357/1991 Pensiones No Contributivas": "BOE-A-1991-7270",
    "RD 1009/2023 Estructura Ministerios": "BOE-A-2023-24842"
}

def save_json(data, filename):
    """Saves data dictionary to JSON file."""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved {filepath}")

def main():
    logger.info(f"Starting download of {len(CORRECTED_LAWS)} corrected laws...")
    
    with BOEApiClient() as client:
        success_count = 0
        failed_count = 0
        
        for name, boe_id in CORRECTED_LAWS.items():
            try:
                logger.info(f"Downloading {name} (ID: {boe_id})...")
                
                # Check if file already exists
                filename = f"{boe_id}.json"
                if os.path.exists(os.path.join(DATA_DIR, filename)):
                    logger.info(f"File {filename} already exists. Skipping.")
                    success_count += 1
                    continue

                # Download consolidated document (returns dict parsed from XML)
                doc = client.get_documento_consolidado(boe_id)
                
                # Verify it has text content
                # Structure is { "data": { "texto": ... } } or { "documento_consolidado": ... } depending on parser
                # BOEApiClient._parse_xml_response typically returns root children.
                # Use recursive get or check for 'data' key which seems to be the root for these API calls.
                
                texto_node = None
                if 'data' in doc and 'texto' in doc['data']:
                    texto_node = doc['data']['texto']
                elif 'texto' in doc:
                    texto_node = doc['texto']
                
                if texto_node:
                    save_json(doc, filename)
                    success_count += 1
                    logger.info(f"Successfully downloaded {name}")
                else:
                    logger.warning(f"Downloaded {name} but it has no 'texto' content.")
                    failed_count += 1
                
                # Politeness delay
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error downloading {name} ({boe_id}): {str(e)}")
                failed_count += 1
        
        logger.info(f"Download complete. Success: {success_count}, Failed: {failed_count}")

if __name__ == "__main__":
    main()
