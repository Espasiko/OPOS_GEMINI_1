#!/usr/bin/env python3
"""
Herramienta de revisión humana para Q&A de alto riesgo.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()


class HumanReviewer:
    """Interfaz para revisión humana de Q&A."""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.reviewed_qa = []
        self.stats = {
            "total": 0,
            "reviewed": 0,
            "approved": 0,
            "modified": 0,
            "rejected": 0,
            "skipped": 0
        }
    
    def load_qa(self) -> List[Dict]:
        """Carga Q&A que necesitan revisión."""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            all_qa = json.load(f)
        
        # Filtrar solo las que necesitan revisión humana
        needs_review = [qa for qa in all_qa if qa.get("needs_human_review", False)]
        
        # Ordenar por prioridad (critical primero)
        priority_order = {"critical": 0, "medium": 1, "low": 2}
        needs_review.sort(key=lambda x: priority_order.get(x.get("review_priority", "low"), 3))
        
        return needs_review
    
    def display_qa(self, qa: Dict, index: int, total: int):
        """Muestra una Q&A para revisión."""
        console.clear()
        
        # Header
        console.print(Panel.fit(
            f"[bold blue]Revisión Humana de Q&A[/bold blue]\n"
            f"[cyan]Progreso: {index}/{total}[/cyan]",
            border_style="blue"
        ))
        
        # Metadata
        table = Table(show_header=False, box=None)
        table.add_row("[yellow]Fuente:[/yellow]", qa.get("source", "N/A"))
        table.add_row("[yellow]Riesgo:[/yellow]", self._format_risk(qa.get("risk_level", "unknown")))
        table.add_row("[yellow]Tipo:[/yellow]", qa.get("content_type", "N/A"))
        table.add_row("[yellow]Complejidad:[/yellow]", qa.get("complexity", "N/A"))
        table.add_row("[yellow]Confianza IA:[/yellow]", f"{qa.get('confidence', 0.0):.2f}")
        console.print(table)
        console.print()
        
        # Q&A
        console.print(Panel(
            f"[bold]Pregunta:[/bold]\n{qa.get('pregunta', '')}",
            border_style="cyan"
        ))
        console.print()
        console.print(Panel(
            f"[bold]Respuesta:[/bold]\n{qa.get('respuesta', '')}\n\n"
            f"[dim]Referencia: {qa.get('referencia', 'N/A')}[/dim]",
            border_style="green"
        ))
        console.print()
        
        # Problemas detectados
        if qa.get("verification_issues"):
            console.print("[yellow]⚠ Problemas detectados por IA:[/yellow]")
            for issue in qa["verification_issues"]:
                console.print(f"  • {issue}")
            console.print()
    
    def _format_risk(self, risk: str) -> str:
        """Formatea el nivel de riesgo con colores."""
        if risk == "high":
            return "[bold red]ALTO[/bold red]"
        elif risk == "medium":
            return "[yellow]MEDIO[/yellow]"
        else:
            return "[green]BAJO[/green]"
    
    def review_qa(self, qa: Dict) -> Dict:
        """Revisa una Q&A interactivamente."""
        console.print("[bold]Opciones:[/bold]")
        console.print("  [green]1[/green] - Aprobar (correcta)")
        console.print("  [yellow]2[/yellow] - Modificar (editar)")
        console.print("  [red]3[/red] - Rechazar (eliminar)")
        console.print("  [cyan]4[/cyan] - Saltar (revisar después)")
        console.print("  [dim]5[/dim] - Guardar y salir")
        console.print()
        
        choice = Prompt.ask("Acción", choices=["1", "2", "3", "4", "5"], default="1")
        
        if choice == "1":
            # Aprobar
            qa["human_reviewed"] = True
            qa["human_review_status"] = "approved"
            qa["human_reviewer"] = Prompt.ask("Tu nombre/ID", default="reviewer")
            self.stats["approved"] += 1
            return qa
        
        elif choice == "2":
            # Modificar
            console.print("\n[yellow]Editando Q&A...[/yellow]")
            
            if Confirm.ask("¿Modificar pregunta?"):
                new_question = Prompt.ask("Nueva pregunta", default=qa.get("pregunta", ""))
                qa["pregunta"] = new_question
            
            if Confirm.ask("¿Modificar respuesta?"):
                console.print("[dim]Respuesta actual:[/dim]")
                console.print(qa.get("respuesta", ""))
                new_answer = Prompt.ask("Nueva respuesta", default=qa.get("respuesta", ""))
                qa["respuesta"] = new_answer
            
            if Confirm.ask("¿Modificar referencia?"):
                new_ref = Prompt.ask("Nueva referencia", default=qa.get("referencia", ""))
                qa["referencia"] = new_ref
            
            notes = Prompt.ask("Notas de revisión (opcional)", default="")
            
            qa["human_reviewed"] = True
            qa["human_review_status"] = "modified"
            qa["human_reviewer"] = Prompt.ask("Tu nombre/ID", default="reviewer")
            qa["review_notes"] = notes
            self.stats["modified"] += 1
            return qa
        
        elif choice == "3":
            # Rechazar
            reason = Prompt.ask("Razón del rechazo")
            qa["human_reviewed"] = True
            qa["human_review_status"] = "rejected"
            qa["rejection_reason"] = reason
            qa["human_reviewer"] = Prompt.ask("Tu nombre/ID", default="reviewer")
            self.stats["rejected"] += 1
            return None  # No incluir en dataset final
        
        elif choice == "4":
            # Saltar
            self.stats["skipped"] += 1
            return qa
        
        elif choice == "5":
            # Guardar y salir
            return "EXIT"
    
    def run(self):
        """Ejecuta el proceso de revisión."""
        qa_list = self.load_qa()
        self.stats["total"] = len(qa_list)
        
        if not qa_list:
            console.print("[yellow]No hay Q&A que necesiten revisión humana[/yellow]")
            return
        
        console.print(f"\n[bold green]Encontradas {len(qa_list)} Q&A para revisar[/bold green]")
        console.print("[dim]Presiona Enter para comenzar...[/dim]")
        input()
        
        for i, qa in enumerate(qa_list, 1):
            self.display_qa(qa, i, len(qa_list))
            
            result = self.review_qa(qa)
            
            if result == "EXIT":
                console.print("\n[yellow]Guardando progreso...[/yellow]")
                break
            elif result is not None:
                self.reviewed_qa.append(result)
                self.stats["reviewed"] += 1
        
        # Guardar resultados
        self.save_results()
        self.show_summary()
    
    def save_results(self):
        """Guarda Q&A revisadas."""
        output_path = Path(self.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.reviewed_qa, f, ensure_ascii=False, indent=2)
        
        console.print(f"\n[green]✓ Guardadas {len(self.reviewed_qa)} Q&A → {output_path}[/green]")
    
    def show_summary(self):
        """Muestra resumen de la revisión."""
        console.print("\n" + "="*60)
        console.print(Panel.fit(
            f"[bold green]Resumen de Revisión Humana[/bold green]\n\n"
            f"[cyan]Total para revisar:[/cyan] {self.stats['total']}\n"
            f"[green]✓ Aprobadas:[/green] {self.stats['approved']}\n"
            f"[yellow]✎ Modificadas:[/yellow] {self.stats['modified']}\n"
            f"[red]✗ Rechazadas:[/red] {self.stats['rejected']}\n"
            f"[dim]⊙ Saltadas:[/dim] {self.stats['skipped']}\n\n"
            f"[bold]Revisadas:[/bold] {self.stats['reviewed']}/{self.stats['total']} "
            f"({self.stats['reviewed']/self.stats['total']*100:.1f}%)",
            border_style="green"
        ))


def main():
    parser = argparse.ArgumentParser(description="Revisión humana de Q&A")
    parser.add_argument("--input", required=True, help="Archivo JSON con Q&A verificadas")
    parser.add_argument("--output", required=True, help="Archivo JSON con Q&A revisadas")
    
    args = parser.parse_args()
    
    console.print(Panel.fit(
        "[bold blue]👤 Herramienta de Revisión Humana[/bold blue]\n"
        "[cyan]Para Q&A de alto riesgo (normativa, leyes, jurisprudencia)[/cyan]",
        border_style="blue"
    ))
    
    reviewer = HumanReviewer(args.input, args.output)
    reviewer.run()


if __name__ == "__main__":
    main()
