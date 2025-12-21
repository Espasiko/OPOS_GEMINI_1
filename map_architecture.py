
import os
import datetime
import pathlib
import json

ROOT = pathlib.Path("/home/spas/OPOS_GEMINI_1")

# Descriptions for known folders
DESCRIPTIONS = {
    "conceptual_materials": "📂 **Textos Base**: Contiene PDFs y textos jurídicos extraídos con OCR (Tesseract) para ser indexados.",
    "extracted_texts": "📂 **Staging Area**: Zona temporal donde se guardan los textos procesados antes de ir a Base de Datos (JSONs, TXTs).",
    "golden_dataset": "🏆 **Ground Truth**: Preguntas y respuestas verificadas manualmente (Dataset Oro) para evaluación de modelos.",
    "dataset_generator": "⚙️ **Motor de IA**: Scripts Python para generar preguntas (QA) y casos prácticos. Aquí viven los scripts de Mistral, DeepSeek y Groq.",
    "backend": "🧠 **API Server**: Núcleo FastAPI que conecta con Qdrant (RAG) y PostgreSQL. Maneja usuarios, autenticación y búsquedas.",
    "frontend": "🎨 **UI Web**: Interfaz de usuario React/Next.js para opositores (Tests, Temario, Chat con IA).",
    "mcp-server": "🔌 **MCP Gateway**: Servidor de Protocolo de Contexto de Modelo para conectar Claude Desktop con nuestras herramientas locales.",
    "scripts": "🛠️ **Utilidades**: Scripts de mantenimiento (backups, limpieza, migraciones).",
    "scripts_20_12": "📜 **Legado (Dec 20)**: Scripts de generación específicos de la fase 'Multi-Modelo' (Mistral Agent SDK v1).",
    "docs": "📚 **Documentación**: Informes técnicos, memorias, y guías de desarrollo (.md).",
    "basura": "🗑️ **Papelera**: Archivos temporales o fallidos (ya eliminada).",
    ".github": "🤖 **CI/CD**: Workflows de GitHub Actions (tests, linting).",
    "node_modules": "📦 **Librerías Node**: Dependencias instaladas (ignoradas en git)."
}

def analyze_folder(path):
    info = []
    
    # Check for Dependencies
    if (path / "requirements.txt").exists():
        info.append("🐍 Python Env (requirements.txt)")
    if (path / "package.json").exists():
        info.append("📦 Node Env (package.json)")
    if (path / "Dockerfile").exists():
        info.append("🐳 Dockerized")
        
    # Count specific files
    py_count = len(list(path.glob("*.py")))
    js_count = len(list(path.glob("*.ts"))) + len(list(path.glob("*.tsx"))) + len(list(path.glob("*.js")))
    pdf_count = len(list(path.glob("*.pdf")))
    json_count = len(list(path.glob("*.json")))
    
    if py_count > 0: info.append(f"{py_count} Python scripts")
    if js_count > 0: info.append(f"{js_count} JS/TS files")
    if pdf_count > 0: info.append(f"{pdf_count} PDFs")
    if json_count > 0: info.append(f"{json_count} JSON datasets")
    
    return ", ".join(info)

def main():
    date_str = datetime.datetime.now().strftime("%d_%m_%y")
    filename = f"{date_str}_mapa_arquitectura_completo.md"
    
    report = f"# Mapa Arquitectónico del Proyecto OPOSITAIA ({date_str})\n\n"
    report += "Este documento detalla la estructura física del repositorio, explicando la función de cada carpeta principal y su contenido.\n\n"
    
    # List top-level folders
    dirs = sorted([d for d in ROOT.iterdir() if d.is_dir() and not d.name.startswith(".")])
    
    for d in dirs:
        desc = DESCRIPTIONS.get(d.name, "📂 Carpeta del Proyecto")
        analysis = analyze_folder(d)
        
        report += f"## {d.name}\n"
        report += f"{desc}\n\n"
        if analysis:
            report += f"> **Contenido Detectado:** {analysis}\n"
        
        # Sub-level Check (Depth 2)
        subdirs = sorted([sd for sd in d.iterdir() if sd.is_dir() and not sd.name.startswith(".") and sd.name != "node_modules" and sd.name != "__pycache__"])
        if subdirs:
            report += "\n**Subcarpetas Clave:**\n"
            for sd in subdirs:
                sub_analysis = analyze_folder(sd)
                report += f"*   `{sd.name}/`: {sub_analysis}\n"
        
        report += "\n---\n"

    report += "\n## Archivos en Raíz\n"
    report += "*   `.env`: Configuración global de entorno y secretos.\n"
    report += "*   `docker-compose.yml`: Orquestador de servicios (Postgres + Qdrant).\n"
    report += "*   `pnpm-lock.yaml`: Gestor de dependencias global (Monorepo).\n"

    with open(filename, "w") as f:
        f.write(report)
        
    print(f"Generated: {filename}")

if __name__ == "__main__":
    main()
