# 🗂️ PLAN DE REORGANIZACIÓN ROOT DIRECTORY
**Fecha:** 10 Diciembre 2025  
**Objetivo:** Organizar 75 archivos .md del root en estructura temática  
**Estado:** Listo para ejecutar

---

## 📊 PROBLEMA ACTUAL

**Root directory desorganizado:**
- 75 archivos .md sin estructura temática
- Dificultad para encontrar documentación específica
- Mezcla de documentos activos, obsoletos, y de diferentes sprints
- Fechas inconsistentes en nombres (5_DIC, 08_DIC_2025, etc.)

---

## 🎯 ESTRUCTURA PROPUESTA

```
/home/spas/OPOS_GEMINI_1/
│
├─ README.md                              # Mantener en root
├─ INSTALLATION.md                        # Mantener en root
├─ SETUP.md                               # Mantener en root
├─ docker-compose.yml                     # Mantener en root
├─ .gitignore, .env*, metadata.json       # Mantener en root
│
├─ docs/
│  │
│  ├─ 01_arquitectura/                    # Decisiones técnicas y arquitectura
│  │  ├─ ARQUITECTURA_REAL_WSL.md
│  │  ├─ DECISIONES_CLAVE.md
│  │  ├─ ARCHITECTURE.md
│  │  ├─ MULTI_AGENT_ARCHITECTURE.md
│  │  ├─ BOE_API_INTEGRATION.md
│  │  ├─ CREDENTIALS_MANAGEMENT.md
│  │  └─ DATA_MODEL.md
│  │
│  ├─ 02_planes/                          # Planes maestros y roadmaps
│  │  ├─ MEGA_PLAN_ACTUALIZADO_COMPLETO.md
│  │  ├─ ROADMAP_RESUMEN_EJECUTIVO.md
│  │  ├─ PLAN_DESARROLLO_RAG_COMPLETO.md
│  │  ├─ PLAN_AMPLIACION_DATASET_PREMIUM.md
│  │  ├─ PLAN_SPRINT_2_MISTRAL_EVALUACION.md
│  │  └─ PROPUESTA_MULTI_AGENTES_FINETUNING.md
│  │
│  ├─ 03_investigacion/                   # Investigación técnica
│  │  ├─ EMBEDDINGS_FINETUNING_RESEARCH.md
│  │  ├─ ESTRATEGIAS_QDRANT_COMPLETO.md
│  │  ├─ MISTRAL_8B_EVALUATION.md
│  │  ├─ INVESTIGACION_FORMATO_OPOSICIONES_OFICIAL.md
│  │  ├─ INVESTIGACION_TECNICAS_AVANZADAS.md
│  │  ├─ ACTUALIZACION_INVESTIGACION_FREE_TIERS.md
│  │  ├─ ALTERNATIVAS_CLAUDE_DATASET_QA.md
│  │  ├─ RAG_BEST_PRACTICES_NOV2025.md
│  │  ├─ RAG_COST_ANALYSIS.md
│  │  ├─ RAG_INTEGRATION_PLAN.md
│  │  ├─ COMPETITIVE_ANALYSIS.md
│  │  └─ HALLAZGO_BOE_MATERIALES_OPOSICIONES.md
│  │
│  ├─ 04_datasets/                        # Generación y análisis de datasets
│  │  ├─ ESTRATEGIA_DATASET_GENERATION_05.md
│  │  ├─ ANALISIS_CALIDAD_Q&A_PROFUNDO.md
│  │  ├─ ANALISIS_NUEVOS_TIPOS_CONTENIDO.md
│  │  ├─ COMPLETADO_BAJA_COBERTURA_08_DIC_2025.md
│  │  ├─ FINAL_500_PREMIUM_COMPLETADO_08_DIC_2025.md
│  │  ├─ QUICK_START_DATASET_08_DIC_2025.md
│  │  ├─ RESUMEN_GENERACION_BAJA_COBERTURA_08_DIC_2025.md
│  │  ├─ ANALISIS_DATASET_HF_BOE_2024.md
│  │  └─ ESPECS_DATASET_HF_CHAT.txt
│  │
│  ├─ 05_sprints/                         # Documentación de sprints
│  │  ├─ SPRINT_0_AUDIT_5_DIC_2025.md
│  │  ├─ RESUMEN_SPRINT_2_COMPLETADO.md
│  │  └─ (otros sprints completados)
│  │
│  ├─ 06_auditorias/                      # Auditorías y verificaciones
│  │  ├─ AUDITORIA_ESTADO_REAL_Y_CORRECCIONES.md
│  │  ├─ AUDITORIA_ENTORNOS_Y_DEPENDENCIAS.md
│  │  ├─ AUDITORIA_DATOS_FALSOS_COMPLETADA.md
│  │  ├─ AUDITORIA_CODIGO_MUERTO_SOSPECHOSOS.md
│  │  ├─ AUDIT_GROQ_RESPUESTAS_PROBLEMATICAS.md
│  │  ├─ LOCAL_INFRASTRUCTURE_STATUS.md
│  │  ├─ LOCAL_ENV_AUDIT_PORTATIL.md
│  │  └─ VPS_INFRASTRUCTURE_AUDIT.md
│  │
│  ├─ 07_sesiones/                        # Resúmenes de sesiones de trabajo
│  │  ├─ SESION_5_DIC_2025.md
│  │  ├─ SESION_COMPLETA_08_DIC_2025_FINAL.md
│  │  ├─ SESION_DATASET_TEMAS_FALTANTES_08_DIC_2025.md
│  │  ├─ README_SESION_08_DIC_2025.md
│  │  ├─ RESUMEN_SESION_SIMULACRO_08_DIC.md
│  │  ├─ INDICE_SESION_08_DIC_2025.md
│  │  ├─ RESUMEN_EJECUTIVO_08_DIC_2025.md
│  │  ├─ RESUMEN_FINAL_SESION_08_DIC_2025.md
│  │  └─ RESUMEN_FINAL_INGESTA_COMPLETADA.md
│  │
│  ├─ 08_guias/                           # Guías de inicio y uso
│  │  ├─ GUIA_QUICK_START_5_DIC_2025.md
│  │  ├─ GUIA_INICIAR_BACKEND_05_DIC_2025.md
│  │  ├─ GUIA_INICIAR_BACKEND.md
│  │  ├─ INDICE_DOCUMENTACION_5_DIC_2025.md
│  │  ├─ AI_SPECS_QUICKSTART.md
│  │  ├─ README_REPARACIONES_RESUMEN.md
│  │  ├─ GIT_SYNC_MULTI_MAQUINA_GUIA.md
│  │  ├─ SINCRONIZACION_VSCODE_PORTATIL.md
│  │  └─ SCRIPTS_LISTOS_PARA_EJECUTAR.md
│  │
│  ├─ 09_simulacros/                      # Simulacros y exámenes
│  │  ├─ SIMULACRO_COMPLETADO_RESUMEN.md
│  │  ├─ SIMULACRO_COMPLETO_INDICE.md
│  │  ├─ SIMULACRO_GENERACION_GUIA.md
│  │  ├─ RESUMEN_SIMULACRO_GENERADO.md
│  │  └─ UBICACION_SIMULACRO_COMPLETO.md
│  │
│  ├─ 10_memoria/                         # Documentos de estado y memoria
│  │  ├─ MEMORIA_COMPLETA_10_DIC_2025.md
│  │  ├─ ANALISIS_COMPLETO_PROYECTO_10_DIC_2025.md
│  │  ├─ ANALISIS_PRIORIDAD_LEYES_BOE_10_DIC_2025.md
│  │  ├─ RESUMEN_2_MINUTOS.md
│  │  ├─ RESUMEN_COMPLETO_REPARACIONES.md
│  │  ├─ RESUMEN_REPARACIONES_5_DIC_2025.md
│  │  ├─ LISTA_COMPLETA_CAMBIOS.md
│  │  ├─ INDICE_DOCUMENTOS_CREADOS.md
│  │  └─ ACTUALIZACION_DOCS_5_DIC_2025.md
│  │
│  ├─ 11_configuracion/                   # Configuración de herramientas
│  │  ├─ CONFIGURAR_AGENTE_MISTRAL_STUDIO.md
│  │  ├─ AGENTS.md
│  │  ├─ CLAUDE.md
│  │  ├─ GEMINI.md
│  │  ├─ DEEPSEEK_MODIFICACIONES_RESUMEN.md
│  │  ├─ DEEPSEEK_SCRIPT_COMPLETADO.md
│  │  ├─ RESPUESTA_PREGUNTAS_AGENTE.md
│  │  └─ MEJORES_PRACTICAS_globales_09_11.md
│  │
│  ├─ 12_problemas/                       # Análisis de problemas
│  │  ├─ ANALISIS_PROBLEMAS_ENCONTRADOS.md
│  │  ├─ CORRECCIONES_CODIGO_COMPLETADAS.md
│  │  └─ CORRECCION_VERIFICACION_PLAN.md
│  │
│  ├─ 13_formato/                         # Formato y estructura
│  │  └─ FORMATO_OFICIAL_OPOSICIONES_RESUMEN.md
│  │
│  ├─ 14_funciones/                       # Funciones y JSON configs
│  │  ├─ FUNCION_BUSCAR_RAG_QDRANT_MISTRAL.json
│  │  ├─ FUNCIONES_AGENTE_MISTRAL.json
│  │  └─ FUNCIONES_AGENTE_MISTRAL_CORRECTO.json
│  │
│  ├─ archive/                            # Documentos obsoletos (146 archivos)
│  │  ├─ COMMIT_EXITOSO_25_NOV.md
│  │  ├─ MIGRATION_SUMMARY.md
│  │  └─ ...
│  │
│  └─ Iideas_rama_gemini/                 # Ideas y propuestas (70+ archivos)
│     ├─ INVESTIGACION_PRODUCCION_Y_SEGURIDAD.md
│     ├─ PROPUESTAS_IDEAS_DESARROLLO.md
│     └─ ...
│
├─ backend/                               # Código backend
├─ frontend/                              # Código frontend
├─ dataset_generator/                     # Scripts generación datasets
├─ scripts/                               # Scripts auxiliares
└─ ...
```

