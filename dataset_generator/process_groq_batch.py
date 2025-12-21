
import json
import os
from datetime import datetime

input_file = "dataset_generator/groq_batch_500_results.jsonl"
output_file = "dataset_generator/multi_model_20_12/qa_groq_batch_500_final.jsonl"

def process_results():
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} no encontrado.")
        return

    processed_count = 0
    error_count = 0

    with open(input_file, "r", encoding="utf-8") as fin, \
         open(output_file, "w", encoding="utf-8") as fout:
        
        for line in fin:
            try:
                data = json.loads(line)
                # La respuesta de Groq está en response.body.choices[0].message.content
                content = data["response"]["body"]["choices"][0]["message"]["content"]
                
                # Intentar parsear el contenido como JSON
                # A veces viene envuelto en ```json
                clean_content = content.replace("```json", "").replace("```", "").strip()
                item = json.loads(clean_content)
                
                # Añadir metadatos
                item["model_provider"] = "groq_batch_llama_3.3_70b"
                item["timestamp"] = datetime.now().isoformat()
                
                fout.write(json.dumps(item, ensure_ascii=False) + "\n")
                processed_count += 1
            except Exception as e:
                error_count += 1
                # print(f"⚠️ Error procesando línea: {e}")

    print(f"✨ Procesamiento completado:")
    print(f"✅ Éxito: {processed_count}")
    print(f"❌ Errores: {error_count}")
    print(f"📁 Archivo final: {output_file}")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    process_results()
