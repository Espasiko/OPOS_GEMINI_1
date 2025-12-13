#!/bin/bash
# reorganizar_root.sh
# Fecha: 10 Diciembre 2025
# Propósito: Reorganizar 75 archivos .md del root en estructura temática
# Ejecutar desde: /home/spas/OPOS_GEMINI_1/
# Uso: bash reorganizar_root.sh

set -e  # Salir si hay errores

echo "🗂️  REORGANIZACIÓN ROOT DIRECTORY - OpositaIA"
echo "==========================================="
echo ""

# Crear backup
BACKUP_FILE="backup_root_$(date +%Y%m%d_%H%M%S).tar.gz"
echo "📦 Creando backup: $BACKUP_FILE"
tar -czf "$BACKUP_FILE" *.md *.json 2>/dev/null || echo "⚠️  Algunos archivos no se pudieron respaldar"
echo "✅ Backup creado: $BACKUP_FILE"
echo ""

# Crear estructura de carpetas
echo "📁 Creando estructura de carpetas..."
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
echo "✅ Estructura creada"
echo ""

# Función para mover archivos con reporte
move_file() {
  local file="$1"
  local dest="$2"
  if [ -f "$file" ]; then
    mv "$file" "$dest/" 2>/dev/null && echo "  ✓ $file → $dest/"
  fi
}

# 01_arquitectura
echo "📂 Moviendo archivos de ARQUITECTURA..."
move_file "ARQUITECTURA_REAL_WSL.md" "docs/01_arquitectura"

# 02_planes
echo "📂 Moviendo archivos de PLANES..."
move_file "MEGA_PLAN_ACTUALIZADO_COMPLETO.md" "docs/02_planes"
move_file "ROADMAP_RESUMEN_EJECUTIVO.md" "docs/02_planes"
move_file "PLAN_DESARROLLO_RAG_COMPLETO.md" "docs/02_planes"
move_file "PLAN_AMPLIACION_DATASET_PREMIUM.md" "docs/02_planes"
move_file "PLAN_SPRINT_2_MISTRAL_EVALUACION.md" "docs/02_planes"
move_file "PROPUESTA_MULTI_AGENTES_FINETUNING.md" "docs/02_planes"

# 03_investigacion
echo "📂 Moviendo archivos de INVESTIGACIÓN..."
for file in INVESTIGACION_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/03_investigacion"
done
move_file "ALTERNATIVAS_CLAUDE_DATASET_QA.md" "docs/03_investigacion"
move_file "ACTUALIZACION_INVESTIGACION_FREE_TIERS.md" "docs/03_investigacion"

# 04_datasets
echo "📂 Moviendo archivos de DATASETS..."
move_file "ESTRATEGIA_DATASET_GENERATION_05.md" "docs/04_datasets"
move_file "ANALISIS_CALIDAD_Q&A_PROFUNDO.md" "docs/04_datasets"
move_file "ANALISIS_NUEVOS_TIPOS_CONTENIDO.md" "docs/04_datasets"
move_file "COMPLETADO_BAJA_COBERTURA_08_DIC_2025.md" "docs/04_datasets"
move_file "FINAL_500_PREMIUM_COMPLETADO_08_DIC_2025.md" "docs/04_datasets"
move_file "QUICK_START_DATASET_08_DIC_2025.md" "docs/04_datasets"
move_file "RESUMEN_GENERACION_BAJA_COBERTURA_08_DIC_2025.md" "docs/04_datasets"

# 05_sprints
echo "📂 Moviendo archivos de SPRINTS..."
for file in SPRINT_*.md RESUMEN_SPRINT_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/05_sprints"
done

# 06_auditorias
echo "📂 Moviendo archivos de AUDITORÍAS..."
for file in AUDITORIA_*.md AUDIT_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/06_auditorias"
done

# 07_sesiones
echo "📂 Moviendo archivos de SESIONES..."
for file in SESION_*.md README_SESION_*.md RESUMEN_SESION_*.md INDICE_SESION_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/07_sesiones"
done
move_file "RESUMEN_EJECUTIVO_08_DIC_2025.md" "docs/07_sesiones"
move_file "RESUMEN_FINAL_SESION_08_DIC_2025.md" "docs/07_sesiones"
move_file "RESUMEN_FINAL_INGESTA_COMPLETADA.md" "docs/07_sesiones"

