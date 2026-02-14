# 📱 ESPECIFICACIONES DE PRODUCTO FINAL - OPOSITAIA

**Versión:** 1.0 (11 Dic 2025)
**Producto:** OpositaIA - Asistente Inteligente para Oposiciones C1 Seguridad Social

---

## 1. DEFINICIÓN DEL PRODUCTO (PD)

### Visión
Ser la herramienta definitiva de estudio para opositores de la Administración General del Estado (AGE) y Seguridad Social, combinando la precisión de la ley con la flexibilidad de la IA Generativa.

### Propuesta de Valor
*   **Precisión Legal:** Respuestas basadas estrictamente en el BOE y jurisprudencia (RAG).
*   **Personalización:** Generación de simulacros y planes de estudio adaptados al nivel del usuario.
*   **Eficiencia:** Mapas mentales y resúmenes automáticos para acelerar el repaso.
*   **Privacidad:** Arquitectura local/híbrida que protege los datos del usuario.

### Público Objetivo
*   Opositores al Cuerpo Administrativo de la Seguridad Social (C1).
*   Opositores a Gestión de la Seguridad Social (A2).
*   Opositores a Administrativo del Estado (C1).

---

## 2. ESPECIFICACIONES FUNCIONALES (APP)

### Módulo 1: Asistente de Estudio (Chat RAG)
*   **Funcionalidad:** Chat interactivo para resolver dudas legales.
*   **Requisitos:**
    *   Citas precisas de artículos (ej. "Según el Art. 161 de la LGSS...").
    *   Enlace directo a la fuente (PDF/Web BOE).
    *   Modo "Explicación Sencilla" vs "Modo Jurídico".

### Módulo 2: Generador de Simulacros
*   **Funcionalidad:** Creación de exámenes tipo test a medida.
*   **Requisitos:**
    *   Selección de temas (ej. "Solo Título II LGSS").
    *   Selección de dificultad (Fácil, Medio, Difícil).
    *   Corrección justificada con normativa.

### Módulo 3: Mapas Mentales (Visual Study)
*   **Funcionalidad:** Generación de diagramas jerárquicos de leyes.
*   **Requisitos:**
    *   Visualización de estructura (Títulos > Capítulos > Artículos).
    *   Exportación a formato imagen o editable (Mermaid/Excalidraw).

### Módulo 4: Planificador Inteligente
*   **Funcionalidad:** Calendario de estudio dinámico.
*   **Requisitos:**
    *   Adaptación a fecha de examen.
    *   Repaso espaciado (Spaced Repetition) de temas fallados en simulacros.

---

## 3. ESPECIFICACIONES TÉCNICAS (PO)

### Stack Tecnológico
*   **Frontend:** React + Tailwind CSS (SPA).
*   **Backend:** FastAPI (Python 3.12).
*   **Base de Datos:** PostgreSQL (Usuarios, Progreso) + Qdrant (Vectores Leyes).
*   **IA Core:**
    *   **Embeddings:** `pablosi/bge-m3-spa-law-qa-trained-2`.
    *   **LLM:** Mistral 8B (VPS) / Mistral 7B (Local).
    *   **Orquestación:** YAML

### Requisitos No Funcionales
*   **Latencia:** Respuestas de chat < 5 segundos.
*   **Disponibilidad:** 99.9% (VPS).
*   **Seguridad:** Datos en tránsito cifrados (HTTPS). No almacenamiento de datos sensibles en logs.

---

## 4. ROADMAP DEFINITIVO

### Q4 2025: MVP (Consolidación)
*   ✅ Ingesta de leyes principales (Smart Chunking).
*   ✅ RAG funcional (Local/VPS).
*   🔄 Web App CREADA EN FRONTEND!.

### Q1 2026: Beta Cerrada
*   Generación de Mapas Mentales.
*   Dataset de Fine-tuning (1,000 ejemplos).
*   Pruebas con 50 usuarios reales.

### Q2 2026: Lanzamiento v1.0
*   Planificador Inteligente.
*   Suscripción Premium.

---

## 5. ROLES Y RESPONSABILIDADES
*   **Product Owner:** Definición de alcance y prioridades.
*   **Tech Lead:** Arquitectura RAG y selección de modelos.
*   **Frontend Dev:** UX/UI y conexión con API. 
*   **Data Engineer:** Ingesta BOE y calidad de datos (Scraping).
