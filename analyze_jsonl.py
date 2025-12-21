
import json
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

ROOT = Path("/home/spas/OPOS_GEMINI_1")

def analyze_jsonl(file_path):
    count = 0
    sample_topic = "Unknown"
    has_explanation = False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = True
            for line in f:
                if not line.strip(): continue
                count += 1
                if first_line:
                    try:
                        data = json.loads(line)
                        # Detect schema
                        if "temas" in data: sample_topic = data["temas"][:50]
                        elif "tema" in data: sample_topic = data["tema"][:50]
                        elif "topic" in data: sample_topic = data["topic"][:50]
                        
                        if "explicacion" in data or "explanation" in data:
                            has_explanation = True
                            
                        first_line = False
                    except:
                        pass
                        
        return count, sample_topic, has_explanation
    except Exception as e:
        return -1, str(e), False

def main():
    date_str = datetime.now().strftime("%d_%m_%y")
    filename = f"{date_str}_inventario_jsonl.md"
    
    # 1. Find Files
    files = sorted(ROOT.rglob("*.jsonl"))
    
    report = f"# Inventario de Datasets JSONL ({date_str})\n\n"
    report += "| Archivo | Cantidad | Tema Muestra | ¿Tiene Explicación? |\n"
    report += "|---------|----------|--------------|---------------------|\n"
    
    total_items = 0
    
    for f in files:
        # Ignore site-packages or node_modules if find missed them
        if "node_modules" in str(f) or "site-packages" in str(f): continue
        if ".venv" in str(f): continue
        
        rel_path = f.relative_to(ROOT)
        count, topic, explanation = analyze_jsonl(f)
        
        if count == -1:
            report += f"| `{rel_path}` | ❌ Error | {topic} | - |\n"
        else:
            report += f"| `{rel_path}` | **{count}** | {topic} | {'✅' if explanation else '❌'} |\n"
            total_items += count

    report += f"\n**Total Global de Items Detectados:** {total_items}\n"

    with open(filename, "w") as f:
        f.write(report)
        
    print(f"Generated Inventory: {filename}")

if __name__ == "__main__":
    main()
