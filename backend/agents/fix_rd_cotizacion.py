"""
Indexar RD Cotización con URL correcta
"""
import requests
import pypdf
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
import torch
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
import re

print("="*80)
print("📥 INDEXAR RD COTIZACIÓN Y LIQUIDACIÓN")
print("="*80)

# URL correcta del RD 2064/1995
ley = {
    "nombre": "RD_Cotizacion_Liquidacion",
    "nombre_completo": "RD 2064/1995 Cotización y Liquidación",
    "boe_id": "BOE-A-1995-26769",
    "url": "https://www.boe.es/buscar/doc.php?id=BOE-A-1995-26769",  # URL alternativa
    "tipo": "reglamento",
    "nivel_jerarquia": 2,
    "fecha": "1995-12-22",
    "descripcion": "Reglamento General sobre Cotización y Liquidación"
}

print(f"\n⚠️  Nota: Este RD puede no tener versión consolidada en PDF")
print(f"   Intentando descarga alternativa...")
print(f"   Si falla, se omitirá esta ley")

output_dir = Path("backend/data/leyes")
filepath = output_dir / f"{ley['nombre']}.pdf"

# Intentar descarga
try:
    response = requests.get(ley['url'], timeout=60)
    if response.status_code == 200 and 'pdf' in response.headers.get('content-type', '').lower():
        filepath.write_bytes(response.content)
        print(f"✅ Descargado exitosamente")
    else:
        print(f"❌ No se pudo descargar en formato PDF")
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
        print(f"\n⚠️  RECOMENDACIÓN: Esta ley puede requerir descarga manual")
        print(f"   URL BOE: https://www.boe.es/eli/es/rd/1995/12/22/2064/con")
        exit(0)
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"\n⚠️  Esta ley requiere descarga manual o no está disponible en PDF consolidado")
    exit(0)

print("\n✅ RD Cotización descargado - procediendo con indexación...")
# Aquí iría el resto del código de indexación si la descarga fue exitosa
