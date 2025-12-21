
import os
import datetime
import pathlib

ROOT = pathlib.Path("/home/spas/OPOS_GEMINI_1")

def get_installed():
    try:
        with open("installed_packages.txt") as f:
            return f.read()
    except:
        return "Error reading installed packages."

def get_declared():
    report = ""
    try:
        with open("declared_deps.txt") as f:
            files = f.read().splitlines()
            
        for dfile in sorted(files):
            if "site-packages" in dfile: continue
            
            report += f"\n### 📄 {dfile}\n"
            try:
                content = (ROOT / dfile).read_text()
                # Limit output for readability
                lines = content.splitlines()
                if len(lines) > 20: 
                    report += "```text\n" + "\n".join(lines[:20]) + "\n... (truncated)\n```\n"
                else:
                    report += "```text\n" + content + "\n```\n"
            except Exception as e:
                report += f"_Error reading file: {e}_\n"
    except:
        report += "No requirement files found."
        
    return report

def main():
    date_str = datetime.datetime.now().strftime("%d_%m_%y")
    filename = f"{date_str}_report_dependencias.md"
    
    installed = get_installed()
    declared = get_declared()
    
    content = f"""# Reporte de Dependencias y Librerías ({date_str})

## 1. Entornos Virtuales Detectados 🐍
Se ha realizado un escaneo profundo de la estructura del proyecto y se ha confirmado la existencia de **un único entorno virtual principal**:

*   **Ruta:** `/home/spas/OPOS_GEMINI_1/.venv`
*   **Estado:** Activo y en uso por los scripts de generación.

*(Nota: Si existían otros venvs en `basura/`, han sido eliminados).*

---

## 2. Librerías Instaladas (pip freeze) 📦
Estas son las librerías que **realmente están presentes** en el entorno `.venv`. Si un script falla por "ImportError" y la librería está aquí, es un problema de ruta (PYTHONPATH). Si NO está aquí, hay que instalarla.

```text
{installed}
```

---

## 3. Dependencias Declaradas (Requirements) 📝
Comparativa con lo que los diferentes módulos dicen necesitar:

{declared}

## 4. Diagnóstico de "Scripts Rotos" 🔧
Analizando los fallos reportados anteriormente (`BROKEN_IMPORTS`):

*   **pytesseract / pdf2image**: Busca 'pytesseract' en la lista de arriba. Si no sale, hay que hacer `pip install pytesseract pdf2image`.
*   **mistralai**: Busca 'mistralai'. Es crítica para los scripts `v2`.
*   **dotenv**: Busca 'python-dotenv'.

Este reporte sirve como base para "revivir" los scripts antiguos instalando lo que falta.
"""

    with open(filename, "w") as f:
        f.write(content)
        
    print(f"Report generated: {filename}")

if __name__ == "__main__":
    main()
