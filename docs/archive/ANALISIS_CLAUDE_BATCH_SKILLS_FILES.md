# 🔍 Análisis Completo: Claude Batch API + Skills + Files

**Fecha**: 1 Diciembre 2025  
**Objetivo**: Maximizar calidad y minimizar coste para 300 Q&A complejas

---

## 📊 CLAUDE BATCH API

### **¿Qué es?**
Procesa múltiples requests en lote con **50% descuento** vs API normal.

### **Características:**
```python
import anthropic

client = anthropic.Anthropic(api_key="tu_key")

# Crear batch
message_batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "qa-001",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 2000,
                "messages": [{
                    "role": "user",
                    "content": "Genera Q&A sobre art. 205 LGSS..."
                }]
            }
        },
        {
            "custom_id": "qa-002",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 2000,
                "messages": [{
                    "role": "user",
                    "content": "Genera Q&A sobre art. 206 LGSS..."
                }]
            }
        }
        # ... hasta 10,000 requests
    ]
)

# Esperar resultados (procesamiento asíncrono)
# Puede tardar minutos u horas según volumen
```

### **Ventajas:**
✅ **50% descuento** en precio  
✅ Procesa hasta **10,000 requests** en un batch  
✅ Resultados en 24h máximo  
✅ Ideal para generación masiva  

### **Desventajas:**
⚠️ **No es inmediato** (procesamiento asíncrono)  
⚠️ **No hay streaming** (esperas al final)  
⚠️ **Complejidad** en manejo de errores  

### **Precios con Batch:**
```
Claude 4.5 Sonnet:
- Normal: $3/MTok input, $15/MTok output
- Batch:  $1.5/MTok input, $7.5/MTok output (50% OFF)

Para 300 Q&A complejas:
- Input: ~150K tokens × $1.5/M = $0.225
- Output: ~300K tokens × $7.5/M = $2.25
- TOTAL: $2.475 (vs $4.95 normal)

AHORRO: $2.475 por 300 Q&A ✅
```

---

## 🎯 CLAUDE SKILLS

### **¿Qué son?**
Instrucciones reutilizables que Claude puede seguir automáticamente.

### **Skills Disponibles:**

#### 1. **PDF Processing**
```
Triggers: PDF, .pdf, extract, merge, split
Capacidades:
- Extraer texto y tablas
- Crear nuevos PDFs
- Merge/split documentos
- Manejar formularios
```

**Uso para nosotros:**
```python
# Subir PDF de ley
file = client.beta.files.upload(
    file=("LGSS.pdf", open("backend/data/leyes/LGSS.pdf", "rb"), "application/pdf")
)

# Generar Q&A directamente del PDF
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2000,
    messages=[{
        "role": "user",
        "content": f"Lee este PDF y genera 10 Q&A sobre jubilación: {file.id}"
    }]
)
```

#### 2. **Excel Spreadsheet Handler**
```
Triggers: Excel, spreadsheet, .xlsx, data table
Capacidades:
- Crear/editar Excel
- Fórmulas y formato
- Análisis de datos
- Gráficos
```

**Uso para nosotros:**
```python
# Generar dataset en Excel
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{
        "role": "user",
        "content": "Crea un Excel con estas 300 Q&A organizadas por tema..."
    }]
)
```

#### 3. **Word Document Handler**
```
Triggers: Word, document, .docx
Capacidades:
- Crear/editar Word
- Tracked changes
- Comentarios
- Formato
```

#### 4. **PowerPoint Suite**
```
Triggers: PowerPoint, presentation, .pptx
Capacidades:
- Crear presentaciones
- Editar slides
- Análisis
```

### **¿Cómo activar Skills?**
```python
# Las skills se activan automáticamente por triggers
# Solo menciona las palabras clave en tu prompt

# Ejemplo:
prompt = """
Lee este PDF de la LGSS y extrae el artículo 205.
Luego genera 5 Q&A en formato Excel.
"""
# Activa automáticamente: PDF Processing + Excel Handler
```

---

## 📁 CLAUDE FILES API

### **¿Qué es?**
Sube archivos a Claude para que los procese directamente.

