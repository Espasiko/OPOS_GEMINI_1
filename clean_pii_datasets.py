#!/usr/bin/env python3
"""
Limpiador de PII (Datos Identificables) de Datasets
Elimina referencias a academias, emails, teléfonos y otros datos reveladores
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.progress import track

console = Console()

# Patrones de PII a eliminar/reemplazar
PII_PATTERNS = {
    # Academias
    r'Academia Las Cortes': '[ACADEMIA]',
    r'academialascortes\.com': '[WEB_ACADEMIA]',
    r'info@academialascortes\.com': '[EMAIL_ACADEMIA]',
    r'Las Cortes': '[ACADEMIA]',
    r'www\.academialascortes\.com': '[WEB_ACADEMIA]',
    
    # Teléfonos
    r'633\s*32\s*44\s*32': '[TELEFONO]',
    r'\d{3}\s*\d{2}\s*\d{2}\s*\d{2}': '[TELEFONO]',
    r'\+34\s*\d{9}': '[TELEFONO]',
    
    # Otros patrones de academias
    r'[Oo]posita': '[ACADEMIA]',
    r'[Pp]reparador[a]?': '[PREPARADOR]',
    r'[Pp]rofesor[a]?\s+[A-Z][a-záéíóú]+': '[PROFESOR]',
    
    # URLs de academias (genéricas)
    r'www\.[a-z]+academia[a-z]*\.com': '[WEB_ACADEMIA]',
    r'www\.prepara[a-z]+\.com': '[WEB_ACADEMIA]',
}

# Patrones que indican Q&A problemáticas (eliminar completamente)
PROBLEMATIC_PATTERNS = [
    r'inscri[bp]irse en la academia',
    r'matrícula.*academia',
    r'clases online.*academia',
    r'temario.*academia',
    r'pago.*matrícula',
]


class PIICleaner:
    """Limpiador de PII en datasets"""
    
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            "files_processed": 0,
            "files_with_pii": 0,
            "qa_processed": 0,
            "qa_cleaned": 0,
            "qa_removed": 0,
            "pii_replacements": 0
        }
    
    def clean_text(self, text: str) -> tuple[str, int]:
        """Limpia texto de PII, devuelve (texto_limpio, num_reemplazos)"""
        if not text:
            return text, 0
        
        replacements = 0
        cleaned = text
        
        for pattern, replacement in PII_PATTERNS.items():
            matches = len(re.findall(pattern, cleaned, re.IGNORECASE))
            if matches > 0:
                cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
                replacements += matches
        
        return cleaned, replacements
    
    def is_problematic(self, qa: dict) -> bool:
        """Determina si una Q&A es problemática y debe eliminarse"""
        text = json.dumps(qa, ensure_ascii=False).lower()
        
        for pattern in PROBLEMATIC_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def clean_qa(self, qa: dict) -> tuple[dict, bool, int]:
        """
        Limpia una Q&A de PII
        Devuelve: (qa_limpia, fue_limpiada, num_reemplazos)
        """
        total_replacements = 0
        cleaned_qa = qa.copy()
        
        # Limpiar campos de texto
        text_fields = ['pregunta', 'respuesta', 'explicacion', 'question', 'answer', 
                       'explanation', 'contexto', 'context', 'fuente', 'source']
        
        for field in text_fields:
            if field in cleaned_qa and cleaned_qa[field]:
                cleaned_text, reps = self.clean_text(str(cleaned_qa[field]))
                cleaned_qa[field] = cleaned_text
                total_replacements += reps
        
        # Limpiar opciones si existen
        if 'opciones' in cleaned_qa and isinstance(cleaned_qa['opciones'], list):
            cleaned_options = []
            for opt in cleaned_qa['opciones']:
                if isinstance(opt, str):
                    cleaned_opt, reps = self.clean_text(opt)
                    cleaned_options.append(cleaned_opt)
                    total_replacements += reps
                else:
                    cleaned_options.append(opt)
            cleaned_qa['opciones'] = cleaned_options
        
        # Marcar como limpiada
        if total_replacements > 0:
            cleaned_qa['pii_cleaned'] = True
            cleaned_qa['pii_replacements'] = total_replacements
        
        return cleaned_qa, total_replacements > 0, total_replacements
    
    def process_jsonl_file(self, filepath: Path) -> Path:
        """Procesa un archivo JSONL y genera versión limpia"""
        console.print(f"\n[cyan]Procesando: {filepath.name}[/cyan]")
        
        cleaned_qa_list = []
        file_replacements = 0
        removed_count = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in track(lines, description=f"  Limpiando"):
            line = line.strip()
            if not line:
                continue
            
            try:
                qa = json.loads(line)
                self.stats["qa_processed"] += 1
                
                # Verificar si es problemática
                if self.is_problematic(qa):
                    removed_count += 1
                    self.stats["qa_removed"] += 1
                    continue
                
                # Limpiar PII
                cleaned_qa, was_cleaned, reps = self.clean_qa(qa)
                
                if was_cleaned:
                    self.stats["qa_cleaned"] += 1
                    file_replacements += reps
                
                cleaned_qa_list.append(cleaned_qa)
                
            except json.JSONDecodeError:
                continue
        
        # Guardar versión limpia
        output_path = self.output_dir / f"{filepath.stem}_CLEAN.jsonl"
        with open(output_path, 'w', encoding='utf-8') as f:
            for qa in cleaned_qa_list:
                f.write(json.dumps(qa, ensure_ascii=False) + '\n')
        
        self.stats["files_processed"] += 1
        if file_replacements > 0 or removed_count > 0:
            self.stats["files_with_pii"] += 1
        self.stats["pii_replacements"] += file_replacements
        
        console.print(f"  [green]✓ {len(cleaned_qa_list)} Q&A guardadas[/green]")
        console.print(f"  [yellow]  Reemplazos PII: {file_replacements}[/yellow]")
        console.print(f"  [red]  Eliminadas: {removed_count}[/red]")
        
        return output_path
    
    def process_json_file(self, filepath: Path) -> Path:
        """Procesa un archivo JSON y genera versión limpia"""
        console.print(f"\n[cyan]Procesando: {filepath.name}[/cyan]")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        file_replacements = 0
        removed_count = 0
        
        # Puede ser lista o dict
        if isinstance(data, list):
            cleaned_list = []
            for qa in track(data, description=f"  Limpiando"):
                self.stats["qa_processed"] += 1
                
                if self.is_problematic(qa):
                    removed_count += 1
                    self.stats["qa_removed"] += 1
                    continue
                
                cleaned_qa, was_cleaned, reps = self.clean_qa(qa)
                if was_cleaned:
                    self.stats["qa_cleaned"] += 1
                    file_replacements += reps
                
                cleaned_list.append(cleaned_qa)
            
            output_data = cleaned_list
        else:
            # Es un dict, limpiar recursivamente
            cleaned_data, reps = self.clean_text(json.dumps(data, ensure_ascii=False))
            output_data = json.loads(cleaned_data)
            file_replacements = reps
        
        # Guardar versión limpia
        output_path = self.output_dir / f"{filepath.stem}_CLEAN.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        self.stats["files_processed"] += 1
        if file_replacements > 0 or removed_count > 0:
            self.stats["files_with_pii"] += 1
        self.stats["pii_replacements"] += file_replacements
        
        if isinstance(data, list):
            console.print(f"  [green]✓ {len(output_data)} items guardados[/green]")
        console.print(f"  [yellow]  Reemplazos PII: {file_replacements}[/yellow]")
        console.print(f"  [red]  Eliminadas: {removed_count}[/red]")
        
        return output_path
    
    def process_all(self, files_with_pii: list = None):
        """Procesa todos los archivos con PII"""
        console.print("[bold green]🧹 LIMPIADOR DE PII - dataset_output[/bold green]\n")
        
        if files_with_pii:
            files = [self.input_dir / f for f in files_with_pii]
        else:
            files = list(self.input_dir.glob("*.json")) + list(self.input_dir.glob("*.jsonl"))
        
        console.print(f"Archivos a procesar: {len(files)}\n")
        
        for filepath in files:
            if not filepath.exists():
                console.print(f"[yellow]⚠️  No existe: {filepath.name}[/yellow]")
                continue
            
            if filepath.suffix == '.jsonl':
                self.process_jsonl_file(filepath)
            else:
                self.process_json_file(filepath)
        
        self.print_stats()
    
    def print_stats(self):
        """Muestra estadísticas finales"""
        console.print(f"\n{'='*60}")
        console.print("[bold cyan]📊 ESTADÍSTICAS DE LIMPIEZA[/bold cyan]")
        console.print(f"{'='*60}")
        console.print(f"Archivos procesados:    {self.stats['files_processed']}")
        console.print(f"Archivos con PII:       {self.stats['files_with_pii']}")
        console.print(f"Q&A procesadas:         {self.stats['qa_processed']}")
        console.print(f"Q&A limpiadas:          {self.stats['qa_cleaned']}")
        console.print(f"Q&A eliminadas:         {self.stats['qa_removed']}")
        console.print(f"Reemplazos PII:         {self.stats['pii_replacements']}")
        console.print(f"{'='*60}\n")
        
        # Guardar stats
        stats_file = self.output_dir / f"pii_cleaning_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2)
        console.print(f"[green]✓ Stats guardadas: {stats_file}[/green]")


def main():
    """Función principal"""
    # Archivos conocidos con PII
    FILES_WITH_PII = [
        "SIMULACRO_COMPLETO_112_OFICIAL_20251208_205851.json",
        "SIMULACRO_COMPLETO_112_PREGUNTAS_OFICIAL_BOE.json",
        "SIMULACRO_MINI_5_40_PREGUNTAS.json",
        "extracted_hard_questions.json",
        "qa_baja_cobertura_500_PREMIUM_FINAL_20251208.jsonl",
        "qa_baja_cobertura_PREMIUM_20251208.jsonl",
        "qa_completo_unificado_20251208.jsonl",
        "qa_completo_unificado_CORREGIDO_20251208.jsonl",
        "qa_kiro_boe_limpio_20251208.jsonl",
        "qa_kiro_boe_verificado_20251206.jsonl",
    ]
    
    cleaner = PIICleaner(
        input_dir="dataset_generator/dataset_output",
        output_dir="dataset_generator/dataset_output_CLEAN"
    )
    
    cleaner.process_all(FILES_WITH_PII)
    
    console.print("\n[bold green]✅ LIMPIEZA COMPLETADA[/bold green]")
    console.print("[yellow]Próximo paso: Revisar archivos en dataset_output_CLEAN/[/yellow]\n")


if __name__ == "__main__":
    main()
