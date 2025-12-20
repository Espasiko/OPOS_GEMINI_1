#!/usr/bin/env python3
"""
Generador Híbrido de Q&A Conceptuales
- Genera con Mistral Local (Ollama)
- Prepara para verificación con Gemini
- Enfocado en relaciones, comparaciones y procedimientos
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from rich.console import Console
from rich.progress import track
import hashlib

console = Console()

# Configuración
OLLAMA_URL = "http://localhost:11434"
ESQUEMAS_DIR = "conceptual_materials/extracted_texts"
OUTPUT_DIR = "conceptual_materials/qa_generated"

# Tipos de Q&A conceptuales (OPTIMIZADO - menos Q&A por tipo)
QA_TYPES = {
    "relacion": {
        "descripcion": "Preguntas sobre cómo se relacionan conceptos",
        "num_per_esquema": 2,  # Reducido de 5 a 2
        "prompt_template": """Esquema: {tema}

{esquema_texto}

Genera 2 preguntas sobre RELACIONES entre conceptos.

JSON:
[{{
  "pregunta": "¿Cómo se relaciona X con Y?",
  "conceptos_relacionados": ["X", "Y"],
  "respuesta": "explicación breve",
  "tipo": "relacion"
}}]"""
    },
    "comparacion": {
        "descripcion": "Preguntas sobre diferencias y similitudes",
        "num_per_esquema": 2,  # Reducido de 3 a 2
        "prompt_template": """Esquema: {tema}

{esquema_texto}

Genera 2 preguntas de COMPARACIÓN.

JSON:
[{{
  "pregunta": "¿Qué diferencia hay entre X e Y?",
  "conceptos_comparados": ["X", "Y"],
  "respuesta": "diferencias clave",
  "tipo": "comparacion"
}}]"""
    },
    "procedimiento": {
        "descripcion": "Preguntas sobre procesos y procedimientos",
        "num_per_esquema": 2,  # Reducido de 4 a 2
        "prompt_template": """Esquema: {tema}

{esquema_texto}

Genera 2 preguntas sobre PROCEDIMIENTOS.

