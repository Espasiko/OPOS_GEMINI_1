# 📚 Índice de Documentación del Proyecto

> Versión inicial generada para orientar a agentes y humanos. Se puede ampliar y modificar libremente.

---

## 1. Documentos núcleo (docs/)

- **[MEGA_PLAN_ACTUALIZADO_COMPLETO.md](./../MEGA_PLAN_ACTUALIZADO_COMPLETO.md)**  
  Plan maestro 16 semanas: RAG 3→4 capas, dataset, fine‑tuning, deploy.
- **[MULTI_AGENT_ARCHITECTURE.md](./MULTI_AGENT_ARCHITECTURE.md)**  
  Diseño de arquitectura multi‑agente y flujos de trabajo.
- **[RAG_BEST_PRACTICES_NOV2025.md](./RAG_BEST_PRACTICES_NOV2025.md)**  
  Mejores prácticas RAG 2025: chunking, CRAG, hybrid search, self‑reflective RAG.
- **[RAG_INTEGRATION_PLAN.md](./RAG_INTEGRATION_PLAN.md)**  
  Plan detallado de integración RAG con backend y Qdrant.
- **[DECISIONES_CLAVE.md](./DECISIONES_CLAVE.md)**  
  Decisiones técnicas críticas consolidadas.
- **[IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)**  
  Estado de implementación y funcionalidades completadas.
- **[LOCAL_INFRASTRUCTURE_STATUS.md](./LOCAL_INFRASTRUCTURE_STATUS.md)**  
  Estado de Qdrant local, Ollama, PostgreSQL, etc.
- **[VPS_INFRASTRUCTURE_AUDIT.md](./VPS_INFRASTRUCTURE_AUDIT.md)**  
  Auditoría VPS Hostinger y opciones de despliegue.
- **[EMBEDDINGS_FINETUNING_RESEARCH.md](./EMBEDDINGS_FINETUNING_RESEARCH.md)**  
  Investigación y decisiones sobre embeddings y fine‑tuning.
- **[TESTING_STRATEGY.md](./TESTING_STRATEGY.md)**  
  Estrategia de testing y cobertura esperada.
- **[COMPETITIVE_ANALYSIS.md](./COMPETITIVE_ANALYSIS.md)**  
  Análisis competitivo frente a soluciones comerciales.
- **[DATA_MODEL.md](./DATA_MODEL.md)**  
  Modelo de datos principal del sistema.
- **[ARCHITECTURE.md](./ARCHITECTURE.md)**  
  Visión general de arquitectura del sistema.
- **[BOE_API_INTEGRATION.md](./BOE_API_INTEGRATION.md)**  
  Uso de APIs oficiales del BOE (legislación, sumarios, documentos).
- **[CREDENTIALS_MANAGEMENT.md](./CREDENTIALS_MANAGEMENT.md)**  
  Gestión de credenciales y buenas prácticas de seguridad.
- **[AI_AGENTS.md](./AI_AGENTS.md)**  
  Visión general de agentes de IA y su rol en el sistema.

- **[LOCAL_ENV_AUDIT_PORTATIL.md](./LOCAL_ENV_AUDIT_PORTATIL.md)**  
  Auditoría del entorno técnico del portátil (CPU/RAM/GPU, Ollama, Docker, Python, Node/pnpm) y recomendaciones.

Para ideas y notas adicionales de diseño: ver carpeta `docs/Iideas_rama_gemini/`.

---

## 2. Archivo histórico / análisis detallados (docs/archive/)

Estos documentos capturan auditorías, planes de distintas fechas y decisiones intermedias. Son valiosos para entender el porqué del plan actual.

### 2.1. RAG, indexación y datasets

- **[DIAGNOSTICO_COMPLETO_RAG_3_CAPAS.md](./archive/DIAGNOSTICO_COMPLETO_RAG_3_CAPAS.md)**  
  Diagnóstico de la arquitectura RAG 3 capas previa.
- **[PLAN_RAG_3_CAPAS_JSON_BOE.md](./archive/PLAN_RAG_3_CAPAS_JSON_BOE.md)**  
  Plan de indexación de leyes y BOE en JSON.
- **[REINDEXACION_IMV_COMPLETADA.md](./archive/REINDEXACION_IMV_COMPLETADA.md)**  
  Informe de reindexaciones previas.
- **[RESUMEN_INDEXACION_COMPLETA_27NOV.md](./archive/RESUMEN_INDEXACION_COMPLETA_27NOV.md)**  
  Estado de indexación antes del mega plan.
- **[INVENTARIO_MATERIALES_ACADEMIA_COMPLETO.md](./archive/INVENTARIO_MATERIALES_ACADEMIA_COMPLETO.md)**  
  Inventario exhaustivo de materiales de academia.
