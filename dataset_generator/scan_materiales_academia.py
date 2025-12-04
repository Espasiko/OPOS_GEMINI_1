#!/usr/bin/env python3
"""
Escáner de Materiales de Academia
Categoriza todos los PDFs encontrados en la carpeta de materiales
"""

import os
import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

class MaterialesScanner:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.categories = {
            "examenes_oficiales": [],
            "simulacros": [],
            "tests": [],
            "esquemas": [],
            "temarios": [],
            "resumenes": [],
            "casos_practicos": [],
            "otros": []
        }
        
    def categorize_file(self, filename: str, filepath: str) -> str:
        """Categoriza un archivo según su nombre"""
        filename_lower = filename.lower()
        
        # Exámenes oficiales
        if any(keyword in filename_lower for keyword in [
            'examen_c1', 'gestion_libre', 'gestion_pi', 
            'respuestas_examen', 'respuestas_gestion',
            'examen_oficial', 'convocatoria'
        ]):
            return "examenes_oficiales"
        
        # Simulacros
        if any(keyword in filename_lower for keyword in [
            'simulacro', 'simul'
        ]):
            return "simulacros"
        
        # Tests
        if any(keyword in filename_lower for keyword in [
            'test_', 'tests', 'preguntas'
        ]):
            return "tests"
        
        # Esquemas
        if any(keyword in filename_lower for keyword in [
            'esquema', 'resumen', 'tabla'
        ]):
            # Distinguir entre esquemas y resúmenes
            if 'resumen' in filename_lower:
                return "resumenes"
            return "esquemas"
        
        # Temarios
        if any(keyword in filename_lower for keyword in [
            'temario', 'tema_', 'tema ', 't6 ', 't7 '
        ]):
            return "temarios"
        
        # Casos prácticos
        if any(keyword in filename_lower for keyword in [
            'caso', 'practico', 'supuesto'
        ]):
            return "casos_practicos"
        
        # Prestaciones específicas (esquemas)
        prestaciones = [
            'it.pdf', 'ip_', 'jubilacion', 'viudedad', 
            'orfandad', 'nycm', 'encuadramiento', 
            'cotizacion', 'prestaciones_familiares'
        ]
        if any(prest in filename_lower for prest in prestaciones):
            return "esquemas"
        
        return "otros"
    
    def scan_directory(self, directory: str, parent_folder: str = "") -> None:
        """Escanea un directorio recursivamente"""
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                
                if os.path.isdir(item_path):
                    # Recursión en subdirectorios
                    folder_name = os.path.basename(item_path)
                    self.scan_directory(item_path, folder_name)
                    
                elif item.lower().endswith('.pdf'):
                    # Procesar PDF
                    category = self.categorize_file(item, item_path)
                    
                    # Obtener tamaño del archivo
                    size_bytes = os.path.getsize(item_path)
                    size_mb = size_bytes / (1024 * 1024)
                    
                    # Obtener ruta relativa
                    rel_path = os.path.relpath(item_path, self.base_path)
                    
                    file_info = {
                        "filename": item,
                        "path": rel_path,
                        "full_path": item_path,
                        "size_mb": round(size_mb, 2),
                        "parent_folder": parent_folder,
                        "category": category
                    }
                    
                    self.categories[category].append(file_info)
                    
        except PermissionError:
            print(f"⚠️  Sin permisos para acceder a: {directory}")
        except Exception as e:
            print(f"❌ Error procesando {directory}: {e}")
    
    def generate_report(self) -> Dict:
        """Genera reporte del escaneo"""
        total_files = sum(len(files) for files in self.categories.values())
        total_size = sum(
            file['size_mb'] 
            for files in self.categories.values() 
            for file in files
        )
        
        report = {
            "total_pdfs": total_files,
            "total_size_mb": round(total_size, 2),
            "categories": {}
        }
        
        for category, files in self.categories.items():
            if files:
                category_size = sum(f['size_mb'] for f in files)
                report["categories"][category] = {
                    "count": len(files),
                    "size_mb": round(category_size, 2),
                    "files": sorted(files, key=lambda x: x['filename'])
                }
        
        return report
    
    def generate_markdown_report(self, report: Dict, output_file: str) -> None:
        """Genera reporte en formato Markdown"""
        
        md = f"""# 📚 INVENTARIO DE MATERIALES DE ACADEMIA

**Fecha de escaneo**: {self._get_timestamp()}
**Total de PDFs**: {report['total_pdfs']}
**Tamaño total**: {report['total_size_mb']:.2f} MB

---

## 📊 RESUMEN POR CATEGORÍAS

"""
        
        # Tabla resumen
        md += "| Categoría | Cantidad | Tamaño (MB) |\n"
        md += "|-----------|----------|-------------|\n"
        
        for category, data in sorted(report['categories'].items(), 
                                     key=lambda x: x[1]['count'], 
                                     reverse=True):
            md += f"| {category.replace('_', ' ').title()} | {data['count']} | {data['size_mb']:.2f} |\n"
        
        md += "\n---\n\n"
        
        # Detalle por categoría
        priority_categories = [
            "examenes_oficiales",
            "simulacros", 
            "tests",
            "esquemas",
            "temarios",
            "casos_practicos",
            "resumenes",
            "otros"
        ]
        
        for category in priority_categories:
            if category in report['categories']:
                data = report['categories'][category]
                md += f"## 📁 {category.replace('_', ' ').upper()}\n\n"
                md += f"**Total**: {data['count']} archivos ({data['size_mb']:.2f} MB)\n\n"
                
                # Agrupar por carpeta padre
                by_folder = defaultdict(list)
                for file in data['files']:
                    folder = file['parent_folder'] or 'raíz'
                    by_folder[folder].append(file)
                
                for folder, files in sorted(by_folder.items()):
                    if folder != 'raíz':
                        md += f"### 📂 {folder}\n\n"
                    
                    for file in files:
                        md += f"- **{file['filename']}** ({file['size_mb']:.2f} MB)\n"
                        md += f"  - Ruta: `{file['path']}`\n"
                    
                    md += "\n"
                
                md += "---\n\n"
        
        # Recomendaciones
        md += self._generate_recommendations(report)
        
        # Guardar archivo
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"\n✅ Reporte guardado en: {output_file}")
    
    def _generate_recommendations(self, report: Dict) -> str:
        """Genera recomendaciones basadas en el análisis"""
        md = "## 💡 RECOMENDACIONES PARA INDEXACIÓN\n\n"
        
        # Prioridad 1: Exámenes oficiales
        if "examenes_oficiales" in report['categories']:
            count = report['categories']['examenes_oficiales']['count']
            md += f"### 🎯 PRIORIDAD ALTA: Exámenes Oficiales\n"
            md += f"- **{count} archivos** identificados\n"
            md += f"- Estos son documentos públicos y oficiales\n"
            md += f"- Contienen preguntas reales de convocatorias anteriores\n"
            md += f"- **Acción**: Indexar primero en RAG con metadata específica\n"
            md += f"- **Uso**: Generar variaciones con Mistral local\n\n"
        
        # Prioridad 2: Esquemas
        if "esquemas" in report['categories']:
            count = report['categories']['esquemas']['count']
            md += f"### 📋 PRIORIDAD MEDIA: Esquemas de Prestaciones\n"
            md += f"- **{count} archivos** identificados\n"
            md += f"- Contienen información estructurada de prestaciones\n"
            md += f"- Ideales para generar Q&A desde contenido legal\n"
            md += f"- **Acción**: Indexar con chunking optimizado\n"
            md += f"- **Uso**: Generar preguntas conceptuales\n\n"
        
        # Prioridad 3: Tests y simulacros
        test_count = report['categories'].get('tests', {}).get('count', 0)
        simul_count = report['categories'].get('simulacros', {}).get('count', 0)
        if test_count + simul_count > 0:
            md += f"### 📝 PRIORIDAD MEDIA: Tests y Simulacros\n"
            md += f"- **{test_count} tests** + **{simul_count} simulacros**\n"
            md += f"- Contienen preguntas de academias (no oficiales)\n"
            md += f"- **Precaución**: Verificar derechos de autor\n"
            md += f"- **Acción**: Usar solo para análisis de patrones\n"
            md += f"- **Uso**: Detectar duplicados y generar variaciones transformadas\n\n"
        
        md += "### 🔒 ESTRATEGIA DE PRIVACIDAD\n\n"
        md += "1. **Indexar en Qdrant local** (Docker WSL)\n"
        md += "2. **Usar BGE-M3** como modelo de embeddings\n"
        md += "3. **Procesar con Mistral local** (Ollama)\n"
        md += "4. **Generar variaciones** que no dejen rastro del origen\n"
        md += "5. **Validar calidad** antes de exportar\n\n"
        
        return md
    
    def _get_timestamp(self) -> str:
        """Obtiene timestamp actual"""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def export_json(self, report: Dict, output_file: str) -> None:
        """Exporta reporte en JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON exportado: {output_file}")

def main():
    """Función principal"""
    # Ruta base en WSL
    base_path = "/home/espasiko/OPOS_GEMINI_1/elemplos_leyes_info/de_mi_hija"
    
    if not os.path.exists(base_path):
        print(f"❌ No se encontró la ruta: {base_path}")
        return
    
    print("🔍 Escaneando materiales de academia...")
    print(f"📁 Ruta base: {base_path}\n")
    
    scanner = MaterialesScanner(base_path)
    scanner.scan_directory(base_path)
    
    print("\n📊 Generando reporte...")
    report = scanner.generate_report()
    
    # Generar archivos de salida
    output_md = "INVENTARIO_MATERIALES_ACADEMIA_COMPLETO.md"
    output_json = "inventario_materiales_academia.json"
    
    scanner.generate_markdown_report(report, output_md)
    scanner.export_json(report, output_json)
    
    # Mostrar resumen en consola
    print("\n" + "="*60)
    print("📊 RESUMEN DEL ESCANEO")
    print("="*60)
    print(f"Total PDFs encontrados: {report['total_pdfs']}")
    print(f"Tamaño total: {report['total_size_mb']:.2f} MB\n")
    
    print("Distribución por categoría:")
    for category, data in sorted(report['categories'].items(), 
                                 key=lambda x: x[1]['count'], 
                                 reverse=True):
        print(f"  - {category.replace('_', ' ').title()}: {data['count']} archivos")
    
    print("\n✅ Escaneo completado!")
    print(f"📄 Revisa el archivo: {output_md}")

if __name__ == "__main__":
    main()