---

## 🚀 SCRIPT DE REORGANIZACIÓN

### Opción 1: Script Bash (Recomendado)

```bash
#!/bin/bash
# reorganizar_root.sh
# Ejecutar desde: /home/spas/OPOS_GEMINI_1/

echo "🗂️ Reorganizando root directory..."

# Crear estructura de carpetas
mkdir -p docs/01_arquitectura
mkdir -p docs/02_planes
mkdir -p docs/03_investigacion
mkdir -p docs/04_datasets
mkdir -p docs/05_sprints
mkdir -p docs/06_auditorias
mkdir -p docs/07_sesiones
mkdir -p docs/08_guias
mkdir -p docs/09_simulacros
mkdir -p docs/10_memoria
mkdir -p docs/11_configuracion
mkdir -p docs/12_problemas
mkdir -p docs/13_formato
mkdir -p docs/14_funciones

echo "✅ Carpetas creadas"

# 01_arquitectura
mv ARQUITECTURA_REAL_WSL.md docs/01_arquitectura/ 2>/dev/null

# 02_planes
mv MEGA_PLAN_ACTUALIZADO_COMPLETO.md docs/02_planes/ 2>/dev/null
mv ROADMAP_RESUMEN_EJECUTIVO.md docs/02_planes/ 2>/dev/null
mv PLAN_DESARROLLO_RAG_COMPLETO.md docs/02_planes/ 2>/dev/null
mv PLAN_AMPLIACION_DATASET_PREMIUM.md docs/02_planes/ 2>/dev/null
mv PLAN_SPRINT_2_MISTRAL_EVALUACION.md docs/02_planes/ 2>/dev/null
mv PROPUESTA_MULTI_AGENTES_FINETUNING.md docs/02_planes/ 2>/dev/null

# 03_investigacion
mv INVESTIGACION_*.md docs/03_investigacion/ 2>/dev/null
mv ALTERNATIVAS_CLAUDE_DATASET_QA.md docs/03_investigacion/ 2>/dev/null
mv ACTUALIZACION_INVESTIGACION_FREE_TIERS.md docs/03_investigacion/ 2>/dev/null

# 04_datasets
mv ESTRATEGIA_DATASET_GENERATION_05.md docs/04_datasets/ 2>/dev/null
mv ANALISIS_CALIDAD_Q*.md docs/04_datasets/ 2>/dev/null
mv ANALISIS_NUEVOS_TIPOS_CONTENIDO.md docs/04_datasets/ 2>/dev/null
mv COMPLETADO_BAJA_COBERTURA_08_DIC_2025.md docs/04_datasets/ 2>/dev/null
mv FINAL_500_PREMIUM_COMPLETADO_08_DIC_2025.md docs/04_datasets/ 2>/dev/null
mv QUICK_START_DATASET_08_DIC_2025.md docs/04_datasets/ 2>/dev/null
mv RESUMEN_GENERACION_BAJA_COBERTURA_08_DIC_2025.md docs/04_datasets/ 2>/dev/null

# 05_sprints
mv SPRINT_*.md docs/05_sprints/ 2>/dev/null
mv RESUMEN_SPRINT_*.md docs/05_sprints/ 2>/dev/null

# 06_auditorias
mv AUDITORIA_*.md docs/06_auditorias/ 2>/dev/null
mv AUDIT_*.md docs/06_auditorias/ 2>/dev/null

# 07_sesiones
mv SESION_*.md docs/07_sesiones/ 2>/dev/null
mv README_SESION_*.md docs/07_sesiones/ 2>/dev/null
mv RESUMEN_SESION_*.md docs/07_sesiones/ 2>/dev/null
mv INDICE_SESION_*.md docs/07_sesiones/ 2>/dev/null
mv RESUMEN_EJECUTIVO_08_DIC_2025.md docs/07_sesiones/ 2>/dev/null
mv RESUMEN_FINAL_SESION_*.md docs/07_sesiones/ 2>/dev/null
mv RESUMEN_FINAL_INGESTA_COMPLETADA.md docs/07_sesiones/ 2>/dev/null

# 08_guias
mv GUIA_*.md docs/08_guias/ 2>/dev/null
mv INDICE_DOCUMENTACION_*.md docs/08_guias/ 2>/dev/null
mv AI_SPECS_QUICKSTART.md docs/08_guias/ 2>/dev/null
mv README_REPARACIONES_RESUMEN.md docs/08_guias/ 2>/dev/null
mv GIT_SYNC_MULTI_MAQUINA_GUIA.md docs/08_guias/ 2>/dev/null
mv SINCRONIZACION_VSCODE_PORTATIL.md docs/08_guias/ 2>/dev/null
mv SCRIPTS_LISTOS_PARA_EJECUTAR.md docs/08_guias/ 2>/dev/null

# 09_simulacros
mv SIMULACRO_*.md docs/09_simulacros/ 2>/dev/null
mv RESUMEN_SIMULACRO_*.md docs/09_simulacros/ 2>/dev/null
mv UBICACION_SIMULACRO_COMPLETO.md docs/09_simulacros/ 2>/dev/null

# 10_memoria
mv MEMORIA_COMPLETA_*.md docs/10_memoria/ 2>/dev/null
mv ANALISIS_COMPLETO_PROYECTO_*.md docs/10_memoria/ 2>/dev/null
mv ANALISIS_PRIORIDAD_LEYES_BOE_*.md docs/10_memoria/ 2>/dev/null
mv RESUMEN_2_MINUTOS.md docs/10_memoria/ 2>/dev/null
mv RESUMEN_COMPLETO_REPARACIONES.md docs/10_memoria/ 2>/dev/null
mv RESUMEN_REPARACIONES_*.md docs/10_memoria/ 2>/dev/null
mv LISTA_COMPLETA_CAMBIOS.md docs/10_memoria/ 2>/dev/null
mv INDICE_DOCUMENTOS_CREADOS.md docs/10_memoria/ 2>/dev/null
mv ACTUALIZACION_DOCS_*.md docs/10_memoria/ 2>/dev/null

# 11_configuracion
mv CONFIGURAR_AGENTE_MISTRAL_STUDIO.md docs/11_configuracion/ 2>/dev/null
mv AGENTS.md docs/11_configuracion/ 2>/dev/null
mv CLAUDE.md docs/11_configuracion/ 2>/dev/null
mv GEMINI.md docs/11_configuracion/ 2>/dev/null
mv DEEPSEEK_*.md docs/11_configuracion/ 2>/dev/null
mv RESPUESTA_PREGUNTAS_AGENTE.md docs/11_configuracion/ 2>/dev/null
mv MEJORES_PRACTICAS_*.md docs/11_configuracion/ 2>/dev/null

# 12_problemas
mv ANALISIS_PROBLEMAS_ENCONTRADOS.md docs/12_problemas/ 2>/dev/null
mv CORRECCIONES_CODIGO_COMPLETADAS.md docs/12_problemas/ 2>/dev/null
mv CORRECCION_VERIFICACION_PLAN.md docs/12_problemas/ 2>/dev/null

# 13_formato
mv FORMATO_OFICIAL_OPOSICIONES_RESUMEN.md docs/13_formato/ 2>/dev/null

# 14_funciones
mv FUNCION_*.json docs/14_funciones/ 2>/dev/null
mv FUNCIONES_*.json docs/14_funciones/ 2>/dev/null

# Mover a archive (obsoletos)
mv COMMIT_EXITOSO_25_NOV.md docs/archive/ 2>/dev/null
mv MIGRATION_SUMMARY.md docs/archive/ 2>/dev/null

echo "✅ Archivos movidos"

# Generar reporte
echo ""
echo "📊 REPORTE DE REORGANIZACIÓN"
echo "================================"
echo "01_arquitectura:     $(ls docs/01_arquitectura/*.md 2>/dev/null | wc -l) archivos"
echo "02_planes:           $(ls docs/02_planes/*.md 2>/dev/null | wc -l) archivos"
echo "03_investigacion:    $(ls docs/03_investigacion/*.md 2>/dev/null | wc -l) archivos"
echo "04_datasets:         $(ls docs/04_datasets/*.md 2>/dev/null | wc -l) archivos"
echo "05_sprints:          $(ls docs/05_sprints/*.md 2>/dev/null | wc -l) archivos"
echo "06_auditorias:       $(ls docs/06_auditorias/*.md 2>/dev/null | wc -l) archivos"
echo "07_sesiones:         $(ls docs/07_sesiones/*.md 2>/dev/null | wc -l) archivos"
echo "08_guias:            $(ls docs/08_guias/*.md 2>/dev/null | wc -l) archivos"
echo "09_simulacros:       $(ls docs/09_simulacros/*.md 2>/dev/null | wc -l) archivos"
echo "10_memoria:          $(ls docs/10_memoria/*.md 2>/dev/null | wc -l) archivos"
echo "11_configuracion:    $(ls docs/11_configuracion/*.md 2>/dev/null | wc -l) archivos"
echo "12_problemas:        $(ls docs/12_problemas/*.md 2>/dev/null | wc -l) archivos"
echo "13_formato:          $(ls docs/13_formato/*.md 2>/dev/null | wc -l) archivos"
echo "14_funciones:        $(ls docs/14_funciones/*.json 2>/dev/null | wc -l) archivos"
echo ""
echo "Archivos restantes en root:"
ls -1 *.md 2>/dev/null | wc -l

echo ""
echo "✅ Reorganización completada"
```

