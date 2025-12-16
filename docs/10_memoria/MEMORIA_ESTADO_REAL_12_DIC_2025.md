# MEMORIA DE ESTADO REAL Y ARQUITECTURA HÍBRIDA (12/12/2025)

**Fecha:** 12 de Diciembre de 2025
**Estado:** 🟢 VERIFICADO (Auditoría Técnica)
**Arquitectura:** Híbrida VPS + Cloud Free Tier

---

## 1. 🏗️ ARQUITECTURA DEFINITIVA (CORREGIDA)

Hemos descartado la arquitectura monolítica en VPS. La estrategia "Brownfield" real para OpositAIA aprovecha servicios externos gratuitos para descargar al VPS.

### A. Capa de Datos (Híbrida)
Separamos Vectores de Texto para eficiencia máxima.

1.  **Vectores (Nube): Qdrant Cloud (Free Tier) o Pinecone**
    *   **Función:** Almacena SOLO los embeddings (números) y los IDs.
    *   **Por qué:** Los vectores consumen mucha RAM. Al moverlos a la nube (Free Tier ~1GB), liberamos ~1-2GB de RAM en el VPS.
    *   **Coste:** €0/mes.
2.  **Texto Legal (Local/VPS): PostgreSQL**
    *   **Función:** Almacena el TEXTO completo de leyes, sentencias y contenido.
    *   **Por qué:** El almacenamiento en disco (SSD del VPS) es barato. Guardar texto en Qdrant Cloud encarece o llena el límite rápido.
    *   **Flujo:** El RAG busca IDs en Qdrant (rápido, nube) -> Consulta Texto en Postgres (rápido, local).

### B. Capa de Inteligencia (Inferencia Local)
**"El Cerebro Residente"**

*   **Motor:** Ollama + Mistral 8B (Fine-tuned GGUF q4_k_m).
*   **Ubicación:** VPS (8GB RAM).
*   **Consumo:** ~5-6 GB RAM fijos.
*   **Concepto: ¿Qué es Inferencia?**
    *   "Inferencia" es el acto de **usar** el modelo para responder preguntas.
    *   Para responder instantáneamente (chat), el modelo debe estar cargado en la Memoria RAM permanentemente.
    *   Si lo apagas para ahorrar RAM, cada vez que un usuario hable tardará 14-20 segundos en "despertar" (cargar de disco a RAM). **Por eso el uso de RAM es uso constante.**

### C. Capa de Aplicación (Backend)
*   **FastAPI:** Orquestador ligero (<500MB). Recibe requests, llama a Qdrant (Nube) y Ollama (Local).
*   **MCP (Model Context Protocol):** NO es el backend app. Es el puente para que AGENTES (Kiro, Cursor) administren el sistema desde fuera.

---

## 2. 💎 ESTRATEGIA DE CALIDAD (NEMOTRON)

**¿Cómo aseguramos calidad 99% GRATIS?**

Utilizamos **Nvidia Nemotron-70B-Reward** (API Gratuita).

*   **¿Qué es?** No es un modelo que "sepa leyes". Es un **Juez de Calidad**. Ha sido entrenado para distinguir una respuesta excelente (bien estructurada, útil, clara) de una mala.
*   **¿Cómo funciona?**
    1.  Le envías: `Pregunta` + `Respuesta del Mistral`.
    2.  Devuelve: `Score` (ej: 3.5 sobre 4).
    3.  **Filtrado:** Si el score es bajo (ej: < 0), la respuesta es basura (alucinación, mal formato) y se descarta AUTOMÁTICAMENTE.
*   **Resultado:** Limpiamos el dataset de "ruido" sin leer 5,000 preguntas a mano.

---

## 3. 🚨 ESTADO CRÍTICO ACTUAL

> **PROCESO DE EMBEDDINGS EN CURSO (WSL)**
> *   **Acción:** NO INTERRUMPIR.
> *   **Dato:** Qdrant local (en WSL) está ingiriendo datos.
> *   **Migración:** Cuando termine, NO copiar el índice Qdrant entero al VPS.
>     *   Extraer los vectores -> Subir a Qdrant Cloud.
>     *   Extraer el texto -> Subir a Postgres VPS.

---

## 4. PLAN DE ACCIÓN INMEDIATO (Brownfield Way)

1.  **Dataset (Portátil 16GB):**
    *   Esperar fin de ingesta.
    *   Ejecutar script `verificar_qa_nemotron_reward.py` (Filtrado de Calidad).
    *   Ejecutar Fine-tuning en Portátil (Unsloth). Generar `.gguf`.
2.  **Infraestructura (VPS + Nube):**
    *   Configurar Qdrant Cloud (o Pinecone) Free Tier.
    *   Instalar Postgres en VPS (si no está ya).
    *   Subir `.gguf` al VPS (Ollama).
    *   Desplegar Backend FastAPI conectado a ambos.

Esta arquitectura optimiza cada recurso (RAM, Disco, Nube Gratuita) para lograr coste cero con rendimiento profesional.
