
import json
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

ROOT = Path("/home/spas/OPOS_GEMINI_1")
OUTPUT_FILE = ROOT / "golden_dataset" / "consolidated" / "FINAL_TRAINING_DATASET_20251221.jsonl"

# 1. SOURCES CONFIGURATION
# We define exactly what goes in.



JSONL_SOURCES = [
    ROOT / "golden_dataset/premium/ALL_PREMIUM_100.jsonl",
    ROOT / "conceptual_materials/qa_generated/conceptual_qa_FINAL.jsonl",
    ROOT / "conceptual_materials/qa_generated/conceptual_qa_IMPROVED.jsonl",
    ROOT / "golden_dataset/official_exams_qa_FINAL.jsonl",
    ROOT / "golden_dataset/premium/premium_qa_batch3_20251219_124449.jsonl",
    ROOT / "golden_dataset/premium/premium_qa_gemini_20251219_122633.jsonl",
    ROOT / "dataset_generator/dataset_output_CLEAN/file_01kcxxfda7e9c8rmdrm4wjj75w.jsonl"
]

CASE_JSON_DIRS = [
    ROOT / "dataset_generator/premium_content/deepseek_extreme",
    ROOT / "dataset_generator/premium_content/mistral_extreme",
    ROOT / "dataset_generator/premium_content/groq_extreme"
]

def make_finetune_entry(instruction, input_text, output_text, source="unknown", quality="high"):
    """
    Standardizes the entry format for Finetuning (Alpaca/ShareGPT style).
    Adjust schema as needed for Nemotron. Here we use a generic Instruct format.
    """
    return {
        "instruction": instruction,
        "input": input_text,
        "output": output_text,
        "meta": {
            "source": str(source),
            "quality": quality,
            "timestamp": datetime.now().isoformat()
        }
    }

def process_case_json(file_path):
    """
    Converts a CASE STUDY JSON (scenario + 15 questions) into individual Q&A training samples.
    """
    try:
        data = json.loads(file_path.read_text())
        entries = []
        scenario = data.get("scenario", "")
        
        for q in data.get("questions", []):
            # Input: Scenario + Question + Options
            q_text = f"Escenario: {scenario}\n\nPregunta: {q.get('question_text')}\n"
            for opt in q.get("options", []):
                q_text += f"- {opt}\n"
            
            # Output: Correct Answer + Explanation (Chain of Thought)
            correct_opt = q.get("correct_option_id")
            explanation = q.get("explanation", "Sin explicación.")
            output_text = f"Respuesta Correcta: {correct_opt}\n\nRazonamiento: {explanation}"
            
            entries.append(make_finetune_entry(
                instruction="Resuelve el siguiente caso práctico jurídico razonando la respuesta.",
                input_text=q_text,
                output_text=output_text,
                source=file_path.name,
                quality="premium_case"
            ))
        return entries
    except Exception as e:
        logger.error(f"Error processing case {file_path.name}: {e}")
        return []

def extract_qa_from_item(item):
    """
    Helper to extract QA data from various formats (Direct, Groq Batch, etc.)
    """
    # 1. Try Groq Batch API Format
    if "response" in item and "body" in item["response"]:
        try:
            choices = item["response"]["body"]["choices"]
            content_str = choices[0]["message"]["content"]
            # Clean possible markdown wrapping
            if content_str.startswith("```json"):
                content_str = content_str.replace("```json", "").replace("```", "")
            return json.loads(content_str)
        except:
            pass # Failed to parse inner JSON
            
    # 2. Return item directly (Standard JSONL)
    return item

def main():
    logger.info("Starting FINAL Consolidation...")
    total_entries = 0
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        
        # 1. Process JSONL Sources (Standard QA)
        for src in JSONL_SOURCES:
            if not src.exists():
                logger.warning(f"Skipping missing source: {src}")
                continue
                
            logger.info(f"Processing JSONL: {src.name}")
            with open(src, "r") as f:
                for line in f:
                    try:
                        raw_item = json.loads(line)
                        item = extract_qa_from_item(raw_item)
                        
                        # Adapt existing items to Schema if needed
                        # Assuming they map roughly to instruction/output or QA
                        instruction = item.get("pregunta", item.get("instruction", ""))
                        if not instruction: continue # Skip empty or failed parses
                        
                        entry = make_finetune_entry(
                             instruction=instruction,
                             input_text="", # Simple QA usually has no context
                             output_text=item.get("respuesta", item.get("output", "Ver explicación.")), # Some might use 'respuesta_correcta' + 'explicacion'
                             source=src.name,
                             quality="golden_qa"
                        )
                        # Enrich output if we have separate fields
                        if "respuesta_correcta" in item and "explicacion" in item:
                             entry["output"] = f"Respuesta Correcta: {item['respuesta_correcta']}\n\nRazonamiento: {item['explicacion']}"

                        out_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                        total_entries += 1
                    except Exception as e:
                        # logger.warning(f"Skipping line in {src.name}: {e}")
                        pass

        # 2. Process High-Value CASE Studies (JSONs)
        for folder in CASE_JSON_DIRS:
            if not folder.exists(): continue
            logger.info(f"Processing Cases in: {folder.name}")
            
            for case_file in sorted(folder.glob("*.json")):
                entries = process_case_json(case_file)
                for entry in entries:
                    out_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    total_entries += 1
                    
    logger.info(f"DONE. Total Training Samples: {total_entries}")
    logger.info(f"Output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
