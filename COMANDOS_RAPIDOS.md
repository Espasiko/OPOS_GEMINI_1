# ⚡ COMANDOS RÁPIDOS - PRUEBA SALAMANDRA VPS

## 🚀 Iniciar Sistema

```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Prueba
python test_salamandra_caso.py
```

## 🔍 Verificaciones Rápidas

```bash
# Health check general
curl http://localhost:8000/health

# Health check casos prácticos
curl http://localhost:8000/casos/health

# Verificar Salamandra VPS
curl http://147.93.95.67:11434/api/tags

# Verificar Salamandra local
curl http://localhost:11434/api/tags
```

## 📝 Generar Caso (curl)

```bash
curl -X POST http://localhost:8000/casos/generate-one \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Incapacidad Temporal por Enfermedad Común, base 1500€, día 10",
    "dificultad": "media"
  }' | jq .
```

## 🧪 Variaciones de Prueba

```bash
# Caso fácil (día 5)
curl -X POST http://localhost:8000/casos/generate-one \
  -H "Content-Type: application/json" \
  -d '{"tema": "IT por EC, base 1200€, día 5", "dificultad": "facil"}' | jq .

# Caso medio (día 10)
curl -X POST http://localhost:8000/casos/generate-one \
  -H "Content-Type: application/json" \
  -d '{"tema": "IT por EC, base 1500€, día 10", "dificultad": "media"}' | jq .

# Caso difícil (día 25)
curl -X POST http://localhost:8000/casos/generate-one \
  -H "Content-Type: application/json" \
  -d '{"tema": "IT por EC, base 2000€, día 25", "dificultad": "dificil"}' | jq .

# Accidente de Trabajo
curl -X POST http://localhost:8000/casos/generate-one \
  -H "Content-Type: application/json" \
  -d '{"tema": "IT por Accidente de Trabajo, base 1800€, día 5", "dificultad": "media"}' | jq .
```

## 📊 Ver Resultados

```bash
# Ver último caso generado
cat caso_generado_salamandra.json | jq .

# Ver solo confidence
cat caso_generado_salamandra.json | jq .confidence

# Ver solo caso
cat caso_generado_salamandra.json | jq .caso

# Ver solo cálculo
cat caso_generado_salamandra.json | jq .calculo_usado
```

## 🐛 Debugging

```bash
# Ver logs del backend
tail -f backend/backend.log

# Ver logs en tiempo real
cd backend && python main.py 2>&1 | tee backend.log

# Test calculadora directamente
python -c "
from backend.calculators.calculos_ss import calcular_subsidio_it
print(calcular_subsidio_it(1500, 'EC', 10))
"

# Test dispatcher directamente
python -c "
from backend.calculators.dispatcher import CasosPracticosDispatcher
result = CasosPracticosDispatcher.procesar_tema('IT por EC, base 1500€, día 10')
import json
print(json.dumps(result, indent=2))
"
```

## 🔄 Reiniciar Sistema

```bash
# Matar backend
pkill -f "python main.py"

# Reiniciar
cd backend && python main.py
```

## 📦 Instalar Dependencias (si falta algo)

```bash
pip install httpx pyyaml fastapi uvicorn python-dotenv
```

## 🎯 Validación Rápida

```bash
# 1. Backend healthy?
curl -s http://localhost:8000/health | jq .status

# 2. Casos endpoint healthy?
curl -s http://localhost:8000/casos/health | jq .status

# 3. Salamandra VPS accesible?
curl -s http://147.93.95.67:11434/api/tags | jq .

# 4. Generar caso de prueba
python test_salamandra_caso.py

# 5. Verificar resultado
cat caso_generado_salamandra.json | jq .confidence.level
```

## 📈 Benchmark (10 casos)

```bash
# Generar 10 casos y medir tiempo
for i in {1..10}; do
  echo "Caso $i..."
  time curl -X POST http://localhost:8000/casos/generate-one \
    -H "Content-Type: application/json" \
    -d "{\"tema\": \"IT por EC, base $((1000 + i*100))€, día $((5 + i))\", \"dificultad\": \"media\"}" \
    -o "caso_$i.json" 2>&1 | grep real
done

# Ver confidence de todos
for i in {1..10}; do
  echo "Caso $i: $(cat caso_$i.json | jq -r .confidence.level)"
done
```

## 🧹 Limpiar

```bash
# Borrar casos generados
rm caso_*.json caso_generado_salamandra.json

# Borrar logs
rm backend/backend.log
```
