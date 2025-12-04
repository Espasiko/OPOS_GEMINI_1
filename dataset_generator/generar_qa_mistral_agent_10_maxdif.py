#!/usr/bin/env python3
"""
Generador de 10 Q&A de MÁXIMA DIFICULTAD usando el Agente Mistral con Herramientas
- Usa RAG para obtener contexto legal preciso
- Genera preguntas tipo "trampa" como las de exámenes reales
- Incluye cálculos complejos, excepciones y casos límite
"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient
import hashlib
from typing import List, Dict, Optional

# Configuración
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
QDRANT_URL = "http://localhost:6333"
COLLECTION_LEYES = "opositaia_leyes_seguridad_social"  # 7861 puntos - leyes
COLLECTION_EXAMENES = "materiales_academia"  # 364 puntos - exámenes

# Definición de herramientas para el agente
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "buscar_rag_qdrant",
            "description": "Busca contexto legal relevante en Qdrant con leyes de Seguridad Social",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Consulta sobre tema legal"},
                    "top_k": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generar_qa_maxima_dificultad",
            "description": "Genera una Q&A de máxima dificultad con trampas y excepciones",
            "parameters": {
                "type": "object",
                "properties": {
                    "contexto_legal": {"type": "string"},
                    "tema": {"type": "string"},
                    "tipo_trampa": {"type": "string", "enum": ["excepcion_regla", "calculo_complejo", "caso_limite", "normativa_reciente", "jurisprudencia"]}
                },
                "required": ["contexto_legal", "tema"]
            }
        }
    }
]

class MistralAgentQAGenerator:
    def __init__(self):
        self.api_key = MISTRAL_API_KEY
        self.qdrant = QdrantClient(url=QDRANT_URL)
        self.generated_qa = []
        
        print("🤖 Agente Mistral con Herramientas inicializado")
        print(f"   API Key: {self.api_key[:8]}...")
        print(f"   Qdrant: {QDRANT_URL}")
        print(f"   Colección Leyes: {COLLECTION_LEYES} (7861 docs)")
        print(f"   Colección Exámenes: {COLLECTION_EXAMENES} (364 docs)")
    
    def buscar_rag_qdrant(self, query: str, top_k: int = 5) -> str:
        """Ejecuta búsqueda RAG en Qdrant - busca en ambas colecciones"""
        try:
            results = []
            
            # 1. Buscar en colección de LEYES/TEMARIOS (7861 docs)
            points_leyes, _ = self.qdrant.scroll(
                collection_name=COLLECTION_LEYES,
                limit=100,
                with_payload=True,
                with_vectors=False
            )
            
            # 2. Buscar en colección de EXAMENES (364 docs)
            points_exam, _ = self.qdrant.scroll(
                collection_name=COLLECTION_EXAMENES,
                limit=100,
                with_payload=True,
                with_vectors=False
            )
            
            query_lower = query.lower()
            keywords = [w for w in query_lower.split() if len(w) > 3]
            
            # Procesar temarios/leyes
            for p in points_leyes:
                text = p.payload.get('text', '').lower()
                matches = sum(1 for kw in keywords if kw in text)
                if matches >= 1:
                    results.append({
                        'text': p.payload.get('text', '')[:500],
                        'fuente': p.payload.get('material_nombre', 'Temario'),
                        'tipo': 'temario',
                        'matches': matches
                    })
            
            # Procesar exámenes
            for p in points_exam:
                text = p.payload.get('text', '').lower()
                matches = sum(1 for kw in keywords if kw in text)
                if matches >= 1:
                    results.append({
                        'text': p.payload.get('text', '')[:500],
                        'fuente': p.payload.get('filename', 'Examen'),
                        'tipo': 'examen',
                        'matches': matches
                    })
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['matches'], reverse=True)
            
            if results:
                return json.dumps(results[:top_k], ensure_ascii=False)
            else:
                # Devolver contenido de exámenes por defecto
                return json.dumps([{
                    'text': p.payload.get('text', '')[:400],
                    'fuente': p.payload.get('filename', 'Examen')
                } for p in points_exam[:top_k]], ensure_ascii=False)
                
        except Exception as e:
            print(f"   ⚠️ Error RAG: {e}")
            return json.dumps({"error": str(e)})
    
    def call_mistral_with_tools(self, messages: List[Dict], tools: List[Dict] = None) -> Dict:
        """Llama a Mistral API con herramientas"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "mistral-large-latest",
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 4000
            }
            
            if tools:
                payload["tools"] = tools
                payload["tool_choice"] = "auto"
            
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error API: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def process_tool_calls(self, tool_calls: List[Dict]) -> List[Dict]:
        """Procesa las llamadas a herramientas"""
        results = []
        for call in tool_calls:
            func_name = call['function']['name']
            args = json.loads(call['function']['arguments'])
            
            print(f"   🔧 Ejecutando: {func_name}")
            
            if func_name == "buscar_rag_qdrant":
                result = self.buscar_rag_qdrant(args.get('query', ''), args.get('top_k', 5))
            else:
                result = json.dumps({"status": "ok"})
            
            results.append({
                "role": "tool",
                "tool_call_id": call['id'],
                "content": result
            })
        
        return results
    
    def generate_max_difficulty_qa(self, tema: str, tipo_trampa: str) -> Optional[Dict]:
        """Genera una Q&A de máxima dificultad"""
        
        # Prompt del sistema para el agente
        system_prompt = """Eres un EXPERTO en crear preguntas de oposiciones de Seguridad Social de MÁXIMA DIFICULTAD.

Tu objetivo es crear preguntas que:
1. Solo el 10-15% de opositores acertaría
2. Incluyan "trampas" sutiles basadas en excepciones legales
3. Requieran conocimiento profundo de la normativa
4. Combinen varios conceptos o artículos
5. Incluyan casos prácticos con cálculos complejos

TIPOS DE PREGUNTAS DIFÍCILES:
- Excepciones a reglas generales (ej: "EXCEPTO cuando...")
- Cálculos con múltiples variables y coeficientes
- Casos límite temporales (plazos, fechas, períodos transitorios)
- Normativa reciente que modifica reglas anteriores
- Jurisprudencia que matiza la ley

FORMATO DE RESPUESTA (JSON):
{
    "pregunta": "texto completo con caso práctico detallado",
    "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "respuesta_correcta": "A/B/C/D",
    "explicacion": "explicación detallada con referencias legales",
    "tema": "tema específico",
    "dificultad": "muy_alta",
    "tipo_trampa": "tipo de trampa usada",
    "articulos_referencia": ["art. X LGSS", "art. Y RD..."],
    "conceptos_clave": ["concepto1", "concepto2"],
    "errores_comunes": ["error típico 1", "error típico 2"],
    "porcentaje_acierto_estimado": 10-15
}"""

        # Mensaje del usuario
        user_message = f"""Genera UNA pregunta de MÁXIMA DIFICULTAD sobre: {tema}

Tipo de trampa a usar: {tipo_trampa}

INSTRUCCIONES:
1. Primero busca contexto legal relevante usando buscar_rag_qdrant
2. Crea una pregunta que solo expertos acertarían
3. Las opciones incorrectas deben ser plausibles (errores comunes)
4. La explicación debe ser exhaustiva con artículos específicos

Responde SOLO con el JSON de la Q&A."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Primera llamada - puede usar herramientas
        response = self.call_mistral_with_tools(messages, TOOLS)
        if not response:
            return None
        
        choice = response['choices'][0]
        
        # Si hay tool calls, procesarlas
        if choice.get('finish_reason') == 'tool_calls' or choice['message'].get('tool_calls'):
            tool_calls = choice['message']['tool_calls']
            tool_results = self.process_tool_calls(tool_calls)
            
            # Añadir resultados y continuar
            messages.append(choice['message'])
            messages.extend(tool_results)
            
            # Segunda llamada para obtener la Q&A
            response = self.call_mistral_with_tools(messages)
            if not response:
                return None
            choice = response['choices'][0]
        
        # Extraer JSON de la respuesta
        content = choice['message']['content']
        try:
            # Buscar el JSON principal (primer objeto completo)
            json_start = content.find('{')
            if json_start >= 0:
                # Contar llaves para encontrar el cierre correcto
                depth = 0
                json_end = json_start
                for i, char in enumerate(content[json_start:], json_start):
                    if char == '{':
                        depth += 1
                    elif char == '}':
                        depth -= 1
                        if depth == 0:
                            json_end = i + 1
                            break
                
                json_str = content[json_start:json_end]
                qa = json.loads(json_str)
                qa['generated_at'] = datetime.now().isoformat()
                qa['model'] = 'mistral-large-latest (agent)'
                qa['hash'] = hashlib.md5(qa['pregunta'].lower().encode()).hexdigest()[:12]
                return qa
        except Exception as e:
            print(f"   ❌ Error parseando JSON: {e}")
        
        return None
    
    def generate_dataset(self, num_questions: int = 10) -> List[Dict]:
        """Genera dataset de preguntas de máxima dificultad"""
        
        # Temas y tipos de trampa para máxima dificultad
        temas_dificiles = [
            ("Cálculo de base reguladora con lagunas de cotización y períodos asimilados", "calculo_complejo"),
            ("Jubilación anticipada: coeficientes reductores y excepciones por discapacidad", "excepcion_regla"),
            ("Incapacidad permanente: revisión por mejoría vs agravación y plazos", "caso_limite"),
            ("Compatibilidad pensión jubilación con trabajo por cuenta propia", "normativa_reciente"),
            ("Prestación por desempleo: suspensión vs extinción y reanudación", "excepcion_regla"),
            ("IMV: cómputo de rentas y patrimonio, exclusiones específicas", "calculo_complejo"),
            ("Cotización RETA: bases mínimas y máximas según tramos de rendimientos", "normativa_reciente"),
            ("Muerte y supervivencia: pensión de viudedad con parejas de hecho", "caso_limite"),
            ("Recargo de prestaciones por falta de medidas de seguridad", "jurisprudencia"),
            ("Integración de lagunas: diferencia entre contingencias comunes y profesionales", "excepcion_regla")
        ]
        
        print(f"\n{'='*60}")
        print(f"🎯 GENERACIÓN DE {num_questions} Q&A DE MÁXIMA DIFICULTAD")
        print(f"{'='*60}")
        
        for i, (tema, tipo_trampa) in enumerate(temas_dificiles[:num_questions], 1):
            print(f"\n--- Pregunta {i}/{num_questions} ---")
            print(f"📚 Tema: {tema[:50]}...")
            print(f"🎭 Tipo trampa: {tipo_trampa}")
            
            qa = self.generate_max_difficulty_qa(tema, tipo_trampa)
            
            if qa:
                self.generated_qa.append(qa)
                print(f"✅ Q&A generada (dificultad: {qa.get('dificultad', 'N/A')})")
                print(f"   Acierto estimado: {qa.get('porcentaje_acierto_estimado', 'N/A')}%")
            else:
                print(f"❌ Error generando Q&A")
        
        return self.generated_qa
    
    def export_dataset(self) -> str:
        """Exporta el dataset generado"""
        if not self.generated_qa:
            print("❌ No hay Q&A para exportar")
            return None
        
        os.makedirs('dataset_output', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'dataset_output/qa_mistral_agent_maxdif_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.generated_qa, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Dataset exportado: {output_file}")
        return output_file
    
    def show_sample(self, num_samples: int = 2):
        """Muestra ejemplos de Q&A generadas"""
        if not self.generated_qa:
            return
        
        print(f"\n{'='*60}")
        print(f"📋 MUESTRAS DE Q&A MÁXIMA DIFICULTAD")
        print(f"{'='*60}")
        
        for i, qa in enumerate(self.generated_qa[:num_samples], 1):
            print(f"\n--- Muestra {i} ---")
            print(f"🎯 Tema: {qa.get('tema', 'N/A')}")
            print(f"📊 Dificultad: {qa.get('dificultad', 'N/A')}")
            print(f"🎭 Tipo trampa: {qa.get('tipo_trampa', 'N/A')}")
            print(f"📚 Artículos: {qa.get('articulos_referencia', [])}")
            print(f"🔑 Conceptos: {qa.get('conceptos_clave', [])}")
            print(f"⚠️  Errores comunes: {qa.get('errores_comunes', [])}")
            print(f"📈 Acierto estimado: {qa.get('porcentaje_acierto_estimado', 'N/A')}%")
            print(f"\n❓ Pregunta:\n{qa.get('pregunta', '')[:300]}...")
            print(f"\n✅ Respuesta correcta: {qa.get('respuesta_correcta', 'N/A')}")
            print(f"\n📖 Explicación (extracto):\n{qa.get('explicacion', '')[:200]}...")


def main():
    print("\n🎯 GENERADOR DE Q&A MÁXIMA DIFICULTAD CON AGENTE MISTRAL")
    print("=" * 60)
    
    if not MISTRAL_API_KEY:
        print("❌ Error: MISTRAL_API_KEY no configurada")
        return
    
    # Crear agente
    agent = MistralAgentQAGenerator()
    
    # Generar 10 Q&A de máxima dificultad
    dataset = agent.generate_dataset(num_questions=10)
    
    if dataset:
        # Mostrar muestras
        agent.show_sample(2)
        
        # Exportar
        output_file = agent.export_dataset()
        
        print(f"\n{'='*60}")
        print(f"✅ GENERACIÓN COMPLETADA")
        print(f"{'='*60}")
        print(f"📊 Total Q&A: {len(dataset)}")
        print(f"📁 Archivo: {output_file}")
        print(f"🎯 Dificultad: MÁXIMA (10-15% acierto estimado)")
    else:
        print("\n❌ No se pudo generar el dataset")


if __name__ == "__main__":
    main()
