
import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_on_boe(articulo: str, ley: str):
    """
    Busca una referencia legal en la web del BOE para verificar su existencia.
    """
    query = f"site:boe.es {ley} artículo {articulo}"
    # Nota: Realizar una búsqueda directa en BOE o vía Google (simulado aquí con la búsqueda de BOE)
    # Una forma más directa es usar el buscador de BOE: https://www.boe.es/buscar/ayudas/boe_ayuda.php
    
    # Intento de URL directa si conocemos el ID (ej. LGSS 2015: BOE-A-2015-11724)
    # Por ahora, haremos una búsqueda simple de texto para validar.
    
    search_url = f"https://www.boe.es/buscar/boe.php?campo%5B0%5D=TIT&dato%5B0%5D={urllib.parse.quote(ley)}&campo%5B1%5D=TEXT&dato%5B1%5D=art%EDculo+{articulo}"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Si hay resultados, el BOE suele mostrar una lista de enlaces
            results = soup.find_all('div', class_='listadoResultados')
            if not results:
                # Comprobar si hay un aviso de "No se han encontrado resultados"
                if "No se han encontrado resultados" in response.text:
                    return {"valid": False, "message": f"No se encontró el artículo {articulo} en la norma '{ley}' en BOE."}
            
            return {"valid": True, "url": search_url, "message": "Referencia encontrada en el listado de resultados de BOE."}
        else:
            return {"valid": None, "message": f"Error de conexión con BOE: {response.status_code}"}
            
    except Exception as e:
        logger.error(f"Error verificando en BOE: {e}")
        return {"valid": None, "message": str(e)}

if __name__ == "__main__":
    # Test
    res = verify_on_boe("165", "Ley General de la Seguridad Social")
    print(f"Resultado: {res}")
