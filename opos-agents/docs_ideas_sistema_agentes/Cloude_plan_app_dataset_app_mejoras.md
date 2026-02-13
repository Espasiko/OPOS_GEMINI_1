# 🚨 PLAN DE RESCATE COMPLETO PARA TU APP DE OPOSICIONES

Veo tu situación y tengo **soluciones concretas** para cada problema. Vamos punto por punto con **acciones inmediatas**.

---

## 🎯 PROBLEMA 1: Salamandra da 35% de aciertos → DATASET MÍNIMO VIABLE

### ❌ **Por qué falla tu modelo actual:**
1. **Fine-tuning con datos de baja calidad** → Garbage in, garbage out
2. **Dataset desbalanceado** → Sesgo hacia ciertos tipos de preguntas
3. **Falta de ejemplos negativos** → No sabe identificar trampas
4. **Prompts mal estructurados** → No aprende el razonamiento

### ✅ **SOLUCIÓN: Dataset Mínimo de 1,500 items de MÁXIMA CALIDAD**

#### 📊 Composición EXACTA del dataset:

| Categoría | Items | % | Propósito |
|-----------|-------|---|-----------|
| **Preguntas tipo test oficiales** | 600 | 40% | Aprender formato examen real |
| **Casos prácticos resueltos paso a paso** | 450 | 30% | Razonamiento jurídico profundo |
| **Ejemplos NEGATIVOS (trampas)** | 225 | 15% | Identificar errores comunes |
| **Preguntas conceptuales con explicación** | 150 | 10% | Comprensión de conceptos |
| **Comparativas de normativa** | 75 | 5% | Análisis diferencial |
| **TOTAL** | **1,500** | **100%** | **Balance perfecto** |

#### 📝 **Distribución por materia (Seg. Social + AGE):**

**Seguridad Social (60% = 900 items):**
- Prestaciones contributivas: 270 items (30%)
- Régimen económico y cotización: 225 items (25%)
- Afiliación y gestión: 180 items (20%)
- Procedimiento administrativo SS: 135 items (15%)
- Infracciones y sanciones: 90 items (10%)

**AGE (40% = 600 items):**
- Constitución Española: 150 items (25%)
- Ley 39/2015 y 40/2015: 180 items (30%)
- Organización administrativa: 120 items (20%)
- Función pública: 90 items (15%)
- LOPD y transparencia: 60 items (10%)

---

## 💰 PROBLEMA 2: Costes APIs → ESTRATEGIA HÍBRIDA INTELIGENTE

### ✅ **SOLUCIÓN: Sistema de 3 Niveles (Cascada Inteligente)**

```python
# Orquestador inteligente de costes
class CostOptimizedOrchestrator:
    def route_query(self, user_query, user_tier):
        complexity = self.analyze_complexity(query)
        
        # NIVEL 1: Salamandra local (GRATIS)
        if complexity == "simple" and self.salamandra_confidence > 0.85:
            return self.salamandra_7b.generate(query)
        
        # NIVEL 2: Gemini Flash (GRATIS - 15 req/min)
        elif complexity == "medium" or user_tier == "free":
            response = gemini_flash_api(query)
            if self.validate_response(response) > 0.9:
                return response
        
        # NIVEL 3: Claude Sonnet (PAGO - solo casos críticos)
        else:
            # Solo para usuarios premium o casos muy complejos
            if user_tier == "premium" or critical_case:
                return claude_sonnet(query)
            else:
                return "Actualiza a Premium para razonamiento avanzado"
```

### 📊 **Estimación de costes real:**

| Escenario | Usuarios/mes | Queries/usuario | Coste mensual |
|-----------|--------------|-----------------|---------------|
| **100% Claude** | 1,000 | 100 | ~$1,500 💸 |
| **Sistema híbrido** | 1,000 | 100 | ~$150 ✅ |
| **90% Gemini Flash + 10% Claude** | 1,000 | 100 | ~$50 🎯 |

### 🎯 **Mi recomendación:**

