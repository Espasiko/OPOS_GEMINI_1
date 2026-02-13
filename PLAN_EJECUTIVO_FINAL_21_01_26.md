# 🎯 PLAN EJECUTIVO FINAL - OpositaIA
**Fecha:** 21 de Enero de 2026  
**Versión:** 1.0 - Post-Brainstorming Party Mode  
**Prioridad:** DATASET EXCELENTE para Fine-tuning Salamandra

---

## 📊 PARTE 1: VERIFICACIÓN DEL CÓDIGO REAL

### ✅ Lo que REALMENTE tenemos (verificado en código):

**Backend FastAPI:**
- ✅ 8 routers operativos (rag.py, rag_v2.py, chat.py, ai_functions.py, upload.py, user.py, boe.py, mcp_gateway.py)
- ✅ 9 funciones IA en `/ai/*`:
  1. `/practical-case` - Genera casos prácticos
  2. `/mind-map` - Genera mapas mentales
  3. `/mock-exam` - Genera simulacros (hasta 100 preguntas)
  4. `/flashcards` - Genera flashcards
  5. `/flashcards/export` - Exporta a Anki (.apkg)
  6. `/schema` - Genera esquemas
  7. `/summary` - Genera resúmenes
  8. `/compare` - Compara textos legales
  9. `/study-plan` - Genera planes de estudio

**Qdrant (2 colecciones):**
- ✅ `opositaia_knowledge_v2` - 48,866 chunks con vectores híbridos (Dense 1024D + Sparse BM25)
- ✅ `opositaia_leyes_master` - 54 leyes con metadata completa (SIN chunks, solo referencia)

**Datasets Generados:**
- ✅ ~500 casos prácticos (NO 12k - verificar archivos reales)
- ✅ ~5,000 preguntas tipo test
- ✅ Archivos: MASTER_DATASET_v11, v12_PLATINUM, v12_SUPPLEMENT

**Frontend React:**
- ✅ 20+ componentes operativos
- ✅ Dashboard, casos prácticos, simulacros, mapas mentales, flashcards
- ✅ Integración con backend via backendService.ts

**VPS Hostinger:**
- ✅ Salamandra 7B (Q4_K_M, 4.85 GB)
- ✅ llama-server en puerto 8080
- ✅ Dominio: electroyhogarpelotazo.tienda

**Multi-proveedor LLM:**
- ✅ Groq (Llama 3.3 70B/8B)
- ✅ Gemini (2.5 Pro, Flash)
- ✅ DeepSeek (V3 Reasoner)
- ✅ Mistral (local VPS)

### ❌ Lo que NO tenemos (PostgreSQL eliminado):
- ❌ PostgreSQL - TODO está en Qdrant
- ❌ Sistema de agentes implementado (solo diseñado)
- ❌ Legal Judge operativo
- ❌ Calculadoras SS deterministas

---

## 💡 PARTE 2: 50 MODELOS DE NEGOCIO INNOVADORES

### 🔥 TIER S - Modelos Disruptivos 2024-2026

**Basado en investigación web (fuentes: editorialge.com, ainvest.com, pricingsaas.com)**

#### 1-10: Modelos Basados en Valor (Value-Based)

1. **Pay-per-Outcome** - Pagas solo si apruebas el examen (€0 si suspendes, €200 si apruebas)
2. **Success-Based Pricing** - % del salario del primer año como funcionario (ej: 5% = €1,500)
3. **Confidence Score Pricing** - Precio basado en tu nivel de confianza (Nivel 1: €10/mes, Nivel 5: €50/mes)
4. **Time-to-Approval** - Pagas según cuánto tiempo ahorras (6 meses → €30/mes, 3 meses → €60/mes)
5. **ROI Guarantee** - Garantía de devolución si no mejoras tu score en 30 días
6. **Performance Tiers** - Precio dinámico según tu progreso (mejoras rápido = descuento)
7. **Exam-Pass Insurance** - Seguro de aprobación (€50/mes, reembolso total si no apruebas)
8. **Milestone Payments** - Pagas por hitos (Nivel 1→2: €15, Nivel 2→3: €20, etc.)
9. **Shared Success** - Crowdfunding entre opositores (todos pagan menos si todos mejoran)
10. **Reverse Auction** - Opositores pujan por acceso premium (los más comprometidos pagan más)

#### 11-20: Modelos Basados en Uso (Usage-Based)

