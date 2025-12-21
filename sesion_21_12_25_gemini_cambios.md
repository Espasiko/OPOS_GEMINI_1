# Resumen de Sesión: Avances Premium (21/12/2025)

Este documento consolida los hitos, estrategias y descubrimientos realizados durante la sesión del 21 de Diciembre de 2025.

## 1. El Hito "Multimodelo Premium" (Estrategia Two-Pass)

Hemos descifrado cómo hacer que modelos "pequeños" (Mistral 7B) o rápidos (Llama 3 en Groq) generen contenido de **Calidad Extrema** (nivel Tribunal) que antes solo conseguía DeepSeek R1.

### La Estrategia Ganadora: "Two-Pass CoT"
En lugar de pedir el JSON directamente (donde el modelo falla en lógica), dividimos el proceso en dos llamadas agénticas:
1.  **Fase "Arquitecto" (Thinking)**:
    *   **Rol**: Miembro del Tribunal / Jurista Experto.
    *   **Prompt**: "Diseña las trampas, busca conflictos normativos y planea el escenario. NO escribas el examen aún."
    *   **Output**: Un texto denso de "Pensamiento" (Chain of Thought sintético).
2.  **Fase "Redactor" (Execution)**:
    *   **Rol**: Redactor Oficial.
    *   **Input**: El "Plan del Arquitecto".
    *   **Prompt**: "Convierte este plan en un JSON estricto con 15+3 preguntas."

### Resultados Comparados
| Modelo | Antes | Con Two-Pass | Veredicto |
| :--- | :--- | :--- | :--- |
| **Groq (Llama 3)** | 15 preguntas (sin reserva), escenario simple | **18 preguntas perfectas**, escenario complejo con fechas | ⭐⭐⭐⭐ (Producción Masiva) |
| **Mistral (Local)** | Fallos de formato | (En proceso de validación) | Prometedor (Gratis) |
| **DeepSeek R1** | Excelente | N/A (Ya es Reasoner nativo) | ⭐⭐⭐⭐⭐ (Gold Standard) |

## 2. Descubrimientos Tecnológicos

### Groq: Mucho más que Llama
*   **GPT OSS 120B (El Juez)**:
    *   Modelo masivo (117B MoE).
    *   **Uso Estratégico**: Auditoría de Calidad. Detectó fallos jurídicos sutiles (ej. carencia 15 años jubilación) en nuestros tests.
    *   **Coste**: Caro para generar, barato para auditar (filtro final).
*   **Compound Systems (El Investigador)**:
    *   Wrappers agénticos con acceso a **Web Search** y **Python**.
    *   **Prueba de Fuego**: Encontró el SMI de 2025 (1.184€) y calculó subsidios correctamente.
    *   **Integración**: Será el "Agente RAG Web" en la arquitectura final.

### Modelos Locales (Mistral GGUF)
*   **Desafío**: Tiempos de inferencia largos en CPU (timeout errors).
*   **Solución**: Aumentar timeouts (1200s) y usar estrategias de caché para no reprocesar el contexto RAG.

## 3. Hoja de Ruta: "La Factoría de Datos"

### Pipeline Propuesto (Dataset 5.500 items)
1.  **Generación Masiva**:
    *   Usar `Groq Batch` (más barato) para crear 100 casos/día con la estrategia Two-Pass.
2.  **Limpieza y Auditoría**:
    *   **Filtro 1**: Scripts de validación JSON (estructura 15+3).
    *   **Filtro 2**: Modelos "Juez" (OSS 120B o Nemotron-4-Reward en HuggingFace local) para puntuar calidad jurídica.
    *   **Reranking**: Usar Cohere (o BGE-M3 local) para ordenar por relevancia/dificultad.
3.  **Fine-tuning**:
    *   Entrenar un Mistral 7B específico ("OpositaLLM") usando este dataset "Golden" auditado.

## 4. Scripts Clave Creados
*   `generate_premium_groq_twopass.py`: Implementación Cloud de la estrategia.
*   `generate_premium_mistral_local.py`: Implementación Local (Ollama).
*   `generate_premium_groq_experiments.py`: Pruebas de Juez y Researcher.
*   `consolidate_premium_cases.py`: Unificación de éxitos.

---
**Estado Actual**: Ejecutando Rerun de Mistral Local y preparando escalado de Groq Batch.
