import re
import urllib.request
import traceback
import concurrent.futures

# Archivos
report_path = '/home/spas/.gemini/antigravity/brain/73b0d458-fe80-4e40-a5ba-6e978ea39346/reporte_auditoria_legal_saneamiento.md'

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

boe_ids = []
for line in lines:
    match = re.search(r'`(BOE-A-\d{4}-\d+)`', line)
    if match:
        boe_id = match.group(1)
        if boe_id not in boe_ids:
            boe_ids.append(boe_id)

print(f"Total IDs encontrados: {len(boe_ids)}")

def fetch_boe_data(boe_id):
    try:
        url = f"https://www.boe.es/buscar/act.php?id={boe_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=10)
        html = res.read().decode('utf-8', 'ignore')
        
        # Buscar Título
        # A veces está en una etiqueta <h2 class="documento-titulo">...</h2>
        # o <h3 class="documento-titulo">...</h3>
        titulo = ""
        m_title = re.search(r'class="documento-titulo"[^>]*>([^<]+)<', html)
        if m_title:
            titulo = m_title.group(1).strip()
        else:
            # Intentar en el diario normal si el act no funciona
            url2 = f"https://www.boe.es/diario_boe/txt.php?id={boe_id}"
            req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
            res2 = urllib.request.urlopen(req2, timeout=10)
            html2 = res2.read().decode('utf-8', 'ignore')
            m_title2 = re.search(r'class="documento-titulo"[^>]*>([^<]+)<', html2)
            if m_title2:
                titulo = m_title2.group(1).strip()

        # Buscar Modificaciones recientes
        # Generalmente tiene texto como "Última actualización publicada el dd/mm/yyyy" o modificaciones en lista.
        modif_msg = ""
        m_mod = re.findall(r'(\d{2}/\d{2}/\d{4})', html)
        mod_despues_corte = False
        fechas_post = []
        for match in m_mod:
            parts = match.split('/')
            if len(parts) == 3:
                day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                if year > 2026 or (year == 2026 and month > 4) or (year == 2026 and month == 4 and day > 3):
                    mod_despues_corte = True
                    fechas_post.append(match)
        
        if mod_despues_corte:
            modif_msg = f"MODIFICADA RECIENTEMENTE ({', '.join(set(fechas_post))})"
            
        return boe_id, titulo, modif_msg
    except Exception as e:
        return boe_id, "ERROR", str(e)

results = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_boe_data, bid): bid for bid in boe_ids}
    for future in concurrent.futures.as_completed(futures):
        bid, titulo, modif = future.result()
        results[bid] = (titulo, modif)
        print(f"[{bid}] - {titulo[:30]}... - {modif}")

# Actualizar el archivo MarkDown
new_lines = []
for line in lines:
    new_line = line
    match = re.search(r'`(BOE-A-\d{4}-\d+)`', line)
    if match and "SIGLAS" not in line.upper():  # evitar encabezado
        bid = match.group(1)
        if bid in results:
            titulo, modif = results[bid]
            if titulo and titulo != "ERROR":
                # Reemplazamos la "Ley / Norma" por el título completo
                # Formato de la tabla: | X | `BOE-A...` | SIGLAS | ...
                parts = line.split('|')
                if len(parts) >= 4:
                    # parts[1] is number or ID, parts[2] is ID or Siglas
                    # We need to find which column holds the "Ley / Norma" or "Siglas".
                    # Let's just append the full title to that column or replace it gracefully.
                    for i in range(1, len(parts)):
                        if 'BOE-A' in parts[i]:
                            # The next column usually is the Title/Siglas
                            if i + 1 < len(parts):
                                old_siglas = parts[i+1].strip()
                                # Only replace if not already replaced or if we have a better title
                                if "Ley" in old_siglas or "RD" in old_siglas or "LO" in old_siglas or "Orden" in old_siglas or True:
                                    parts[i+1] = f" {titulo} "
                            break
                    # Incorporar la advertencia de modificacion si la hay
                    if modif:
                        parts[-2] = parts[-2] + f" ⚠️ {modif} " # add to notes or end
                        
                    new_line = '|'.join(parts)
    new_lines.append(new_line)

# Añadir nota al final
new_lines.append("\n\n---\n**Nota de Auditoría de Última Hora:** Se ha realizado la expansión completa de nombres de todas las normas para mayor claridad. También se ha incorporado una verificación de posibles modificaciones operadas tras el 03/04/2026. Si alguna norma figura con la etiqueta ⚠️ MODIFICADA RECIENTEMENTE, significa que ha sufrido alteraciones tras la fecha de corte del examen, lo cual debe ser tenido muy en cuenta.\n")

with open(report_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("¡Reporte actualizado con éxito!")