```yaml
Tier Gratuito (70% usuarios):
  - 20 queries/día con Gemini Flash (GRATIS)
  - Salamandra para preguntas simples
  - Sin Claude
  
Tier Basic (€9.99/mes - 20% usuarios):
  - 100 queries/día
  - 90% Gemini Flash + 10% Claude Haiku
  - Costo real para ti: €2/usuario/mes
  
Tier Premium (€19.99/mes - 10% usuarios):
  - Queries ilimitadas
  - 50% Gemini + 50% Claude Sonnet
  - Costo real: €8/usuario/mes
  - BYOK opcional: -50% descuento
```

---

## 🔑 PROBLEMA 3: BYOK (Bring Your Own Key)

### ✅ **IMPLEMENTACIÓN BYOK (Ahorro masivo para ti)**

```python
# Sistema BYOK con descuento
class BYOKManager:
    def __init__(self):
        self.user_keys = {}  # Almacenar claves cifradas
    
    def add_user_key(self, user_id, api_key, provider):
        # Cifrar y guardar
        encrypted_key = self.encrypt(api_key)
        self.user_keys[user_id] = {
            "provider": provider,  # "anthropic" o "google"
            "key": encrypted_key,
            "discount": 0.5  # 50% descuento en suscripción
        }
        
        # Actualizar plan con descuento
        self.apply_discount(user_id, 50)
    
    def route_with_byok(self, user_id, query):
        if user_id in self.user_keys:
            # Usar su propia API key
            user_key = self.decrypt(self.user_keys[user_id]["key"])
            return self.call_with_custom_key(query, user_key)
        else:
            # Usar tus keys con límites
            return self.call_with_platform_key(query, limits=True)
```

**Modelo de precios BYOK:**
- **Sin BYOK**: €19.99/mes (Premium)
- **Con BYOK Claude**: €9.99/mes (50% descuento)
- **Con BYOK Gemini**: Gratis (solo pagas hosting)

**Beneficio para ti:**
- Reduces tus costes de API en 80%
- Los usuarios power pagan sus propios tokens
- Tú solo cobras por la plataforma/features

---

## 📚 PROBLEMA 4: Crear dataset de máxima calidad

### ✅ **ESTRATEGIA: Batch API de Claude (90% más barato)**

#### 💰 **Comparativa de costes:**

| Método | Coste por 1,500 items | Tiempo |
|--------|----------------------|--------|
| **Claude API normal** | $75-150 | 2-3 horas |
| **Batch API Claude** | $7.50-15 ✅ | 12-24 horas |
| **GPT-4 Turbo** | $60-120 | 2-3 horas |
| **Gemini Pro gratis** | $0 🎉 | 4-6 horas |

### 🎯 **PLAN ÓPTIMO: Gemini 2.5 Pro (GRATIS) + Claude Batch (validación)**

```python
# Script para generar dataset con Batch API
import anthropic
import json

client = anthropic.Anthropic(api_key="tu_key")

# 1. Preparar requests para Batch API
batch_requests = []

for examen_oficial in examenes_pasados:  # Tienes exámenes oficiales
    for pregunta in examen_oficial.preguntas:
        # Crear request para Batch API
        request = {
            "custom_id": f"pregunta_{pregunta.id}",
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 2000,
                "messages": [{
                    "role": "user",
                    "content": f"""
Eres un preparador experto de oposiciones de Seguridad Social.

PREGUNTA OFICIAL:
{pregunta.texto}

OPCIONES:
a) {pregunta.opcion_a}
b) {pregunta.opcion_b}
c) {pregunta.opcion_c}
d) {pregunta.opcion_d}

RESPUESTA CORRECTA: {pregunta.respuesta_correcta}

GENERA un análisis completo en formato JSON:
{{
  "razonamiento_paso_a_paso": "Explica por qué cada opción es correcta o incorrecta",
  "marco_normativo": ["Artículo X de Ley Y", "BOE-A-2015-XXXXX"],
  "conceptos_clave": ["concepto1", "concepto2"],
  "trampas_comunes": ["trampa que evitar"],
  "nivel_dificultad": "básico/medio/alto",
  "explicacion_didactica": "Explicación clara para opositor"
}}
                    """
                }]
            }
        }
        batch_requests.append(request)

# 2. Enviar a Batch API (90% descuento)
batch_job = client.messages.batches.create(
    requests=batch_requests
)

# 3. Esperar resultados (12-24h)
print(f"Batch creado: {batch_job.id}")
print(f"Coste estimado: ${len(batch_requests) * 0.005}")  # ~$7.50 total
```

