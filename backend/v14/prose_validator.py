"""
Prose Validator V14.5 — verifica que el texto LLM no contradice el schema Python.
Mejorado para Sprint 6: Soporte multi-blueprint, validación de personajes y conflictos.
Si el schema dice 85,18% y el LLM escribió 70%, bloqueo automático.
"""
import re
from backend.v14.case_schema_builder import CaseSchema


def extraer_numeros_texto(text: str) -> list:
    """
    Extrae TODOS los números del texto: porcentajes, cuantías, años, plazos.
    Mejorado V14.5: Soporte multi-blueprint, validación de personajes y conflictos.
    """
    # Patrones específicos para evitar sobre-matches
    patrones = [
        r'\d{1,4}[años]{0,2}\d{1,2}[m]{0,2}',  # 38a3m, 2a6m
        r'\d{1,6}[.,]\d{1,4}%',           # 85.18%, 50%
        r'\d{1,6}[.,]\d{1,4}€',            # 1.825,29€
        r'\d{1,6}[.,]\d{1,4}€/mes',       # 628,80€/mes
        r'\d{1,6}[.,]\d{1,4}€/año',       # 8.803,20€/año
        r'\d{1,4} semanas?',                # 19 semanas
        r'\d{1,4} días?',                   # 15 días
        r'\d{1,4} años?',                   # 65 años
    ]
    
    matches = []
    for patron in patrones:
        for m in re.finditer(patron, text):
            raw = m.group()
            
            # Manejo específico según el tipo de número
            if '%' in raw:
                # Para porcentajes: eliminar solo el % y convertir
                clean = raw.replace('%', '').replace(',', '.')
                try:
                    val = float(clean)
                    matches.append((raw, val))
                except ValueError:
                    continue
            elif '€' in raw:
                # Para cantidades: eliminar € y convertir
                clean = raw.replace('€', '').replace(',', '.')
                try:
                    val = float(clean)
                    matches.append((raw, val))
                except ValueError:
                    continue
            elif 'años' in raw or 'año' in raw:
                # Para años con letra: extraer solo el número
                clean = raw.replace('años', '').replace('año', '')
                try:
                    val = float(clean)
                    matches.append((raw, val))
                except ValueError:
                    continue
            else:
                # Para números puros
                clean = raw.replace(',', '.')
                try:
                    val = float(clean)
                    matches.append((raw, val))
                except ValueError:
                    continue
    
    # Eliminar duplicados (mismo valor numérico)
    valores_unicos = {}
    for raw, val in matches:
        valores_unicos[val] = raw  # Mantiene el último raw encontrado
    
    return [(valores_unicos[val], val) for val in valores_unicos]

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


def validar_coherencia_texto(texto_llm: str, schema: CaseSchema) -> dict:
    """
    Sprint 2.5: Validador de coherencia interna del texto LLM
    """
    errores = []
    
    # Validar coherencia de género
    for personaje in schema.personajes:
        nombre = personaje.nombre
        genero_detectado = None
        
        # Detectar género por el nombre
        if nombre.lower().startswith("maría") or nombre.lower().startswith("ana") or nombre.lower().startswith("carmen"):
            genero_detectado = "femenino"
        elif nombre.lower().startswith("carlos") or nombre.lower().startswith("jorge") or nombre.lower().startswith("sergio"):
            genero_detectado = "masculino"
        
        # Buscar inconsistencias en el texto
        if genero_detectado == "femenino":
            # Buscar "padre" cerca de nombre femenino
            patron = re.compile(rf'{re.escape(nombre)}.*?padre', re.IGNORECASE)
            if patron.search(texto_llm):
                errores.append({
                    "error": f"Incoherencia de género: {nombre} es femenino pero se menciona 'padre'",
                    "personaje": nombre,
                    "severidad": "alta"
                })
        
        if genero_detectado == "masculino":
            # Buscar "madre" cerca de nombre masculino
            patron = re.compile(rf'{re.escape(nombre)}.*?madre', re.IGNORECASE)
            if patron.search(texto_llm):
                errores.append({
                    "error": f"Incoherencia de género: {nombre} es masculino pero se menciona 'madre'",
                    "personaje": nombre,
                    "severidad": "alta"
                })
    
    return {
        "valid": len(errores) == 0,
        "errores": errores,
        "coherencia_validada": True
    }

