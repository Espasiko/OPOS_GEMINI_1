# 🗺️ PLAN DE DESARROLLO 2026: ESTRATEGIA "SLOW & SOLID"

**Versión:** 1.0 (Borrador Inicial)  
**Fecha:** 1 Enero 2026  
**Objetivo:** Crear la plataforma definitiva de oposiciones (monetizable Día 1, Coste 0, Calidad Suprema).

---

## 🛑 PRINCIPIOS INNEGOCIABLES (User Directive)
1.  **NO CORRER:** La velocidad no importa. La calidad es suprema.
2.  **CERO ALUCINACIONES:** Comprobación paso a paso.
3.  **MONETIZACIÓN DÍA 1:** Packs, Academias, B2B.
4.  **METODOLOGÍA BMAD:** Epics -> Stories -> Tasks -> E2E Tests -> Security -> Deploy.
5.  **DECISIONES INFORMADAS:** Nada de suposiciones.

---

## 1. ⚖️ EVALUACIÓN TECNOLÓGICA (FACT-CHECK)

### A. Frontend: React Desplegado en Vercel vs VPS (Vite)
**El Dilema:** Quieres monetizar desde el Día 1.
*   **Vercel Free Tier:** ❌ **PROHÍBE USO COMERCIAL**. Si cobras por la app, violas los términos. Coste Pro: $20/mes/miembro.
*   **VPS Hostinger (Actual):** ✅ **GRATIS** (Ya pagado). Permite uso comercial ilimitado.

**✅ DECISIÓN: Vite (React SPA) alojado en tu VPS.**
*   **Por qué Vite?** Es más ligero que Next.js para el VPS. Genera archivos estáticos HTML/JS que Nginx sirve sin consumir CPU/RAM del servidor (dejando todo el recurso para Salamandra).
*   **Framework:** React + TypeScript (Estándar industria, compatible con Excalidraw).

### B. Base de Datos: Supabase Free vs Postgres Local
*   **Supabase Free:** 500MB límite. Excelente para empezar rápido (Auth, UI), pero riesgo de límite si creces mucho (logs detallados).
*   **Postgres Local (VPS):** Sin límites (tienes 50GB espacio).

**✅ DECISIÓN: Híbrida Inteligente.**
*   Usar **Supabase** para Auth (Usuarios) y Tablas Core (Pago, Suscripciones) para seguridad.
*   Usar **Postgres VPS** para datos masivos (Logs de chat, historial detallado) para no llenar los 500MB de Supabase.

### C. Herramientas Visuales
*   **Excalidraw:** ✅ Confirmado, existe librería oficial para React (`@excalidraw/excalidraw`). Totalmente integrable.

---

## 2. 🏗️ NUEVA ARQUITECTURA DE AGENTES (YAML)

El sistema no será un script monolítico, sino una orquestación de agentes especializados definidos en YAML system prompt:

```yaml
system:
  orchestrator: "Coordina peticiones y asigna al especialista. Nunca alucina."
  sub_agents:
    - name: "boe_analyst"
      role: "Experto en XML y Metadatos BOE. Analiza sección 'analisis' para vigencia."
      tools: ["xml_parser", "date_comparator"]
    - name: "cosm_generator"
      role: "Generador de Simulacros COSM. Mantiene lógica jurídica, varía datos fácticos."
      strategy: "Template-based variable substitution"
    - name: "visual_thinker"
      role: "Generador de estructuras Mermaid/Excalidraw para Mapas Mentales."
    - name: "quality_gate"
      role: "Auditor Sr. Revisa cada respuesta generada. Bloquea si hay duda."
```

---

## 3. 🛣️ ROADMAP FUNCIONAL (Los 14 Puntos)

Ordenado lógicamente para construir cimientos sólidos antes de decorar.

### FASE 1: CIMIENTOS COMERCIALES & SEGURIDAD (Sprint 1-2)
*   **Objetivo:** Tener una app segura y vendible.
*   **Punto 14 (Backend Tests):** Auditoría completa de tests actuales. Eliminar obsoletos. Crear suite E2E real.
*   **Punto 13 (Monetización/Config):**
    *   Implementar sistema de **Packs** (Stripe Link).
    *   Estrategia BYOK (Bring Your Own Key) bien arquitecturada para usuarios avanzados.
    *   Configuración de usuario robusta.

### FASE 2: EL MOTOR DE CONTENIDO (Sprint 3-5)
*   **Objetivo:** Generar contenido infinito de alta calidad sin coste API excesivo.
*   **Punto 11 (Agente BOE):** Desarrollo del `boe_analyst` que lee los metadatos XML de "analisis" del BOE para detectar derogaciones exactas.
*   **Punto 10 (Simulacros COSM):**
    *   Crear motor de plantillas lógicas.
    *   "Juan robó una manzana" -> "Pedro hurtó una pera" (Mismo delito, distintos datos).
*   **Punto 2 (Generador de Casos):**
    *   Vista dividida (Split View): Enunciado izq / Preguntas der. adaptables, con boton de cerrarlas y activarlas!
    *   Validación con "Criterios Exquisitos".

### FASE 2b: EXÁMENES OFICIALES & ENTRENAMIENTO (Sprint 5b)
*   **Target:** 36 PDFs Oficiales (Ingeniería Inversa del Tribunal).
*   **Pipeline:**
    1.  **Extract & Pair:** OCR + Asociación (Pregunta <-> Respuesta).
    2.  **Enriquecimiento AI (Claude):** Generar explicaciones jurídicas detalladas para cada respuesta correcta ("Training Data").
    3.  **Destino Dual:**
        *   **RAG:** Ingesta en Qdrant (`layer="official_exam"`) para consultas.
        *   **Fine-Tuning:** JSONL para entrenar a Salamandra V2.
*   **Nota:** Esta fase es CRÍTICA para que el modelo "piense" como un examinador oficial.

### FASE 3: HERRAMIENTAS DE ESTUDIO (Sprint 6-8)
*   **Objetivo:** Retención y fidelización del usuario.
*   **Punto 4 (Temario Propio):** Sistema de Ingesta Usuario (RAG personal).
*   **Punto 5 (Mapas Mentales):** Integración Excalidraw editable.
*   **Punto 12 (Formatos):** Todo exportable y editable.
*   **Punto 9 (Flashcards):**
    *   Exportación `.apkg` (Anki real).
    *   Generador de Memes context-aware (Opción "Fun Mode").

### FASE 4: INTELIGENCIA ADAPTATIVA (Sprint 9-11)
*   **Objetivo:** Personalización total.
*   **Punto 6 & 7 (Planificador y Progreso):**
    *   Algoritmo de Repaso Espaciado (SM-2).
    *   Adaptación a fecha examen y disponibilidad horaria.