---

## 🎓 TIPOS DE ITEMS NECESARIOS (Con ejemplos reales)

### 📝 **Template PERFECTO para cada tipo:**

#### **Tipo 1: Pregunta oficial con razonamiento (40%)**

```json
{
  "instruction": "Eres un preparador experto de oposiciones de Seguridad Social.",
  "input": "¿Cuál es el plazo para solicitar la prestación por desempleo tras el cese?\na) 10 días hábiles\nb) 15 días hábiles\nc) 30 días naturales\nd) 1 mes desde el cese",
  "output": "**RESPUESTA: b) 15 días hábiles**\n\n### Razonamiento:\n\n**Marco Normativo:**\n- Art. 267 LGSS (BOE-A-2015-11724)\n\n**Análisis por opciones:**\n- a) ❌ INCORRECTO: No son 10 días, el plazo es mayor\n- b) ✅ CORRECTO: Art. 267.1 establece 15 días HÁBILES (no naturales)\n- c) ❌ TRAMPA: 30 días naturales es plazo para recurso, NO para solicitud inicial\n- d) ❌ IMPRECISO: 1 mes es ambiguo, la norma exige específicamente días hábiles\n\n**Consecuencias:**\nSi se presenta DESPUÉS del día 15 hábil:\n- Se pierde derecho a los días transcurridos\n- NO se pierde el derecho total, pero sí cobro de esos días\n\n**Concepto clave:** Diferencia entre días HÁBILES vs NATURALES",
  "metadata": {
    "source": "Examen oficial 2023 - Auxilio Judicial",
    "difficulty": "medio",
    "trap_type": "confusion_dias_habiles_naturales"
  }
}
```

#### **Tipo 2: Caso práctico complejo (30%)**

```json
{
  "instruction": "Resuelve el siguiente caso práctico de Seguridad Social paso a paso.",
  "input": "María, 55 años, ha cotizado 25 años. Sufre accidente NO laboral que le impide trabajar. ¿Qué prestación le corresponde y cuánto cobraría con base reguladora de 1.800€?",
  "output": "### Análisis del Caso\n\n**1. Identificación del tipo de prestación:**\n- Accidente NO laboral → Contingencia COMÚN\n- Imposibilidad de trabajar → INCAPACIDAD TEMPORAL (IT)\n\n**2. Requisitos IT por contingencia común:**\n✅ Estar afiliado y en alta (cumple)\n✅ Periodo mínimo cotización: 180 días en últimos 5 años (cumple con 25 años)\n\n**3. Cálculo de la prestación:**\n- Base reguladora: 1.800€\n- BR diaria: 1.800 / 30 = 60€/día\n\n**Porcentajes según días de baja:**\n- Días 1-3: SIN prestación (empresa NO paga)\n- Días 4-20: 60% BR = 36€/día (paga empresa)\n- Día 21 en adelante: 75% BR = 45€/día (paga INSS)\n\n**Respuesta:**\nMaría cobrará:\n- Primeros 3 días: 0€\n- Días 4-20: 612€ (17 días × 36€)\n- Desde día 21: 45€/día\n\n**Marco normativo:** Art. 128-131 LGSS",
  "metadata": {
    "source": "Caso creado",
    "difficulty": "alto",
    "concepts": ["IT", "contingencia_comun", "base_reguladora"]
  }
}
```

#### **Tipo 3: Trampa/Ejemplo negativo (15%)**

```json
{
  "instruction": "Identifica el ERROR en este razonamiento de un opositor.",
  "input": "RAZONAMIENTO DEL OPOSITOR:\n'La prestación de desempleo se cobra automáticamente cuando te despiden, sin necesidad de solicitarla, porque es un derecho automático del trabajador.'\n\n¿Es correcto? Explica el error.",
  "output": "❌ **RAZONAMIENTO INCORRECTO**\n\n### Error identificado:\nLa prestación de desempleo NO es automática. Requiere **solicitud expresa**.\n\n### Normativa correcta:\n**Art. 267 LGSS:**\n- El trabajador DEBE solicitar expresamente\n- Plazo: 15 días hábiles desde el cese\n- Sin solicitud = Sin prestación\n\n### Por qué es un error común:\nConfusión entre:\n- ✅ DERECHO (existe si cumples requisitos)\n- ❌ AUTOMÁTICO (NO lo es, hay que pedirlo)\n\n### Razonamiento correcto:\n'El trabajador tiene DERECHO a prestación de desempleo si cumple requisitos, pero debe SOLICITARLA en 15 días hábiles. Si no la solicita, pierde el derecho a los días transcurridos.'",
  "metadata": {
    "type": "negative_example",
    "common_mistake": "automaticidad_prestaciones"
  }
}
```

