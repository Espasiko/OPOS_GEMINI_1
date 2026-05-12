# Plan de Diseño: Agente EscritorAIA (Standalone .EXE) — v2.0
## Fecha: 26 de Abril de 2026

## 1. Visión General (Filosofía Karpathy/Wiki-OS)
El sistema evoluciona de ser un simple chatbot con herramientas a ser un **Compilador de Conocimiento Literario**. Siguiendo la idea de Karpathy (llm-wiki), el agente no solo recupera información, sino que **mantiene y construye** un Wiki interconectado en tiempo real.

**Arquitectura de Capas:**
1. **Raw Source (`raw/`):** Capítulos del borrador en búlgaro. Inmutables.
2. **Wiki Literario (`wiki/`):** Páginas de personajes, glosario, lugares y tramas mantenidas por la IA.
3. **Schema (`00_Agentes/`):** Instrucciones y reglas de continuidad (EditorLiterario.md).

## 2. Diagrama de Arquitectura Actualizada

```text
[ OBSIDIAN (BMO Chatbot) ] 
       │ 
       │ (1) Nina escribe en búlgaro: "¿Quién es el guardián de la espada?"
       ▼ 
[ MIDDLEWARE (AgenteEscritor.exe) ]
       │ 
       │ (2) Inyecta el "Hot Cache" (index.md) y el Glosario de términos míticos.
       │ 
       ├──[ TOOL: search_vault ]    ---> Busca en el Wiki literario por "espada".
       ├──[ TOOL: read_chapter ]    ---> Lee el capítulo raw donde aparece la espada.
       ├──[ TOOL: update_wiki ]     ---> Si hay nueva info, actualiza la ficha de la espada.
       │ 
       │ (3) Mistral Large sintetiza la respuesta basándose en el glosario inventado.
       ▼ 
[ OBSIDIAN (BMO Chatbot) ]
       (4) BMO responde en búlgaro: "Здравей Нина! Пазителят е..."
```

## 3. Fases de Desarrollo Actualizadas

### FASE 1: Middleware de Agencia y Idioma
1. **Soporte Búlgaro:** Configuración de Mistral Large para manejar gramática y contexto cultural búlgaro.
2. **Gestión de Glosario:** Herramienta específica para leer y escribir en una nota de glosario centralizada para términos inventados.
3. **Hot Cache (`index.md`):** El middleware mantendrá un índice actualizado de la bóveda para que la IA sepa siempre qué personajes existen sin re-indexar todo cada vez.

### FASE 2: Empaquetado y Seguridad
1. **Limpieza de API Keys:** El sistema se entrega sin llaves. El instalador `.bat` pedirá o guiará al usuario para poner su llave de Mistral en el primer arranque.
2. **Compilación .EXE:** Se compila el middleware con soporte para UTF-8 (Cyrillic) robusto.

### FASE 3: Bóveda de Libros (Nina_Editor)
1. **Perfil Nina_Editor:** Saludo personalizado y rol de editor literario búlgaro.
2. **Estructura Compilada:** Al "Ingerir" un capítulo nuevo, el agente crea automáticamente fichas de personajes nuevos encontrados.

## 4. Próximo Paso
- Probar la herramienta `update_wiki` para asegurar que el agente puede mantener la continuidad sin que el usuario tenga que crear las fichas a mano.
##  5. plan implementacion 26.04.2026 para revisar! 
 Plan de Implementación: Bóveda de Libros (EscritorAIA) + Integración Karpathy
Este plan detalla la configuración de la bóveda de Obsidian para el proyecto del libro en búlgaro, la adaptación de los agentes de BMO y la evolución del plan maestro basado en la filosofía de "Wiki Personal Compilada" de Karpathy.