*   **Punto 1 (Chat V2):** Botón "Feedback" que alimenta la memoria del modelo para futuras respuestas. 

### FASE 5: HERRAMIENTAS AVANZADAS (Sprint 12+)
*   **Objetivo:** Diferenciación mercado.
*   **Punto 8 (Comparador Legal):** Diff visual de versiones legislativas.
*   **Punto 3 (Buscador Web):**
    *   Scraper selectivo (limitado por fecha convocatoria oficial).
    *   Fuentes: BOE, Web Seg. Social, Foros administración y opositores para feedback e ideas de mejora.

---

## 4. 📝 METODOLOGÍA BMAD (MODO DE TRABAJO)

Para cada uno de los puntos anteriores, seguiremos ESTRICTAMENTE este ciclo:
 0. ¡¡¡PRIMERO E IMPORTANTE!!! ¡¡¡averiguar en que carpeta los colocamos para estar accesibles para agente antigravity y bmad a la vez!!!
1.  **Definición (Epic):** Crear documento `.md` describiendo la funcionalidad.
2.  **Arquitectura (Story):** Definir agentes YAML y flujo de datos.
3.  **Seguridad (Simulación):** ¿Cómo podría abusarse de esto? Mitigación.
4.  **Criterios de Aceptación:** Lista checklable de qué define "Estar hecho".
5.  **Desarrollo TDD:** Test primero, código después.
6.  **Verificación E2E:** Usuario simulado prueba todo el flujo.
7.  **Aprobación:** Tú das el OK.

---

## 5. 🚦 SIGUIENTES PASOS INMEDIATOS
 0. ¡¡¡ PRIMERO E IMPORTANTE!!! leer los puntos de investigacion abajo, investigarlos ¡TODOS!, evaluarlos y hacer un plan de acción concretos para implementar los que corresponden.

1.  **Aprobación del Plan:** ¿Estás de acuerdo con usar Vite en VPS (para poder cobrar) y la arquitectura híbrida Supabase/Local?
2.  **Limpieza:** Ejecutar Punto 14. Auditar lo que hay, borrar basura obsoleta.
3.  **Inicio Fase 1:** Definir la Epic de "Infraestructura Base & Monetización".
## para investigar, eveluar e implementar, si cabe ##
1. Hay que investigar si usamos notebook con un conjunto de PDF de leyes o algo parecido, si procede.
2. Investigar los temas que faltan los tratados de Unión Europea código civil y órdenes anuales. 
3. averiguar como mejorar las búsquedas en BOE para el MCP nuestro
4. subir todos los exámenes oficiales y crear temas enteros gratis, inspiradas en los de las academisa, pero con salamandra, comparar y mejorarlas!
5. desarrollar temas enteros para , leer ejemplos por temaa 
6. investigar mapas mentales esquemas temario, conceptos, logica y meterlo todo en un juego con castillos y bibliotecas, conquistando el premio "APROBADO" con gamificación y hacerlo divertido 
7. investigar el seguimiento del progreso del usuario PARA DARLE alertas de lo que debe repasr, cambios impportantes etc.
8. VER como usar las bases de datos y las memorias para que se pueda hacer el seguimiento efectivo. 
9. tenemos fórmulas y podemos crear una calculadora de éxito y nota, está poracer 
10. investigar la competencia en qué formatos entregan sus cosas aparte del vídeo, decidir la IU para los chats con pfd-s y URL-s, mejorando el >IU y UX para ser cómodo y fácil e intuitivo. 
11. investigar cómo hacer aprender mi IA a con los fallos de los usuarios 
12. comprobar si lo ingestado está en UTF-8 correcto con los tildes que antes había problemas 
13. investigar la posibilidad de usar un Excel o ggldrive u otras opciones mejores cuáles son los requisitos y cómo se usa esto para historial de usuario 
14. investigar workers en cloudFlare con Durable objects , mcp, ia etc, no conozco el sistema!!! 
15. También ver cómo preparar los textos para que los dispositivos los puedan leer en voz alta para escucharlo en el coche o en la cocina o donde sea, sin usar la ia de voz!!!
16. Hacer la ventana divivdida en el caso de casos practicos para poder ver a la vez anunciado+preguntas. !
17. Ver como hacer la salamandra que vea lo subrayado por el usuario, o por colores, por ej. verde-explicar termino, rojo - tener cuidado con esta cuestion y ponerla en los flashcards, con un boton flotante al subrayar etc. etc. 
18. leer de nuevo el plan de ideas de brainstorming para meter las mejores practicas oficiales y alternativas de estudio y memorizacion y reinvestigarlo bien!
19. crear ya conjuntos de casos practicos con chat explicativo de IA, tests, simulacros y algunas mapas mentales comunes, esquemas, temas enteros(estos sin chat explicativo) y falshcards todo para evaluar y regalar a los primeros interesados y venderlas ya!!!
20. considerar  extraer con mistral ocr los documentos de /home/spas/OPOS_GEMINI_1/academias ver los temas entero desarrollados las esquema s y otros ficheros que ofrece la competencia y anonimizarlos bien, para poder usar la ia que se inspire en ellos y crea cosas propias buenas utiles y alineados con nuesto modelo de educacion avanzado(mezcla de ideas en el /home/spas/OPOS_GEMINI_1/docs/03_investigacion/BRAINSTORMING_RECOPILACION_IDEAS_12_DIC_2025.md y )! 
21. analisis del mercado: 1. Resumen Ejecutivo y Alcance del Análisis
El presente informe constituye un análisis exhaustivo y pormenorizado del ecosistema competitivo actual en el sector de la preparación de oposiciones en España, con un foco quirúrgico en los Cuerpos Administrativo y de Gestión de la Administración de la Seguridad Social. El objetivo central de esta investigación es validar y diseñar la estrategia de penetración de mercado para una nueva herramienta tecnológica basada en Inteligencia Artificial (IA) "finetuneada" (ajustada específicamente) sobre legislación española, caracterizada por una arquitectura de "cero alucinaciones" y funcionalidades avanzadas de interacción documental (Chat con PDF, mapas mentales generativos, simulacros).
El mercado de las oposiciones en España se encuentra en una encrucijada histórica. La convergencia de una oferta de empleo público masiva —impulsada por la necesidad de relevo generacional en la administración— y la maduración de las tecnologías de procesamiento de lenguaje natural (NLP) ha creado una ventana de oportunidad única. Sin embargo, el análisis de los primeros 20 resultados de búsqueda y la "inteligencia de foros" revela un mercado saturado de soluciones parciales: plataformas de test estáticas que no enseñan, academias tradicionales que no escalan, y herramientas de IA generalistas que "alucinan" y generan inseguridad jurídica.
Este documento, estructurado en siete bloques analíticos, no solo disecciona precios y competidores, sino que profundiza en la psicología del "opositor a la Seguridad Social", un perfil que valora la certeza normativa por encima de la innovación estética. A través de este análisis, se propone una hoja de ruta para desplegar un modelo de negocio SaaS (Software as a Service) con una inversión en marketing inicial de entre 0 y 100 euros, apalancándose en tácticas de guerrilla digital y crecimiento orgánico viral.
2. Contexto del Mercado: El Perfil del Opositor a la Seguridad Social y la Demanda de Certeza
Para entender cómo desbancar a la competencia, primero debemos comprender profundamente al usuario. El opositor a Administrativo (C1) o Gestión (A2) de la Seguridad Social no es un estudiante promedio. Se enfrenta a uno de los temarios más técnicos, volátiles y densos de la Administración General del Estado. La normativa de la Seguridad Social (Ley General de la Seguridad Social, reglamentos de cotización, afiliación, recaudación) es un "organismo vivo" que cambia constantemente.
2.1. La Psicología del Miedo y la Necesidad de Actualización
El análisis de los foros especializados  y las reseñas de competidores  revela que el principal "dolor" (pain point) del usuario no es la dificultad del temario, sino la incertidumbre de la actualización. Un opositor vive con el miedo constante a estudiar una norma derogada.
 * El Factor "BOE": La obsesión por el Boletín Oficial del Estado (BOE) es total. Herramientas que tardan semanas en actualizar sus bases de datos (como se quejan usuarios de GoKoan en las reseñas analizadas) pierden inmediatamente la confianza del usuario.
 * La Demanda de Supuestos Prácticos: A diferencia de otras oposiciones puramente memorísticas, la Seguridad Social exige aplicar la ley a casos reales (cálculo de bases reguladoras, determinación de hechos causantes). Los opositores agotan rápidamente los libros de supuestos de editoriales como MAD o ADAMS y quedan "huerfanos" de material práctico nuevo. Aquí reside una oportunidad crítica para una IA generativa capaz de crear infinitos casos prácticos coherentes.
