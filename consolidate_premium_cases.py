
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

PREMIUM_DIR = Path("dataset_generator/premium_content")
ARCHIVE_DIR = Path("dataset_generator/archive")
OUTPUT_FILE = Path("golden_dataset/premium/30_casos_premium_consolidated_20251221.json")

def main():
    logger.info("Consolidating 30 Premium Cases...")
    
    consolidated = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_cases": 0,
            "models": {
                "mistral": 0,
                "deepseek": 0,
                "groq": 0
            }
        },
        "cases": []
    }
    
    # 1. DeepSeek
    for f in sorted((PREMIUM_DIR / "deepseek_extreme").glob("*.json")):
        try:
            case = json.loads(f.read_text())
            case["model_source"] = "deepseek-reasoner"
            case["difficulty"] = "EXTREME"
            consolidated["cases"].append(case)
            consolidated["metadata"]["models"]["deepseek"] += 1
        except Exception as e:
            logger.error(f"Error reading {f.name}: {e}")

    # 2. Mistral
    for f in sorted((PREMIUM_DIR / "mistral_extreme").glob("*.json")):
        try:
            case = json.loads(f.read_text())
            case["model_source"] = "mistral-large-agent"
            case["difficulty"] = "HIGH"
            consolidated["cases"].append(case)
            consolidated["metadata"]["models"]["mistral"] += 1
        except Exception as e:
            logger.error(f"Error reading {f.name}: {e}")

    # 3. Groq
    for f in sorted((PREMIUM_DIR / "groq_extreme").glob("*.json")):
        try:
            case = json.loads(f.read_text())
            case["model_source"] = "llama-3.3-70b"
            case["difficulty"] = "MEDIUM-HIGH"
            consolidated["cases"].append(case)
            consolidated["metadata"]["models"]["groq"] += 1
        except Exception as e:
            logger.error(f"Error reading {f.name}: {e}")
            
    # Counts
    total = len(consolidated["cases"])
    consolidated["metadata"]["total_cases"] = total
    
    # Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(consolidated, f, indent=2, ensure_ascii=False)
        
    logger.info(f"SUCCESS: Saved {total} cases to {OUTPUT_FILE}")
    logger.info(f"Breakdown: {consolidated['metadata']['models']}")

if __name__ == "__main__":
    main()
