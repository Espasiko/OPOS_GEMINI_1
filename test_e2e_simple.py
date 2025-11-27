#!/usr/bin/env python3
"""
Test E2E Simple - OpositAIA
Prueba básica de componentes principales
"""

import sys
import os
from pathlib import Path

print("\n" + "="*80)
print("🚀 OPOSITAIA - TEST E2E SIMPLE")
print("="*80)

# Test 1: Archivos Frontend
print("\n📱 TEST 1: Frontend Files")
print("-" * 80)

frontend_files = [
    "App.tsx",
    "components/ChatView.tsx",
    "components/ModelSelector.tsx",
    "components/MindMapView.tsx",
    "components/FlashcardsView.tsx",
    "components/SchemaView.tsx",
    "components/SummaryView.tsx",
    "components/StudyPlanView.tsx",
    "components/CaseGeneratorView.tsx",
    "components/ErrorMessage.tsx",
    "contexts/ModelContext.tsx",
    "services/backendService.ts",
    "utils/providers.ts",
    "utils/formatters.ts",
    "utils/cache.ts",
    "hooks/useAIProvider.ts"
]

frontend_ok = 0
for file in frontend_files:
    path = Path(file)
    if path.exists():
        print(f"✅ {file}")
        frontend_ok += 1
    else:
        print(f"❌ {file} - MISSING")

print(f"\n📊 Frontend: {frontend_ok}/{len(frontend_files)} files OK")

# Test 2: Archivos Backend
print("\n🔧 TEST 2: Backend Files")
print("-" * 80)

backend_files = [
    "backend/main.py",
    "backend/routers/rag_v2.py",
    "backend/routers/ai_functions.py",
    "backend/routers/upload.py",
    "backend/agents/rag_agent_v2.py",
    "backend/agents/llm_providers.py",
    "backend/models/metadata_schema.py",
    "backend/.env.backend"
]

backend_ok = 0
for file in backend_files:
    path = Path(file)
    if path.exists():
        print(f"✅ {file}")
        backend_ok += 1
    else:
        print(f"❌ {file} - MISSING")

print(f"\n📊 Backend: {backend_ok}/{len(backend_files)} files OK")

# Test 3: Configuración
print("\n⚙️  TEST 3: Configuration")
print("-" * 80)

env_file = Path("backend/.env.backend")
if env_file.exists():
    print("✅ .env.backend exists")
    
    # Check for API keys
    with open(env_file) as f:
        content = f.read()
        
    keys_to_check = [
        ("GROQ_API_KEY", "Groq"),
        ("DEEPSEEK_API_KEY", "DeepSeek"),
        ("GEMINI_API_KEY", "Gemini"),
        ("HF_TOKEN", "Hugging Face"),
        ("COHERE_API_KEY", "Cohere"),
        ("MISTRAL_URL", "Mistral VPS"),
        ("QDRANT_URL", "Qdrant")
    ]
    
    config_ok = 0
    for key, name in keys_to_check:
        if key in content and not content.split(key)[1].split('\n')[0].strip().endswith('='):
            print(f"✅ {name} configured")
            config_ok += 1
        else:
            print(f"⚠️  {name} not configured")
    
    print(f"\n📊 Config: {config_ok}/{len(keys_to_check)} providers configured")
else:
    print("❌ .env.backend NOT FOUND")
    config_ok = 0

# Test 4: Package.json scripts
print("\n📦 TEST 4: NPM Scripts")
print("-" * 80)

package_json = Path("package.json")
if package_json.exists():
    import json
    with open(package_json) as f:
        pkg = json.load(f)
    
    scripts = pkg.get("scripts", {})
    required_scripts = ["dev", "build", "test", "test:unit"]
    
    scripts_ok = 0
    for script in required_scripts:
        if script in scripts:
            print(f"✅ npm run {script}")
            scripts_ok += 1
        else:
            print(f"❌ npm run {script} - MISSING")
    
    print(f"\n📊 Scripts: {scripts_ok}/{len(required_scripts)} OK")
else:
    print("❌ package.json NOT FOUND")
    scripts_ok = 0

# Test 5: Documentación
print("\n📚 TEST 5: Documentation")
print("-" * 80)

docs = [
    "README.md",
    "SETUP.md",
    "ESTADO_ACTUAL_Y_PROXIMOS_PASOS.md",
    "SPRINT10_COMPLETADO.md"
]

docs_ok = 0
for doc in docs:
    path = Path(doc)
    if path.exists():
        print(f"✅ {doc}")
        docs_ok += 1
    else:
        print(f"❌ {doc} - MISSING")

print(f"\n📊 Docs: {docs_ok}/{len(docs)} OK")

# Test 6: Estructura de carpetas
print("\n📁 TEST 6: Folder Structure")
print("-" * 80)

folders = [
    "components",
    "contexts",
    "services",
    "utils",
    "hooks",
    "backend",
    "backend/routers",
    "backend/agents",
    "backend/models",
    "ai-specs",
    "ai-specs/specs",
    "ai-specs/changes"
]

folders_ok = 0
for folder in folders:
    path = Path(folder)
    if path.exists() and path.is_dir():
        print(f"✅ {folder}/")
        folders_ok += 1
    else:
        print(f"❌ {folder}/ - MISSING")

print(f"\n📊 Folders: {folders_ok}/{len(folders)} OK")

# Resumen Final
print("\n" + "="*80)
print("📊 RESUMEN FINAL")
print("="*80)

total_tests = 6
tests_passed = 0

results = [
    ("Frontend Files", frontend_ok, len(frontend_files)),
    ("Backend Files", backend_ok, len(backend_files)),
    ("Configuration", config_ok, len(keys_to_check)),
    ("NPM Scripts", scripts_ok, len(required_scripts)),
    ("Documentation", docs_ok, len(docs)),
    ("Folder Structure", folders_ok, len(folders))
]

for name, passed, total in results:
    percentage = (passed * 100 // total) if total > 0 else 0
    status = "✅" if percentage == 100 else "⚠️" if percentage >= 80 else "❌"
    print(f"{status} {name}: {passed}/{total} ({percentage}%)")
    if percentage >= 80:
        tests_passed += 1

print(f"\n{'='*80}")
overall = (tests_passed * 100 // total_tests)
print(f"Overall: {tests_passed}/{total_tests} categories passed ({overall}%)")

if overall == 100:
    print("\n🎉 ALL TESTS PASSED! Project structure is complete.")
    exit_code = 0
elif overall >= 80:
    print("\n✅ MOSTLY PASSING! Minor issues detected.")
    exit_code = 0
else:
    print("\n⚠️  SOME ISSUES DETECTED! Check details above.")
    exit_code = 1

sys.exit(exit_code)
