# 📋 Plan de Sprints y Ideas - 19/12/2025

**Estado:** ⏳ PENDIENTE APROBACIÓN

---

## 🎯 ORDEN LÓGICO DE SPRINTS

```
┌─────────────────────────────────────────────────────────┐
│  FASE 1: GENERAR MÁXIMO CONTENIDO                       │
│  ├── Sprint 1: Mistral Agentic + MCP → Más Q&A         │
│  └── Sprint 2: BOE /analisis → Estructura leyes        │
├─────────────────────────────────────────────────────────┤
│  FASE 2: CONSOLIDAR Y LIMPIAR                           │
│  └── Sprint 3: Deduplicar TODO junto                   │
├─────────────────────────────────────────────────────────┤
│  FASE 3: ENTRENAMIENTO                                  │
│  └── Sprint 4: Fine-tuning Mistral 7B GGUF + LoRA      │
├─────────────────────────────────────────────────────────┤
│  FASE 4: SERVIR AL USUARIO (POSTERIOR)                  │
│  ├── Sprint 5: Verificación Claude Batch               │
│  └── Sprint 6: COSM/Mezclador                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📌 SPRINT 1: MISTRAL AGENTIC + MCP (PRIORIDAD ALTA)

### Objetivo
Generar el máximo de Q&A de calidad usando Mistral 8B en modo agentic con acceso al RAG local.

### Prerrequisitos
- ✅ Endpoint FastAPI existente que expone MCP
- ✅ Qdrant local con 17,403 vectores
- ✅ PostgreSQL con leyes (26MB, tabla 'laws')

### Tareas
| # | Tarea | Estado |
|---|-------|--------|
| 1.1 | Verificar endpoint FastAPI MCP | ⏳ |
| 1.2 | Configurar Mistral 8B HuggingFace | ⏳ |
| 1.3 | Conectar con Qdrant local via MCP | ⏳ |
| 1.4 | Pipeline: consulta → generación → verificación | ⏳ |
| 1.5 | Generar 200+ Q&A nuevas verificadas | ⏳ |

### Modelos a usar
- **Mistral 8B** (HuggingFace) → Generación + Tools
- **Groq llama-3.3-70b** → CoT + Function calling (barato)
- **DeepSeek R1** → Solo CoT (sin tools, para razonamiento)

---

## 📌 SPRINT 2: BOE /analisis ENDPOINT

### Objetivo
Integrar análisis estructural de leyes del BOE para mejor indexación.

### Tareas
| # | Tarea | Estado |
|---|-------|--------|
| 2.1 | Probar endpoint `/analisis/{id}` del BOE | ⏳ |
| 2.2 | Parsear estructura XML de secciones | ⏳ |
| 2.3 | Indexar por apartados en Qdrant | ⏳ |
| 2.4 | Generar Q&A por sección específica | ⏳ |

---

## 📌 SPRINT 3: DEDUPLICACIÓN TOTAL

### Objetivo
Consolidar y limpiar TODOS los datasets generados.

### Datasets a procesar
- `golden_dataset/official_exams_qa_FINAL_V3.jsonl` (370)
- `golden_dataset/premium/ALL_PREMIUM_100.jsonl` (100)
- `conceptual_materials/qa_generated/conceptual_qa_100.jsonl` (106)
- `dataset_generator/dataset_output_CLEAN/*.jsonl` (~3,953)
- **NUEVOS de Sprint 1** (~200+)

### Tareas
| # | Tarea | Estado |
|---|-------|--------|
| 3.1 | Unificar todos los JSONL | ⏳ |
| 3.2 | Calcular hash de cada pregunta | ⏳ |
| 3.3 | Detectar duplicados por embeddings | ⏳ |
| 3.4 | Eliminar duplicados, conservar mejor calidad | ⏳ |
| 3.5 | Exportar dataset consolidado limpio | ⏳ |

---

## 📌 SPRINT 4: FINE-TUNING

### Objetivo
Entrenar Mistral 7B GGUF con LoRA usando el dataset consolidado.

### Tareas
| # | Tarea | Estado |
|---|-------|--------|
| 4.1 | Convertir a formato ChatML/Alpaca | ⏳ |
| 4.2 | Preparar train/val split | ⏳ |
| 4.3 | Configurar LoRA (rank=64, alpha=128) | ⏳ |
| 4.4 | Entrenar en Colab (T4/V100) | ⏳ |
| 4.5 | Evaluar resultados | ⏳ |

---

## 📌 SPRINT 5: VERIFICACIÓN CLAUDE (POSTERIOR)

### Objetivo
Usar los 5€ en Claude Batch para verificar Q&A complejas.

### Notas
- Batch API: 50% descuento (esperar 24h)
- Solo para casos prácticos complejos
- Después de fine-tuning para evaluar modelo

---

## 📌 SPRINT 6: COSM/MEZCLADOR (FINAL)

### Objetivo
Diseñar estrategia de "Mezclador" para servir al usuario final.

### Notas
- Solo después de modelo fine-tuneado
- Combinar fichas de leyes pre-generadas
- Ahorrar tokens en producción

---

## 💡 IDEAS GOOGLE SHEETS/DRIVE

### Usos con Gemini Pro
| Uso | Descripción |
|-----|-------------|
| **Dashboard Q&A** | Vista global de todas las preguntas |
| **Enlaces Útiles** | URLs BOE, leyes, artículos frecuentes |
| **FAQs Oposiciones** | Preguntas comunes recolectadas |
| **Tracking Duplicados** | Hash + estado de duplicación |
| **Mapas Conceptuales** | Tablas tema→subtema→artículos |
| **Historial Verificaciones** | Auditoría de calidad |

### Hojas Propuestas
```
HOJA 1: LEYES_INDEX
├── Ley | Artículos clave | Temas | URL BOE

HOJA 2: CONCEPTOS_MAPA
├── Concepto | Relacionado_con | Ley_base | Dificultad

HOJA 3: PREGUNTAS_TRACKING
├── ID | Pregunta | Tipo | Calidad | Hash | Duplicado_de

HOJA 4: FLASHCARDS_EXPORT
├── Frente | Dorso | Tags (formato Anki)
```

---

## 💡 IDEAS GOOGLE COLAB NOTEBOOKS

### Notebooks Planificados
| Notebook | Uso |
|----------|-----|
| **1_analisis_dataset.ipynb** | Estadísticas, distribución, calidad |
| **2_verificacion_gemini.ipynb** | Batch verificación con Gemini API |
| **3_generacion_agentic.ipynb** | Mistral HF + Tools + Qdrant |
| **4_finetuning_lora.ipynb** | Preparación y entrenamiento |
| **5_evaluacion_modelo.ipynb** | Benchmarks post-fine-tuning |

---

## 💡 IDEAS GUARDADAS (NO OLVIDAR)

| Idea | Fase | Prioridad |
|------|------|-----------|
| Excalidraw mapas mentales | Post-COSM | Media |
| Anki flashcards export | Post-COSM | Media |
| Workflows YAML fábrica agentes | Evaluar | Baja |
| Resúmenes leyes COSM | Sprint 6 | Alta |

---

## 🔧 WORKFLOWS BMAD CIS A USAR

| Workflow/Agente | Cuándo usar |
|-----------------|-------------|
| `brainstorming-coach` | Generar ideas nuevos tipos Q&A |
| `innovation-strategist` | Diseñar COSM (Sprint 6) |
| `creative-problem-solver` | Resolver problemas deduplicación |
| `design-thinking` | UX comparador versiones |

---

**Estado:** ⏳ PENDIENTE APROBACIÓN USUARIO
