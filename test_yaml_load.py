#!/usr/bin/env python3
"""
Script de prueba para verificar la carga del YAML de Salamandra
"""
import yaml
from pathlib import Path
import json

config_path = Path("backend/config/prompts/salamandra.yaml")

print(f"📂 Cargando: {config_path}")
print(f"   Existe: {config_path.exists()}")
print()

with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

print("🔍 Estructura del YAML cargado:")
print(f"   Tipo: {type(config)}")
print(f"   Claves raíz: {list(config.keys())}")
print()

if 'prompts' in config:
    prompts = config['prompts']
    print("✅ Clave 'prompts' encontrada")
    print(f"   Tipo: {type(prompts)}")
    print(f"   Claves: {list(prompts.keys())}")
    print()
    
    if 'generate_case' in prompts:
        generate_case = prompts['generate_case']
        print("✅ Clave 'generate_case' encontrada")
        print(f"   Tipo: {type(generate_case)}")
        print(f"   Claves: {list(generate_case.keys()) if isinstance(generate_case, dict) else 'NO ES DICT'}")
        print()
        
        if isinstance(generate_case, dict):
            if 'system' in generate_case:
                print(f"✅ 'system' prompt: {generate_case['system'][:100]}...")
            if 'user' in generate_case:
                print(f"✅ 'user' prompt: {generate_case['user'][:100]}...")
        else:
            print(f"❌ ERROR: 'generate_case' NO es un diccionario")
            print(f"   Valor: {generate_case}")
    else:
        print("❌ Clave 'generate_case' NO encontrada")
else:
    print("❌ Clave 'prompts' NO encontrada")