# 08_guias
echo "📂 Moviendo archivos de GUÍAS..."
for file in GUIA_*.md INDICE_DOCUMENTACION_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/08_guias"
done
move_file "AI_SPECS_QUICKSTART.md" "docs/08_guias"
move_file "README_REPARACIONES_RESUMEN.md" "docs/08_guias"
move_file "GIT_SYNC_MULTI_MAQUINA_GUIA.md" "docs/08_guias"
move_file "SINCRONIZACION_VSCODE_PORTATIL.md" "docs/08_guias"
move_file "SCRIPTS_LISTOS_PARA_EJECUTAR.md" "docs/08_guias"

# 09_simulacros
echo "📂 Moviendo archivos de SIMULACROS..."
for file in SIMULACRO_*.md RESUMEN_SIMULACRO_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/09_simulacros"
done
move_file "UBICACION_SIMULACRO_COMPLETO.md" "docs/09_simulacros"

# 10_memoria
echo "📂 Moviendo archivos de MEMORIA..."
for file in MEMORIA_COMPLETA_*.md ANALISIS_COMPLETO_PROYECTO_*.md ANALISIS_PRIORIDAD_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/10_memoria"
done
move_file "RESUMEN_2_MINUTOS.md" "docs/10_memoria"
move_file "RESUMEN_COMPLETO_REPARACIONES.md" "docs/10_memoria"
for file in RESUMEN_REPARACIONES_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/10_memoria"
done
move_file "LISTA_COMPLETA_CAMBIOS.md" "docs/10_memoria"
move_file "INDICE_DOCUMENTOS_CREADOS.md" "docs/10_memoria"
for file in ACTUALIZACION_DOCS_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/10_memoria"
done
move_file "PLAN_REORGANIZACION_ROOT_10_DIC_2025.md" "docs/10_memoria"

# 11_configuracion
echo "📂 Moviendo archivos de CONFIGURACIÓN..."
move_file "CONFIGURAR_AGENTE_MISTRAL_STUDIO.md" "docs/11_configuracion"
move_file "AGENTS.md" "docs/11_configuracion"
move_file "CLAUDE.md" "docs/11_configuracion"
move_file "GEMINI.md" "docs/11_configuracion"
for file in DEEPSEEK_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/11_configuracion"
done
move_file "RESPUESTA_PREGUNTAS_AGENTE.md" "docs/11_configuracion"
for file in MEJORES_PRACTICAS_*.md Seguridad_*.md; do
  [ -f "$file" ] && move_file "$file" "docs/11_configuracion"
done

# 12_problemas
echo "📂 Moviendo archivos de PROBLEMAS..."
move_file "ANALISIS_PROBLEMAS_ENCONTRADOS.md" "docs/12_problemas"
move_file "CORRECCIONES_CODIGO_COMPLETADAS.md" "docs/12_problemas"
move_file "CORRECCION_VERIFICACION_PLAN.md" "docs/12_problemas"

# 13_formato
echo "📂 Moviendo archivos de FORMATO..."
move_file "FORMATO_OFICIAL_OPOSICIONES_RESUMEN.md" "docs/13_formato"

# 14_funciones
echo "📂 Moviendo archivos JSON de FUNCIONES..."
for file in FUNCION_*.json FUNCIONES_*.json; do
  [ -f "$file" ] && move_file "$file" "docs/14_funciones"
done

# Mover a archive (obsoletos)
echo "📂 Moviendo archivos OBSOLETOS a archive..."
move_file "COMMIT_EXITOSO_25_NOV.md" "docs/archive"
move_file "MIGRATION_SUMMARY.md" "docs/archive"

echo ""
echo "📊 REPORTE DE REORGANIZACIÓN"
echo "================================"
for dir in docs/0*; do
  if [ -d "$dir" ]; then
    count=$(find "$dir" -type f \( -name "*.md" -o -name "*.json" \) 2>/dev/null | wc -l)
    printf "%-25s %2d archivos\n" "$(basename $dir):" "$count"
  fi
done

echo ""
echo "Archivos restantes en root:"
remaining=$(ls -1 *.md 2>/dev/null | wc -l)
echo "$remaining archivos .md"
if [ "$remaining" -gt 0 ]; then
  echo ""
  echo "Archivos que quedan (deben ser README, INSTALLATION, SETUP):"
  ls -1 *.md 2>/dev/null | head -10
fi

echo ""
echo "✅ REORGANIZACIÓN COMPLETADA"
echo ""
echo "💾 Backup guardado en: $BACKUP_FILE"
echo "📁 Nueva estructura en: docs/01_arquitectura/ hasta docs/14_funciones/"
echo ""
echo "🔄 Próximos pasos:"
echo "  1. Verificar: ls docs/01_arquitectura/"
echo "  2. Actualizar README.md con nuevas rutas"
echo "  3. Commit: git add . && git commit -m 'docs: reorganizar root en estructura temática'"
echo "  4. Push: git push origin main"
echo ""