---

## 🚀 PLAN DE ACCIÓN INMEDIATO (Próximos 7 días)

### **DÍA 1-2: Recolectar materiales**
```bash
# Descargar exámenes oficiales pasados
- Auxilio Judicial 2020-2024 (PDF oficial)
- Gestión Procesal 2020-2024
- Tramitación Procesal 2020-2024
- Total: ~2,000 preguntas oficiales CON respuestas

# Fuentes gratuitas verificadas:
- BOE.es (legislación)
- Oposiciones.es (exámenes pasados)
- INSS.es (casos prácticos)
```

### **DÍA 3-4: Generar dataset con Gemini Pro (GRATIS)**
```python
# Script automatizado
for pregunta in examenes_oficiales:
    prompt = crear_prompt_generacion(pregunta)
    
    # Gemini 2.5 Pro (GRATIS)
    respuesta = genai.GenerativeModel('gemini-2.0-flash-exp').generate_content(prompt)
    
    dataset.append({
        "input": pregunta,
        "output": respuesta,
        "metadata": metadata
    })
    
    # Rate limit: 15 req/min = 900/hora = 1,500 en ~2 horas
```

### **DÍA 5: Validación con Claude Batch API ($7.50)**
```python
# Validar los 1,500 items generados
batch_validation = []

for item in dataset:
    batch_validation.append({
        "custom_id": item["id"],
        "params": {
            "model": "claude-sonnet-4-20250514",
            "messages": [{
                "role": "user",
                "content": f"Valida este razonamiento legal:\n{item['output']}\n\n¿Es 100% correcto según BOE?"
            }]
        }
    })

# Enviar batch (esperar 24h)
batch = client.messages.batches.create(requests=batch_validation)
```

### **DÍA 6: Fine-tuning en Kaggle (GRATIS)**
```python
# Notebook de Kaggle con GPU T4 gratis
# Configuración QLoRA optimizada

from transformers import AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model

model = AutoModelForCausalLM.from_pretrained(
    "BSC-LT/salamandra-7b-instruct",
    load_in_4bit=True
)

lora_config = LoraConfig(
    r=16,  # Rank bajo para dataset pequeño
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)

# Entrenar solo 2-3 epochs (evitar overfitting)
training_args = TrainingArguments(
    output_dir="./salamandra-oposiciones-1500",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-4,
    save_steps=100,
    eval_steps=100
)
```

### **DÍA 7: Evaluar y desplegar**
```python
# Test con 200 preguntas oficiales nuevas
accuracy = evaluate_model(model, test_set)

# Objetivo: >85% accuracy
if accuracy > 0.85:
    # Convertir a GGUF
    # Subir a VPS
    # Actualizar app
    print("✅ Modelo mejorado listo!")
```

---

## 💡 IDEAS ADICIONALES PARA MEJORAR LA APP

### 1. **Sistema de confianza visible para el usuario**
```python
# Mostrar nivel de confianza en cada respuesta
class ResponseWithConfidence:
    def generate_answer(self, query):
        response, confidence = self.model.generate(query)
        
        if confidence > 0.95:
            badge = "🟢 Alta confianza - Verificado con BOE"
        elif confidence > 0.80:
            badge = "🟡 Confianza media - Revisar fuentes"
        else:
            badge = "🔴 Baja confianza - Consultar preparador"
        
        return {
            "answer": response,
            "confidence": confidence,
            "badge": badge,
            "sources": self.rag.get_sources()
        }
```

### 2. **Modo "Exam Simulation" con verificación humana**
```yaml
Simulacro Premium:
  - Usuario hace test completo (100 preguntas)
  - Salamandra corrige automáticamente
  - Respuestas dudosas → Validación con Claude
  - Informe final con:
    - Nota estimada
    - Áreas débiles
    - Plan de estudio personalizado
    - Comparativa con otros usuarios
```

