# Memoria del Proyecto OpositaIA - 22 Diciembre 2025

**Última actualización**: 22/12/2025 18:30  
**Estado**: Estrategia Híbrida de Enriquecimiento + Limpieza Masiva

---

## 📋 ÍNDICE (ACTUALIZADO)

1. [Arquitectura General](#arquitectura-general)
2. [Estrategia de Datos (Mega Plan)](#estrategia-de-datos)
3. [Infraestructura y Limpieza](#infraestructura-y-limpieza)
4. [Estrategia Fine-Tuning y Modelos Móviles](#estrategia-fine-tuning-y-modelos-móviles)

---

## 1. ARQUITECTURA GENERAL

Se mantiene la arquitectura base (FastAPI + Qdrant + Postgres), pero se ha pivotado la estrategia de **Generación de Datos** hacia un modelo de calidad ultra-alta para Fine-Tuning.

---

## 2. ESTRATEGIA DE DATOS (MEGA PLAN)

### Dataset Consolidado: `golden_dataset/final_v1_train.jsonl`
Compuesto por **1,228 ítems** de alta calidad:
- **Thinking Cases** (Groq): Casos complejos con razonamiento oculto.
- **Enriched Exams** (Mistral API): Preguntas oficiales con referencias inyectadas.
- **Extreme Cases** (DeepSeek): Casos de dificultad experta.
- **Standard QA**: Preguntas verificadas.

---

## 3. INFRAESTRUCTURA Y LIMPIEZA

### Acciones Realizadas (22/12)
1. **Limpieza de PII**: Eliminados emails de academias de `extracted_texts`.
2. **Organización**: Movidos +50 scripts experimentales a `archive`.
3. **Rescate Abandonado**: Se descartó recuperar logs de DeepSeek por ineficiencia.

### El Rol de Nemotron & Cohere
- **Cohere Rerank**: Filtro crítico pre y post training. Se recomienda versión gratuita para desarrollo.
- **Nemotron (Judge)**: Auditoría de calidad final.

---

## 4. ESTRATEGIA FINE-TUNING Y MODELOS MÓVILES

### A. Entorno: Google Colab + Unsloth (Recomendado)
- **Por qué**: Usar GPU T4 Gratis es 100x más rápido que tu portátil CPU.
- **Notebook Generado**: `fine_tuning_mistral_unsloth.ipynb`.
- **Checkpointing**: El notebook está configurado para **guardar cada 50 pasos**. Si se desconecta, puedes reanudar donde lo dejaste sin empezar de cero.

### B. Entorno: Portátil Local (16GB RAM, Sin GPU Potente)
- **Viabilidad**: Iniciar entrenamiento de 7B desde cero es **muy lento** (días) y sobrecalentará el portátil.
- **Recomendación**: Usa el portátil solo para inferencia (probar el modelo) o para entrenar modelos diminutos (1B - 3B).

### C. Investigación: Modelos "Móviles" (Q4 2025)
Para el VPS de 8GB y despliegue móvil, estos son los ganadores hoy:

1.  **Llama 3.2 3B (Meta)**:
    - **El rey del móvil**. Contexto 128k.
    - Muy bueno en español y tareas generales.
    - Cabe en 2.5GB de RAM.

2.  **Phi-3.5 Mini (Microsoft)**:
    - **El rey del razonamiento**. 3.8B parámetros.
    - Supera a Llama 3.2 en lógica y tests (MMLU).
    - Ideal para opositores (resolver casos).

**Veredicto**: Entrenaremos Mistral 7B en Colab (Maestro) y luego haremos "Distillation" (enseñar) a un **Phi-3.5 Mini** para la versión móvil/barata.

---

**Autor**: OpositaIA Agent Team (Antigravity)
**Validado**: 22/12/2025 18:30