2.2. La Brecha Tecnológica Actual
El mercado se divide actualmente en dos extremos insatisfactorios:
 * Fiabilidad sin Inteligencia: Plataformas como OpositaTest  ofrecen test actualizados y fiables, pero son herramientas pasivas. No explican por qué más allá de una reseña estática, no adaptan el aprendizaje
 22. Informe Estratégico de Investigación de Mercado: Disrupción mediante Inteligencia Artificial en la Preparación de Oposiciones a la Seguridad Social en España (2026)1. Resumen Ejecutivo y Alcance del AnálisisEl presente informe constituye un análisis exhaustivo y pormenorizado del ecosistema competitivo actual en el sector de la preparación de oposiciones en España, con un foco quirúrgico en los Cuerpos Administrativo y de Gestión de la Administración de la Seguridad Social. El objetivo central de esta investigación es validar y diseñar la estrategia de penetración de mercado para una nueva herramienta tecnológica basada en Inteligencia Artificial (IA) "finetuneada" (ajustada específicamente) sobre legislación española, caracterizada por una arquitectura de "cero alucinaciones" y funcionalidades avanzadas de interacción documental (Chat con PDF, mapas mentales generativos, simulacros).El mercado de las oposiciones en España se encuentra en una encrucijada histórica. La convergencia de una oferta de empleo público masiva —impulsada por la necesidad de relevo generacional en la administración— y la maduración de las tecnologías de procesamiento de lenguaje natural (NLP) ha creado una ventana de oportunidad única. Sin embargo, el análisis de los primeros 20 resultados de búsqueda y la "inteligencia de foros" revela un mercado saturado de soluciones parciales: plataformas de test estáticas que no enseñan, academias tradicionales que no escalan, y herramientas de IA generalistas que "alucinan" y generan inseguridad jurídica.Este documento, estructurado en siete bloques analíticos, no solo disecciona precios y competidores, sino que profundiza en la psicología del "opositor a la Seguridad Social", un perfil que valora la certeza normativa por encima de la innovación estética. A través de este análisis, se propone una hoja de ruta para desplegar un modelo de negocio SaaS (Software as a Service) con una inversión en marketing inicial de entre 0 y 100 euros, apalancándose en tácticas de guerrilla digital y crecimiento orgánico viral.2. Contexto del Mercado: El Perfil del Opositor a la Seguridad Social y la Demanda de CertezaPara entender cómo desbancar a la competencia, primero debemos comprender profundamente al usuario. El opositor a Administrativo (C1) o Gestión (A2) de la Seguridad Social no es un estudiante promedio. Se enfrenta a uno de los temarios más técnicos, volátiles y densos de la Administración General del Estado. La normativa de la Seguridad Social (Ley General de la Seguridad Social, reglamentos de cotización, afiliación, recaudación) es un "organismo vivo" que cambia constantemente.2.1. La Psicología del Miedo y la Necesidad de ActualizaciónEl análisis de los foros especializados 1 y las reseñas de competidores 3 revela que el principal "dolor" (pain point) del usuario no es la dificultad del temario, sino la incertidumbre de la actualización. Un opositor vive con el miedo constante a estudiar una norma derogada.El Factor "BOE": La obsesión por el Boletín Oficial del Estado (BOE) es total. Herramientas que tardan semanas en actualizar sus bases de datos (como se quejan usuarios de GoKoan en las reseñas analizadas) pierden inmediatamente la confianza del usuario.La Demanda de Supuestos Prácticos: A diferencia de otras oposiciones puramente memorísticas, la Seguridad Social exige aplicar la ley a casos reales (cálculo de bases reguladoras, determinación de hechos causantes). Los opositores agotan rápidamente los libros de supuestos de editoriales como MAD o ADAMS y quedan "huerfanos" de material práctico nuevo. Aquí reside una oportunidad crítica para una IA generativa capaz de crear infinitos casos prácticos coherentes.2.2. La Brecha Tecnológica ActualEl mercado se divide actualmente en dos extremos insatisfactorios:Fiabilidad sin Inteligencia: Plataformas como OpositaTest 5 ofrecen test actualizados y fiables, pero son herramientas pasivas. No explican por qué más allá de una reseña estática, no adaptan el aprendizaje y no permiten interrogar al contenido.Inteligencia sin Fiabilidad: Herramientas como ChatGPT o modelos generalistas ofrecen interactividad, pero sufren de "alucinaciones".7 En un contexto legal, una alucinación (inventar un plazo de carencia o un porcentaje de pensión) es fatal. El usuario sabe esto y desconfía de la IA genérica.Su propuesta de valor —una IA que combina la interactividad de los modelos avanzados con la fiabilidad de una base de datos legislativa cerrada ("cero alucinaciones")— ataca directamente este hueco de mercado. No es "otra app de test"; es un tutor jurídico infalible.3. Análisis Granular del Ecosistema Competitivo (Top 20 Resultados)Hemos realizado un barrido exhaustivo de los actores que aparecen en las primeras posiciones de búsqueda y en las conversaciones de las comunidades de opositores. La competencia no es monolítica; se agrupa en distintos clústeres según su propuesta de valor y madurez tecnológica. A continuación, se detalla el análisis de cada competidor relevante, sus precios y sus vulnerabilidades explotables.3.1. Clúster 1: Los Nativos de IA (Competencia Directa Tecnológica)Este grupo representa la amenaza más inmediata en términos de posicionamiento, aunque a menudo carecen de la profundidad vertical en Seguridad Social que su herramienta promete.GoKoanPosicionamiento: Se autodefine como un "método de estudio inteligente" validado científicamente por la Universidad de Valencia.9 No venden "test", venden "planificación y optimización del tiempo".Oferta de Producto:Planificación algorítmica basada en disponibilidad horaria."Tutora Virtual" (Sofía) para dudas básicas.Temario propio y test.Estrategia de Precios: Modelo de suscripción premium, posicionado por encima de las apps de test pero por debajo de las academias presenciales.Trimestral: 135€ (aprox. 45€/mes).Semestral: 240€ (aprox. 40€/mes).Anual: 300€ (aprox. 25€/mes).11Análisis de Vulnerabilidades (Insights de Usuarios):Desactualización: Las reseñas más recientes 3 son devastadoras en este aspecto. Usuarios como "Jartiblita Power" y "Isabel S" denuncian temarios no actualizados y errores en test que el soporte tarda en corregir. Esto indica que su "IA" puede ser más marketing que realidad operativa en la gestión de contenidos.Rigidez: El usuario está atado al temario de GoKoan. No permite subir apuntes propios o legislación externa para ser analizada, lo que limita su utilidad para opositores avanzados que prefieren sus propias fuentes.Typed AI (y similares como Humata/ChatPDF)Posicionamiento: Herramienta de productividad académica basada en documentos.12 "Tu segundo cerebro para estudiar".Oferta de Producto:Chat con PDF.Generación automática de test y flashcards a partir del documento subido.Estrategia de Precios: Modelo SaaS Freemium accesible.Gratuito: Limitado a 3 documentos y 40 páginas.Básico: 8,99€/mes.Premium: 11,99€/mes (Documentos ilimitados).12Análisis de Vulnerabilidades:Generalista: No está entrenada en Derecho Administrativo español. Es un "wrapper" de modelos LLM (probablemente GPT-4 o Claude). Esto significa que si el documento subido es complejo (como la LGSS con sus disposiciones transitorias), la IA tiende a perder contexto o simplificar en exceso.13Falta de Contexto Externo: Solo sabe lo que hay en el PDF. No puede relacionar el artículo 14 de la Constitución con la Ley de Igualdad si no están en el mismo archivo. Su herramienta, al estar "finetuneada" con la legislación española global, puede hacer estas conexiones transversales críticas para supuestos prácticos.Algor EducationPosicionamiento: Enfoque visual y creativo. "Mapas conceptuales con IA".13Oferta de Producto: Transformación de texto a mapas mentales y resúmenes visuales.Estrategia de Precios: Modelo basado en créditos (complejo de entender para el usuario).Básico: ~6,99€/mes.Pro: ~9,99€/mes.Análisis de Vulnerabilidades:Enfoque Escolar: Su estética y funcionalidad están muy orientadas a estudiantes de secundaria o universidad, no al rigor de una oposición del Grupo A2/C1.Superficialidad: Los mapas mentales automáticos de leyes suelen ser deficientes porque las leyes no tienen una estructura narrativa simple, sino jerárquica y llena de excepciones que la IA generalista suele omitir.3.2. Clúster 2: Los Gigantes del Test (Líderes de Volumen y Cuota)Estos competidores definen el precio de referencia (Anchor Pricing) en la mente del consumidor.OpositaTestPosicionamiento: El líder indiscutible del mercado de práctica. "La herramienta que usan 9 de cada 10 opositores".5Oferta de Producto:Base de datos masiva de preguntas actualizadas.Justificación de respuestas (texto estático).Cursos en vídeo (formato tradicional).Estrategia de Precios: Volumen y bajo coste unitario.1 Mes: ~15€ - 20€.6 Meses: ~60€ (10€/mes).12 Meses: ~80€ - 100€ (<7€/mes).16Análisis de Vulnerabilidades:Pasividad: Es un "gimnasio de test". El usuario hace preguntas y ve fallos, pero la plataforma no le "enseña" activamente ni resuelve dudas conceptuales.Falta de IA: No hay personalización real del aprendizaje ni capacidad de diálogo. Es una base de datos SQL robusta, no una IA. Si un usuario no entiende una justificación, está solo.OpoSapiensPosicionamiento: Gamificación móvil. "Juega y aprueba".17Precios: Muy agresivos (Low-cost).Anual: ~80€ (6,60€/mes).16Vulnerabilidades: Se percibe como un complemento ligero, no como una herramienta de estudio central. Insuficiente para la profundidad de los supuestos prácticos de Seguridad Social.3.3. Clúster 3: Las Academias Tradicionales (El "Viejo Mundo")MAD / ADAMS / MasterD / FlouPosicionamiento: "Todo en uno". Seguridad, tutores humanos, temarios físicos.18Precios: Alto ticket.Mensualidades: 90€ - 250€ / mes.Cursos completos: 1.500€ - 3.000€.Análisis de Vulnerabilidades:Precio Desorbitado: En un contexto económico difícil, pagar 150€/mes es una barrera enorme.Obsolescencia Digital: Sus plataformas suelen ser repositorios de PDF arcaicos. La experiencia de usuario es pobre comparada con apps nativas.Ineficiencia: Clases de 4 horas que podrían resumirse en 15 minutos de estudio focalizado con IA.4. Evaluación Comparativa y Estrategia de DiferenciaciónPara visualizar el hueco de mercado, presentamos una matriz comparativa basada en las dimensiones críticas para el opositor de Seguridad Social.CompetidorModelo de PrecioCoste/Mes (Aprox)Chat con DocumentosCalidad Jurídica (IA)Supuestos PrácticosPercepción de UsuarioSu SoluciónSaaS / Freemium12€ - 25€Sí (Avanzado)Alta (Finetuned)Generativo (Infinito)Innovador & SeguroGoKoanSuscripción25€ - 45€NoMedia (Dudosa)EstáticosBueno pero con fallosOpositaTestSuscripción6€ - 15€NoNula (Base Datos)Estáticos (Limitados)Fiable pero básicoTyped AISaaS9€ - 12€Sí (Básico)Baja (Generalista)No especializadoÚtil para resúmenesAcademiasMensualidad100€+NoNulaManuales (Profesor)Caro y rígido4.1. El Problema de las Alucinaciones en IA: Su Gran Ventaja CompetitivaEl mercado teme a la IA por las alucinaciones. Como indican los informes de Kaspersky y expertos en derecho 7, los modelos LLM estándar (GPT-4, Claude) tienden a "inventar" jurisprudencia o mezclar artículos de leyes diferentes cuando no tienen el contexto adecuado ("Source-Reference Divergence").Su Diferencial: Al declarar "Cero Alucinaciones", usted no solo vende una característica técnica, vende paz mental. Debe comunicar que su IA funciona con tecnología RAG (Retrieval-Augmented Generation) estricta: la IA no responde lo que "cree", sino lo que "encuentra" en la legislación oficial cargada.5. Propuesta de Mejoras y Hoja de Ruta de ProductoPara superar a competidores establecidos como OpositaTest (volumen) y GoKoan (tecnología), su producto debe ofrecer funcionalidades que ellos no pueden replicar fácilmente debido a su deuda técnica o modelo de negocio.5.1. Funcionalidad "Killer Feature": El Generador de Supuestos Prácticos InfinitosEl Problema: Los opositores de Seguridad Social temen el segundo examen (práctico). Compran libros de MAD o ADAMS, hacen los 50 supuestos que traen, y se quedan sin material.La Solución: Implementar un módulo donde el usuario configure parámetros:Tipo: Jubilación, Incapacidad, Desempleo, Recaudación.Dificultad: Básica (literalidad) o Compleja (cálculo de bases, lagunas de cotización).Acción: La IA genera un enunciado único, con datos numéricos aleatorios pero coherentes, y —lo más importante— resuelve el caso paso a paso citando los artículos aplicables.Ventaja: Esto convierte su app en una herramienta indispensable, incluso para quienes ya van a una academia.5.2. "Chat con el BOE" (Actualización Radical en Tiempo Real)El Problema: GoKoan tarda en actualizarse. Las academias tardan meses en sacar anexos.La Solución: Su IA debe estar conectada a un feed diario del BOE.Feature: "Alerta de Impacto Legislativo". Cuando el usuario entra, la app le dice: "Ayer se modificó el Art. 10 de la Ley de Clases Pasivas. Tus flashcards y apuntes han sido actualizados automáticamente. ¿Quieres ver un resumen de los cambios?".Ventaja: Convierte la ansiedad por la actualización en una sensación de control absoluto.5.3. Modo "Simulador de Tribunal Oral"El Problema: El estudio solitario atrofia la capacidad de respuesta rápida.La Solución: Utilizar las capacidades de voz de la IA para simular un interrogatorio. La IA hace preguntas cortas de repaso ("Dime los plazos de la Incapacidad Temporal") y evalúa la respuesta hablada del usuario en tiempo real, corrigiendo imprecisiones.5.4. Integración de Mapas Mentales "Vivos"El Problema: Algor crea mapas estáticos.La Solución: Mapas mentales donde cada nodo es interactivo. Si el usuario hace clic en "Prestación por Nacimiento", el nodo se expande mostrando requisitos, cuantía y duración. Si hace clic de nuevo, se genera un mini-test de 5 preguntas solo sobre ese nodo. Es navegación semántica activa.6. Estrategias de Precios y Modelos de NegocioEl modelo de negocio debe romper la barrera de entrada (miedo a probar una IA nueva) y maximizar el valor a largo plazo (LTV). Recomendamos una estrategia híbrida que ataque los puntos débiles de los precios de la competencia.6.1. Psicología de Precios: El "Sweet Spot"El usuario compara precios mentales con dos anclas:Ancla Baja: OpositaTest (10€/mes). "Es barato, pero básico".Ancla Alta: GoKoan/Academias (40€-150€/mes). "Es caro, tiene que ser bueno".Su Precio: Debe situarse en la franja de 15€ - 25€. Suficientemente alto para denotar calidad "Premium AI", pero suficientemente bajo para ser una compra impulsiva comparada con una academia.6.2. Arquitectura de Planes PropuestaPlanPrecio SugeridoPúblico ObjetivoCaracterísticas ClaveEstrategiaPlan "Curioso" (Freemium)0€ (Para siempre)Captación de LeadsChat con Constitución y TREBEP. 10 test/día. Sin subida de PDF propios.Eliminar barrera de entrada. Mostrar la potencia de la IA sin riesgo.Plan "Opositor" (Mensual)14,90€ / mesUsuario OpositaTestChat ilimitado con PDFs. Flashcards ilimitadas. Acceso a toda la legislación SS.Precio de entrada competitivo. Ataca directamente a la base de usuarios de OpositaTest ofreciendo "más por lo mismo".Plan "Plaza" (Trimestral)39,90€ / trimestre (Sale a 13,30€/mes)Usuario ComprometidoIncluye Generador de Supuestos Prácticos. Mapas Mentales Vivos.El "Upsell" natural. Se vende el generador de supuestos como la característica premium.Plan "Vitalicio" (Lifetime Deal)149€ - 199€ (Pago Único)Early AdoptersAcceso de por vida + Actualizaciones futuras.Generación de caja (Cashflow) inmediato para financiar marketing inicial. Crea evangelizadores de marca.6.3. Táctica de "Precios Dinámicos" basada en ConvocatoriasLos opositores funcionan por picos de ansiedad.Oferta "Sprint Final": Cuando salga la fecha de examen en el BOE, lance un "Pack de Repaso Intensivo" de 1 mes por 29€ que incluya simulacros de alta dificultad y predicción de nota. Monetice la urgencia.7. Estrategia de Go-to-Market: Marketing de Guerrilla (Inversión 0€ - 100€)Con un presupuesto limitado, no podemos competir en Google Ads (donde el CPC para "oposiciones" supera los 1-2€). Debemos ganar la batalla en el terreno de la atención orgánica y la confianza comunitaria.7.1. Infiltración en Comunidades (Coste: 0€)Los opositores se organizan en "tribus" digitales cerradas para compartir material y penas.Objetivos: Canales de Telegram como "Administrativos Seguridad Social" 23, grupos de Facebook y foros como BuscaOposiciones.1Táctica del "Regalo Troyano":No entre vendiendo ("probad mi app"). Entre regalando valor.Use su IA para generar un documento de altísimo valor, por ejemplo: "Tabla Comparativa de Plazos de Resolución y Silencios Administrativos en la Seguridad Social - Actualizado 2026".Diseñe este documento en PDF con una marca de agua al pie: "Generado automáticamente con" y un código QR.Distribúyalo gratis en los grupos: "Hola compis, me estaba volviendo loco con los silencios así que me he hecho esta tabla con una IA que chequea la ley. Os la dejo por si os sirve".Resultado: Tráfico cualificado y agradecido. La marca de agua hace el marketing.7.2. Viralidad en Redes Sociales: El Fenómeno "Studygram" (Coste: 0€ - Tiempo)Instagram y TikTok están llenos de "Studygrams" (cuentas de estudio).Estrategia de Contenido: "Cazador de Mitos":Cree vídeos cortos (Reels/TikTok) comparando respuestas.Pantalla partida: A la izquierda, ChatGPT (versión gratis) respondiendo mal a una pregunta trampa de Seguridad Social (alucinando). A la derecha, su IA respondiendo bien y citando el artículo.Mensaje: "¿Sigues fiándote de ChatGPT? Te estás jugando la plaza. Usa una IA entrenada con el BOE".Este tipo de contenido genera miedo (a estudiar mal) y solución (su app) simultáneamente.7.3. Influencers y Micro-Influencers (Presupuesto 100€)No intente contratar a grandes influencers. Vaya a los micro-influencers de nicho (1.000 - 5.000 seguidores) que son opositores reales.Identificación: Busque hashtags como #opozulo #seguridadsocial #oposiciones2026. Cuentas como las mencionadas en los snippets (ej. perfiles tipo "Srta Opositora", "Tiempopapeles" 25).Propuesta de Valor (Barter): Ofrezca una cuenta "Lifetime Pro" gratuita (valor 200€) a cambio de que prueben la herramienta en sus Stories. Para un opositor, ahorrarse el coste de materiales es un incentivo enorme.Sorteo Estratégico (Inversión 50€):Colabore con una cuenta de tamaño medio.Premio: "Pack de Opositor Pro": Su App (1 año gratis) + Unos subrayadores de marca + Una agenda física bonita (coste total material ~30-40€).Requisito: Seguir su cuenta, mencionar a 2 amigos opositores.Esto viraliza su cuenta rápidamente entre el público objetivo exacto.7.4. SEO Programático de "Long Tail" (Coste: 0€ - Tiempo)Las grandes academias pelean por la keyword "Oposiciones Seguridad Social".Usted debe pelear por las dudas específicas. Use su IA para generar cientos de páginas de aterrizaje (Landing Pages) que respondan a preguntas concretas:"Diferencia entre nacimiento y adopción prestación seguridad social""Plazos recurso alzada ley 39/2015 esquema""Test gratis articulo 174 LGSS"Cuando el usuario busque esa duda concreta en Google, llegará a su página, verá la respuesta generada por su IA y un botón: "¿Tienes más dudas como esta? Pregúntale a nuestra IA gratis".8. Conclusión FinalTiene ante sí una oportunidad de mercado clara. El segmento de opositores a la Seguridad Social está infraservido tecnológicamente. Están pagando precios de oro por academias lentas o precios bajos por test estáticos que no enseñan.Su ventaja competitiva no es la IA en sí misma ("everyone has AI"), sino la verticalización (Especialización en Seguridad Social) y la seguridad jurídica (Cero Alucinaciones). Si logra comunicar eficazmente que su herramienta es el único "lugar seguro" para preguntar dudas legales a las 3 de la mañana, ganará el mercado.La estrategia de precios debe ser agresiva al principio (Freemium + Tier bajo) para robar base de usuarios a OpositaTest, y luego usar las funcionalidades avanzadas (Supuestos Prácticos) para aumentar el ticket medio. Con un marketing de guerrilla inteligente, centrado en aportar valor gratuito en comunidades antes de pedir dinero, puede construir una base de usuarios leales y rentables con una inversión de capital mínima.(Nota: Este informe ha sido elaborado sintetizando datos de mercado actuales, análisis de competidores en tiempo real y principios de estrategia de negocio digital, cumpliendo con la extensión y profundidad requerida para la toma de decisiones ejecutivas.)Desarrollo Profundo del Análisis Competitivo y Estratégico (Detalle Exhaustivo)A continuación, se expande cada sección clave para proporcionar la granularidad y el detalle requerido (15.000 palabras) en un formato narrativo continuo, integrando los datos de los snippets de investigación.1. El Paisaje del Mercado: Una Radiografía de la Oposición a la Seguridad SocialLa oposición a la Seguridad Social en España no es meramente un examen; es un ecosistema de alta presión donde convergen la necesidad de estabilidad laboral y la complejidad técnica. Al analizar los datos de las convocatorias recientes y los foros de discusión como BuscaOposiciones 1, observamos un patrón claro: el perfil del aspirante está cambiando. Ya no es solo el recién graduado en Derecho; es también el profesional de 30-40 años que busca reconvertirse desde el sector privado y que exige herramientas eficientes que respeten su tiempo.1.1. La Tiranía del Temario y la Obsolescencia ProgramadaEl temario de Administrativo y Gestión de la Seguridad Social es notoriamente volátil. Las reformas de las pensiones, los cambios en el Ingreso Mínimo Vital o las actualizaciones en los procedimientos administrativos digitales hacen que los libros de texto impresos queden obsoletos a veces antes de llegar a las librerías. Aquí radica la primera gran brecha de mercado: la latencia de actualización.Las academias tradicionales como MAD o ADAMS 26 intentan paliar esto con "campus virtuales" donde suben adendas en PDF, pero la experiencia de usuario es fragmentada. El estudiante tiene que estudiar con un libro lleno de tachaduras y notas adhesivas. Una herramienta digital nativa que actualice el contenido en la fuente (el "código fuente" del estudio) tiene una ventaja logística insuperable.1.2. El "Supuesto Práctico" como Barrera de EntradaEl segundo ejercicio de estas oposiciones es el filtro real. No basta con memorizar; hay que aplicar. Los snippets de foros 1 muestran que muchos opositores aprueban el test teórico gracias a la memorización bruta (ayudados por OpositaTest), pero fracasan en el práctico por falta de comprensión profunda. Las herramientas actuales fallan aquí estrepitosamente. OpositaTest ofrece test, no casos complejos interrelacionados. GoKoan ofrece planificación, pero sus casos prácticos son finitos y estáticos.Su IA, con capacidad de generar escenarios nuevos ad infinitum basados en parámetros legales, ataca directamente el punto de mayor dolor y miedo del opositor.2. Disección Forense de la Competencia (Análisis de los Top 20)Para vencer al enemigo, hay que conocerlo mejor que él mismo. Hemos deconstruido la oferta de los principales actores identificados en la investigación.2.1. GoKoan: El Innovador con Pies de BarroGoKoan 9 ha hecho un excelente trabajo de marketing posicionándose como la alternativa "inteligente". Su promesa de "estudiar menos y aprobar antes" es seductora.Análisis de Producto: Su núcleo es el algoritmo de planificación. El usuario introduce sus horas disponibles y la fecha del examen, y el sistema le dice qué hacer. Esto reduce la carga mental ("decision fatigue") del opositor.La Grieta en la Armadura: Sin embargo, la ejecución del contenido deja que desear según las evidencias recolectadas. Usuarios en Trustpilot y foros 3 reportan errores graves en el contenido legislativo. Una usuaria ("Isabel S") menciona explícitamente haber encontrado "casi 20 fallos en menos de 1 mes" y que al reportarlos, la respuesta fue lenta. Otra usuaria ("Jartiblita Power") canceló su suscripción por "temario que no se actualiza".Implicación para su Estrategia: Esto valida que la tecnología (el algoritmo) sin contenido impecable (la ley actualizada) no retiene al usuario. Su estrategia debe ser inversa: la fiabilidad legislativa es el cimiento; la IA es la herramienta. Usted no debe prometer "magia", debe prometer "verdad jurídica".2.2. OpositaTest: El Gigante DormidoOpositaTest 5 ha mercantilizado (commoditized) el mercado de los test. Han bajado los precios tanto que es difícil competir por precio puro.Análisis de Producto: Su base de datos es inmensa y su sistema de justificación de respuestas es robusto, aunque estático. Tienen una gran comunidad y una marca muy fuerte.La Grieta: Son una herramienta de "fuerza bruta". El usuario hace miles de preguntas para memorizar patrones, pero no necesariamente para entender conceptos. Si un usuario no entiende por qué una respuesta es la C, OpositaTest no puede explicárselo de otra manera. Es un callejón sin salida pedagógico.Implicación: Su IA debe posicionarse como el "Profesor Particular" frente al "Gimnasio" que es OpositaTest. "Usa OpositaTest para sudar, usa nuestra IA para entender".2.3. Typed AI y Herramientas de Chat PDF: La Promesa GenéricaHerramientas como Typed AI 12 están surgiendo con fuerza. Permiten subir temarios y testearse.Análisis de Producto: Son agnósticas al contenido. Sirven igual para estudiar Historia del Arte que Derecho Administrativo.La Grieta: La falta de especialización es su debilidad. La legislación española tiene matices semánticos que un modelo generalista pasa por alto. Por ejemplo, la diferencia entre "silencio administrativo positivo" y "negativo" depende de contextos muy específicos que un PDF aislado puede no contener. Además, su modelo de precios (por documento/página) penaliza al opositor que maneja miles de páginas de BOE.Implicación: Su herramienta debe venir "pre-cargada" con la biblioteca legislativa completa. El usuario no debería tener que buscar y subir la LGSS; ya debe estar ahí, indexada y lista para ser consultada.2.4. Algor Education: La Trampa VisualAlgor 13 atrae a quienes tienen memoria visual.Análisis: Crea mapas bonitos, pero ¿son útiles? En derecho, un mapa mental automático que simplifica demasiado puede inducir a error. Omitir una excepción en una norma puede costar una pregunta de examen.Implicación: Sus mapas mentales deben ser jerárquicos y profundos, no solo estéticos. Deben permitir "zoom in" hasta el nivel del artículo literal.3. La Amenaza de las Alucinaciones y la Arquitectura de ConfianzaEl informe de Kaspersky 7 y los artículos de prensa 8 sobre abogados sancionados por usar ChatGPT destacan el riesgo reputacional y operativo de la IA en el ámbito legal.Para un opositor, usar una IA que alucina es como usar una calculadora que a veces suma mal: inutiliza todo el proceso.3.1. Definición del Problema TécnicoLos Modelos de Lenguaje Grande (LLM) son probabilísticos, no deterministas. Predicen la siguiente palabra más probable. Si no tienen el dato exacto, lo "rellenan" para mantener la coherencia semántica. En una novela, esto es creatividad; en una oposición, es una mentira.3.2. Su Solución: RAG Estricto y TrazabilidadPara superar esto, su arquitectura técnica debe ser transparente en el marketing:Indexación Vectorial: Toda la normativa de Seguridad Social se convierte en vectores buscables.Recuperación (Retrieval): Cuando el usuario pregunta, el sistema busca los fragmentos relevantes.Generación Restringida: El prompt del sistema debe ser: "Responde SOLO usando la información proporcionada en el contexto. Si no está, di 'No lo sé'".Cita de Fuentes: Cada afirmación debe llevar un footnote interactivo.Este enfoque convierte una debilidad de la industria en su mayor fortaleza de venta. Usted no vende "IA mágica", vende "Búsqueda Semántica Infalible".4. Estrategias de Precios: Psicología y Economía del ComportamientoEl análisis de precios de la competencia nos da un rango amplio, desde los ~7€ de OpositaTest hasta los ~250€ de academias como ADAMS.28 ¿Dónde situarse?4.1. El Efecto Decoy (Señuelo)Recomendamos una estructura de tres precios donde el plan intermedio sea el más atractivo.Plan Básico (9€): Muy limitado. Solo para que la gente vea que "existe" una opción barata. Funciona como ancla baja.Plan Pro (19€): El que queremos vender. Incluye todo lo necesario. Al compararlo con los 9€ (que da muy poco) y los 150€ de una academia, parece una ganga.Plan Academia Virtual (49€): Incluye tutorías humanas (si es posible en el futuro) o funcionalidades ultra-premium. Sirve para que el Plan Pro de 19€ parezca barato.4.2. Monetización del Miedo (Micro-transacciones)Además de la suscripción, puede ofrecer "Power-Ups" puntuales:"Pack Simulacro Real": 4,99€. Un examen generado con la misma distribución de temas que la última convocatoria oficial, con cronómetro y corrección analítica. Muchos usuarios gratuitos pagarán este micro-importe antes del examen.5. Marketing de Guerrilla: Ejecución Táctica (0€ - 100€)La clave aquí es el Capital Social sobre el Capital Financiero.5.1. Operación "Robin Hood" en TelegramLos canales de Telegram listados en los snippets (como "Administrativos seguridad social" 23) son ecosistemas cerrados. Si entra vendiendo, le expulsarán.Estrategia: Sea el "héroe" que libera contenido.Use su IA para encontrar contradicciones en temarios populares. Ejemplo: "He visto que en el temario de MAD dicen X sobre la jubilación parcial, pero la ley cambió en enero. Aquí os dejo la corrección con la referencia al BOE".Esto construye autoridad. En su perfil de Telegram, tenga el enlace a su herramienta. La gente hará clic por curiosidad y gratitud.5.2. El Poder de los "Studygrams"Cuentas como @ursula_campos33 o @oposicioneseducacioninfantil 25 tienen una influencia masiva porque muestran la realidad dura del opositor.Estrategia de Acercamiento: No pida publicidad. Pida "ayuda para mejorar".Escriba a estos influencers: "Hola Úrsula, he creado una herramienta para evitar que nos volvamos locos buscando actualizaciones en el BOE. Me gustaría regalártela para que la uses y me digas qué mejorarías. Sin compromiso".Si el producto es bueno (y resuelve un dolor real), lo compartirán orgánicamente porque es contenido útil para su audiencia.5.3. SEO de Contenidos Generados por el Usuario (UGC)Incentive a sus usuarios a compartir sus "Mapas Mentales" generados por su IA.Táctica: "Comparte tu mapa mental de la Ley 39/2015 en Twitter mencionándonos y gana una semana Pro gratis".Esto inunda las redes sociales con capturas de pantalla de su producto, funcionando como prueba social masiva a coste cero.5.4. Optimización de la Conversión (CRO) en la WebSu página de inicio no debe hablar de "IA" o "Algoritmos". Debe hablar de beneficios:Mal: "IA Generativa con RAG y NLP".Bien: "Pregunta cualquier duda legal y obtén respuesta inmediata con el artículo del BOE en la mano. Deja de buscar en Google".Mal: "Generador de test".Bien: "Simula el examen real tantas veces como quieras. Nunca repetirás la misma pregunta".6. Conclusión y Visión de FuturoEl mercado de las oposiciones a la Seguridad Social es el candidato perfecto para la disrupción. Los actores actuales son demasiado lentos (academias) o demasiado superficiales (apps de test). La tecnología de IA "finetuneada" permite, por primera vez, democratizar el acceso a una preparación de calidad "Premium" a un coste marginal.Si ejecuta esta estrategia centrada en la fiabilidad extrema y el marketing de comunidad, no solo capturará a los opositores descontentos de la competencia, sino que expandirá el mercado atrayendo a aquellos que no se atrevían a opositar por miedo a la complejidad del temario. Su herramienta no es solo un facilitador de estudio; es un democratizador del acceso a la función pública.
 22.🎛️ Comparación: Tu setup actual vs Cloudflare Workers AI



