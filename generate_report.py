
import pathlib
import json

ROOT = pathlib.Path("/home/spas/OPOS_GEMINI_1")

def main():
    # 1. Load Data
    try:
        all_scripts = pathlib.Path("/tmp/all_scripts.txt").read_text().splitlines()
        success_logs = pathlib.Path("/tmp/success_logs.txt").read_text().splitlines()
        outputs = pathlib.Path("/tmp/outputs.txt").read_text().splitlines()
    except Exception as e:
        print(f"Error loading temp files: {e}")
        return

    # Helper Sets for O(1) lookup
    success_map = set()
    for log_file in success_logs:
        # If a log file indicates success, we try to associate it with a script
        # Heuristic: mistral_gen.log -> generate_cases_mistral.py
        name = pathlib.Path(log_file).name
        if "mistral" in name: success_map.add("generate_cases_mistral.py")
        if "deepseek" in name: success_map.add("generate_cases_deepseek.py")
        if "groq" in name: success_map.add("generate_cases_groq.py")

    report = []
    
    # Golden Scripts (Hardcoded based on recent memory)
    GOLDEN = {
        "generate_cases_mistral.py",
        "generate_cases_deepseek.py", 
        "generate_cases_groq.py",
        "backend/main.py",
        "backend/agents/rag_agent_v2.py"
    }

    for script_path in all_scripts:
        path_obj = pathlib.Path(script_path)
        name = path_obj.name
        rel_path = str(pathless_script := path_obj.relative_to("."))
        
        status = "UNKNOWN"
        reason = ""

        # Logic
        if "venv" in rel_path or "site-packages" in rel_path:
            continue # Skip venv files

        if name in GOLDEN:
            status = "ACTIVE (GOLD)"
            reason = "Core Generation Script"
        elif "archive" in rel_path:
            status = "LEGACY"
            reason = "Already in archive"
        elif "test" in name or "debug" in name:
            status = "TEST/DEBUG"
            reason = "Test file"
        elif name in success_map:
            status = "ACTIVE" 
            reason = "Associated with success logs"
        elif "agent" in name and "mistral" in name and name != "generate_cases_mistral.py":
             status = "LEGACY (Candidate)"
             reason = "Old Mistral iteration"
        else:
             status = "REVIEW NEEDED"
             reason = "No clear signal"

        report.append(f"| `{rel_path}` | {status} | {reason} |")

    # Generate Markdown
    with open("scripts_status.md", "w") as f:
        f.write("# Auditoría de Scripts del Proyecto\n\n")
        f.write("| Script | Estado | Razón |\n")
        f.write("|--------|--------|-------|\n")
        for line in sorted(report):
             f.write(line + "\n")

    print(f"Generated scripts_status.md with {len(report)} entries.")

if __name__ == "__main__":
    main()
