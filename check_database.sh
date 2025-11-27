#!/bin/bash
# Script para explorar la base de datos PostgreSQL de OpositaIA

echo "=========================================="
echo "🔍 EXPLORACIÓN DE BASE DE DATOS"
echo "=========================================="
echo ""

# Listar todas las bases de datos
echo "📊 Bases de datos disponibles:"
echo "=========================================="
psql -U postgres -l
echo ""

# Conectar a opositaia y explorar
echo "📋 Tablas en la base de datos 'opositaia':"
echo "=========================================="
psql -U postgres -d opositaia -c "\dt" 2>/dev/null || echo "⚠️  Base de datos 'opositaia' no existe"
echo ""

# Si existe, mostrar estadísticas
if psql -U postgres -d opositaia -c "SELECT 1" &>/dev/null; then
    echo "📈 Estadísticas de tablas:"
    echo "=========================================="
    psql -U postgres -d opositaia -c "
    SELECT 
        schemaname,
        tablename,
        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
        n_live_tup AS rows
    FROM pg_stat_user_tables
    ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
    "
    echo ""
    
    echo "👤 Usuarios en user_progress:"
    echo "=========================================="
    psql -U postgres -d opositaia -c "
    SELECT 
        username,
        email,
        total_preguntas,
        total_correctas,
        precision_global,
        dias_estudiados,
        racha_actual,
        ultima_sesion
    FROM user_progress
    LIMIT 10;
    " 2>/dev/null || echo "⚠️  Tabla user_progress no existe"
    echo ""
    
    echo "📝 Historial de respuestas (últimas 10):"
    echo "=========================================="
    psql -U postgres -d opositaia -c "
    SELECT 
        tema_nombre,
        es_correcta,
        tiempo_respuesta,
        created_at
    FROM answer_history
    ORDER BY created_at DESC
    LIMIT 10;
    " 2>/dev/null || echo "⚠️  Tabla answer_history no existe"
    echo ""
    
    echo "🎯 Simulacros realizados:"
    echo "=========================================="
    psql -U postgres -d opositaia -c "
    SELECT 
        tipo,
        nombre,
        puntuacion,
        preguntas_correctas,
        preguntas_totales,
        tiempo_total,
        created_at
    FROM simulacros
    ORDER BY created_at DESC
    LIMIT 10;
    " 2>/dev/null || echo "⚠️  Tabla simulacros no existe"
    echo ""
    
    echo "🗺️ Mapas mentales creados:"
    echo "=========================================="
    psql -U postgres -d opositaia -c "
    SELECT 
        tema_nombre,
        titulo,
        es_publico,
        likes,
        created_at
    FROM mind_maps
    ORDER BY created_at DESC
    LIMIT 10;
    " 2>/dev/null || echo "⚠️  Tabla mind_maps no existe"
    echo ""
    
    echo "🔍 Consultas RAG (últimas 10):"
    echo "=========================================="
    psql -U postgres -d opositaia -c "
    SELECT 
        query_text,
        documentos_encontrados,
        top_score,
        tiempo_busqueda,
        fue_util,
        created_at
    FROM rag_queries
    ORDER BY created_at DESC
    LIMIT 10;
    " 2>/dev/null || echo "⚠️  Tabla rag_queries no existe"
    echo ""
fi

echo "=========================================="
echo "✅ Exploración completada"
echo "=========================================="
