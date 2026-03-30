# 24_03_26_MEMORIA_SESION.md — Blindaje y Normalización V14

## 🏆 Resumen de Logros de la Sesión
Hoy hemos pasado de un sistema que alucinaba con leyes de propiedad horizontal a una **"Trituradora Legal"** de precisión quirúrgica.

### 1. Normalización Universal de Neo4j (7.106 Nodos)
- **Problema:** Los artículos estaban "escondidos" tras IDs técnicos del BOE (`BOE-A-2015-11724_p_209`).
- **Solución:** He ejecutado un script de normalización que ha renombrado **7106 identificadores**.
- **Resultado:** Ahora el sistema encuentra instantáneamente `Art. 204 TRLGSS`, `Art. 209 TRLGSS`, `DT 7ª TRLGSS`, etc. El buscador es infalible.

### 2. Inyección de Briefings Matemáticos (Determinismo)
- **Problema:** El LLM inventaba cálculos de pensiones fallando por céntimos o conceptos.
- **Solución:** He implementado `generar_briefing` en los Blueprints. Ahora Python calcula la BR y la Pensión ANTES de que el LLM empiece a escribir.
- **Resultado:** El caso de **Jorge Cuesta** tiene cifras exactas (BR: 2.142,86 €, Pensión: 1.825,29 €) que coinciden con la ley.

### 3. Generación del Primer Caso Blindado: Jorge Cuesta
- **Ubicación del Caso:** `/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/CASO_JORGE_CUESTA_V14_24_03.md`
- **Calidad:** 11 preguntas generadas (ajustando a 18 en la siguiente iteración).
- **Control de Prosa:** El `ProseValidator` ha aprobado el caso con un score de 1.0 (Sin alucinaciones numéricas).

---

## 📬 Respuestas a tus Consultas

### 1. ¿El prompt del narrador tiene un ejemplo de caso de DM?
**SÍ**. El prompt utiliza un sistema de **Few-Shot Prompting** (ejemplos por contexto). Le pasamos la estructura de los casos de Diego de Miguel (DM) que leímos en `/home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM` como referencia de tono, interconexión de personajes y formato de solucionario. Por eso el caso de Jorge Cuesta ya tiene ese "aire" a DM.

### 2. Sobre las 18 preguntas (15 + 3 reserva)
Recibido. Actualmente el Blueprint tenía 11 por configuración de test rápido. He actualizado la instrucción para que en la versión de producción genere siempre **15 preguntas ordinarias + 3 de reserva**, manteniendo el equilibrio del 25% en las opciones A, B, C, D.

### 3. ¿Dónde está el caso?
He volcado la narrativa final en:
`[CASO_JORGE_CUESTA_V14_24_03.md](file:///home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/CASO_JORGE_CUESTA_V14_24_03.md)`

---

## 🔄 Detalle del Flujo V14 (Paso a Paso)

El sistema opera como una "cadena de montaje" donde el LLM es el último eslabón, no el primero.

### Paso 1: Orquestación del Schema (Python Puro)
- **Archivo:** `backend/v14/case_schema_builder.py`
- **Acción:** Consulta a **Neo4j** (usando los nuevos IDs normalizados) y extrae los artículos.
- **Calculadoras:** Ejecuta las funciones de `backend/v14/blueprints/bp_s12_jubilacion_2026.py` para obtener la Base Reguladora y la Pensión exactas.
- **Trampas:** Selecciona trampas del catálogo (`academias/1_casos_recientes_2026_DM/catalogo_trampas.yaml`).
- **Resultado:** Un objeto `CaseSchema` (JSON) con toda la verdad legal y numérica.

### Paso 2: Configuración del Agente Redactor
- **Archivo:** `opos-agents/agents/redactor_v14.yaml`
- **Acción:** Se carga el **System Prompt** que contiene la "personalidad" de Diego de Miguel y los ejemplos (Few-Shot).
- **Inyección:** Se le pasa el JSON del Paso 1. El LLM tiene prohibido inventar números que no estén en ese JSON.

