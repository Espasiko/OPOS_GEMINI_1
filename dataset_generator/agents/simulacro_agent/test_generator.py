#!/usr/bin/env python3
"""
Generador de Tests Personalizados - OpositaIA
=============================================
Genera tests personalizados mezclando preguntas del dataset existente.

Características:
- Selección por tema
- Selección por dificultad
- Mezcla aleatoria de opciones
- Exportación a múltiples formatos
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import defaultdict


class TestGenerator:
    """Generador de tests personalizados"""
    
    def __init__(self, dataset_path: Optional[Path] = None):
        self.base_path = Path(__file__).parent.parent.parent
        self.dataset_path = dataset_path or self.base_path / "DATASET_FINAL_300_SS_AGE.jsonl"
        self.output_path = self.base_path / "dataset_output"
        self.preguntas: List[Dict] = []
        self.preguntas_por_tema: Dict[str, List[Dict]] = defaultdict(list)
        self.preguntas_por_dificultad: Dict[str, List[Dict]] = defaultdict(list)
        self._load_dataset()
    
    def _load_dataset(self):
        """Cargar y clasificar preguntas del dataset"""
        datasets_to_try = [
            self.dataset_path,
            self.base_path / "dataset_output" / "qa_baja_cobertura_500_PREMIUM_FINAL_20251208.jsonl",
            self.base_path / "dataset_output" / "qa_completo_unificado_CORREGIDO_20251208.jsonl"
        ]
        
        for ds_path in datasets_to_try:
            if ds_path.exists():
                with open(ds_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                p = json.loads(line)
                                self.preguntas.append(p)
                                
                                # Clasificar por tema
                                tema = p.get("tema", p.get("subtema", "General"))
                                self.preguntas_por_tema[tema].append(p)
                                
                                # Clasificar por dificultad
                                dif = p.get("dificultad", "media").lower()
                                self.preguntas_por_dificultad[dif].append(p)
                                
                            except json.JSONDecodeError:
                                continue
                
                if self.preguntas:
                    print(f"✓ Cargadas {len(self.preguntas)} preguntas de {ds_path.name}")
                    break
    
    def get_temas_disponibles(self) -> List[str]:
        """Obtener lista de temas disponibles"""
        return sorted(self.preguntas_por_tema.keys())
    
    def get_estadisticas(self) -> Dict[str, Any]:
        """Obtener estadísticas del dataset"""
        return {
            "total_preguntas": len(self.preguntas),
            "temas": {k: len(v) for k, v in self.preguntas_por_tema.items()},
            "dificultades": {k: len(v) for k, v in self.preguntas_por_dificultad.items()}
        }
    
    def generar_test(
        self,
        num_preguntas: int = 80,
        temas: Optional[List[str]] = None,
        dificultad: Optional[str] = None,
        mezclar_opciones: bool = True
    ) -> Dict[str, Any]:
        """
        Generar test personalizado
        
        Args:
            num_preguntas: Número de preguntas a incluir
            temas: Lista de temas a incluir (None = todos)
            dificultad: Filtrar por dificultad (facil/media/alta)
            mezclar_opciones: Si mezclar el orden de las opciones
        """
        # Filtrar preguntas
        pool = self.preguntas.copy()
        
        if temas:
            pool = [p for p in pool if p.get("tema", "") in temas or p.get("subtema", "") in temas]
        
        if dificultad:
            pool = [p for p in pool if p.get("dificultad", "media").lower() == dificultad.lower()]
        
        if len(pool) < num_preguntas:
            print(f"⚠ Solo hay {len(pool)} preguntas disponibles con los filtros aplicados")
            num_preguntas = len(pool)
        
        if num_preguntas == 0:
            return {"error": "No hay preguntas disponibles con los filtros aplicados"}
        
        # Seleccionar aleatoriamente
        seleccionadas = random.sample(pool, num_preguntas)
        
        # Formatear preguntas
        preguntas_fmt = []
        for i, p in enumerate(seleccionadas, 1):
            pregunta = {
                "numero": i,
                "pregunta": p.get("pregunta", p.get("question", "")),
                "opciones": self._formatear_opciones(p),
                "respuesta_correcta": p.get("respuesta_correcta", "A").lower(),
                "tema": p.get("tema", "General"),
                "dificultad": p.get("dificultad", "media"),
                "explicacion": p.get("explicacion", "")
            }
            
            if mezclar_opciones:
                pregunta["opciones"], pregunta["respuesta_correcta"] = self._mezclar_opciones(
                    pregunta["opciones"], pregunta["respuesta_correcta"]
                )
            
            preguntas_fmt.append(pregunta)
        
        # Crear test
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test = {
            "metadata": {
                "titulo": "TEST PERSONALIZADO - OpositaIA",
                "fecha_generacion": datetime.now().isoformat(),
                "total_preguntas": num_preguntas,
                "filtros_aplicados": {
                    "temas": temas,
                    "dificultad": dificultad
                },
                "opciones_mezcladas": mezclar_opciones,
                "generado_por": "TestGenerator v1.0"
            },
            "preguntas": preguntas_fmt,
            "estadisticas": self._calcular_estadisticas(preguntas_fmt)
        }
        
        # Guardar
        filtro_str = ""
        if dificultad:
            filtro_str += f"_{dificultad}"
        if temas:
            filtro_str += f"_{len(temas)}temas"
        
        output_file = self.output_path / f"TEST_PERSONALIZADO{filtro_str}_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Test guardado en: {output_file}")
        return test
    
    def generar_test_por_tema(self, tema: str, num_preguntas: int = 20) -> Dict[str, Any]:
        """Generar test de un tema específico"""
        return self.generar_test(num_preguntas=num_preguntas, temas=[tema])
    
    def generar_test_mixto(
        self,
        num_facil: int = 20,
        num_media: int = 40,
        num_alta: int = 20
    ) -> Dict[str, Any]:
        """Generar test con distribución específica de dificultades"""
        preguntas_seleccionadas = []
        
        # Seleccionar por dificultad
        for dif, num in [("facil", num_facil), ("media", num_media), ("alta", num_alta)]:
            pool = self.preguntas_por_dificultad.get(dif, [])
            if len(pool) >= num:
                preguntas_seleccionadas.extend(random.sample(pool, num))
            else:
                preguntas_seleccionadas.extend(pool)
                print(f"⚠ Solo hay {len(pool)} preguntas de dificultad {dif}")
        
        # Mezclar orden
        random.shuffle(preguntas_seleccionadas)
        
        # Formatear
        preguntas_fmt = []
        for i, p in enumerate(preguntas_seleccionadas, 1):
            pregunta = {
                "numero": i,
                "pregunta": p.get("pregunta", p.get("question", "")),
                "opciones": self._formatear_opciones(p),
                "respuesta_correcta": p.get("respuesta_correcta", "A").lower(),
                "tema": p.get("tema", "General"),
                "dificultad": p.get("dificultad", "media"),
                "explicacion": p.get("explicacion", "")
            }
            pregunta["opciones"], pregunta["respuesta_correcta"] = self._mezclar_opciones(
                pregunta["opciones"], pregunta["respuesta_correcta"]
            )
            preguntas_fmt.append(pregunta)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test = {
            "metadata": {
                "titulo": "TEST MIXTO - Distribución por Dificultad",
                "fecha_generacion": datetime.now().isoformat(),
                "total_preguntas": len(preguntas_fmt),
                "distribucion_objetivo": {
                    "facil": num_facil,
                    "media": num_media,
                    "alta": num_alta
                },
                "generado_por": "TestGenerator v1.0"
            },
            "preguntas": preguntas_fmt,
            "estadisticas": self._calcular_estadisticas(preguntas_fmt)
        }
        
        output_file = self.output_path / f"TEST_MIXTO_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Test mixto guardado en: {output_file}")
        return test
    
    def _formatear_opciones(self, pregunta: Dict) -> Dict[str, str]:
        """Formatear opciones de respuesta"""
        if "opciones" in pregunta and isinstance(pregunta["opciones"], list):
            opciones = {}
            for i, opt in enumerate(pregunta["opciones"]):
                letra = chr(97 + i)
                texto = opt
                if len(opt) > 2 and opt[1] == ')':
                    texto = opt[2:].strip()
                elif len(opt) > 3 and opt[2] == ')':
                    texto = opt[3:].strip()
                opciones[letra] = texto
            return opciones
        elif "opciones" in pregunta and isinstance(pregunta["opciones"], dict):
            return pregunta["opciones"]
        return {"a": "Opción A", "b": "Opción B", "c": "Opción C", "d": "Opción D"}
    
    def _mezclar_opciones(self, opciones: Dict[str, str], respuesta: str) -> tuple:
        """Mezclar opciones manteniendo track de la respuesta"""
        items = list(opciones.items())
        random.shuffle(items)
        
        nuevas = {}
        nueva_resp = respuesta
        
        for i, (letra_orig, texto) in enumerate(items):
            nueva_letra = chr(97 + i)
            nuevas[nueva_letra] = texto
            if letra_orig == respuesta.lower():
                nueva_resp = nueva_letra
        
        return nuevas, nueva_resp
    
    def _calcular_estadisticas(self, preguntas: List[Dict]) -> Dict[str, Any]:
        """Calcular estadísticas del test"""
        dist = {"a": 0, "b": 0, "c": 0, "d": 0}
        temas = {}
        difs = {"facil": 0, "media": 0, "alta": 0}
        
        for p in preguntas:
            resp = p.get("respuesta_correcta", "a").lower()
            if resp in dist:
                dist[resp] += 1
            
            tema = p.get("tema", "General")
            temas[tema] = temas.get(tema, 0) + 1
            
            dif = p.get("dificultad", "media").lower()
            if dif in difs:
                difs[dif] += 1
        
        total = len(preguntas)
        return {
            "distribucion_respuestas": dist,
            "porcentajes": {k: round(v/total*100, 1) for k, v in dist.items()} if total else {},
            "temas": temas,
            "dificultades": difs
        }


def main():
    """Ejemplo de uso"""
    gen = TestGenerator()
    
    print("\n📊 Estadísticas del dataset:")
    stats = gen.get_estadisticas()
    print(f"   Total preguntas: {stats['total_preguntas']}")
    print(f"   Dificultades: {stats['dificultades']}")
    print(f"   Temas: {len(stats['temas'])}")
    
    print("\n📝 Temas disponibles:")
    for tema in gen.get_temas_disponibles()[:10]:
        print(f"   - {tema}")
    
    # Generar test de ejemplo
    print("\n⏳ Generando test de 80 preguntas...")
    test = gen.generar_test(80)
    print(f"✅ Test generado con {test['metadata']['total_preguntas']} preguntas")


if __name__ == "__main__":
    main()