JSON:
[{{
  "pregunta": "¿Cuál es el procedimiento para X?",
  "procedimiento": "nombre",
  "respuesta": "pasos del procedimiento",
  "tipo": "procedimiento",
  "pasos": ["paso1", "paso2"]
}}]"""
    }
}


class ConceptualQAGenerator:
    """Generador híbrido de Q&A conceptuales"""
    
    def __init__(self):
        self.ollama_url = OLLAMA_URL
        self.esquemas_dir = Path(ESQUEMAS_DIR)
        self.output_dir = Path(OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        console.print("[bold cyan]🎯 Generador Híbrido Q&A Conceptuales[/bold cyan]\n")
        console.print(f"Ollama: {self.ollama_url}")
        console.print(f"Esquemas: {self.esquemas_dir}")
        console.print(f"Output: {self.output_dir}\n")
        
        # Verificar Ollama
        if not self.check_ollama():
            raise Exception("❌ Ollama no está disponible")
        
        console.print("✅ Ollama conectado\n")
        
        self.generated_qa = []
        self.stats = {
            "esquemas_procesados": 0,
            "qa_generadas": 0,
            "qa_validadas": 0,
            "qa_rechazadas": 0,
            "por_tipo": {"relacion": 0, "comparacion": 0, "procedimiento": 0}
        }
    
    def check_ollama(self) -> bool:
        """Verifica que Ollama esté funcionando"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def query_mistral(self, prompt: str, temperature: float = 0.4, max_retries: int = 2) -> Optional[str]:
        """Consulta a Mistral local via Ollama con reintentos"""
        for attempt in range(max_retries):
            try:
                payload = {
                    "model": "mistral:latest",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "top_p": 0.9,
                        "max_tokens": 2000,  # Reducido de 3000
                        "num_predict": 2000
                    }
                }
                
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=600  # Aumentado de 300 a 600 segundos (10 min)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('response', '').strip()
                else:
                    console.print(f"[yellow]⚠️  Error en Ollama: {response.status_code}[/yellow]")
                    if attempt < max_retries - 1:
                        console.print(f"[yellow]Reintentando ({attempt + 1}/{max_retries})...[/yellow]")
                        continue
                    return None
            
            except requests.Timeout:
                console.print(f"[yellow]⚠️  Timeout (intento {attempt + 1}/{max_retries})[/yellow]")
                if attempt < max_retries - 1:
                    console.print("[yellow]Reintentando con prompt más corto...[/yellow]")
                    continue
                return None
            
            except Exception as e:
                console.print(f"[red]❌ Error consultando Mistral: {e}[/red]")
                if attempt < max_retries - 1:
                    continue
                return None
    
    def extract_json_from_response(self, response: str) -> Optional[List[Dict]]:
        """Extrae JSON de la respuesta de Mistral"""
        try:
            # Buscar array JSON
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            
            # Buscar objeto JSON único
            json_start = response.find('{')
            if json_start >= 0:
                # Contar llaves para encontrar el cierre
                depth = 0
                json_end = json_start
                for i, char in enumerate(response[json_start:], json_start):
                    if char == '{':
                        depth += 1
                    elif char == '}':
                        depth -= 1
                        if depth == 0:
                            json_end = i + 1
                            break
                
                json_str = response[json_start:json_end]
                obj = json.loads(json_str)
                return [obj] if isinstance(obj, dict) else obj
            
            return None
            
        except json.JSONDecodeError as e:
            console.print(f"[yellow]⚠️  Error parseando JSON: {e}[/yellow]")
            return None
    
    def validate_qa(self, qa: Dict, qa_type: str) -> bool:
        """Valida que una Q&A cumpla los requisitos"""
        # Campos básicos
        if not qa.get('pregunta') or len(qa['pregunta']) < 20:
            return False
        
        if not qa.get('respuesta') or len(qa['respuesta']) < 50:
            return False
        
        if qa.get('tipo') != qa_type:
            qa['tipo'] = qa_type  # Corregir tipo
        
        # Validaciones específicas por tipo
        if qa_type == "relacion":
            if not qa.get('conceptos_relacionados') or len(qa['conceptos_relacionados']) < 2:
                return False
        
        elif qa_type == "comparacion":
            if not qa.get('conceptos_comparados') or len(qa['conceptos_comparados']) < 2:
                return False
        
        elif qa_type == "procedimiento":
            if not qa.get('procedimiento'):
                return False
        
        return True
    
    def generate_qa_for_esquema(self, esquema_file: Path, qa_type: str) -> List[Dict]:
        """Genera Q&A de un tipo específico para un esquema"""
        
        # Leer esquema
        with open(esquema_file, 'r', encoding='utf-8') as f:
            esquema_texto = f.read()
        
        # Limitar texto para el prompt (primeros 800 chars - REDUCIDO)
        esquema_texto_truncado = esquema_texto[:800]
        
        # Extraer tema del nombre del archivo
        tema = esquema_file.stem.replace('_', ' ')
        
        # Crear prompt
        qa_config = QA_TYPES[qa_type]
        prompt = qa_config["prompt_template"].format(
            tema=tema,
            esquema_texto=esquema_texto_truncado,
            esquema_nombre=esquema_file.name
        )
        
        console.print(f"  [cyan]Generando {qa_type}...[/cyan]")
        
        # Consultar Mistral
        response = self.query_mistral(prompt, temperature=0.4)
        
        if not response:
            console.print(f"  [yellow]⚠️  No se obtuvo respuesta[/yellow]")
            return []
        
        # Extraer JSON
        qa_list = self.extract_json_from_response(response)
        
        if not qa_list:
            console.print(f"  [yellow]⚠️  No se pudo extraer JSON[/yellow]")
            return []
        
        # Validar y enriquecer
        valid_qa = []
        for qa in qa_list:
            if self.validate_qa(qa, qa_type):
                # Enriquecer con metadata
                qa['fuente_esquema'] = esquema_file.name
                qa['generated_at'] = datetime.now().isoformat()
                qa['model'] = 'mistral:latest (ollama)'
                qa['hash'] = hashlib.md5(qa['pregunta'].lower().encode()).hexdigest()[:12]
                qa['verified'] = False  # Pendiente de verificación Gemini
                qa['verification_status'] = 'pending'
                
                valid_qa.append(qa)
                self.stats['qa_generadas'] += 1
                self.stats['qa_validadas'] += 1
                self.stats['por_tipo'][qa_type] += 1
            else:
                self.stats['qa_rechazadas'] += 1
        
        console.print(f"  [green]✓ {len(valid_qa)} Q&A generadas[/green]")
        return valid_qa
    
    def process_all_esquemas(self) -> List[Dict]:
        """Procesa todos los esquemas y genera Q&A"""
        esquemas = sorted(self.esquemas_dir.glob("*.txt"))
        
        console.print(f"[bold]📚 Procesando {len(esquemas)} esquemas...[/bold]\n")
        
        all_qa = []
        
        for esquema in track(esquemas, description="Procesando esquemas"):
            console.print(f"\n[bold cyan]--- {esquema.name} ---[/bold cyan]")
            
            # Generar Q&A de cada tipo
            for qa_type in QA_TYPES.keys():
                qa_list = self.generate_qa_for_esquema(esquema, qa_type)
                all_qa.extend(qa_list)
            
            self.stats['esquemas_procesados'] += 1
        
        self.generated_qa = all_qa
        return all_qa
    
    def export_dataset(self):
        """Exporta dataset generado"""
        if not self.generated_qa:
            console.print("[yellow]⚠️  No hay Q&A para exportar[/yellow]")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Exportar JSONL (para procesamiento)
        jsonl_file = self.output_dir / f"conceptual_qa_raw_{timestamp}.jsonl"
        with open(jsonl_file, 'w', encoding='utf-8') as f:
            for qa in self.generated_qa:
                f.write(json.dumps(qa, ensure_ascii=False) + '\n')
        
        console.print(f"\n[green]✓ Dataset JSONL: {jsonl_file}[/green]")
        
        # Exportar JSON legible
        json_file = self.output_dir / f"conceptual_qa_raw_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.generated_qa, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]✓ Dataset JSON: {json_file}[/green]")
        
        # Exportar estadísticas
        stats_file = self.output_dir / f"stats_{timestamp}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]✓ Estadísticas: {stats_file}[/green]")
    
    def print_stats(self):
        """Muestra estadísticas"""
        console.print(f"\n[bold]{'='*60}[/bold]")
        console.print(f"[bold cyan]📊 ESTADÍSTICAS DE GENERACIÓN[/bold cyan]")
        console.print(f"[bold]{'='*60}[/bold]")
        console.print(f"Esquemas procesados:  {self.stats['esquemas_procesados']}")
        console.print(f"Q&A generadas:        {self.stats['qa_generadas']}")
        console.print(f"Q&A validadas:        {self.stats['qa_validadas']}")
        console.print(f"Q&A rechazadas:       {self.stats['qa_rechazadas']}")
        
        console.print(f"\n[bold]Por tipo:[/bold]")
        for tipo, count in self.stats['por_tipo'].items():
            console.print(f"  {tipo:15} {count}")
        
        if self.stats['qa_generadas'] > 0:
            success_rate = (self.stats['qa_validadas'] / self.stats['qa_generadas']) * 100
            console.print(f"\nTasa de éxito:        {success_rate:.1f}%")
        
        console.print(f"[bold]{'='*60}[/bold]\n")
    
    def show_samples(self, num_samples: int = 3):
        """Muestra muestras del dataset"""
        if not self.generated_qa:
            return
        
        console.print(f"\n[bold]{'='*60}[/bold]")
        console.print(f"[bold cyan]📋 MUESTRAS DEL DATASET[/bold cyan]")
        console.print(f"[bold]{'='*60}[/bold]\n")
        
        for i, qa in enumerate(self.generated_qa[:num_samples], 1):
            console.print(f"[bold]--- Muestra {i} ---[/bold]")
            console.print(f"Tipo: {qa['tipo']}")
            console.print(f"Fuente: {qa['fuente_esquema']}")
            console.print(f"\n[bold]Pregunta:[/bold]")
            console.print(f"{qa['pregunta']}\n")
            console.print(f"[bold]Respuesta:[/bold]")
            console.print(f"{qa['respuesta'][:200]}...\n")
            console.print(f"[bold]{'='*60}[/bold]\n")


def main():
    """Función principal"""
    console.print("\n[bold green]🚀 GENERADOR HÍBRIDO Q&A CONCEPTUALES[/bold green]")
    console.print("[bold green]Mistral Local + Gemini Verification[/bold green]\n")
    
    try:
        # Crear generador
        generator = ConceptualQAGenerator()
        
        # Generar Q&A
        dataset = generator.process_all_esquemas()
        
        if dataset:
            # Mostrar estadísticas
            generator.print_stats()
            
            # Mostrar muestras
            generator.show_samples(num_samples=3)
            
            # Exportar
            generator.export_dataset()
            
            console.print("\n[bold green]✅ GENERACIÓN COMPLETADA[/bold green]")
            console.print(f"[green]Total Q&A: {len(dataset)}[/green]")
            console.print(f"[yellow]Próximo paso: Verificar con Gemini[/yellow]\n")
        else:
            console.print("\n[red]❌ No se pudo generar el dataset[/red]\n")
    
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