- **[INVENTARIO_MATERIALES_OPOSICIONES_SS.md](./archive/INVENTARIO_MATERIALES_OPOSICIONES_SS.md)**  
  Inventario de materiales de oposiciones SS.
- **[EJEMPLOS_DATASET_FINETUNING.md](./archive/EJEMPLOS_DATASET_FINETUNING.md)**  
  Ejemplos de dataset para fine‑tuning.
- **[PIPELINE_DATASET_QA_MULTIAGENTE.md](./archive/PIPELINE_DATASET_QA_MULTIAGENTE.md)**  
  Pipeline multi‑agente para generación de Q&A.

### 2.2. Arquitectura, agentes y seguridad

- **[DECISIONES_ARQUITECTURA_Y_PLAN_FINAL.md](./archive/DECISIONES_ARQUITECTURA_Y_PLAN_FINAL.md)**  
  Decisiones de arquitectura y plan final previo.
- **[ESTRATEGIA_IMPLEMENTACION_FINAL.md](./archive/ESTRATEGIA_IMPLEMENTACION_FINAL.md)**  
  Estrategia de implementación completa.
- **[GUIA_CONFIGURAR_AGENTE_MISTRAL_CON_QDRANT.md](./archive/GUIA_CONFIGURAR_AGENTE_MISTRAL_CON_QDRANT.md)**  
  Guía para el agente Mistral conectado a Qdrant.
- **[INSTRUCCIONES_AGENTE_MISTRAL_ACTUALIZADO.md](./archive/INSTRUCCIONES_AGENTE_MISTRAL_ACTUALIZADO.md)**  
  Instrucciones actualizadas para el agente Mistral.
- **[SECURITY_AUDIT_REPORT.md](./archive/SECURITY_AUDIT_REPORT.md)**  
  Auditoría de seguridad del sistema.
- **[EVALUACION_HERRAMIENTAS_AUDITORIA_CODIGO.md](./archive/EVALUACION_HERRAMIENTAS_AUDITORIA_CODIGO.md)**  
  Evaluación de herramientas de auditoría de código.
- **[TAREA5_GDPR_Y_LEGISLACION_ESPAÑOLA.md](./archive/TAREA5_GDPR_Y_LEGISLACION_ESPAÑOLA.md)**  
  Consideraciones GDPR y legales.

### 2.3. Infraestructura, despliegue y costes

- **[DEPLOYMENT_AUDIT_REPORT.md](./archive/DEPLOYMENT_AUDIT_REPORT.md)**  
  Auditoría de despliegue y pipelines.
- **[DEPLOYMENT_FIXES.md](./archive/DEPLOYMENT_FIXES.md)**  
  Correcciones aplicadas en despliegue.
- **[ESTRATEGIA_COMPLETA_REDUCCION_COSTES_IA.md](./archive/ESTRATEGIA_COMPLETA_REDUCCION_COSTES_IA.md)**  
  Estrategia de reducción de costes IA.
- **[RAG_COST_ANALYSIS.md](./../docs/RAG_COST_ANALYSIS.md)**  
  Análisis de costes RAG (docs/).

### 2.4. Roadmaps, sprints y resúmenes

- **[ROADMAP_VISUAL_8_SEMANAS.md](./archive/ROADMAP_VISUAL_8_SEMANAS.md)**  
  Roadmap visual previo.
- **[SPRINT8_COMPLETADO.md](./archive/SPRINT8_COMPLETADO.md)** y **SPRINT9/10/11_COMPLETADO.md**  
  Estado de sprints anteriores.
- **[RESUMEN_EJECUTIVO_PLAN.md](./archive/RESUMEN_EJECUTIVO_PLAN.md)**  
  Resumen ejecutivo de planes previos.
- **[RESUMEN_DECISIONES_FINALES_ACTUALIZADO.md](./archive/RESUMEN_DECISIONES_FINALES_ACTUALIZADO.md)**  
  Consolidación de decisiones finales.

> Nota: hay muchos más `.md` en `docs/archive/`. Este índice inicial prioriza los más relevantes para RAG, agentes, seguridad e infraestructura. Se puede ampliar con más secciones o subgrupos.

---

## 3. Cómo usar este índice

- **Para agentes BMAD / LLMs:** usar este archivo como punto de entrada para localizar rápidamente el contexto correcto (plan maestro, decisiones clave, estado de infra, estrategias RAG y seguridad).
- **Para humanos:** empezar por el mega plan y luego ir a las secciones 1 y 2 según la duda (arquitectura, RAG, seguridad, despliegue, datasets...).

---

## 4. Próximas mejoras sugeridas

1. Añadir más documentos de `docs/archive/` con descripciones breves.
2. Crear un `project-context.md` en la raíz que resuma reglas clave y enlace a este índice.
3. Mantener este índice actualizado tras cada gran cambio de arquitectura o plan.
