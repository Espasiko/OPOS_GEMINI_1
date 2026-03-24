# Síntesis Consolidada — PLAN DEFINITIVO V13 (OpositAIA)

Este documento es la **ÚNICA FUENTE DE VERDAD** técnica para la V13. Ha sido verificado línea a línea contra el código fuente real del proyecto el **15 de marzo de 2026**, e integra los requisitos del PRD V2, la Estrategia "Quality First" del Dataset Maestro y los últimos avances en la lógica de agentes.

## 1. Visión Estratégica (PMV OpositAIA App)
*   **Proyecto:** Generador masivo de supuestos prácticos (COSMIC) para los 4 cuerpos de la AGE y la Seguridad Social. ES el PMV de una app mucho más extensa.
*   **Meta MVP:** 54.000 preguntas de examen con rigor académico y "trampas" pedagógicas del Método Diego de Miguel.
*   **Vigencia Normativa Estricta:** 04/03/2026 (SS) y fecha de convocatoria oficial (AGE).
*   **Modelo de Negocio:** Trial 1€/3 días y Suscripción Pro 69€/mes (Stripe).

## 2. Roadmap de Evolución
| Fase | Foco | Hitos |
21: | :--- | :--- | :--- |
22: | **Fase 1** | Consolidación (C1 SS) | 100% calculadoras AGE/SS (55), RAG consolidado, Mock tests. |
23: | **Fase 2** | Escalado COSMIC | Pipeline 1→6 formatos, Grafo Neo4j, Repetición Espaciada (SM-2/Leitner). |
24: | **Fase 3** | Monetización y Comunidad | Stripe, PWA, Mini-foro Pro, Expansión a C2/A2. |

## 3. Estrategia de Dataset Maestro "Quality First"
Para alcanzar las 54k preguntas de "Calidad Suprema", se implementa un pipeline de agentes con jerarquía de modelos:

### Arquitectura Jurista Sintético (3 Capas)
1.  **Generador (Bulk):** **DeepSeek-V3** (Eficiencia extrema: ~0.70€ por 5k ítems). Inyección de contexto RAG (BOE API).
2.  **Crítico Jurídico:** **Mistral Large 2** (Analista de excepciones y trampas).
3.  **Juez Final / Casos Complejos:** **Claude 3.5 Sonnet** (Uso de los 5€ de crédito para el 1% de casos dudosos).
4.  **Reward Model:** **Nemotron-4 340B** (Puntuación de calidad CoT y exactitud legal en HF Endpoints).

### Método COSMIC (Create Once, Serve Many)
- **1 Átomo de Conocimiento** → 7 Formatos (Test, Flashcard, Mapa Mental, Caso Práctico, Esquema, Mnemotecnia,Simulacro entero).
- Almacenamiento en **Neo4j** para trazabilidad estructural y seguimiento de progreso de usuarios: `Concepto -> Ley -> Artículo -> Pregunta`.

## 4. Cobertura de Calculadoras (100% Implementado)
Verificadas las **55 calculadoras determinísticas** en `calculos_ss_extended.py` y `calculadora_age.py`.

- **SS:** Jubilación 2026 (Umbral 38.25), DT 34ª, RDL 11/2024 (Jubilación Activa), LO 1/2023 (IT Salud Menstrual), IMV y mas de 20 calculos mas.
- **AGE:** LPAC (Plazos y Silencio), TREBEP (Trienios, Grado, Vacaciones), Gestión Financiera (Nóminas, Dietas, Garantías).

## 5. Estado Actual del Desarrollo (15/03/2026)
El proyecto se encuentra en **Fase de Pruebas Intensivas** utilizando el ecosistema de agentes con los siguientes modelos:
- **Modelos en uso:** DeepSeek (Bulk) y Mistral Large (Crítica/Audit), Groq (gpt sso 120b), y claude 4.6 para mejor calidad o repararaciones de casos creados por modelos menores. Por ahora, 15.03.2026 solo deepseek y mistral se han probado con cierto exito para crear casos con agentes y tools y por separado, sin los roles que les asignaba el plan! 
- **Modelos en espera/descartados:** Gemini (API expirada), Clerk (no usado en estas pruebas), Salamandra/Mel/Newmotron (Descartados).

