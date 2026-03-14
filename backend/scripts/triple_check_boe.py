#!/usr/bin/env python3
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))
from boe_api_client import BOEApiClient

def verificar_boes():
    boes_candidatos = {
        "Pensiones (DT 34)": "BOE-A-2023-6967",
        "Jurisdicción Social": "BOE-A-2011-15936",
        "Estructura AGE": "BOE-A-2020-1246",
        "Ingreso AGE": "BOE-A-1995-8729",
        "Situaciones AGE": "BOE-A-1995-8730",
        "ENI": "BOE-A-2010-1331"
    }

    client = BOEApiClient(timeout=15)

    for nombre, boe_id in boes_candidatos.items():
        print(f"\n======== VERIFICANDO {nombre} ({boe_id}) ========")
        try:
            meta = client.get_metadatos(boe_id, formato="json")
        except Exception as e:
            print(f"Error fetching consolidado {boe_id}: {e}")
            meta = {}

        if not isinstance(meta, dict):
            print(f"Resultado no es dict para {boe_id}: tipo {type(meta)}")
            meta = {}
            
        data_node = meta.get("data", {}) if meta else {}
        if isinstance(data_node, list):
            # The BOE API might return a list of items inside "data"
            if len(data_node) > 0:
                documento_node = data_node[0]
            else:
                documento_node = {}
        elif isinstance(data_node, dict):
            documento_node = data_node.get("documento", {})
        else:
            documento_node = {}

        titulo = documento_node.get("titulo", "N/A")
        metadatos_node = documento_node.get("metadatos", {}) if isinstance(documento_node, dict) else {}
        rango = metadatos_node.get("rango", "N/A") if isinstance(metadatos_node, dict) else "N/A"
        estado = metadatos_node.get("estatus", "N/A") if isinstance(metadatos_node, dict) else "N/A"
        
        print(f"RANGO: {rango}")
        print(f"ESTADO: {estado}")
        print(f"TÍTULO: {titulo}")
        
        rango_str = str(rango).lower()
        titulo_str = str(titulo).lower()
        
        basura_terms = ["resolución", "subvención", "nombramiento", "orden ministerial de", "concurso", "ayuntamiento"]
        ley_terms = ["ley", "real decreto", "constitucion", "acuerdo"]
        
        es_basura = any(t in rango_str for t in basura_terms) or any(t in titulo_str for t in basura_terms)
        es_ley = any(t in rango_str for t in ley_terms) or any(t in titulo_str for t in ley_terms)
        
        if es_basura:
            print("❌ PELIGRO: POSIBLE BASURA DETECTADA")
        elif es_ley:
            print("✅ VERIFICADO: ES NORMATIVA")
        else:
            print("⚠️ INDETERMINADO: REVISAR MANUALMENTE")

if __name__ == "__main__":
    verificar_boes()
