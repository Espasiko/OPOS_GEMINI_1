
import ast
import pathlib
import sys
import importlib.util

ROOT = pathlib.Path("/home/spas/OPOS_GEMINI_1")

def check_syntax(file_path):
    try:
        source = file_path.read_text()
        ast.parse(source)
        return True, "Syntax OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Read Error: {e}"

def check_imports_resolvable(file_path):
    """
    Rudimentary check to see if imports *could* work.
    Does NOT import the module, just parses AST for Import/ImportFrom nodes.
    """
    try:
        source = file_path.read_text()
        tree = ast.parse(source)
        
        missing = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if not importlib.util.find_spec(alias.name.split('.')[0]):
                         # Check if it's a local file
                         if not (file_path.parent / (alias.name.replace('.', '/') + '.py')).exists():
                             missing.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and not importlib.util.find_spec(node.module.split('.')[0]):
                     if not (file_path.parent / (node.module.replace('.', '/') + '.py')).exists():
                         missing.append(node.module)
        
        if missing:
            return False, f"Missing Imports: {', '.join(missing[:3])}..."
        return True, "Imports OK"
        
    except Exception as e:
        return False, f"Import Check Error: {e}"

def main():
    # Load targets from status v2
    try:
        with open("scripts_status_v2.md", "r") as f:
            lines = f.readlines()[4:]
    except FileNotFoundError:
        print("Error: scripts_status_v2.md not found.")
        return

    results = []

    for line in lines:
        if "|" not in line: continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 3: continue
        
        rel_path = parts[0].strip("`")
        status = parts[1]
        
        # Only check unproven scripts
        if "LEGACY" in status or "UTILITY" in status or "UNKNOWN" in status:
            path_obj = ROOT / rel_path
            
            if not path_obj.exists() or path_obj.suffix != ".py":
                continue

            syn_ok, syn_msg = check_syntax(path_obj)
            
            final_status = "VALID"
            final_msg = syn_msg
            
            if syn_ok:
                imp_ok, imp_msg = check_imports_resolvable(path_obj)
                if not imp_ok:
                    final_status = "BROKEN_IMPORTS"
                    final_msg = imp_msg
            else:
                 final_status = "BROKEN_SYNTAX"

            results.append(f"| `{rel_path}` | {final_status} | {final_msg} |")

    # Output Results
    with open("dry_run_results.md", "w") as f:
        f.write("# Validación 'Dry Run' (Sin Ejecución)\n\n")
        f.write("| Script | Estado Técnico | Detalle |\n")
        f.write("|--------|----------------|---------|\n")
        for r in sorted(results):
            f.write(r + "\n")
            
    print("Dry Run Complete. See dry_run_results.md")

if __name__ == "__main__":
    main()