Situación Real Detectada
Bóveda Actual: Es una estructura limpia con carpetas para agentes, BMO y Copilot, pero sin contenido (capítulos) ni carpeta raw.
Configuración BMO: El perfil actual BMO.md sigue configurado para oposiciones en español.
Middleware: Está configurado para apuntar a un proxy local (localhost:8000).
Tarea 1: Informe de Estructura y Karpathy
1.1 Estructura de la Bóveda BOOK_VAULT_TEST
Carpetas de Agentes: 00_Agentes/ contiene EditorLiterario.md.
Carpetas BMO: BMO/Profiles/ y BMO/Prompts/. El perfil activo es BMO.md.
Capítulos/MDs: Actualmente no existen carpetas de capítulos ni archivos de contenido fuera de los logs de Copilot.
Carpeta Raw: No existe. Se propone crearla siguiendo el modelo de Karpathy.
1.2 Ideas Principales de Karpathy (llm-wiki) y Comentarios
Wiki como Compilado: No usar RAG tradicional (búsqueda de fragmentos), sino hacer que la IA "compile" y mantenga un Wiki de markdown interconectado.
Tres Capas:
raw/: Fuentes inmutables (el borrador sin tocar).
wiki/: Páginas de personajes, temas y mundo mantenidas por la IA.
schema/: Instrucciones de cómo la IA debe operar sobre el wiki.
Hot Cache: Tener un archivo index.md o context.md que la IA lee siempre para no perder el hilo.
Crítica Zettelkasten: Algunos desarrolladores proponen notas atómicas inmutables para evitar que la IA "alucine" al reescribir páginas largas.
Automatización Mecánica: Delegar tareas de fontanería (hashing, listado de archivos) a scripts locales para ahorrar tokens.
Tarea 2: Configuración para Nina (Libro en Búlgaro)
Se creará un nuevo perfil de BMO optimizado para el libro y para la usuaria final.

[NEW] 
Nina_Editor.md
Saludo: "Здравей Нина" (Zdravei Nina) en cirílico.
Idioma: Búlgaro estricto para las respuestas.
Modelo: mistral-large-latest.
Instrucciones: Manejo de glosario de términos míticos/inventados.

Tarea 3: Actualización del Plan Maestro v2.1
[MODIFY] 
25_04_26_plan_agente_escritor.md
- **Arquitectura Karpathy**: Implementada estructura de 3 capas (raw/, wiki/, schema/).
- **Zettelkasten**: Las notas en `wiki/` deben ser atómicas e inmutables (una nota por personaje/término) para prevenir alucinaciones del LLM en documentos largos.
- **Hot Cache**: Uso obligatorio de `index.md` en la raíz como hub de contexto para que el agente mantenga el hilo narrativo sin leer todo el vault.
- **Reporte de Agentes**: Se confirma la instalación de 112 agentes/skills `bmad` en `/home/spas/OPOS_GEMINI_1/.agents/skills/`.

Plan de Verificación
1. **Perfil Nina**: Cargar el perfil `Nina_Editor.md` en BMO (ya configurado como default en data.json).
2. **Saludo**: Verificar que el agente responda con "Здравей Нина!" en búlgaro.
3. **Conexión**: Si persiste el `ERR_CONNECTION_REFUSED`, el usuario debe arrancar el proxy local o configurar su propia API Key de Mistral en la interfaz de BMO (las keys han sido borradas de data.json por seguridad).
4. **Estructura**: Las carpetas `raw/`, `wiki/`, `schema/` y el archivo `index.md` ya han sido creados.
5. **Prompting**: Probar que el agente reconoce términos del glosario inexistentes en el conocimiento general pero definidos en la bóveda.

---

## 6. Hito 27/04/2026 — Compilación a `.exe` standalone

**Objetivo conseguido (FASE 2 del plan):** el proxy ya es un único ejecutable
Windows que Nina puede usar sin Python, sin WSL y sin saber programar.

**Entregable:** `D:\AgenteEscritor_Para_Nina.zip` (17.6 MB) con:

- `AgenteEscritor.exe` (18 MB, PE32+ x86-64, compilado con PyInstaller `--onefile`).
- `.env` con claves reales (Mistral medium + Tavily + Obsidian).
- `1_arrancar.bat`, `2_parar.bat`, `3_verificar.bat` (UX numerada).
- `LEEME.txt` en castellano simple.