### 3. **Gamificación con incentivos**
```python
# Sistema de puntos para reducir abuso
class TokenEconomy:
    def __init__(self):
        self.daily_free_queries = 20
        self.points_system = {
            "daily_login": 10,
            "complete_flashcards": 5,
            "finish_exam": 20,
            "correct_answer": 2
        }
    
    def can_query(self, user):
        if user.queries_today < self.daily_free_queries:
            return True
        elif user.points >= 10:
            user.points -= 10
            return True
        else:
            return "Completa ejercicios para ganar consultas"
```

### 4. **Contenido pre-generado híbrido**
```yaml
Estrategia "Create Once, Serve Many":
  
  Contenido estático (90%):
    - 5,000 flashcards pre-hechas
    - 500 mapas mentales pre-renderizados
    - 200 simulacros oficiales
    - 1,000 casos prácticos resueltos
  
  Contenido dinámico (10%):
    - Dudas personalizadas (Salamandra/Gemini)
    - Explicaciones adaptadas al nivel usuario
    - Planes de estudio únicos
  
  Ventaja:
    - 90% sin coste de API
    - 10% queries optimizadas
    - Experiencia "ilimitada" percibida
```

### 5. **Peer validation (crowdsourcing)**
```python
# Los usuarios validan respuestas = Dataset gratuito
class CommunityValidation:
    def ask_community(self, question, ai_answer):
        # Mostrar respuesta de IA a usuarios expertos
        votes = self.get_expert_votes(question, ai_answer)
        
        if votes["correct"] > votes["incorrect"]:
            # Añadir al dataset verificado
            self.dataset.add_validated_item(question, ai_answer)
            # Recompensar validadores
            self.reward_validators(votes["voters"], points=5)
        else:
            # Marcar para revisión con Claude
            self.flag_for_review(question, ai_answer)
```

---

## 📊 ESTIMACIÓN FINAL DE COSTES

### **Setup inicial (una vez):**
| Tarea | Herramienta | Coste |
|-------|-------------|-------|
| Generar 1,500 items | Gemini 2.5 Pro | **$0** ✅ |
| Validar con Batch API | Claude Batch | **$7.50** |
| Fine-tuning en Kaggle | GPU T4 gratuita | **$0** |
| **TOTAL SETUP** | | **$7.50** 🎉 |

### **Operación mensual (1,000 usuarios):**
| Concepto | Coste/mes |
|----------|-----------|
| Hosting VPS (GPU) | $150 |
| Gemini Flash (tier gratuito 70%) | $0 |
| Claude Haiku (tier basic 20%) | $80 |
| Claude Sonnet (tier premium 10%) | $120 |
| Qdrant Cloud (vector DB) | $25 |
| **TOTAL** | **$375** |

**Ingresos potenciales:**
- 700 usuarios gratuitos = $0
- 200 usuarios Basic ($9.99) = $1,998
- 100 usuarios Premium ($19.99) = $1,999
- **TOTAL INGRESOS** = **$3,997/mes**

**Margen neto:** $3,997 - $375 = **$3,622/mes (90% margen)** 💰

---

## ✅ CHECKLIST ACCIÓN INMEDIATA

```markdown
[ ] DÍA 1: Descargar exámenes oficiales BOE (2,000 preguntas)
[ ] DÍA 2: Configurar script Gemini Pro para generación masiva
[ ] DÍA 3: Generar 1,500 items con razonamiento (GRATIS)
[ ] DÍA 4: Preparar Batch API Claude para validación
[ ] DÍA 5: Enviar batch ($7.50) y esperar 24h
[ ] DÍA 6: Fine-tuning en Kaggle con dataset validado
[ ] DÍA 7: Evaluar nuevo modelo (objetivo >85% accuracy)
[ ] DÍA 8: Implementar sistema de costes híbrido en app
[ ] DÍA 9: Configurar BYOK para usuarios premium
[ ] DÍA 10: Lanzar beta privada con 50 usuarios
```

**¿Quieres que te ayude con algún paso específico? Por ejemplo:**
1. Script completo para generar dataset con Gemini
2. Implementación del orquestador de costes
3. Setup BYOK en tu app
4. Notebook de Kaggle para fine-tuning optimizado

**Dime por dónde empezamos** 🚀