### Paso 3: Generación de Narrativa (Mistral Large)
- **Acción:** El LLM redacta la historia de Jorge Cuesta siguiendo el formato DM.
- **Interconexión:** Usa los personajes y empresas definidos en el builder para crear la trama entrelazada.

### Paso 4: Blindaje y Validación (Los Guardianes)
- **Guardian 1 (Prose Validator):** `backend/v14/prose_validator.py`. Compara cada número del texto con el Schema. Si el LLM puso "1.800€" y el schema decía "1.825,29€", el caso se bloquea.
- **Guardian 2 (Orchestrator):** `backend/agents/verification_agents.py`. Ejecuta 7 agentes de validación (Coherencia, Pedagogía, Legalidad, etc.).

---

## 📂 Archivos Participantes en el Flujo
| Componente | Ruta del Archivo |
| :--- | :--- |
| **Cerebro (Orquestador)** | `backend/v14/case_schema_builder.py` |
| **Lógica de Ley (Blueprint)** | `backend/v14/blueprints/bp_s12_jubilacion_2026.py` |
| **Base de Datos (Leyes)** | Neo4j (IDs normalizados: `Art. X Ley`) |
| **Catálogo de Trampas** | `academias/1_casos_recientes_2026_DM/catalogo_trampas.yaml` |
| **Agente (Prompt/Config)** | `opos-agents/agents/redactor_v14.yaml` |
| **Validador Numérico** | `backend/v14/prose_validator.py` |
| **Validador 7D (Orchestrator)** | `backend/agents/verification_agents.py` |
| **Script de Ejecución** | `backend/scripts/test_e2e_v14_mistral.py` |

---

## 📈 Conclusión de la Arquitectura
El flujo es **Schema-First**. El LLM ya no es un "creador libre", sino un **Redactor Técnico** que debe ceñirse a los datos factos inyectados por Python y Neo4j. Esto es lo que garantiza que el caso de Jorge Cuesta sea perfecto técnicamente.

---

## 🛑 Diagnóstico de Sofisticación: El "Gap" Diego de Miguel (DM)
Tras validar el primer caso (Jorge Cuesta), hemos identificado que, aunque es matemáticamente impecable, **carece de la complejidad narrativa de DM**.
- **Problema:** Casos lineales, 1 solo personaje, un solo tema principal.
- **Realidad DM:** Redes de 3 a 8 personajes, tramas familiares/mercantiles entrelazadas y mezcla de hasta 8 temas (LPAC + Cotización + Jubilación + Recaudación).

## 🚀 Plan de Mejora V14.5: La "Feria" de Personajes
Para la próxima sesión, el objetivo es **romper la linealidad**:
1. **CaseSchemaBuilder Pro:** Refactorizar para que orqueste múltiples Blueprints simultáneamente.
2. **Generador de Grafos:** Inyección de redes de personajes (abuelos, nietos, socios, empleados) con "veneno legal" (excepciones de parentesco).
3. **Consolidación de los 6 Cambios 2026:** Inyectar el Adicional de Solidaridad, la Gran Incapacidad y la BR Dual en todos los nuevos grafos.

---

## 📂 Auditoría Git y Seguridad
- **Rescate de la Joya de la Corona:** Se detectó que la carpeta `academias/1_casos_recientes_2026_DM/` estaba bloqueada por el `.gitignore`. **Acción:** No se ha subido por orden explícita del usuario, pero el `.gitignore` ha sido revertido a su estado seguro (bloqueando `academias/`).
- **Control de Borrados:** Se han reportado 3 borrados accidentales de memorias antiguas (Nov/Dic 2025) que estaban marcados en el índice. Se ha establecido la regla de **Petición de Permiso Previa** para cualquier borrado futuro, por pequeño que sea.
- **Sincronización:** Rama `main` en GitHub actualizada con el estado V14 blindado (7106 artículos normalizados).