### **Formatos Soportados:**
- PDF (hasta 32MB)
- TXT, MD, CSV
- DOCX, XLSX, PPTX
- Imágenes (PNG, JPG)

### **Uso:**
```python
import anthropic

client = anthropic.Anthropic()

# 1. Subir archivo
file = client.beta.files.upload(
    file=(
        "LGSS.pdf",
        open("backend/data/leyes/LGSS.pdf", "rb"),
        "application/pdf"
    )
)

print(f"File ID: {file.id}")

# 2. Usar en conversación
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4000,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "file",
                    "file_id": file.id
                }
            },
            {
                "type": "text",
                "text": "Genera 10 Q&A sobre el artículo 205 de este PDF"
            }
        ]
    }]
)
```

### **Ventajas:**
✅ Claude lee el PDF directamente (no necesitas extraer texto)  
✅ Mantiene formato y estructura  
✅ Puede referenciar páginas específicas  
✅ Procesa tablas y gráficos  

### **Límites:**
- Tamaño máximo: 32MB por archivo
- Tokens: El contenido cuenta como input tokens
- Retención: 24 horas (luego se borra)

---

## 💡 PROMPT CACHING

### **¿Qué es?**
Cachea partes del prompt para reutilizarlas sin pagar de nuevo.

### **Uso:**
```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2000,
    system=[
        {
            "type": "text",
            "text": "Eres experto en Seguridad Social española...",
            "cache_control": {"type": "ephemeral"}  # ← CACHEA ESTO
        }
    ],
    messages=[{
        "role": "user",
        "content": "Genera Q&A sobre art. 205..."
    }]
)
```

### **Ahorro:**
```
Primera llamada:
- Input: 1000 tokens × $3/M = $0.003
- Cache write: 1000 tokens × $3.75/M = $0.00375
- Total: $0.00675

Llamadas siguientes (cache hit):
- Input: 100 tokens × $3/M = $0.0003
- Cache read: 1000 tokens × $0.30/M = $0.0003
- Total: $0.0006

AHORRO: 90% en llamadas repetidas ✅
```

---

## 🎯 ESTRATEGIA ÓPTIMA PARA 300 Q&A

### **Opción 1: Batch + Files (RECOMENDADO)**

```python
import anthropic
from pathlib import Path

client = anthropic.Anthropic()

# 1. Subir PDFs de leyes
leyes_files = {}
leyes_dir = Path("backend/data/leyes")

for pdf in leyes_dir.glob("*.pdf"):
    file = client.beta.files.upload(
        file=(pdf.name, open(pdf, "rb"), "application/pdf")
    )
    leyes_files[pdf.stem] = file.id
    print(f"✓ {pdf.name} → {file.id}")

# 2. Crear batch con 300 requests
batch_requests = []

for i in range(300):
    # Elegir ley aleatoria
    ley_name = random.choice(list(leyes_files.keys()))
    file_id = leyes_files[ley_name]
    
    batch_requests.append({
        "custom_id": f"qa-{i:04d}",
        "params": {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 2000,
            "system": [
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,  # Instrucciones del agente
                    "cache_control": {"type": "ephemeral"}  # Cachear
                }
            ],
            "messages": [{
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {"type": "file", "file_id": file_id}
                    },
                    {
                        "type": "text",
                        "text": f"Genera 1 Q&A compleja tipo oposición sobre {ley_name}"
                    }
                ]
            }]
        }
    })

# 3. Enviar batch
batch = client.messages.batches.create(requests=batch_requests)
print(f"Batch ID: {batch.id}")
print(f"Status: {batch.processing_status}")

# 4. Esperar resultados (polling)
import time

while batch.processing_status != "ended":
    time.sleep(60)  # Esperar 1 minuto
    batch = client.messages.batches.retrieve(batch.id)
    print(f"Progreso: {batch.request_counts.succeeded}/{len(batch_requests)}")

# 5. Descargar resultados
results = client.messages.batches.results(batch.id)

for result in results:
    qa_data = result.result.message.content[0].text
    # Guardar en JSONL
    with open("output/claude_batch_qa.jsonl", "a") as f:
        f.write(json.dumps({
            "id": result.custom_id,
            "qa": qa_data,
            "model": "claude-sonnet-4.5"
        }) + "\n")
```

