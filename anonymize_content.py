#!/usr/bin/env python3
"""
Anonimiza contenido eliminando rastros de academias, autores, etc.
"""
import re
from typing import Dict, List, Tuple
from pathlib import Path
import json

class ContentAnonymizer:
    """Limpia contenido de rastros identificables"""
    
    def __init__(self):
        self.forbidden_patterns = {
            "nombres_autores": [
                r"Sara\s+Domínguez",
                r"Carlos\s+Hernández",
                r"Alfonso\s+Hidalgo",
                r"Víctor\s+Cabeza",
                r"Pablo\s+Segado"
            ],
            "academias": [
                r"Las\s+Cortes",
                r"TEMA\s+DIGITAL",
                r"GoKoan",
                r"Oposiciones\.es"
            ],
            "identificadores": [
                r"5001-\d+",
                r"5002-\d+",
                r"8035-\d+",
                r"8038-\d+",
                r"8039-\d+",
                r"8040-\d+",
                r"Anexo\d+A\d+",
                r"ISBN[\s:-]*[\dX-]+"
            ],
            "copyright": [
                r"Queda\s+prohibido.*?distribución",
                r"©\s*\d{4}.*?Las\s+Cortes",
                r"Copyright.*?\d{4}",
                r"Todos\s+los\s+derechos\s+reservados"
            ],
            "estructuras_especificas": [
                r"villancico",
                r"Simulacro\s+\d{1,2}\s+\(\d{4}\)",
                r"Cuadernillo.*?ejercicio"
            ]
        }
    
    def clean_text(self, text: str) -> Tuple[str, List[str]]:
        """
        Limpia texto de patrones prohibidos
        
        Returns:
            (texto_limpio, patrones_encontrados)
        """
        cleaned_text = text
        found_patterns = []
        
        for category, patterns in self.forbidden_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    found_patterns.append(f"{category}: {matches[0]}")
                    cleaned_text = re.sub(
                        pattern,
                        "[REDACTADO]",
                        cleaned_text,
                        flags=re.IGNORECASE
                    )
        
        return cleaned_text, found_patterns
    
    def is_safe_for_public(self, text: str) -> bool:
        """Verifica si el texto es seguro para colección pública"""
        _, found_patterns = self.clean_text(text)
        return len(found_patterns) == 0
    
    def classify_document(self, file_path: str) -> str:
        """
        Clasifica documento como público o privado
        
        Returns:
            "public" - Exámenes oficiales BOE, leyes
            "private" - Material de academias
        """
        filename = Path(file_path).name.lower()
        
        # Exámenes oficiales (públicos)
        if any(x in filename for x in ["examen_c1", "gestion_libre", "gestion_pi"]):
            # Verificar que NO tenga marca de academia
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)  # Primeros 1000 chars
                    if not self.is_safe_for_public(content):
                        return "private"  # Tiene marca de academia
            except:
                pass
            return "public"
        
        # Casos prácticos (privados por defecto)
        if any(x in filename for x in ["caso", "ip_", "it.", "jubilacion", "mys_"]):
            return "private"
        
        # Por defecto, privado
        return "private"

def main():
    import sys
    from rich.console import Console
    
    console = Console()
    
    if len(sys.argv) < 2:
        console.print("[red]Uso: python anonymize_content.py <archivo_o_directorio>[/red]")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    anonymizer = ContentAnonymizer()
    
    if path.is_file():
        # Procesar un archivo
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        clean_content, patterns = anonymizer.clean_text(content)
        classification = anonymizer.classify_document(str(path))
        
        console.print(f"[cyan]Archivo: {path.name}[/cyan]")
        console.print(f"Clasificación: {classification}")
        console.print(f"Patrones encontrados: {len(patterns)}")
        if patterns:
            for p in patterns:
                console.print(f"  - {p}")
    
    elif path.is_dir():
        # Procesar directorio
        results = {"public": [], "private": []}
        
        for txt_file in path.glob("*.txt"):
            classification = anonymizer.classify_document(str(txt_file))
            results[classification].append(txt_file.name)
        
        console.print(f"\n[bold]Resultados:[/bold]")
        console.print(f"Públicos: {len(results['public'])}")
        console.print(f"Privados: {len(results['private'])}")
        
        # Guardar clasificación
        output = path / "classification_report.json"
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        
        console.print(f"\n[green]✓ Reporte guardado: {output}[/green]")

if __name__ == "__main__":
    main()