11. **Pay-per-Query** - €0.10 por pregunta al tutor IA (paquetes de 100, 500, 1000)
12. **Token-Based** - Compras tokens, cada feature consume tokens (caso: 10 tokens, simulacro: 50 tokens)
13. **Credits System** - Créditos mensuales (100 créditos/mes, rollover permitido)
14. **Time-Based** - Pagas por minutos de uso del tutor IA (€1 por 10 minutos)
15. **Feature Metering** - Cada feature tiene su propio contador (casos ilimitados, simulacros: 10/mes)
16. **Bandwidth Pricing** - Pagas por "ancho de banda de conocimiento" (queries simples baratas, complejas caras)
17. **API Calls** - Modelo para academias: €0.05 por llamada API
18. **Compute Units** - Pagas por poder computacional usado (Legal Judge: 5 units, Chat: 1 unit)
19. **Storage-Based** - Pagas por almacenar tu progreso y materiales (€5/mes por 10GB)
20. **Concurrent Users** - Academias pagan por usuarios simultáneos (10 usuarios: €100/mes)

#### 21-30: Modelos Híbridos Innovadores

21. **Freemium + Ads** - Gratis con anuncios de academias, €15/mes sin ads
22. **Freemium + Data** - Gratis si compartes datos anónimos de estudio (para investigación)
23. **Community-Funded** - Usuarios pagan lo que quieran (mínimo €5/mes)
24. **Sponsor Model** - Empresas patrocinan a opositores (€0 para usuario, empresa paga €50/mes)
25. **Affiliate Revenue** - Gratis, ganas comisión si compran libros/cursos recomendados
26. **White-Label** - Academias pagan €500/mes por versión con su marca
27. **Marketplace** - Plataforma donde profesores venden sus materiales (OpositaIA cobra 20%)
28. **Certification** - Gratis, pero certificado oficial cuesta €50
29. **Premium Content** - Base gratis, contenido premium de expertos (€10/tema)
30. **Tiered Community** - Acceso a comunidad según nivel (Nivel 1: gratis, Nivel 5: €30/mes)

#### 31-40: Modelos B2B/B2G

31. **Enterprise** - Venta a Ministerios/Administraciones (€10k/año por 1000 licencias)
32. **Academia Partnership** - Revenue share 70/30 con academias tradicionales
33. **University Licensing** - Universidades pagan por acceso para estudiantes de Derecho
34. **Government Grant** - Financiación pública como herramienta de empleabilidad
35. **Corporate Training** - Empresas preparan a empleados para oposiciones internas
36. **Consulting** - Asesoría a academias sobre cómo usar IA (€5k/proyecto)
37. **Data Licensing** - Vender datos anónimos de aprendizaje a investigadores
38. **API-as-a-Service** - Otras apps integran tu Legal Judge (€0.10/llamada)
39. **Reseller Program** - Preparadores individuales revenden con comisión (40%)
40. **Franchise Model** - Academias locales usan tu plataforma (€1k setup + €200/mes)

#### 41-50: Modelos Experimentales

41. **NFT Badges** - Badges de logros como NFTs (coleccionables, vendibles)
42. **Gamification Tokens** - Tokens del juego "Castillo de Justicia" (compra/vende en marketplace)
43. **Prediction Market** - Apuestas sobre quién aprobará (OpositaIA cobra comisión)
44. **Crowdsourced Content** - Usuarios crean contenido, ganan % de ventas
45. **Subscription Box** - Caja mensual física con materiales + acceso digital (€40/mes)
46. **Podcast Premium** - Podcast diario gratis, episodios premium €5/mes
47. **Masterclass Series** - Webinars con funcionarios exitosos (€20/webinar)
48. **Mentorship Matching** - Conecta opositores con mentores (OpositaIA cobra €10/match)
49. **Study Buddy** - Matching con compañeros de estudio (premium: €15/mes)
50. **Lifetime Deal** - Pago único €500 por acceso de por vida

---

## 🎯 PARTE 3: PLAN REFINADO (Correcciones Aplicadas)

### Correcciones Críticas del Usuario:

1. ✅ **PostgreSQL eliminado** - Todo en Qdrant (2 colecciones)
2. ✅ **Velocidad ≠ Confianza** - Medir de otra manera
3. ✅ **Solo España** - Olvidar multi-región
4. ✅ **Presupuesto: €10-15/mes por usuario** - No hay dinero para fine-tuning caro
5. ✅ **Calidad y veracidad 97%+** - Requisito único
6. ✅ **COSM Strategy** - Create Once, Serve Many con variaciones
7. ✅ **Módulos separados** - Casos, Simulacros, Tests, Mapas, Temas, Juego, Flashcards
8. ✅ **Pricing estándar rechazado** - Buscar modelos innovadores (ver Parte 2)

### Ideas Validadas por el Usuario:

✅ **Confidence Score System** - Niveles 1-5 (pero medir diferente)
✅ **Legal Logic Explainer** - Estilo Vicente Valera
✅ **COSM API** - Servir casos con variaciones
✅ **Daily Challenge** - Necesita más ejemplos
✅ **Progress Tracker Emocional** - Medir confianza, no solo conocimiento
✅ **Módulos separados** - Cada uno se vende por separado o en pack