### Opción 2: Ejecución Manual (Paso a Paso)

```bash
# Crear estructura
cd /home/spas/OPOS_GEMINI_1
mkdir -p docs/{01_arquitectura,02_planes,03_investigacion,04_datasets,05_sprints,06_auditorias,07_sesiones,08_guias,09_simulacros,10_memoria,11_configuracion,12_problemas,13_formato,14_funciones}

# Mover categoría por categoría (ejemplo)
mv MEGA_PLAN_*.md ROADMAP_*.md PLAN_*.md PROPUESTA_*.md docs/02_planes/

# Verificar
ls docs/02_planes/
```

---

## ✅ VERIFICACIÓN POST-REORGANIZACIÓN

### 1. Verificar que README.md permanece en root
```bash
ls -lh /home/spas/OPOS_GEMINI_1/README.md
```

### 2. Contar archivos en cada categoría
```bash
for dir in docs/0*; do
  echo "$dir: $(find $dir -name "*.md" | wc -l) archivos"
done
```

### 3. Verificar archivos restantes en root
```bash
ls -1 *.md | grep -v -E "(README|INSTALLATION|SETUP)" | wc -l
# Debería ser 0 o muy pocos
```

### 4. Generar índice automático
```bash
echo "# Índice de Documentación" > docs/INDICE_COMPLETO.md
echo "" >> docs/INDICE_COMPLETO.md
for dir in docs/0*; do
  echo "## $(basename $dir)" >> docs/INDICE_COMPLETO.md
  ls -1 $dir/*.md | xargs -I {} basename {} >> docs/INDICE_COMPLETO.md
  echo "" >> docs/INDICE_COMPLETO.md
done
```

