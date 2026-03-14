import os
from qdrant_client import QdrantClient, models

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"

# Inventario extraído de BOE_Verificacion_Completa.md
VERIFIED_INVENTORY = {
    # Confirmados (✅)
    "BOE-A-1978-31229": "CE 1978",
    "BOE-A-2015-11724": "TRLGSS",
    "BOE-A-2015-10565": "LPAC",
    "BOE-A-2015-10566": "LRJSP",
    "BOE-A-2015-11719": "TREBEP",
    "BOE-A-2015-11430": "ET",
    "BOE-A-2018-16673": "LOPDGDD",
    "BOE-A-2007-6115": "LO Igualdad",
    "BOE-A-2004-21760": "LO Violencia de Género",
    "BOE-A-1985-16660": "LO Libertad Sindical",
    "BOE-A-2013-12887": "LTAIBG",
    "BOE-A-1995-24292": "Ley PRL",
    "BOE-A-2015-8168": "Ley Inspección Trabajo",
    "BOE-A-2017-12902": "LCSP",
    "BOE-A-2003-21614": "Ley Presupuestaria General",
    "BOE-A-1987-14115": "Ley Representación AAPP",
    "BOE-A-2000-12140": "MUFACE RDL",
    "BOE-A-2003-7527": "Reglamento MUFACE",
    "BOE-A-2015-7731": "Reutilización modificación",
    "BOE-A-2007-19814": "Reutilización base",
    "BOE-A-2021-5032": "Admin Electrónica",
    "BOE-A-2022-7191": "ENS",
    "BOE-A-2021-21007": "IMV Ley 19/2021",
    "BOE-A-2014-7684": "IT",
    "BOE-A-1995-19848": "Incapacidades laborales",
    "BOE-A-2011-13242": "Modernización SS",
    "BOE-A-2009-4724": "Nacimiento/Cuidado",
    "BOE-A-1991-7270": "PNC",
    "BOE-A-1996-4447": "Afiliación SS",
    "BOE-A-1996-1579": "Cotización SS",
    "BOE-A-2004-11836": "Recaudación SS",
    # Pendientes (⚠️) que vamos a verificar si están
    "BOE-A-2010-1172": "ENI (RD 4/2010)",
    "BOE-A-1987-16764": "Clases Pasivas",
    "BOE-A-2020-2047": "Estructura AGE",
    "BOE-T-2010-11609": "STC 31/2010",
    "BOE-A-1995-10652": "Reglamento Ingreso AGE",
    "BOE-A-1995-10653": "Reglamento Situaciones Admin"
}

def verify():
    client = QdrantClient(url=QDRANT_URL, timeout=120)
    print(f"--- Verificando Inventario vs Qdrant ({COLLECTION_NAME}) ---")
    
    missing = []
    indexed = []
    
    for boe_id, name in VERIFIED_INVENTORY.items():
        count = client.count(
            collection_name=COLLECTION_NAME,
            count_filter=models.Filter(
                must=[models.FieldCondition(key="boe_id", match=models.MatchValue(value=boe_id))]
            )
        )
        if count.count > 0:
            indexed.append(f"✅ {boe_id} ({name}): {count.count} chunks")
        else:
            missing.append(f"❌ {boe_id} ({name})")
            
    print("\n[ YA INDEXADOS ]")
    for item in sorted(indexed): print(item)
    
    print("\n[ FALTANTES ]")
    if not missing:
        print("🎉 ¡Todo el inventario verificado está indexado!")
    else:
        for item in sorted(missing): print(item)
        
if __name__ == "__main__":
    verify()