### **Costes Opción 1:**
```
300 Q&A con Batch + Files + Cache:

Subida de PDFs:
- 8 PDFs × ~500K tokens = 4M tokens
- Cache write: 4M × $3.75/M = $15
- (Solo primera vez)

Generación (batch 50% OFF):
- Input: 300 × 500 tokens = 150K × $1.5/M = $0.225
- Cache read: 300 × 1000 tokens = 300K × $0.15/M = $0.045
- Output: 300 × 1000 tokens = 300K × $7.5/M = $2.25
- TOTAL: $2.52

TOTAL PRIMERA VEZ: $17.52
TOTAL SIGUIENTES: $2.52

Con €5 de saldo:
- Primera vez: NO alcanza
- Siguientes: 1,984 Q&A posibles ✅
```

### **Opción 2: Normal + Files (Sin Batch)**

```python
# Más simple pero más caro
for i in range(300):
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "file", "file_id": file_id}},
                {"type": "text", "text": "Genera Q&A..."}
            ]
        }]
    )
    # Procesar respuesta
```

**Costes:**
```
300 Q&A sin batch:
- Input: 150K × $3/M = $0.45
- Output: 300K × $15/M = $4.50
- TOTAL: $4.95

Con €5: 303 Q&A posibles ✅
```

---

## 🏆 RECOMENDACIÓN FINAL

### **Para 300 Q&A Complejas:**

**USAR: Opción 2 (Normal + Files)**

**Razones:**
1. ✅ **Más simple** de implementar
2. ✅ **Cabe en €5** de saldo
3. ✅ **Inmediato** (no esperas batch)
4. ✅ **Mejor control** de calidad
5. ✅ **Skills automáticas** (PDF processing)

**Implementación:**
```python
# dataset_generator/generate_with_claude_files.py

import anthropic
from pathlib import Path
import json
import random

client = anthropic.Anthropic()

# 1. Subir PDFs
leyes_files = {}
for pdf in Path("backend/data/leyes").glob("*.pdf"):
    file = client.beta.files.upload(
        file=(pdf.name, open(pdf, "rb"), "application/pdf")
    )
    leyes_files[pdf.stem] = file.id

# 2. Generar 300 Q&A
for i in range(300):
    ley = random.choice(list(leyes_files.keys()))
    file_id = leyes_files[ley]
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        system="Eres experto en Seguridad Social española...",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {"type": "file", "file_id": file_id}
                },
                {
                    "type": "text",
                    "text": f"""
                    Genera 1 Q&A compleja tipo oposición sobre {ley}.
                    
                    Formato JSON:
                    {{
                      "pregunta": "...",
                      "respuesta": "...",
                      "referencia": "Art. X",
                      "dificultad": "alta"
                    }}
                    """
                }
            ]
        }]
    )
    
    # Guardar
    qa = json.loads(response.content[0].text)
    qa["model"] = "claude-sonnet-4.5"
    qa["ley"] = ley
    
    with open("output/claude_qa.jsonl", "a") as f:
        f.write(json.dumps(qa, ensure_ascii=False) + "\n")
    
    print(f"✓ Q&A {i+1}/300 generada")

print(f"\n✅ 300 Q&A completadas")
print(f"Coste estimado: $4.95")
```

---

## 📋 RESUMEN EJECUTIVO

| Característica | Batch API | Normal API | Recomendación |
|----------------|-----------|------------|---------------|
| **Precio** | 50% OFF | Normal | Batch mejor |
| **Velocidad** | Horas | Inmediato | Normal mejor |
| **Complejidad** | Alta | Baja | Normal mejor |
| **Control** | Bajo | Alto | Normal mejor |
| **Skills** | ✅ | ✅ | Ambos |
| **Files** | ✅ | ✅ | Ambos |
| **Cache** | ✅ | ✅ | Ambos |

**DECISIÓN: Usar Normal API + Files**
- Coste: $4.95 para 300 Q&A
- Tiempo: ~2 horas
- Calidad: Máxima (Claude 4.5 + PDFs directos)
- Simplicidad: Alta

---

**Próximo paso**: Implementar `generate_with_claude_files.py` 🚀