### Ideas Rechazadas/Modificadas:

❌ **Velocidad = Confianza** - Incorrecto
❌ **Multi-región EU+LATAM** - Solo España
❌ **Fine-tune €5k-10k** - No hay presupuesto
❌ **Pricing estándar** - Demasiado genérico
⚠️ **Calculadora de plazos** - Opositor debe saber calcular sin IA

---

## 🔬 PARTE 4: CÓMO MEDIR CONFIANZA (Sin velocidad)

### Propuesta de Métricas Alternativas:

**1. Consistencia Temporal**
- Misma pregunta en diferentes momentos → misma respuesta = alta confianza
- Variación en respuestas = baja confianza

**2. Método de Descarte**
- Descarta 2 opciones incorrectas antes de elegir = método maduro
- Elige directamente sin descartar = puede ser azar

**3. Explicación Post-Respuesta**
- Usuario explica por qué eligió esa opción
- IA evalúa la lógica de la explicación
- Lógica correcta aunque respuesta incorrecta = comprensión parcial

**4. Confianza Auto-Reportada**
- Después de responder: "¿Qué tan seguro estás? (1-5)"
- Correlación entre confianza reportada y acierto

**5. Patrón de Cambios**
- Cambia de respuesta antes de confirmar = duda
- Confirma inmediatamente = confianza (o impulsividad)

**6. Contexto de Aprendizaje**
- Primera vez que ve el tema = baja confianza esperada
- Después de 10 casos similares = alta confianza esperada

**7. Transferencia de Conocimiento**
- Acierta en variaciones del mismo concepto = comprensión profunda
- Solo acierta la pregunta exacta = memorización

### Fórmula Propuesta:

```python
def calculate_confidence_score(user_history):
    score = 0.0
    
    # Consistencia (30%)
    consistency = check_consistency_over_time(user_history)
    score += consistency * 0.3
    
    # Método de descarte (20%)
    descarte_usage = check_descarte_method(user_history)
    score += descarte_usage * 0.2
    
    # Explicación lógica (25%)
    logic_quality = evaluate_explanation_logic(user_history)
    score += logic_quality * 0.25
    
    # Auto-reporte (10%)
    self_confidence = get_self_reported_confidence(user_history)
    score += self_confidence * 0.1
    
    # Transferencia (15%)
    transfer = check_knowledge_transfer(user_history)
    score += transfer * 0.15
    
    return min(score, 1.0)  # Normalizar 0-1
```

---

## 🎯 TAREA 2: DATASET EXCELENTE PARA FINE-TUNING SALAMANDRA

### PRIORIDAD ABSOLUTA (según plan línea 1443+)

**Objetivo:** Crear dataset de máxima calidad para fine-tunear Salamandra 7B

**Requisitos:**
1. ✅ 1,000 casos prácticos PERFECTOS con lógica legal impecable
2. ✅ 1,000 preguntas tipo test bien equilibradas
3. ✅ Variedad de tipos: Q&A, lógica, procedimientos, comparaciones
4. ✅ Verificación multi-capa antes de incluir en dataset
5. ✅ Formato para fine-tuning (JSONL con prompt/completion)

### Agentes Asignados para TAREA 2:

**🔬 Dr. Quinn (Problem Solver)** - Coordinador principal
- Diseña el pipeline de generación
- Identifica gaps en el dataset
- Propone mejoras iterativas

**💻 Amelia (Dev)** - Implementación técnica
- Scripts de generación con múltiples LLMs
- Scripts de verificación automática
- Pipeline de consolidación

**🧪 Murat (Test Architect)** - Quality Assurance
- Tests de veracidad legal
- Validación de lógica
- Detección de contradicciones

**🏗️ Winston (Architect)** - Diseño del sistema
- Arquitectura del pipeline
- Optimización de costes
- Escalabilidad

**📋 John (PM)** - Métricas y priorización
- Define KPIs de calidad
- Prioriza tipos de contenido
- Tracking de progreso

---

## 📊 SIGUIENTE PASO INMEDIATO

**¿Qué hacemos AHORA?**

**Opción A:** Implementar Confidence Score System (sin velocidad)
**Opción B:** Crear API COSM para servir casos con variaciones
**Opción C:** Empezar TAREA 2 - Dataset para fine-tuning (PRIORIDAD)
**Opción D:** Diseñar módulos separados (Casos, Simulacros, etc.)
**Opción E:** Investigar modelos de negocio innovadores (de los 50 propuestos)

**Recomendación:** **OPCIÓN C** - TAREA 2 es PRIORIDAD ABSOLUTA según el plan.

---

**Documento creado por:** Party Mode Team (17 agentes BMAD)  
**Coordinador:** BMad Master  
**Fecha:** 21 de Enero de 2026  
**Estado:** Listo para ejecución