Aspecto
Tu setup actual
Cloudflare Workers AI



Latencia
VPS España + API externa
Edge España (30-50ms)


Costo IA
Groq + DeepSeek + Salamandra
Unificado + inteligente routing


Escalabilidad
Limitada por VPS
Ilimitada (serverless)


Chat tiempo real
WebSocket en VPS
WebSocket nativo + global CDN


RAG
Qdrant cloud
Qdrant + Vectorize (más rápido)


Monitoreo
Manual
Dashboard automático



🚀 Plan de migración recomendado:
Fase 1 (Mes 1): Setup básico

Mover frontend a Cloudflare Pages ✅
Crear Worker AI Gateway con routing básico
Conectar Qdrant desde Workers
Migrar usuarios/progreso a PostgreSQL cloud

Fase 2 (Mes 2): Optimización IA

Implementar AI Gateway con múltiples modelos
A/B testing DeepSeek vs Groq vs Salamandra
Métricas de costo y optimización

Fase 3 (Mes 3): Escalado

Migrar BD completa si todo va bien
Optimizar prompts para reducir tokens
Implementar caching inteligente


💡 Ventajas específicas para tu app jurídica:

Razonamiento legal avanzado: DeepSeek R1 para casos complejos
Contexto multi-ley: RAG + Vectorize para respuestas precisas
Chat en tiempo real: WebSocket + Edge para latencia mínima
Costo controlado: AI Gateway para optimización automática
Escalabilidad: De 20 a 1000 usuarios sin cambios
23. idea MMR — ¿Qué es y por qué lo mencioné?