---

## 📝 ACTUALIZACIÓN DE REFERENCIAS

### Archivos que pueden contener enlaces rotos:
- `README.md` → Actualizar enlaces a documentos movidos
- `INDICE_DOCUMENTACION_5_DIC_2025.md` → Actualizar rutas
- `MEMORIA_COMPLETA_10_DIC_2025.md` → Actualizar rutas

### Ejemplo de corrección:
```markdown
# Antes
[Ver arquitectura](./ARQUITECTURA_REAL_WSL.md)

# Después
[Ver arquitectura](./docs/01_arquitectura/ARQUITECTURA_REAL_WSL.md)
```

---

## 🔄 ROLLBACK (Si algo sale mal)

```bash
# Crear backup antes de reorganizar
cd /home/spas/OPOS_GEMINI_1
tar -czf backup_root_$(date +%Y%m%d_%H%M%S).tar.gz *.md

# Si necesitas revertir
tar -xzf backup_root_YYYYMMDD_HHMMSS.tar.gz
```

---

## 📊 BENEFICIOS ESPERADOS

1. **Navegación mejorada:** Encuentra documentos por categoría en segundos
2. **Reducción de confusión:** Separación clara entre planes, auditorías, sesiones
3. **Mantenibilidad:** Fácil identificar documentos obsoletos en archive/
4. **Onboarding:** Nuevos colaboradores encuentran guías en docs/08_guias/
5. **Git commits:** Más claros con estructura organizada

---

## ⏱️ TIEMPO ESTIMADO

- **Ejecución script:** 30 segundos
- **Verificación:** 5 minutos
- **Actualización de referencias:** 15 minutos
- **Total:** ~20 minutos

---

## 🚦 PRÓXIMOS PASOS

1. **Backup:** Crear backup_root_*.tar.gz
2. **Ejecutar:** Script de reorganización
3. **Verificar:** Contar archivos en cada carpeta
4. **Actualizar:** README.md y documentos índice
5. **Commit:** `git add . && git commit -m "docs: reorganizar root directory en estructura temática"`
6. **Push:** `git push origin main`

---

**FIN DEL PLAN DE REORGANIZACIÓN**

*Este script está listo para ejecutar. Recomiendo hacer backup primero.*