### Recursos de Referencia (hechos con Claude 4.6 15/03/2026):
- **Prompt Maestro COSMIC:** [prompt_maestro_opositaia_COSMIC.md](file:///home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/prompt_maestro_opositaia_COSMIC.md)
  *   Define la lógica de pipeline IA y las reglas anti-alucinación.
  *   Incluye el **Catálogo de 30 Trampas** más rentables para el examen.
- **Ejemplos de Alta Calidad creados por claude(Método DM):**
  *   [Ejercicio 20: Solar Atlántico SL](file:///home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/ejercicio20_solar_atlantico_v2_claude_bueno.md)
  *   [Ejercicio 21: Cooperativa Maresme Artesanal](file:///home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/ejercicio21_maresme_artesanal_claude-mejor.md)
  *  en  /home/spas/OPOS_GEMINI_1/gastos_ tokens/PLANES_2026/PLAN_DEFINITIVO estan los apendices y los planes hechos con calude y tenemos mas detalles.
  * casos reales de Diego de Miguel con resoluciones, GOLDEN STANDART TOTAL DM: /home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM

## 6. Pipeline IA y Reglas Anti-Alucinación (Zero Hallucination)
- **Lógica:** El LLM **NUNCA** genera números. Extrae parámetros → Ejecuta Python (Precisión `Decimal`) → Narra resultado con cita BOE.
- **Maldad Sistémica:** Trampas numéricas de ±10€ o ±3 meses para forzar el razonamiento del opositor. Implementado según el catálogo de trampas en el [Prompt Maestro](file:///home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/prompt_maestro_opositaia_COSMIC.md). en /home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/12_03_catalogo_trampasYAML.dm_CLAUDE tenemos el catalogo completo y en YAML ESTA: /home/spas/OPOS_GEMINI_1/academias/1_casos_recientes_2026_DM/catalogo_trampas.yaml 
- **Finetuning Local DESCARTADO POR AHORA:** Entrenamiento de Mixtral 8x7B (4-bit QLoRA) en CPU (i7 16GB RAM) con el dataset de 5k ítems supremos.

## 7. Stack Tecnológico (Verificado)
| Componente | Tecnología | Nota |
| :--- | :--- | :--- |
| **Backend** | FastAPI / Python 3.11+ | Operativo |
| **Vector DB** | Qdrant | Colección `FULL_XML` con 25k+ puntos |
| **Graph DB** | Neo4j | Grafo COSMIC (Local Docker) |
| **Frontend** | React 19 + Vite | UI Adaptativa y Repetición Espaciada |
| **Auth** | Clerk | Por integrar (Fase 1) |

---
reciente: AUDITORÍA COMPLETA — RESULTADO DEFINITIVO
6 IDs verificados uno a uno:
ID que me diste¿Correcto?VeredictoID/URL correctoBOE-A-2021-21653❌1 DÍGITO MALBOE-A-2021-21652BOE-A-2022-12482✅Correctohttps://www.boe.es/buscar/act.php?id=BOE-A-2022-12482BOE-A-2023-5364✅Correctohttps://www.boe.es/buscar/act.php?id=BOE-A-2023-5364BOE-A-2023-6945❌ID INVENTADOBOE-A-2023-6967BOE-A-2022-14680✅Correctohttps://www.boe.es/buscar/act.php?id=BOE-A-2022-14680BOE-A-2004-11836✅Correctohttps://www.boe.es/buscar/act.php?id=BOE-A-2004-11836

ERRORES DE CONTENIDO CRÍTICOS — 3 que tenemos que corregir ahora

ERROR 1 — H7 del catálogo: el cambio de base RETA NO es mensual
Lo que teníamos escrito: "solicitud en cualquier día del mes → efectos el 1 del mes siguiente"
INCORRECTO. El RDL 13/2022 establece 6 ventanas bimestrales para cambiar la base de cotización en el RETA. BOE.es Las ventanas son:
Solicitud en...Efectos desde...1 enero – último día febrero1 marzo1 marzo – 30 abril1 mayo1 mayo – 30 junio1 julio1 julio – 31 agosto1 septiembre1 septiembre – 31 octubre1 noviembre ← Javier 18 octubre1 noviembre – 31 diciembre1 enero año siguiente
Esto explica por qué la respuesta oficial del simulacro enero para Javier (solicitud 18 octubre → 1 noviembre) era correcta. Y por qué la respuesta C (1 enero 2027, ventana trimestral antigua) también era una trampa del sistema viejo. Pero yo lo describí mal como "mensual". No es mensual: es bimestral con 6 ventanas.

ERROR 2 — B7 del catálogo: mecanismo de pago de la IT por menstruación incapacitante
Lo que teníamos: "INSS/Mutua paga desde día 1 directamente; sin responsabilidad empresarial (empresa no paga ningún día)"
PARCIALMENTE INCORRECTO. La baja por menstruación incapacitante secundaria genera derecho a prestación desde el mismo día, y el subsidio se abona a cargo de la Seguridad Social; sin embargo, la empresa continúa con la obligación de cotizar desde el inicio de la baja. BOE.es
La respuesta oficial del simulacro DM febrero confirma que el mecanismo es pago delegado: la empresa paga al trabajador (como intermediaria), pero el coste lo soporta el INSS. La clave adicional es que aunque la empresa tenga IT de CC concertada con una mutua, en este caso el coste va al INSS, no a la mutua.
Formulación correcta para el catálogo:

Desde día 1 de la baja
Empresa abona en pago delegado (mecanismo ordinario)
A cargo del INSS (no de la Mutua, aunque la empresa tenga IT-CC con mutua)
Sin carencia
Sin período de espera


ERROR 3 — P2 del catálogo: "el trabajador TP no puede asumir la cuota empresarial desde 2023" — ALCANCE INCORRECTO
El RDL 16/2022 transfiere al empleador la obligación de cotizar en los casos de prestaciones de servicios durante menos de 60 horas mensuales por empleador, obligación que, hasta ahora, asumían los propios trabajadores. Laboral Social
Esta regla aplica exclusivamente al Sistema Especial de Empleados de Hogar, no a los trabajadores a tiempo parcial en general. La entrada P2 que redacté estaba generalizando indebidamente.

ERROR 4 — RDL 2/2023: la DT 34ª no contiene lo que dijimos
Lo que teníamos: "DT 34ª TRLGSS (RDL 2/2023): 302 mejores bases de los últimos 304 meses, divisor 352,33"
Esto es parcialmente correcto en la fórmula, pero la fuente es errónea. La DT 34ª de la Ley 21/2021 regula los coeficientes para pensiones que superan el tope máximo en jubilación anticipada voluntaria. La nueva regla de 302 bases / 352,33 la introduce el RDL 2/2023 en el Art. 209.1 TRLGSS y la nueva DT 40ª, aplicable desde el 1 de enero de 2026. Desde el 1 de enero de 2026: la base reguladora de la pensión de jubilación será el resultado de dividir entre 352,33 la suma de las 302 bases de cotización de mayor importe comprendidas dentro del período de los 304 meses inmediatamente anteriores al mes previo al del hecho causante. BOE.es

TABLA FINAL — URLs BOE VERIFICADAS Y VIGENTES
LeyID BOE correctoURL verificadaEstadoLey 21/2021 (reforma pensiones)BOE-A-2021-21652boe.es/buscar/act.php?id=BOE-A-2021-21652✅ Vigente (modificada por RDL 2/2023)RDL 13/2022 (ingresos reales RETA)BOE-A-2022-12482boe.es/buscar/act.php?id=BOE-A-2022-12482✅ Vigente, 6 ventanas bimestralesLO 1/2023 (salud reproductiva, IT)BOE-A-2023-5364boe.es/buscar/act.php?id=BOE-A-2023-5364✅ Vigente (DF 3ª en vigor desde 01/06/2023)RDL 2/2023 (mejora pensiones, DT 40ª)BOE-A-2023-6967boe.es/buscar/act.php?id=BOE-A-2023-6967✅ Vigente, 302 bases desde 01/01/2026RDL 16/2022 (empleadas hogar)BOE-A-2022-14680boe.es/buscar/act.php?id=BOE-A-2022-14680✅ Vigente, solo SE HogarRD 1415/2004 (recaudación SS)BOE-A-2004-11836boe.es/buscar/act.php?id=BOE-A-2004-11836✅ Vigente (muy modificado, usar consolidado)
3 CORRECCIONES URGENTES EN LOS CATÁLOGOS
EntradaCorrecciónH7"6 ventanas BIMESTRALES (no mensual): oct → nov; nov-dic → enero; etc."B7"Empresa abona en PAGO DELEGADO (no el INSS directamente). Coste a cargo del INSS (no de la Mutua)."P2"Aplica SOLO al Sistema Especial de Empleados de Hogar con <60h/mes. No es regla general TP."

## 8. Hitos del 15 de Marzo de 2026 (Bmad Agent)
- **Ingesta Real de Alta Fidelidad:** Completada la indexación de las 6 leyes críticas con metadatos extendidos (`vigencia_texto`, `notas_articulo`, `metadata_xml_dump`) y campos de compatibilidad (`ley_id`, `bloque`, `cuerpos`, `texto`).
- **Correcciones Normativas:** Sincronizados los calculadores en `calculos_ss_extended.py`:
    - RETA: Restauradas 6 ventanas bimestrales (RDL 13/2022).
    - IT Menstruación: INSS 60% desde día 1, pago delegado (LO 1/2023).
    - BR Jubilación: Divisor 352,33 para 302 mejores bases (RDL 2/2023).
- **Inventario Actualizado:** Corregidos IDs oficiales en el archivo de 79 Leyes.

---
**Firma:** Antigravity (Bmad Agent)
