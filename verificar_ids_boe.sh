#!/bin/bash
# Verificación IDs BOE vs Títulos Reales

echo "🔍 VERIFICACIÓN DE IDs BOE vs TÍTULOS REALES"
echo "========================================="

# Lista de IDs a verificar
ids=(
    "BOE-A-1966-10707"
    "BOE-A-1978-31229" 
    "BOE-A-2015-11724"
    "BOE-A-2015-10565"
    "BOE-A-2015-10566"
    "BOE-A-1996-4447"
    "BOE-A-2004-11836"
    "BOE-A-2021-21007"
    "BOE-A-2023-5364"
    "BOE-A-2024-10235"
)

echo -e "\n📋 VERIFICANDO 10 LEYES MUESTRA:\n"

for id in "${ids[@]}"; do
    echo "🔍 $id"
    
    # Obtener título del BOE
    titulo_boe=$(curl -s "https://www.boe.es/buscar/doc.php?id=$id" | grep -o '<title>[^<]*</title>' | sed 's/<title>//' | sed 's/<\/title>//' | sed 's/BOE-A-[0-9]*-[0-9]* //')
    
    # Obtener título de Neo4j
    titulo_neo4j=$(docker exec opositaia-neo4j cypher-shell -u neo4j -p opositaia2026 "MATCH (l:Ley) WHERE l.boe_id='$id' RETURN l.titulo" 2>/dev/null | grep -v "l.titulo" | tr -d '"')
    
    # Comparar
    if [[ "$titulo_boe" == "$titulo_neo4j" ]]; then
        echo "  ✅ COINCIDEN: $titulo_boe"
    else
        echo "  ❌ DISCREPANCIA:"
        echo "     BOE: $titulo_boe"
        echo "     Neo4j: $titulo_neo4j"
    fi
    echo ""
done

echo "🔍 VERIFICACIÓN DE ERRORES 404:"
echo "================================"

# IDs que dieron 404
ids_404=(
    "BOE-A-1966-10707"
    "BOE-A-1978-31229"
)

for id in "${ids_404[@]}"; do
    echo "🔍 $id (URL alternativa)"
    
    # Probar URL alternativa
    titulo_alt=$(curl -s "https://www.boe.es/eli/es/$id" | grep -o '<title>[^<]*</title>' | sed 's/<title>//' | sed 's/<\/title>//' 2>/dev/null)
    
    if [[ -n "$titulo_alt" && "$titulo_alt" != *"404"* ]]; then
        echo "  ✅ URL alternativa funciona: $titulo_alt"
    else
        echo "  ❌ Sin título encontrado"
    fi
    echo ""
done

echo "🎯 VERIFICACIÓN DE URLs VÁLIDAS:"
echo "================================"

# IDs que sabemos que funcionan
ids_validos=(
    "BOE-A-2015-11724"
    "BOE-A-2015-10565"
    "BOE-A-2015-10566"
)

for id in "${ids_validos[@]}"; do
    echo "🔍 $id"
    
    # Verificar URL normal
    http_code=$(curl -s -o /dev/null -w "%{http_code}" "https://www.boe.es/buscar/doc.php?id=$id")
    
    if [[ "$http_code" == "200" ]]; then
        echo "  ✅ URL válida (200)"
    else
        echo "  ❌ URL inválida ($http_code)"
    fi
    echo ""
done

echo "📊 RESUMEN:"
echo "========="
echo "• IDs verificados: ${#ids[@]}"
echo "• Métodos probados: /buscar/doc.php, /eli/es/"
echo "• Estado: Verificación completada"
