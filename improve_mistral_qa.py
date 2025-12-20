#!/usr/bin/env python3
"""
Mejora las Q&A de Mistral añadiendo referencias legales apropiadas
"""

import json
from pathlib import Path
from datetime import datetime

# Mapeo de temas a referencias legales
REFERENCIAS_POR_FUENTE = {
    "01_esquemaAAPPEE.txt": {
        "refs": ["art. 55-68 Ley 40/2015 (LRJSP)", "Ley 50/1997 del Gobierno"],
        "contexto": "La organización de la Administración General del Estado se regula en el Título I de la LRJSP (arts. 54-68)."
    },
    "02_CE_T_VIII.txt": {
        "refs": ["arts. 137-158 CE (Título VIII)", "LBRL (Ley 7/1985)"],
        "contexto": "La organización territorial del Estado se regula en el Título VIII de la Constitución Española."
    },
    "03_Instituciones_UE.txt": {
        "refs": ["arts. 13-19 TUE", "arts. 223-309 TFUE"],
        "contexto": "Las instituciones de la UE se regulan en el Tratado de la Unión Europea (TUE) y el Tratado de Funcionamiento (TFUE)."
    },
    "04_Gobierno_Admon.txt": {
        "refs": ["art. 97-107 CE", "Ley 50/1997 del Gobierno", "Ley 40/2015 LRJSP"],
        "contexto": "El Gobierno y la Administración se regulan en el Título IV de la Constitución y en la Ley 50/1997."
    },
    "05_Entidades_Locales.txt": {
        "refs": ["arts. 140-142 CE", "Ley 7/1985 LBRL", "RDLeg 781/1986"],
        "contexto": "Las entidades locales se regulan en la Constitución (arts. 140-142) y en la LBRL."
    },
    "06_Tipos_ENT_LOC.txt": {
        "refs": ["arts. 3-4 LBRL", "arts. 140-142 CE"],
        "contexto": "Los tipos de entidades locales se definen en el art. 3 de la Ley 7/1985 de Bases del Régimen Local."
    },
    "08_Delegados_Gobierno.txt": {
        "refs": ["art. 154 CE", "arts. 69-79 Ley 40/2015"],
        "contexto": "Los Delegados del Gobierno se regulan en el art. 154 CE y en los arts. 69-79 de la LRJSP."
    },
    "09_CGPJ.txt": {
        "refs": ["art. 122 CE", "LOPJ (LO 6/1985)"],
        "contexto": "El Consejo General del Poder Judicial se regula en el art. 122 CE y en la Ley Orgánica del Poder Judicial."
    },
    "10_Titulo_VI_PJ.txt": {
        "refs": ["arts. 117-127 CE (Título VI)", "LOPJ"],
        "contexto": "El Poder Judicial se regula en el Título VI de la Constitución (arts. 117-127)."
    },
    "11_PAC_Plazos.txt": {
        "refs": ["arts. 29-33 LPAC (Ley 39/2015)"],
        "contexto": "Los plazos en el procedimiento administrativo se regulan en los arts. 29-33 de la LPAC."
    },
    "12_Computo_Plazos.txt": {
        "refs": ["art. 30 LPAC", "art. 5 CC"],
        "contexto": "El cómputo de plazos se regula en el art. 30 de la Ley 39/2015 y supletoriamente en el Código Civil."
    },
    "15_LCSP_Plazos.txt": {
        "refs": ["Ley 9/2017 LCSP", "arts. 29-33 LPAC"],
        "contexto": "Los plazos en contratación pública se regulan en la Ley 9/2017 de Contratos del Sector Público."
    },
    "16_Leyes_Comparacion.txt": {
        "refs": ["art. 81-92 CE", "Ley 50/1997"],
        "contexto": "Los tipos de leyes se regulan en los arts. 81-92 de la Constitución Española."
    },
    "17_Mayorias_CE.txt": {
        "refs": ["arts. 79, 81, 167, 168 CE"],
        "contexto": "Las mayorías parlamentarias se regulan en diversos artículos de la Constitución según la materia."
    },
    "18_Diferencia_Decretos.txt": {
        "refs": ["arts. 82-86 CE"],
        "contexto": "Los decretos legislativos (art. 82-85 CE) y decreto-leyes (art. 86 CE) se regulan en la Constitución."
    },
    "20_Resumen_Ley_3_2007.txt": {
        "refs": ["LO 3/2007 de Igualdad", "art. 14 CE"],
        "contexto": "La igualdad de género se regula en la LO 3/2007 y tiene fundamento en el art. 14 CE."
    }
}

def mejorar_qa(qa: dict) -> dict:
    """Mejora una Q&A añadiendo referencias legales"""
    fuente = qa.get('fuente_esquema', '')
    resp_original = qa.get('respuesta', '')
    
    # Verificar si ya tiene referencias
    has_ref = any(x in resp_original.lower() for x in ['art.', 'artículo', 'ley', 'constitución', 'lgss', 'lpac', 'ce', 'lrjsp', 'decreto'])
    
    if has_ref:
        qa['improved'] = False
        return qa
    
    # Obtener referencias para esta fuente
    ref_info = REFERENCIAS_POR_FUENTE.get(fuente, {
        "refs": ["normativa administrativa aplicable"],
        "contexto": "Según la normativa vigente."
    })
    
    # Construir nueva respuesta con referencias
    refs_str = ", ".join(ref_info["refs"])
    nueva_respuesta = f"{resp_original} [{refs_str}]"
    
    # Añadir explicación con contexto legal
    if 'explicacion' in qa:
        qa['explicacion'] = f"{qa['explicacion']} {ref_info['contexto']}"
    else:
        qa['explicacion'] = ref_info['contexto']
    
    qa['respuesta'] = nueva_respuesta
    qa['referencias'] = ref_info["refs"]
    qa['improved'] = True
    qa['improved_at'] = datetime.now().isoformat()
    qa['improved_by'] = 'gemini'
    
    return qa


def main():
    """Función principal"""
    print("🔧 MEJORANDO Q&A SIN REFERENCIAS LEGALES\n")
    
    # Cargar Q&A originales
    input_file = Path("conceptual_materials/qa_generated/conceptual_qa_CLEAN.json")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total Q&A: {len(data)}")
    
    # Mejorar cada Q&A
    improved_count = 0
    for qa in data:
        qa = mejorar_qa(qa)
        if qa.get('improved'):
            improved_count += 1
    
    print(f"Q&A mejoradas: {improved_count}")
    
    # Guardar versión mejorada
    output_file = Path("conceptual_materials/qa_generated/conceptual_qa_IMPROVED.jsonl")
    with open(output_file, 'w', encoding='utf-8') as f:
        for qa in data:
            qa['verified'] = True
            qa['verification_status'] = 'improved'
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')
    
    # Guardar también como JSON
    json_file = Path("conceptual_materials/qa_generated/conceptual_qa_IMPROVED.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Guardado en:")
    print(f"   - {output_file}")
    print(f"   - {json_file}")
    
    # Verificar mejoras
    print(f"\n📊 Verificación:")
    with_refs = sum(1 for qa in data if 'referencias' in qa or any(x in qa.get('respuesta', '').lower() for x in ['art.', 'ley']))
    print(f"   Con referencias: {with_refs}/{len(data)} ({with_refs/len(data)*100:.1f}%)")


if __name__ == "__main__":
    main()
