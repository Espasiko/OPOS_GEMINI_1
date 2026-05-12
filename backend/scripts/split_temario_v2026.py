
import re
import os

input_file = "/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/TEMARIO_DM_POR_TEMAS/TEMARIO_BLOQUE_ESPECIFICO_COMPLETO_ACTUALIZADO.txt"
output_dir = "/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/temario_troceado_v2026/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Patterns to match "TEMA 1", "TEMA 2", etc. at the start of a clear section
# Usually they are on a line by themselves or at the start of a line
tema_patterns = [f"TEMA {i}" for i in range(1, 14)]
tema_positions = []

for i, line in enumerate(lines):
    # Check if a line contains "TEMA X" exactly, likely as a header
    # We want the first occurrence of each theme as the split point
    for t_idx, pattern in enumerate(tema_patterns):
        if re.search(fr"^\s*{pattern}\s*$", line):
            # Only record the first time we see "TEMA X" (the main header)
            # though the grep showed multiple occurrences (likely page footers)
            # We filter for the transition points
            tema_positions.append((i, pattern))
            break

# Refine positions: we only want the transitions where the number increases
refined_positions = []
last_tema_num = 0
for pos, pat in tema_positions:
    tema_num = int(pat.split()[1])
    if tema_num == last_tema_num + 1:
        refined_positions.append((pos, pat))
        last_tema_num = tema_num

# Add the end of file as a boundary
refined_positions.append((len(lines), "EOF"))

# Actually write the files
for i in range(len(refined_positions) - 1):
    start_line = refined_positions[i][0]
    end_line = refined_positions[i+1][0]
    tema_name = refined_positions[i][1].replace(" ", "_").lower()
    
    file_path = os.path.join(output_dir, f"{tema_name}.md")
    with open(file_path, 'w', encoding='utf-8') as out:
        out.writelines(lines[start_line:end_line])
    print(f"Generado {file_path}")

print("Proceso completado.")
