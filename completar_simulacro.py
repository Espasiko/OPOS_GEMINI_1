#!/usr/bin/env python3
"""
Completar el simulacro de 112 preguntas usando el dataset disponible
"""

import json
import random
from pathlib import Path
from datetime import datetime

def cargar_dataset():
    """Cargar todas las preguntas del dataset"""
    dataset_file = Path("dataset_output/qa_baja_cobertura_PREMIUM_20251208.jsonl")
    preguntas = []
    
    if not dataset_file.exists():
        print(f"❌ No se encuentra el archivo: {dataset_file}")
        return []
    
    with open(dataset_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    pregunta = json.loads(line)
                    preguntas.append(pregunta)
                except Exception as e:
                    print(f"Error procesando línea: {e}")
                    continue
    
    return preguntas

def normalizar_pregunta(pregunta):
    """Normalizar estructura de pregunta"""
    # Extraer datos
    question = pregunta.get("question") or pregunta.get("pregunta") or ""
    options = pregunta.get("options") or pregunta.get("opciones") or []
    correct = pregunta.get("correct_answer") or pregunta.get("respuesta_correcta") or ""
    theme = pregunta.get("theme") or pregunta.get("tema") or "General"
    difficulty = pregunta.get("difficulty") or pregunta.get("dificultad") or "media"
    
    # Normalizar opciones si vienen como lista
    if isinstance(options, list) and len(options) >= 4:
        opciones_dict = {
            "a": options[0].replace("A) ", "").replace("a) ", "").strip(),
            "b": options[1].replace("B) ", "").replace("b) ", "").strip(),
            "c": options[2].replace("C) ", "").replace("c) ", "").strip(),
            "d": options[3].replace("D) ", "").replace("d) ", "").strip()
        }
    elif isinstance(options, dict):
        opciones_dict = options
    else:
        # Fallback si no hay opciones válidas
        opciones_dict = {
            "a": "Opción A",
            "b": "Opción B", 
            "c": "Opción C",
            "d": "Opción D"
        }
    
    # Normalizar respuesta correcta
    if correct in ["A", "B", "C", "D"]:
        correct = correct.lower()
    
    return {
        "pregunta": question,
        "opciones": opciones_dict,
        "respuesta_correcta": correct,
        "tema": theme,
        "dificultad": difficulty
    }

def reorganizar_opciones(pregunta_norm):
    """Reorganizar opciones para respuesta aleatoria"""
    try:
        opciones = [
            pregunta_norm["opciones"]["a"],
            pregunta_norm["opciones"]["b"], 
            pregunta_norm["opciones"]["c"],
            pregunta_norm["opciones"]["d"]
        ]
        
        # Encontrar posición actual de respuesta correcta
        respuesta_correcta = pregunta_norm["respuesta_correcta"]
        if respuesta_correcta not in ["a", "b", "c", "d"]:
            respuesta_correcta = "a"  # Fallback
            
        pos_actual = {"a": 0, "b": 1, "c": 2, "d": 3}[respuesta_correcta]
        
        # Nueva posición aleatoria
        nueva_pos = random.randint(0, 3)
        
        # Intercambiar si es necesario
        if nueva_pos != pos_actual:
            opciones[pos_actual], opciones[nueva_pos] = opciones[nueva_pos], opciones[pos_actual]
        
        # Crear nueva estructura
        opciones_nuevas = {
            "a": opciones[0],
            "b": opciones[1],
            "c": opciones[2],
            "d": opciones[3]
        }
        
        respuesta_nueva = ["a", "b", "c", "d"][nueva_pos]
        
        return opciones_nuevas, respuesta_nueva
        
    except (KeyError, TypeError) as e:
        # Si hay error, devolver opciones originales
        print(f"Error reorganizando opciones: {e}")
        return pregunta_norm["opciones"], pregunta_norm["respuesta_correcta"]

def es_supuesto_practico(pregunta):
    """Determinar si es supuesto práctico"""
    id_pregunta = pregunta.get("id", "")
    question = pregunta.get("question", "")
    
    # Casos prácticos tienen ID que empieza con "case_"
    if id_pregunta.startswith("case_"):
        return True
    
    # O contienen escenarios/situaciones
    if any(palabra in question.lower() for palabra in ["maría", "juan", "pedro", "ana", "empresa", "trabajador", "funcionario"]):
        if len(question) > 200:  # Preguntas largas suelen ser casos
            return True
    
    return False

def completar_simulacro():
    """Completar simulacro de 112 preguntas"""
    print("🔄 Cargando dataset...")
    todas_preguntas = cargar_dataset()
    
    if not todas_preguntas:
        print("❌ No se pudieron cargar preguntas del dataset")
        return None
        
    print(f"✅ Cargadas {len(todas_preguntas)} preguntas")
    
    # Separar por tipo
    preguntas_generales = []
    supuestos_practicos = []
    
    for p in todas_preguntas:
        # Solo preguntas tipo QA (no flashcards, chat, etc.)
        if p.get("id", "").startswith("qa_") or p.get("id", "").startswith("case_"):
            if es_supuesto_practico(p):
                supuestos_practicos.append(p)
            else:
                preguntas_generales.append(p)
    
    print(f"📊 Preguntas generales: {len(preguntas_generales)}")
    print(f"📊 Supuestos prácticos: {len(supuestos_practicos)}")
    
    # Seleccionar preguntas (máximo disponible)
    num_generales = min(100, len(preguntas_generales))
    num_practicos = min(12, len(supuestos_practicos))
    
    # Si no hay suficientes prácticos, completar con generales
    if len(supuestos_practicos) < 12:
        num_practicos = len(supuestos_practicos)
        num_generales = min(112 - num_practicos, len(preguntas_generales))
    
    seleccionadas_generales = random.sample(preguntas_generales, num_generales) if num_generales > 0 else []
    seleccionadas_practicas = random.sample(supuestos_practicos, num_practicos) if num_practicos > 0 else []
    
    total_seleccionadas = len(seleccionadas_generales) + len(seleccionadas_practicas)
    print(f"🎯 Seleccionadas: {len(seleccionadas_generales)} generales + {len(seleccionadas_practicas)} prácticas = {total_seleccionadas}")
    
    # Crear simulacro
    simulacro = {
        "metadata": {
            "titulo": "SIMULACRO COMPLETO OFICIAL - Cuerpo Administrativo AGE",
            "subtitulo": f"{total_seleccionadas} Preguntas - Formato Oficial BOE-A-2024-11403",
            "fecha_generacion": datetime.now().isoformat(),
            "total_preguntas": total_seleccionadas,
            "duracion_estimada_minutos": 90,
            "instrucciones": "Responda todas las preguntas. Cada respuesta incorrecta penaliza -0.25 puntos. No consulte normativa durante el simulacro.",
            "formato_oficial": "BOE-A-2024-11403 - Resolución de 25 de mayo de 2024"
        },
        "parte_1": {
            "nombre": "Test de Conocimientos Generales",
            "preguntas": len(seleccionadas_generales),
            "puntos_max": 50,
            "minimo_aprobar": 25,
            "descripcion": "Preguntas sobre temario general: Constitución, Derecho Administrativo, Función Pública"
        },
        "parte_2": {
            "nombre": "Supuestos Prácticos", 
            "preguntas": len(seleccionadas_practicas),
            "puntos_max": 50,
            "minimo_aprobar": 25,
            "descripcion": "Casos prácticos sobre Seguridad Social y aplicación de normativa"
        },
        "instrucciones_calificacion": {
            "formula_parte_1": f"Puntos = (Aciertos × 50) / {len(seleccionadas_generales)} - (Errores × 50) / {len(seleccionadas_generales) * 4}",
            "formula_parte_2": f"Puntos = (Aciertos × 50) / {len(seleccionadas_practicas)} - (Errores × 50) / {len(seleccionadas_practicas) * 4}" if len(seleccionadas_practicas) > 0 else "No hay supuestos prácticos",
            "penalizacion": "Cada error resta 0.25 puntos",
            "minimo_total": "50 puntos para aprobar (25 en cada parte)"
        },
        "preguntas": []
    }
    
    # Procesar Parte 1 (Generales)
    print("🔄 Procesando Parte 1...")
    contador_respuestas = {"a": 0, "b": 0, "c": 0, "d": 0}
    
    for i, pregunta in enumerate(seleccionadas_generales, 1):
        pregunta_norm = normalizar_pregunta(pregunta)
        opciones_nuevas, respuesta_nueva = reorganizar_opciones(pregunta_norm)
        contador_respuestas[respuesta_nueva] += 1
        
        item = {
            "numero": i,
            "parte": 1,
            "pregunta": pregunta_norm["pregunta"],
            "opciones": opciones_nuevas,
            "respuesta_correcta": respuesta_nueva,
            "tema": pregunta_norm["tema"],
            "dificultad": pregunta_norm["dificultad"]
        }
        simulacro["preguntas"].append(item)
    
    # Procesar Parte 2 (Prácticos)
    if seleccionadas_practicas:
        print("🔄 Procesando Parte 2...")
        for i, pregunta in enumerate(seleccionadas_practicas, len(seleccionadas_generales) + 1):
            pregunta_norm = normalizar_pregunta(pregunta)
            opciones_nuevas, respuesta_nueva = reorganizar_opciones(pregunta_norm)
            contador_respuestas[respuesta_nueva] += 1
            
            item = {
                "numero": i,
                "parte": 2,
                "pregunta": pregunta_norm["pregunta"],
                "opciones": opciones_nuevas,
                "respuesta_correcta": respuesta_nueva,
                "tema": pregunta_norm["tema"],
                "dificultad": pregunta_norm["dificultad"]
            }
            simulacro["preguntas"].append(item)
    
    # Estadísticas
    total_preguntas = len(simulacro["preguntas"])
    if total_preguntas > 0:
        simulacro["estadisticas"] = {
            "distribucion_respuestas": {
                "opcion_a": contador_respuestas["a"],
                "opcion_b": contador_respuestas["b"],
                "opcion_c": contador_respuestas["c"],
                "opcion_d": contador_respuestas["d"]
            },
            "porcentajes_respuestas": {
                "opcion_a": round((contador_respuestas["a"] / total_preguntas) * 100, 1),
                "opcion_b": round((contador_respuestas["b"] / total_preguntas) * 100, 1),
                "opcion_c": round((contador_respuestas["c"] / total_preguntas) * 100, 1),
                "opcion_d": round((contador_respuestas["d"] / total_preguntas) * 100, 1)
            }
        }
    
    # Guardar archivo completo
    output_file = Path("dataset_output") / "SIMULACRO_COMPLETO_112_PREGUNTAS_OFICIAL_BOE.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(simulacro, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Simulacro completado y guardado: {output_file}")
        print(f"   📊 Total preguntas: {total_preguntas}")
        print(f"   📝 Parte 1: {len(seleccionadas_generales)}")
        print(f"   📝 Parte 2: {len(seleccionadas_practicas)}")
        
        if total_preguntas > 0:
            print(f"\n📊 Distribución de respuestas correctas:")
            for opcion, count in contador_respuestas.items():
                pct = (count / total_preguntas) * 100
                print(f"   {opcion.upper()}: {count} ({pct:.1f}%)")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error guardando archivo: {e}")
        return None

if __name__ == "__main__":
    completar_simulacro()