Buena pregunta.

📌 MMR = Maximal Marginal Relevance

Es una técnica de recuperación que evita esto:

devolver 5 chunks del mismo artículo

ignorar otros artículos relevantes

Ejemplo simple

Pregunta:

“Requisitos para jubilación contributiva”

Sin MMR:

art. 205 (5 fragmentos casi iguales)

Con MMR:

art. 205 (requisitos)

art. 206 (anticipada)

art. 208 (coeficientes)

art. 209 (base reguladora)

👉 Resultado: mejor cobertura legal, menos sesgo.
25. lea estos tambien , mas ideas buenas hay!!! /home/spas/OPOS_GEMINI_1/gastos_ tokens/PLANES_2026/arquitectura_final_plataforma_oposiciones.md
/home/spas/OPOS_GEMINI_1/gastos_ tokens/PLANES_2026/checklist_legal_y_tecnica_produccion.md
/home/spas/OPOS_GEMINI_1/gastos_ tokens/GPT_Desarrollo_proyecto_2026.txt
27. /home/spas/OPOS_GEMINI_1/docs/03_investigacion/PARTY_MODE_SCAMPER_ANALYSIS.md hay mas ideas alli!

---

## 28. 📊 RESULTADOS EXAMEN ENERO 2025 (09-01-2026)

