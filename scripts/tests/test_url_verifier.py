#!/usr/bin/env python3
"""
Test rápido del verificador de URLs
"""

import json
import sys
sys.path.insert(0, 'dataset_generator')

from url_verifier import URLVerifier

# Datos de prueba con URLs reales de Mistral y Claude
test_data = [
    {
        "id": "TEST_001",
        "pregunta": "¿Cuál es la edad de jubilación según art. 205 LGSS?",
        "respuesta": "67 años o 65 con 38.5 años cotizados según art. 205 LGSS",
        "fuentes": [
            "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
            "https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/10963/28393",
            "https://www.inss.es/prestaciones/pension-de-jubilacion"
        ],
        "confidence": 0.95,
        "risk_level": "high"
    },
    {
        "id": "TEST_002",
        "pregunta": "¿Qué es la base reguladora?",
        "respuesta": "Es la base de cálculo para prestaciones de Seguridad Social",
        "fuentes": [
            "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724&p=20230328&tn=1#a205"
        ],
        "confidence": 0.90,
        "risk_level": "medium"
    }
]

# Guardar datos de prueba
with open('test_dataset.jsonl', 'w', encoding='utf-8') as f:
    for item in test_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print("🧪 PROBANDO VERIFICADOR DE URLs\n")
print("="*60)

# Crear verificador
verifier = URLVerifier(timeout=10, max_retries=2)

# Verificar dataset
result = verifier.verify_dataset('test_dataset.jsonl', 'test_dataset_verified.jsonl')

print("\n" + "="*60)
print("✅ PRUEBA COMPLETADA\n")

# Mostrar resultados
print("📄 Resultados guardados en: test_dataset_verified.jsonl\n")

# Leer y mostrar Q&A verificadas
with open('test_dataset_verified.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        qa = json.loads(line)
        print(f"\n{'='*60}")
        print(f"ID: {qa['id']}")
        print(f"Pregunta: {qa['pregunta']}")
        print(f"Confianza original: {qa.get('confidence', 'N/A')}")
        
        if 'url_verification' in qa:
            verif = qa['url_verification']
            print(f"\n🔗 Verificación URLs:")
            print(f"   URLs encontradas: {verif['urls_found']}")
            print(f"   URLs válidas: {verif['urls_valid']}")
            print(f"   URLs inválidas: {verif['urls_invalid']}")
            print(f"   Estado: {verif['verification_status']}")
            print(f"   Penalización: {verif['confidence_penalty']:.2f}")
            
            if 'confidence' in qa:
                print(f"   Confianza ajustada: {qa['confidence']:.2f}")
            
            print(f"\n   Detalles:")
            for detail in verif['details']:
                status = "✅" if detail['valid'] else "❌"
                trusted = "🔒" if detail['trusted'] else ""
                print(f"   {status} {trusted} {detail['url']}")
                if detail['error']:
                    print(f"      Error: {detail['error']}")

print(f"\n{'='*60}")
print("\n💡 INTERPRETACIÓN:")
print("✅ = URL válida (HTTP 200)")
print("❌ = URL inválida (404, timeout, error)")
print("🔒 = Dominio confiable (BOE, Seg-Social, etc.)")
print("\n")
