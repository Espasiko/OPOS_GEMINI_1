import os
import json
from neo4j import GraphDatabase
import datetime
import random

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "opositaia2026")

WIKI_DIR = "/mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/wiki"
OUTPUT_FILE = os.path.join(WIKI_DIR, "_INDICE_EXCEPCIONES.md")
JSON_OUTPUT_FILE = "/home/spas/OPOS_GEMINI_1/backend/data/ground_truth_excepciones.json"

def generar_indice_y_gt():
    print("Conectando a Neo4j para generar Wiki y Ground Truth...")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    try:
        with driver.session() as session:
            # Query all exceptions
            print("Extrayendo relaciones EXCEPCION_A de Neo4j...")
            result = session.run("""
            MATCH (o:Precepto)-[r:EXCEPCION_A]->(d:Precepto)
            MATCH (o)-[:PERTENECE_A]->(l_o:Ley)
            MATCH (d)-[:PERTENECE_A]->(l_d:Ley)
            RETURN 
                o.numero AS origen_num, 
                l_o.siglas AS origen_ley, 
                d.numero AS destino_num, 
                l_d.siglas AS destino_ley, 
                r.tipo AS tipo, 
                r.senal AS senal, 
                r.descripcion AS descripcion, 
                r.relevancia_examen AS relevancia
            ORDER BY l_o.siglas, o.numero
            """)
            
            records = [dict(rec) for rec in result]
            print(f"Total relaciones extraídas: {len(records)}")
            
            if len(records) == 0:
                print("No se encontraron relaciones para exportar.")
                return

            # Write Markdown
            print(f"Generando {OUTPUT_FILE}...")
            os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(f"# Índice Maestro de Excepciones Legales\n\n")
                f.write(f"> **Última actualización:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"> **Total excepciones verificadas:** {len(records)}\n\n")
                f.write("Este índice consolida todas las excepciones jurídicas verificadas manualmente y etiquetadas en la base de datos Neo4j de OpositAIA.\n\n")
                
                f.write("## Tabla Maestra\n\n")
                f.write("| Origen (Ley/Art) | Destino (Excepciona a) | Tipo | Relevancia | Señal Textual | Descripción |\n")
                f.write("|---|---|---|---|---|---|\n")
                for rec in records:
                    origen = f"{rec['origen_ley']} - {rec['origen_num']}"
                    destino = f"{rec['destino_ley']} - {rec['destino_num']}"
                    descripcion = (rec['descripcion'] or "").replace("\n", " ").replace("|", "\\|")
                    senal = (rec['senal'] or "").replace("\n", " ").replace("|", "\\|")
                    f.write(f"| {origen} | {destino} | `{rec['tipo']}` | {rec['relevancia']} | \"{senal}\" | {descripcion} |\n")
                    
            print("Archivo Markdown generado correctamente.")

            # Generate Ground Truth Test Set
            print(f"Generando Ground Truth Test Set en {JSON_OUTPUT_FILE}...")
            random.seed(42) # For reproducibility
            
            # Select 20 examples distributed by type if possible
            tipos = list(set([r['tipo'] for r in records if r['tipo']]))
            ground_truth = []
            
            if tipos:
                per_type = max(1, 20 // len(tipos))
                for t in tipos:
                    type_records = [r for r in records if r['tipo'] == t]
                    sample_size = min(len(type_records), per_type)
                    ground_truth.extend(random.sample(type_records, sample_size))
            
            # Fill the rest randomly up to 20
            remaining = 20 - len(ground_truth)
            if remaining > 0:
                available = [r for r in records if r not in ground_truth]
                ground_truth.extend(random.sample(available, min(remaining, len(available))))
                
            os.makedirs(os.path.dirname(JSON_OUTPUT_FILE), exist_ok=True)
            with open(JSON_OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(ground_truth, f, ensure_ascii=False, indent=2)
                
            print(f"Ground Truth Test Set con {len(ground_truth)} casos generado correctamente.")
            
    finally:
        driver.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    generar_indice_y_gt()
