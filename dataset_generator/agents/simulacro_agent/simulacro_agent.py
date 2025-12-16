#!/usr/bin/env python3
"""
Agente Generador de Simulacros - OpositaIA
==========================================
Genera simulacros de 112 preguntas y tests de 80 preguntas
usando el RAG de Qdrant via MCP.

Uso:
    python simulacro_agent.py --simulacro    # Genera simulacro 112 preguntas
    python simulacro_agent.py --test         # Genera test 80 preguntas
    python simulacro_agent.py --chat         # Modo chat interactivo
    python simulacro_agent.py --query "..."  # Consulta única al RAG
"""

import os
import sys
import json
import random
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# Añadir path para imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp_client import get_mcp_client, MCPClient

class SimulacroAgent:
    """Agente para generar simulacros y tests de oposiciones"""
    
    def __init__(self):
        self.mcp = get_mcp_client()
        self.base_path = Path(__file__).parent.parent.parent
        self.output_path = self.base_path / "dataset_output"
        self.dataset_path = self.base_path / "DATASET_FINAL_300_SS_AGE.jsonl"
        self.preguntas_pool: List[Dict] = []
        self._load_dataset()
    
    def _load_dataset(self):
        """Cargar el dataset de preguntas existente"""
        if self.dataset_path.exists():
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            self.preguntas_pool.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
            print(f"✓ Cargadas {len(self.preguntas_pool)} preguntas del dataset")
        else:
            print(f"⚠ Dataset no encontrado: {self.dataset_path}")
            # Intentar cargar datasets alternativos
            alt_datasets = [
                self.base_path / "dataset_output" / "qa_baja_cobertura_500_PREMIUM_FINAL_20251208.jsonl",
                self.base_path / "dataset_output" / "qa_completo_unificado_CORREGIDO_20251208.jsonl"
            ]
            for alt in alt_datasets:
                if alt.exists():
                    with open(alt, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                try:
                                    self.preguntas_pool.append(json.loads(line))
                                except:
                                    continue
                    print(f"✓ Cargadas {len(self.preguntas_pool)} preguntas de {alt.name}")
                    break
    
    def consultar_rag(self, query: str) -> str:
        """Consultar el RAG y devolver respuesta formateada"""
        results = self.mcp.search_rag(query, limit=5)
        
        if results.get("error"):
            return f"Error: {results['error']}"
        
        if not results.get("results"):
            return "No se encontraron resultados relevantes."
        
        response = f"📚 Resultados para: '{query}'\n\n"
        for i, r in enumerate(results["results"], 1):
            score = r.get("score", 0)
            content = r.get("content", "")[:500]
            response += f"**{i}. (Score: {score:.2f})**\n{content}\n\n"
        
        return response
    
    def generar_simulacro(self, num_preguntas: int = 112) -> Dict[str, Any]:
        """
        Generar simulacro completo de 112 preguntas
        Formato oficial BOE-A-2024-11403
        """
        if len(self.preguntas_pool) < num_preguntas:
            print(f"⚠ Solo hay {len(self.preguntas_pool)} preguntas disponibles")
            num_preguntas = min(num_preguntas, len(self.preguntas_pool))
        
        # Seleccionar preguntas aleatorias
        preguntas_seleccionadas = random.sample(self.preguntas_pool, num_preguntas)
        
        # Dividir en Parte 1 (25) y Parte 2 (resto)
        parte_1_count = min(25, num_preguntas)
        parte_2_count = num_preguntas - parte_1_count
        
        preguntas_formateadas = []
        for i, p in enumerate(preguntas_seleccionadas, 1):
            parte = 1 if i <= parte_1_count else 2
            
            # Adaptar formato del dataset al formato simulacro
            pregunta_fmt = {
                "numero": i,
                "parte": parte,
                "pregunta": p.get("pregunta", p.get("question", "")),
                "opciones": self._formatear_opciones(p),
                "respuesta_correcta": p.get("respuesta_correcta", p.get("answer", "A")).lower(),
                "tema": p.get("tema", p.get("subtema", "General")),
                "dificultad": p.get("dificultad", "media"),
                "explicacion": p.get("explicacion", p.get("answer", ""))
            }
            preguntas_formateadas.append(pregunta_fmt)
        
        # Mezclar opciones de respuesta
        for p in preguntas_formateadas:
            p["opciones"], p["respuesta_correcta"] = self._mezclar_opciones(
                p["opciones"], p["respuesta_correcta"]
            )
        
        # Crear estructura del simulacro
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        simulacro = {
            "metadata": {
                "titulo": "SIMULACRO COMPLETO OFICIAL - Cuerpo Administrativo AGE",
                "subtitulo": f"{num_preguntas} Preguntas - Formato Oficial BOE-A-2024-11403",
                "fecha_generacion": datetime.now().isoformat(),
                "total_preguntas": num_preguntas,
                "duracion_estimada_minutos": 90,
                "instrucciones": "Responda todas las preguntas. Cada respuesta incorrecta penaliza -0.25 puntos.",
                "formato_oficial": "BOE-A-2024-11403",
                "generado_por": "SimulacroAgent v1.0"
            },
            "parte_1": {
                "nombre": "Test de Conocimientos Generales",
                "preguntas": parte_1_count,
                "puntos_max": 50,
                "minimo_aprobar": 25
            },
            "parte_2": {
                "nombre": "Supuestos Prácticos",
                "preguntas": parte_2_count,
                "puntos_max": 50,
                "minimo_aprobar": 25
            },
            "preguntas": preguntas_formateadas,
            "estadisticas": self._calcular_estadisticas(preguntas_formateadas)
        }
        
        # Guardar
        output_file = self.output_path / f"SIMULACRO_GENERADO_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(simulacro, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Simulacro guardado en: {output_file}")
        return simulacro
    
    def generar_test(self, num_preguntas: int = 80) -> Dict[str, Any]:
        """Generar test rápido de 80 preguntas"""
        if len(self.preguntas_pool) < num_preguntas:
            num_preguntas = len(self.preguntas_pool)
        
        preguntas_seleccionadas = random.sample(self.preguntas_pool, num_preguntas)
        
        preguntas_formateadas = []
        for i, p in enumerate(preguntas_seleccionadas, 1):
            pregunta_fmt = {
                "numero": i,
                "pregunta": p.get("pregunta", p.get("question", "")),
                "opciones": self._formatear_opciones(p),
                "respuesta_correcta": p.get("respuesta_correcta", "A").lower(),
                "tema": p.get("tema", "General"),
                "dificultad": p.get("dificultad", "media")
            }
            # Mezclar opciones
            pregunta_fmt["opciones"], pregunta_fmt["respuesta_correcta"] = self._mezclar_opciones(
                pregunta_fmt["opciones"], pregunta_fmt["respuesta_correcta"]
            )
            preguntas_formateadas.append(pregunta_fmt)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test = {
            "metadata": {
                "titulo": "TEST RÁPIDO - Seguridad Social y AGE",
                "fecha_generacion": datetime.now().isoformat(),
                "total_preguntas": num_preguntas,
                "duracion_estimada_minutos": 60,
                "generado_por": "SimulacroAgent v1.0"
            },
            "preguntas": preguntas_formateadas,
            "estadisticas": self._calcular_estadisticas(preguntas_formateadas)
        }
        
        output_file = self.output_path / f"TEST_GENERADO_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Test guardado en: {output_file}")
        return test
    
    def _formatear_opciones(self, pregunta: Dict) -> Dict[str, str]:
        """Formatear opciones de respuesta"""
        if "opciones" in pregunta and isinstance(pregunta["opciones"], list):
            opciones = {}
            for i, opt in enumerate(pregunta["opciones"]):
                letra = chr(97 + i)  # a, b, c, d
                # Limpiar prefijo si existe (A), B), etc.)
                texto = opt
                if len(opt) > 2 and opt[1] == ')':
                    texto = opt[2:].strip()
                elif len(opt) > 3 and opt[2] == ')':
                    texto = opt[3:].strip()
                opciones[letra] = texto
            return opciones
        elif "opciones" in pregunta and isinstance(pregunta["opciones"], dict):
            return pregunta["opciones"]
        else:
            # Crear opciones dummy si no existen
            return {
                "a": "Opción A",
                "b": "Opción B", 
                "c": "Opción C",
                "d": "Opción D"
            }
    
    def _mezclar_opciones(self, opciones: Dict[str, str], respuesta_correcta: str) -> tuple:
        """Mezclar opciones manteniendo track de la respuesta correcta"""
        items = list(opciones.items())
        random.shuffle(items)
        
        nuevas_opciones = {}
        nueva_respuesta = respuesta_correcta
        
        for i, (letra_original, texto) in enumerate(items):
            nueva_letra = chr(97 + i)  # a, b, c, d
            nuevas_opciones[nueva_letra] = texto
            if letra_original == respuesta_correcta.lower():
                nueva_respuesta = nueva_letra
        
        return nuevas_opciones, nueva_respuesta
    
    def _calcular_estadisticas(self, preguntas: List[Dict]) -> Dict[str, Any]:
        """Calcular estadísticas del simulacro/test"""
        dist = {"a": 0, "b": 0, "c": 0, "d": 0}
        temas = {}
        dificultades = {"facil": 0, "media": 0, "alta": 0}
        
        for p in preguntas:
            resp = p.get("respuesta_correcta", "a").lower()
            if resp in dist:
                dist[resp] += 1
            
            tema = p.get("tema", "General")
            temas[tema] = temas.get(tema, 0) + 1
            
            dif = p.get("dificultad", "media").lower()
            if dif in dificultades:
                dificultades[dif] += 1
        
        total = len(preguntas)
        return {
            "distribucion_respuestas": dist,
            "porcentajes_respuestas": {k: round(v/total*100, 1) for k, v in dist.items()} if total > 0 else {},
            "temas": temas,
            "dificultades": dificultades
        }
    
    def modo_chat(self):
        """Modo chat interactivo"""
        print("\n" + "="*60)
        print("🎓 AGENTE OPOSITAIA - Modo Chat")
        print("="*60)
        print("Comandos especiales:")
        print("  /simulacro - Generar simulacro de 112 preguntas")
        print("  /test      - Generar test de 80 preguntas")
        print("  /colecciones - Ver colecciones Qdrant")
        print("  /salir     - Salir del chat")
        print("="*60 + "\n")
        
        while True:
            try:
                query = input("📝 Tu pregunta: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ["/salir", "/exit", "/quit"]:
                    print("👋 ¡Hasta luego!")
                    break
                
                if query.lower() == "/simulacro":
                    print("\n⏳ Generando simulacro de 112 preguntas...")
                    self.generar_simulacro(112)
                    continue
                
                if query.lower() == "/test":
                    print("\n⏳ Generando test de 80 preguntas...")
                    self.generar_test(80)
                    continue
                
                if query.lower() == "/colecciones":
                    cols = self.mcp.list_collections()
                    print(json.dumps(cols, indent=2, ensure_ascii=False))
                    continue
                
                # Consulta normal al RAG
                print("\n⏳ Buscando en el RAG...")
                respuesta = self.consultar_rag(query)
                print(f"\n{respuesta}")
                
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Agente Generador de Simulacros OpositaIA")
    parser.add_argument("--simulacro", action="store_true", help="Generar simulacro de 112 preguntas")
    parser.add_argument("--test", action="store_true", help="Generar test de 80 preguntas")
    parser.add_argument("--chat", action="store_true", help="Modo chat interactivo")
    parser.add_argument("--query", type=str, help="Consulta única al RAG")
    parser.add_argument("--num", type=int, default=None, help="Número de preguntas (override)")
    
    args = parser.parse_args()
    
    agent = SimulacroAgent()
    
    if args.simulacro:
        num = args.num or 112
        print(f"\n⏳ Generando simulacro de {num} preguntas...")
        simulacro = agent.generar_simulacro(num)
        print(f"\n✅ Simulacro generado con {simulacro['metadata']['total_preguntas']} preguntas")
        
    elif args.test:
        num = args.num or 80
        print(f"\n⏳ Generando test de {num} preguntas...")
        test = agent.generar_test(num)
        print(f"\n✅ Test generado con {test['metadata']['total_preguntas']} preguntas")
        
    elif args.query:
        print(f"\n⏳ Consultando: {args.query}")
        respuesta = agent.consultar_rag(args.query)
        print(f"\n{respuesta}")
        
    elif args.chat:
        agent.modo_chat()
        
    else:
        # Por defecto, mostrar ayuda
        parser.print_help()
        print("\n📊 Estado del dataset:")
        print(f"   Preguntas disponibles: {len(agent.preguntas_pool)}")
        cols = agent.mcp.list_collections()
        if cols.get("collections"):
            print("   Colecciones Qdrant:")
            for c in cols["collections"]:
                print(f"     - {c['name']}: {c['points_count']} puntos")


if __name__ == "__main__":
    main()
