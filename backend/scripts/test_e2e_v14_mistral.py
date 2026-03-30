import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from dotenv import load_dotenv
load_dotenv()

import json
import yaml
from mistralai import Mistral
from backend.v14.case_schema_builder import CaseSchemaBuilder
from backend.v14.prose_validator import validar_prose_vs_schema
from backend.agents.verification_agents import VerificationOrchestrator

def run_e2e_test():
    import dataclasses
    print("==================================================")
    print("🚀 INICIANDO TEST E2E V14 CON MISTRAL LARGE")
    print("==================================================")
    builder = CaseSchemaBuilder()

    # 1. Generar Schema complejo (3 blueprints aleatorios, ~18 preguntas, personajes únicos)
    print("\n🛠️ [1/4] CONSTRUYENDO SCHEMA COMPLEJO (Python Puro)...")
    try:
        schema = builder.build_complex(fecha_caso="2026-03-24")
        schema_json = json.dumps(dataclasses.asdict(schema), indent=2, ensure_ascii=False)
        print(f"✅ Schema creado: {len(schema.questions)} preguntas | {len(schema.personajes)} personajes")
        print(f"   Blueprints: {schema.blueprint_ids}")
        print(f"   Personajes: {[p.nombre for p in schema.personajes]}")
    except Exception as e:
        print(f"❌ Error construyendo schema: {e}")
        import traceback; traceback.print_exc()
        return

    # 2. Cargar Prompt Redactor V14
    try:
        yaml_paths = [
            "opos-agents/agents/redactor_v14.yaml",
            "/home/spas/OPOS_GEMINI_1/opos-agents/agents/redactor_v14.yaml",
        ]
        config = None
        for p in yaml_paths:
            if os.path.exists(p):
                with open(p, "r") as f:
                    config = yaml.safe_load(f)["agent"]
                break
        if not config:
            raise FileNotFoundError("redactor_v14.yaml no encontrado")
        system_prompt = config["system_prompt"].replace("{schema_json}", schema_json)
        model = config["model"]
        temperature = config["temperature"]
    except Exception as e:
        print(f"❌ Error cargando configuración del redactor: {e}")
        return

    # 3. Llamar a Mistral Large
    print(f"\n🤖 [2/4] LLAMANDO A MISTRAL LARGE...")
    print(f"   Modelo: {model} | Temperatura: {temperature}")
    api_key = os.environ.get("MISTRAL_API_KEY")
    client = Mistral(api_key=api_key)

    try:
        response = client.chat.complete(
            model=model,
            temperature=temperature,
            max_tokens=config.get("max_tokens", 8000),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": (
                    "Redacta el caso práctico completo. RECUERDA: "
                    "un párrafo narrativo por personaje, luego sus preguntas numeradas. "
                    "Las preguntas deben referirse explícitamente al personaje correspondiente. "
                    "Usa los datos exactos del schema_json."
                )}
            ]
        )
        narrativa = response.choices[0].message.content
        print(f"✅ Narrativa generada: {len(narrativa)} caracteres.")
        with open("/tmp/narrativa_e2e_v14.md", "w") as f:
            f.write(narrativa)
        print("   → /tmp/narrativa_e2e_v14.md")
    except Exception as e:
        print(f"❌ Error en llamada al LLM Mistral: {e}")
        return

    # 4. Validar Prosa
    print("\n🛡️ [3/4] PROSE VALIDATOR (Matemáticas VS Texto)...")
    try:
        validacion = validar_prose_vs_schema(narrativa, schema)
        if validacion["bloqueado"]:
            print("❌ BLOQUEO AUTOMÁTICO — el LLM inventó cifras:")
            for err in validacion["errores"]:
                print(f"   - {err['error']}")
        else:
            print("✅ Prose Validator APRUEBA — sin alucinaciones numéricas.")
    except Exception as e:
        print(f"⚠️  Error en Prose Validator: {e}")

    # 5. Verification Orchestrator
    print("\n⚖️ [4/4] VERIFICATION ORCHESTRATOR...")
    try:
        orchestrator = VerificationOrchestrator()
        # Pasar preguntas para que agents 5, 7, 8 puedan evaluarlas
        questions_dicts = [dataclasses.asdict(q) for q in schema.questions]
        personajes_dicts = [dataclasses.asdict(p) for p in schema.personajes]
        caso_dict = {
            "narrativa": narrativa,
            "texto": narrativa,
            "schema": schema_json,
            "preguntas": questions_dicts,
            "personajes": personajes_dicts,
        }
        report = orchestrator.verify_caso_completo(caso_dict)
        print("\n🏆 RESULTADO GLOBAL DE EVALUACIÓN:")
        report_str = json.dumps(report, indent=2, ensure_ascii=False)
        print(report_str)
        with open("/tmp/reporte_orquestador_v14.md", "w") as f:
            f.write(report_str)
        print("   → /tmp/reporte_orquestador_v14.md")
    except Exception as e:
        print(f"❌ Error en orquestador: {e}")
        import traceback; traceback.print_exc()

    print("\n🎉 TEST E2E FINALIZADO.")

if __name__ == "__main__":
    run_e2e_test()
