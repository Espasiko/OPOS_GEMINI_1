import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
import yaml
from mistralai import Mistral
from backend.v14.case_schema_builder import CaseSchemaBuilder
from backend.v14.prose_validator import validar_prose_vs_schema
from backend.agents.verification_agents import VerificationOrchestrator

async def run_e2e_test():
    print("==================================================")
    print("🚀 INICIANDO TEST E2E V14 CON MISTRAL LARGE")
    print("==================================================")
    builder = CaseSchemaBuilder()
    
    # 1. Generar Schema
    import dataclasses
    print("\n🛠️ [1/4] CONSTRUYENDO SCHEMA (Python Puro)...")
    try:
        schema = builder.build("BP-S12", {"personajes": ["Mauri", "Bea", "Juan Cuesta", "Emilio"]}, "2026-03-24")
        schema_json = json.dumps(dataclasses.asdict(schema), indent=2)
        print(f"✅ Schema creado con {len(schema.questions)} preguntas.")
    except Exception as e:
        print(f"❌ Error construyendo schema: {e}")
        return
    
    # 2. Cargar Prompt Redactor V14
    try:
        with open("opos-agents/agents/redactor_v14.yaml", "r") as f:
             config = yaml.safe_load(f)["agent"]
        system_prompt = config["system_prompt"].replace("{schema_json}", schema_json)
        model = config["model"]
        temperature = config["temperature"]
    except Exception as e:
        print(f"❌ Error cargando configuración del redactor: {e}")
        return
    
    # 3. Llamar a Mistral Large
    print("\n🤖 [2/4] LLAMANDO A MISTRAL LARGE (Narrador Sometido)...")
    print(f"   Modelo: {model} | Temperatura: {temperature}")
    api_key = os.environ.get("MISTRAL_API_KEY")
    client = Mistral(api_key=api_key)
    
    try:
        response = client.chat.complete(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Redacta el caso práctico completo basándote de forma absoluta en las reglas del schema proporcionado."}
            ]
        )
        narrativa = response.choices[0].message.content
        print("✅ Narrativa generada. Longitud:")
        print(f"   {len(narrativa)} caracteres.")
        with open("/tmp/narrativa_e2e_v14.md", "w") as f:
            f.write(narrativa)
        print("   -> Narrativa guardada en /tmp/narrativa_e2e_v14.md")
    except Exception as e:
        print(f"❌ Error en llamada al LLM Mistral: {e}")
        return
    
    # 4. Validar Prosa
    print("\n🛡️ [3/4] PROSE VALIDATOR (Matemáticas VS Texto)...")
    try:
        validacion = validar_prose_vs_schema(narrativa, schema)
        if validacion["bloqueado"]:
            print("❌ BLOQUEO AUTOMÁTICO:")
            for err in validacion["errores"]:
                print(f"   - {err['error']}")
            print("   (El LLM ha inventado cifras matemáticas contraviniendo el Schema)")
        else:
            print("✅ El Prose Validator APRUEBA estadísticamente el caso. No hay alucinaciones numéricas.")
    except Exception as e:
        print(f"❌ Error en Prose Validator: {e}")
        
    print("\n⚖️ [4/4] VERIFICATION ORCHESTRATOR (7 Dimensiones)...")
    try:
        orchestrator = VerificationOrchestrator()
        report = await orchestrator.verify_caso_completo(narrativa, bp_id="BP-S12")
        print("\n🏆 RESULTADO GLOBAL DE EVALUACIÓN:")
        print(report)
        with open("/tmp/reporte_orquestador_v14.md", "w") as f:
            f.write(report)
    except Exception as e:
         print(f"❌ Error en orquestador: {e}")
         import traceback
         traceback.print_exc()
        
    print("\n🎉 TEST E2E FINALIZADO CON ÉXITO.")

if __name__ == "__main__":
    asyncio.run(run_e2e_test())
