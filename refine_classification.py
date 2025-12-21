
import pathlib
import os

ROOT = pathlib.Path("/home/spas/OPOS_GEMINI_1")

def get_file_header(path, lines=5):
    try:
        content = path.read_text().splitlines()[:lines]
        return "\n".join(content)
    except:
        return ""

def main():
    # Load previous status
    with open("scripts_status.md", "r") as f:
        lines = f.readlines()[4:] # Skip header

    new_report = []
    
    for line in lines:
        if "|" not in line: continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 3: continue
        
        rel_path = parts[0].strip("`")
        status = parts[1]
        reason = parts[2]
        
        path_obj = ROOT / rel_path
        if not path_obj.exists(): continue

        # ACTION 1: Delete LEGACY
        if "LEGACY" in status:
            print(f"🗑️ Deleting: {rel_path}")
            os.remove(path_obj)
            continue
            
        # ACTION 2: Skip Maintenance / Protected
        if "maintenance" in rel_path or "backend/agents" in rel_path or "backend/main.py" in rel_path:
             new_report.append(f"| `{rel_path}` | ACTIVE | Protected System File |")
             continue

        # ACTION 3: Classify Review Needed
        if "REVIEW NEEDED" in status:
            header = get_file_header(path_obj)
            new_status = "UNKNOWN"
            new_reason = "No info"
            
            if "Django" in header or "manage.py" in str(path_obj):
                new_status = "LEGACY (Django)"
                new_reason = "Old framework"
            elif "test" in str(path_obj).lower() or "pytest" in header:
                new_status = "TEST"
                new_reason = "Test file"
            elif "setup" in str(path_obj) or "config" in str(path_obj):
                new_status = "CONFIG"
                new_reason = "Configuration"
            elif "generate" in str(path_obj) and "qa" in str(path_obj):
                new_status = "LEGACY (Old Gen)"
                new_reason = "Old Generation Script"
            else:
                new_status = "UTILITY" 
                new_reason = "Likely helper script"
            
            new_report.append(f"| `{rel_path}` | {new_status} | {new_reason} |")
        else:
            new_report.append(line.strip())

    # Write Updated Report
    with open("scripts_status_v2.md", "w") as f:
        f.write("# Auditoría de Scripts - Fase 2 (Refinado)\n\n")
        f.write("| Script | Estado | Razón |\n")
        f.write("|--------|--------|-------|\n")
        for line in sorted(new_report):
             f.write(line + "\n")
             
    print("Cleanup & Refinement Complete. Check scripts_status_v2.md")

if __name__ == "__main__":
    main()
