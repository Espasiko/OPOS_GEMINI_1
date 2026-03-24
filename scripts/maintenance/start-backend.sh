#!/bin/bash
# OpositAIA Backend - Script de arranque
# VENV: usa .venv en la raíz del proyecto (NO backend/venv — no existe)
# Neo4j: opositaia-neo4j (Docker, 7474/7687) — UP por defecto
# Qdrant: opositaia-qdrant (Docker, 6333) — UP por defecto

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV="$PROJECT_ROOT/.venv"

echo "🚀 Arrancando OpositAIA Backend..."
echo "📁 Proyecto: $PROJECT_ROOT"
echo "🐍 Venv: $VENV"

if [ ! -f "$VENV/bin/activate" ]; then
    echo "❌ Error: venv no encontrado en $VENV"
    exit 1
fi

cd "$PROJECT_ROOT/backend"
source "$VENV/bin/activate"

echo "✅ Venv activado: $(which python)"
echo "📡 Arrancando en http://0.0.0.0:8000"

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
