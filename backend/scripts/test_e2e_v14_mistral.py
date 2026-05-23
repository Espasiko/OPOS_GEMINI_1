import sys
import os

# ── CWD guard: debe ejecutarse desde la raíz del proyecto ──────────────────────
_PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if os.getcwd() != _PROJ_ROOT:
    os.chdir(_PROJ_ROOT)
    print(f"ℹ️  CWD cambiado a: {_PROJ_ROOT}")
sys.path.insert(0, _PROJ_ROOT)

from dotenv import load_dotenv
load_dotenv()

import json
import yaml
from datetime import date
from mistralai import Mistral
from backend.v14.case_schema_builder import CaseSchemaBuilder
from backend.v14.prose_validator import validar_prose_vs_schema
from backend.agents.verification_agents import VerificationOrchestrator

def run_e2e_test():
    import dataclasses
    print("==================================================")
    print("🚀 INICIANDO TEST E2E V14 CON MISTRAL LARGE")
    print("==================================================")

    # ── Check MISTRAL_API_KEY antes de empezar ─────────────────────────────────
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("❌ MISTRAL_API_KEY no encontrada en .env ni en entorno. Abortando.")
        return

    builder = CaseSchemaBuilder()

    # 1. Generar Schema complejo (4 blueprints aleatorios, ~18 preguntas, personajes únicos)
    fecha_caso = date.today().strftime("%Y-%m-%d")
    print(f"\n🛠️ [1/4] CONSTRUYENDO SCHEMA COMPLEJO (Python Puro) — fecha_caso={fecha_caso}...")
    try:
        schema = builder.build_complex(fecha_caso=fecha_caso)
        schema_json = json.dumps(dataclasses.asdict(schema), indent=2, ensure_ascii=False)
        with open("/tmp/schema_e2e_v14.json", "w") as f:
            f.write(schema_json)
        print(f"✅ Schema creado: {len(schema.questions)} preguntas | {len(schema.personajes)} personajes")
        print(f"   Blueprints: {schema.blueprint_ids}")
        print(f"   Personajes: {[p.nombre for p in schema.personajes]}")
        print(f"   → /tmp/schema_e2e_v14.json")
        # ── Verificar que contexto_legal se pobló con texto BOE real ──────────
        n_contexto = len(schema.contexto_legal)
        if n_contexto <= 1:
            print(f"⚠️  contexto_legal solo tiene {n_contexto} entrada(s) — Neo4j puede NO estar devolviendo artículos.")
        else:
            chars_ley = sum(len(c) for c in schema.contexto_legal)
            print(f"✅ contexto_legal: {n_contexto} bloques, {chars_ley} chars de texto BOE real.")
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
        print(f"\n── INICIO NARRATIVA (primeros 600 chars) ──────────────────────")
        print(narrativa[:600])
        print("── FIN PREVIEW ────────────────────────────────────────────────")
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
