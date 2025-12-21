
import json
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

PREMIUM_DIR = Path("dataset_generator/premium_content")

def validate_file(file_path):
    try:
        data = json.loads(file_path.read_text())
        
        # Check Basic Structure
        if "scenario" not in data:
            return False, "Missing 'scenario' field"
        if "questions" not in data:
            return False, "Missing 'questions' field"
            
        questions = data["questions"]
        if not isinstance(questions, list):
             return False, "'questions' is not a list"
             
        # Check Question Quality
        if len(questions) < 12:
            return False, f"Insufficient questions ({len(questions)} < 12)"
            
        for q in questions:
            if "options" not in q or len(q["options"]) != 4:
                return False, f"Question {q.get('id')} has invalid options"
            if "correct_option_id" not in q:
                return False, f"Question {q.get('id')} missing correct answer"
                
        return True, f"Valid ({len(questions)} Qs)"
        
    except json.JSONDecodeError:
        return False, "Invalid JSON Syntax"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    logger.info("Starting Validation of Generated Cases...")
    
    stats = {"Valid": 0, "Invalid": 0, "Total": 0}
    
    # 1. DeepSeek
    logger.info("--- Checking DeepSeek ---")
    for f in sorted((PREMIUM_DIR / "deepseek_extreme").glob("*.json")):
        ok, msg = validate_file(f)
        logger.info(f"{f.name}: {msg}")
        stats["Total"] += 1
        if ok: stats["Valid"] += 1
        else: stats["Invalid"] += 1

    # 2. Mistral
    logger.info("--- Checking Mistral ---")
    for f in sorted((PREMIUM_DIR / "mistral_extreme").glob("*.json")):
        ok, msg = validate_file(f)
        logger.info(f"{f.name}: {msg}")
        stats["Total"] += 1
        if ok: stats["Valid"] += 1
        else: stats["Invalid"] += 1

    # 3. Groq
    logger.info("--- Checking Groq ---")
    for f in sorted((PREMIUM_DIR / "groq_extreme").glob("*.json")):
        ok, msg = validate_file(f)
        logger.info(f"{f.name}: {msg}")
        stats["Total"] += 1
        if ok: stats["Valid"] += 1
        else: stats["Invalid"] += 1
        
    logger.info(f"--- Summary: {stats} ---")
    
    if stats["Invalid"] == 0 and stats["Total"] >= 30:
        print("SUCCESS: All 30 cases passed validation.")
    else:
        print("WARNING: Some cases failed validation.")

if __name__ == "__main__":
    main()