def validar_prose_vs_schema(texto_llm: str, schema: CaseSchema,
                             tolerancia: float = 0.01) -> dict:
    """
    Validación Mejorada V14.5: Soporte multi-blueprint y personajes.
    
    1. Verifica que TODOS los números del schema aparecen en el texto LLM
    2. Verifica que TODOS los personajes del schema aparecen en el texto LLM
    3. Verifica que TODOS los conflictos cruzados aparecen en el texto LLM
    4. Verifica coherencia interna del texto (género, relaciones)
    5. Bloquea si hay discrepancias > tolerancia
    """
    
    # 1. Validación de dominio
    domain_result = domain_check(texto_llm, dominio="SS")
    if not domain_result["domain_ok"]:
        return {
            "valid": False,
            "bloqueado": True,
            "errores": [{"error": domain_result["error"]}]
        }

    # 2. Validación numérica
    numeros_schema = []
    for q in schema.questions:
        if q.calculo_resultado:
            try:
                val = float(str(q.calculo_resultado).replace(',', '.').rstrip('%€'))
                numeros_schema.append((q.pregunta_id, val, q.articulo))
            except ValueError:
                pass

    numeros_texto = extraer_numeros_texto(texto_llm)
    errores_numericos = []
    for p_id, val_schema, art in numeros_schema:
        encontrado = any(abs(val_texto - val_schema) <= tolerancia
                         for _, val_texto in numeros_texto)
        if not encontrado:
            errores_numericos.append({
                "pregunta": p_id,
                "valor_schema": val_schema,
                "articulo": art,
                "error": f"Schema dice {val_schema} pero no aparece en el texto LLM",
            })

    # 3. Validación de personajes (match parcial: cualquier palabra del nombre ≥ 4 letras)
    errores_personajes = []
    for personaje in schema.personajes:
        partes = [p for p in personaje.nombre.split() if len(p) >= 4]
        aparece = any(parte in texto_llm for parte in partes)
        if not aparece:
            errores_personajes.append({
                "personaje": personaje.nombre,
                "error": f"Personaje {personaje.nombre} (ni ninguna de sus palabras) aparece en el texto LLM"
            })

    # 4. Validación de conflictos cruzados (slug normalizado + sin tildes + case-insensitive)
    import unicodedata

    def _normalizar(s: str) -> str:
        s = s.replace('_', ' ')
        return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()

    texto_norm = _normalizar(texto_llm)

    errores_conflictos = []
    if hasattr(schema, 'conflictos_cruzados'):
        for conflicto in schema.conflictos_cruzados:
            # Comprobar que todas las palabras del conflicto aparecen en el texto
            palabras = _normalizar(conflicto).split()
            if not all(p in texto_norm for p in palabras if len(p) >= 4):
                errores_conflictos.append({
                    "conflicto": conflicto,
                    "error": f"Conflicto '{conflicto}' (palabras: {palabras}) no detectado en el texto LLM"
                })

    # 5. Validación de coherencia interna (NUEVO Sprint 2.5)
    coherencia_result = validar_coherencia_texto(texto_llm, schema)
    errores_coherencia = coherencia_result.get("errores", [])

    # Combinar todos los errores
    todos_errores = errores_numericos + errores_personajes + errores_conflictos + errores_coherencia

    return {
        "valid": len(todos_errores) == 0,
        "errores": todos_errores,
        "bloqueado": len(todos_errores) > 0,
        "estadisticas": {
            "numeros_schema": len(numeros_schema),
            "numeros_texto": len(numeros_texto),
            "personajes_validados": len(schema.personajes) - len(errores_personajes),
            "conflictos_validados": len(schema.conflictos_cruzados) - len(errores_conflictos) if hasattr(schema, 'conflictos_cruzados') else 0,
            "coherencia_validada": coherencia_result.get("valid", False),
            "errores_coherencia": len(errores_coherencia)
        }
    }