**Stack de compilación:** Docker + imagen `batonogov/pyinstaller-windows:latest`
(Wine + Python 3.13 Windows + PyInstaller). Cross-compile desde WSL Linux,
sin tocar nada del host.

**Memoria detallada de la sesión:**
[`27_04_2026_memoria_sesion_nina.md`](./27_04_2026_memoria_sesion_nina.md)
(arquitectura, decisiones, comandos exactos, verificaciones, pendientes).

### 6.1 Las 6 entidades del Plan Serie Turca (21/04/2026) — registradas ✅

Resuelto 27/04/2026: las 6 entidades pendientes correspondían al **Plan Serie
Turca** del 21/04/2026 ([`21_04_2026_PLAN_SERIE_TURCA.md`](./21_04_2026_PLAN_SERIE_TURCA.md)),
que se había quedado solo en disco sin reflejar en el grafo MCP. Saldada esa
deuda de 6 días. Las 6 entidades registradas:

1. **`Plan_Serie_Turca_21_04_2026`** (MasterPlan) — plan maestro 466 líneas,
   Cuerpo Adm SS C1 BOE-A-2025-27158, método NEXO. Evoluciona de
   `Plan_Wiki_NEXO_v5_1` (20/04) añadiendo dimensión narrativa.

2. **`Personajes_Ciclo_Vital_OPOS`** (PedagogicalCharacters) — 6 protagonistas
   con vidas entrelazadas tipo serie turca:

   | Personaje | Edad | Fase vital | Temas |
   |---|---|---|---|
   | Amparo Rodríguez | 23 | Entrada al mercado | 1, 3, 11 |
   | Darío Méndez | 35 | Asalariado con accidente AT | 2, 4, 7, 8 |
   | Pilar Sáez | 42 | Autónoma societaria | 1, 4, 8 |
   | Bartolomé Cañete | 51 | Empresario con impagos | 5, 6, 12 |
   | Carmen Ibáñez | 58 | Despido + jubilación | 9, 10, 11 |
   | Estanislao Vela | 72 | Pensionista | 9, 13, complementos |

   Relaciones familiares: Amparo sobrina de Carmen; Darío trabaja para Bartolomé;
   Pilar abogada-autónoma; Estanislao padre de Bartolomé; Carmen hermana de Darío.

3. **`Arquitectura_3_Capas_Wiki`** (Architecture) — Capa Técnica + Capa Narrativa
   + Capa Práctica, todas interconectadas por wikilinks Obsidian. Implementa
   `Patron_LLM_Wiki_Karpathy` y extiende `Patron_WikiForge_Chavi` con la dimensión
   narrativa.

4. **`Modo_Minimal_Regenerador`** (ProposedFeature) — flag `--minimal` para
   `regenerar_vault_trampas.py`, doble salida `wiki/` (interno) + `wiki_publico_minimal/`
   (publicable). Allowlist 5 campos. Estimado 2 h. Pendiente FASE 2.

5. **`Ideas_Creativas_Wiki_12`** (FeatureBacklog) — 12 ideas (A,B,C,D,E,F,G,H,I,J,L,M),
   omitida K (TTS). Orden de prioridad: G→B→F→I→C→D→J→H→A→E→M→L.

6. **`Estrategia_Diferenciacion_Legal_DM`** (LegalStrategy) — qué SÍ es libre
   (BOE, datos, jurisprudencia) vs qué NO copiar (redacción DM, ejemplos
   inventados, esquemas, tono). Decisión MC MUTUAL pendiente.

**Relaciones MCP creadas:** 18 aristas que conectan estas 6 entidades con
`Plan_Wiki_NEXO_v5_1`, `Trampas_Verificadas_184_19_04_26`, `Catalogo_Trampas_100`,
`Script_regenerar_vault_trampas_v2`, `Skill_WikiForge_OPOS`, `OpositAIA` y
`Sesion_27_04_26_Compilacion_Exe_Nina`.

**Detalle completo:** [`27_04_2026_memoria_sesion_nina.md`](./27_04_2026_memoria_sesion_nina.md) §7.3.