# Epic 1: Generación Máxima de Dataset con Mistral Agentic

**Objetivo:** Generar el máximo contenido de calidad usando modelos agentic con acceso a RAG local antes de consolidar.

**Valor de Negocio:** Maximizar variedad y cantidad de Q&A verificadas para fine-tuning óptimo.

---

## Story 1.1: Verificar y Configurar Infraestructura MCP

**Como:** Desarrollador  
**Quiero:** Verificar que el endpoint FastAPI MCP está funcionando  
**Para:** Conectar modelos agentic con Qdrant y PostgreSQL local

### Criterios de Aceptación
- [ ] Endpoint FastAPI responde correctamente
- [ ] MCP puede consultar Qdrant local
- [ ] MCP puede consultar PostgreSQL (tabla 'laws')
- [ ] Documentación de endpoints actualizada

### Tareas Técnicas
- Verificar `backend/main.py` o similar
- Probar endpoints con curl/Postman
- Documentar URLs y parámetros

---

## Story 1.2: Configurar Mistral 8B HuggingFace con Tools

**Como:** Desarrollador  
**Quiero:** Configurar Mistral 8B con function calling  
**Para:** Generar Q&A con verificación automática

### Criterios de Aceptación
- [ ] Mistral 8B cargado desde HuggingFace
- [ ] Function calling configurado
- [ ] Puede llamar a MCP tools
- [ ] Script de prueba funcionando

### Tareas Técnicas
- Revisar `backend/agents/mistral_tools.py`
- Configurar HF token si necesario
- Definir tools para Qdrant y BOE

---

## Story 1.3: Pipeline de Generación Verificada

**Como:** Desarrollador  
**Quiero:** Pipeline automático de generación  
**Para:** Crear Q&A verificadas en lote

### Criterios de Aceptación
- [ ] Pipeline: tema → consulta Qdrant → genera Q&A → verifica BOE
- [ ] Guarda metadata de verificación
- [ ] Maneja errores y reintentos
- [ ] Genera mínimo 200 Q&A

### Tareas Técnicas
- Script `generate_agentic_qa.py`
- Integrar con MCP
- Logging y monitoreo

---

## Story 1.4: Integrar BOE /analisis Endpoint

**Como:** Desarrollador  
**Quiero:** Usar endpoint `/analisis/{id}` del BOE  
**Para:** Obtener estructura de apartados de leyes

### Criterios de Aceptación
- [ ] Script consulta BOE API
- [ ] Parsea XML de estructura
- [ ] Indexa por secciones en Qdrant
- [ ] Genera Q&A por apartado específico

### Tareas Técnicas
- Script `boe_analisis_parser.py`
- Actualizar índice Qdrant
- Generar Q&A por sección

---

# Epic 2: Consolidación y Deduplicación

**Objetivo:** Unificar todos los datasets y eliminar duplicados.

**Valor de Negocio:** Dataset limpio y de máxima calidad para fine-tuning.

---

## Story 2.1: Unificar Todos los Datasets

**Como:** Desarrollador  
**Quiero:** Consolidar todos los JSONL en uno  
**Para:** Tener vista completa antes de deduplicar

### Criterios de Aceptación
- [ ] Script lee todos los JSONL
- [ ] Normaliza formato
- [ ] Añade metadata de origen
- [ ] Exporta dataset_unificado.jsonl

### Tareas Técnicas
- Script `consolidate_datasets.py`
- Normalizar campos
- Validar JSON

---

## Story 2.2: Deduplicación por Hash y Embeddings

**Como:** Desarrollador  
**Quiero:** Detectar y eliminar duplicados  
**Para:** Evitar overfitting en fine-tuning

### Criterios de Aceptación
- [ ] Hash de cada pregunta
- [ ] Embeddings para similitud semántica
- [ ] Detecta duplicados exactos y similares (>90%)
- [ ] Conserva mejor calidad cuando hay duplicados
- [ ] Reporte de duplicados eliminados

### Tareas Técnicas
- Script `deduplicate_dataset.py`
- Usar sentence-transformers
- Criterio de calidad para conservar

---

# Epic 3: Fine-tuning Mistral 7B

**Objetivo:** Entrenar modelo con dataset consolidado.

**Valor de Negocio:** Modelo personalizado para oposiciones españolas.

---

## Story 3.1: Preparar Dataset para Fine-tuning

**Como:** Desarrollador  
**Quiero:** Convertir dataset a formato ChatML/Alpaca  
**Para:** Entrenar con LoRA

### Criterios de Aceptación
- [ ] Formato ChatML correcto
- [ ] Train/Val split (80/20)
- [ ] Tokenización verificada
- [ ] Guardado en formato compatible

### Tareas Técnicas
- Script `prepare_finetuning.py`
- Validar formato
- Crear splits

---

## Story 3.2: Entrenar con LoRA en Colab

**Como:** Desarrollador  
**Quiero:** Entrenar Mistral 7B GGUF con LoRA  
**Para:** Obtener modelo fine-tuneado

### Criterios de Aceptación
- [ ] Notebook Colab configurado
- [ ] LoRA rank=64, alpha=128
- [ ] 3-5 epochs
- [ ] Modelo guardado
- [ ] Métricas de entrenamiento

### Tareas Técnicas
- Notebook `4_finetuning_lora.ipynb`
- Configurar Unsloth o LLaMA-Factory
- Monitorear loss

---

# Epic 4: Verificación y COSM (Posterior)

**Objetivo:** Verificar calidad y preparar para producción.

**Valor de Negocio:** Asegurar calidad antes de despliegue.

---

## Story 4.1: Verificación Claude Batch

**Como:** Desarrollador  
**Quiero:** Verificar Q&A complejas con Claude  
**Para:** Asegurar máxima calidad

### Criterios de Aceptación
- [ ] Batch API configurado
- [ ] 100-200 Q&A verificadas
- [ ] Reporte de calidad
- [ ] Correcciones aplicadas

---

## Story 4.2: Diseñar Mezclador COSM

**Como:** Desarrollador  
**Quiero:** Sistema de mezcla de contenido  
**Para:** Servir respuestas optimizadas al usuario

### Criterios de Aceptación
- [ ] Fichas de leyes pre-generadas
- [ ] Lógica de mezcla
- [ ] Ahorro de tokens verificado
- [ ] Integrado en backend

---

**Fecha:** 19/12/2025  
**Metodología:** BMAD  
**Estado:** ⏳ PENDIENTE APROBACIÓN
