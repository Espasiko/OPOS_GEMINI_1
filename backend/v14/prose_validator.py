"""
Prose Validator V14 — verifica que el texto LLM no contradice el schema Python.
Si el schema dice 85,18% y el LLM escribió 70%, bloqueo automático.
"""
import re
from backend.v14.case_schema_builder import CaseSchema


def extraer_numeros_texto(text: str):
    patron = r'[\d]{1,6}[.,][\d]{1,4}(?:[.,][\d]{1,4})?(?:\s?[%€])?'
    matches = []
    for m in re.finditer(patron, text):
        raw = m.group().replace('.', '').replace(',', '.').rstrip('%€').strip()
        try:
            matches.append((m.group(), float(raw)))
        except ValueError:
            pass
    return matches

DOMINIOS = {
    "SS": {
        "keywords_obligatorias": ["TRLGSS", "Seguridad", "Social", "cotización", 
                                   "prestación", "jubilación", "incapacidad", "pensión"],
        "keywords_prohibidas": ["Ley de Propiedad Horizontal", "LPH", "derrama", 
                                 "comunidad de propietarios", "ascensor"]
    }
}

def domain_check(texto_llm: str, dominio: str = "SS") -> dict:
    config = DOMINIOS[dominio]
    
    # ¿Aparecen palabras del dominio correcto?
    keywords_presentes = [k for k in config["keywords_obligatorias"] 
                          if k.lower() in texto_llm.lower()]
    
    # ¿Aparecen palabras de otro dominio?
    keywords_incorrectas = [k for k in config["keywords_prohibidas"] 
                            if k.lower() in texto_llm.lower()]
    
    if keywords_incorrectas:
        return {
            "domain_ok": False,
            "score": 0.0,
            "error": f"Dominio incorrecto detectado: {keywords_incorrectas}. "
                     f"El caso habla de algo ajeno a SS."
        }
    
    if len(keywords_presentes) < 2:
        return {
            "domain_ok": False, 
            "score": 0.3,
            "error": f"Pocas referencias al dominio SS: {keywords_presentes}"
        }
    
    return {"domain_ok": True, "score": 1.0}


def validar_prose_vs_schema(texto_llm: str, schema: CaseSchema,
                             tolerancia: float = 0.01) -> dict:
    
    domain_result = domain_check(texto_llm, dominio="SS")
    if not domain_result["domain_ok"]:
        return {
            "valid": False,
            "bloqueado": True,
            "errores": [{"error": domain_result["error"]}]
        }

    numeros_schema = []
    for q in schema.questions:
        if q.calculo_resultado:
            try:
                val = float(str(q.calculo_resultado).replace(',', '.').rstrip('%€'))
                numeros_schema.append((q.pregunta_id, val, q.articulo))
            except ValueError:
                pass

    numeros_texto = extraer_numeros_texto(texto_llm)
    errores = []
    for p_id, val_schema, art in numeros_schema:
        encontrado = any(abs(val_texto - val_schema) <= tolerancia
                         for _, val_texto in numeros_texto)
        if not encontrado:
            errores.append({
                "pregunta": p_id,
                "valor_schema": val_schema,
                "articulo": art,
                "error": f"Schema dice {val_schema} pero no aparece en el texto LLM",
            })

    return {
        "valid": len(errores) == 0,
        "errores": errores,
        "bloqueado": len(errores) > 0,
    }