### Prueba de Validación Salamandra

| Métrica | Valor |
|---------|-------|
| **Precisión** | 35.7% (25/70 correctas) |
| **Tiempo total** | 7 horas (89 ejecuciones) |
| **Promedio/pregunta** | 4.7 min |
| **VPS** | Sin errores, 100% disponibilidad |

### Hallazgos Críticos
- ⚠️ **Sesgo hacia B:** 42.9% de respuestas
- ⚠️ **RAG insuficiente:** 10 chunks no bastan
- ⚠️ **Duplicados:** 14 preguntas con respuestas variables

### Informes Detallados
- [ANALISIS_POST_EXAMEN_3_TAREAS.md](file:///home/spas/.gemini/antigravity/brain/cbbd51fa-e58b-4fa9-b13f-dcbd5697c4e9/ANALISIS_POST_EXAMEN_3_TAREAS.md)
- [INFORME_RESPUESTAS_ENERO_2025.md](file:///home/spas/.gemini/antigravity/brain/cbbd51fa-e58b-4fa9-b13f-dcbd5697c4e9/INFORME_RESPUESTAS_ENERO_2025.md)
- [LISTA_MDS_SISTEMA_AGENTES.md](file:///home/spas/.gemini/antigravity/brain/cbbd51fa-e58b-4fa9-b13f-dcbd5697c4e9/LISTA_MDS_SISTEMA_AGENTES.md)

### Próximos Pasos (Prioridad Alta)
1. **Mejorar RAG:** 20-30 chunks, re-ranking, hybrid search
2. **Sistema agentes:** Implementar orquestador multi-agente
3. **Fine-tuning embeddings:** Entrenar con pares juridicos
4. **Checkpoint obligatorio:** Cada pregunta (no cada 5)