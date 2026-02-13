#!/bin/bash
# Script de verificación rápida del VPS
# Uso: ./verificar_vps.sh

set -e

VPS_IP="147.93.95.67"
VPS_USER="root"
DOMAIN="electroyhogarpelotazo.tienda"

echo "🔍 VERIFICACIÓN VPS - $(date)"
echo "================================"
echo ""

# 1. Verificar conexión SSH
echo "1️⃣  Verificando conexión SSH..."
if ssh -o ConnectTimeout=5 ${VPS_USER}@${VPS_IP} "echo 'OK'" &>/dev/null; then
    echo "   ✅ Conexión SSH exitosa"
else
    echo "   ❌ Error de conexión SSH"
    exit 1
fi
echo ""

# 2. Verificar servicios
echo "2️⃣  Verificando servicios systemd..."
ssh ${VPS_USER}@${VPS_IP} "systemctl is-active llama-server.service" &>/dev/null && \
    echo "   ✅ llama-server.service: ACTIVO" || \
    echo "   ❌ llama-server.service: INACTIVO"

ssh ${VPS_USER}@${VPS_IP} "systemctl is-active salamandra-api.service" &>/dev/null && \
    echo "   ✅ salamandra-api.service: ACTIVO" || \
    echo "   ❌ salamandra-api.service: INACTIVO"
echo ""

# 3. Verificar puertos
echo "3️⃣  Verificando puertos internos..."
ssh ${VPS_USER}@${VPS_IP} "ss -tlnp | grep -q ':8080'" && \
    echo "   ✅ Puerto 8080 (llama.cpp): ABIERTO" || \
    echo "   ❌ Puerto 8080: CERRADO"

ssh ${VPS_USER}@${VPS_IP} "ss -tlnp | grep -q '127.0.0.1:8001'" && \
    echo "   ✅ Puerto 8001 (FastAPI): ABIERTO" || \
    echo "   ❌ Puerto 8001: CERRADO"
echo ""

# 4. Verificar recursos
echo "4️⃣  Recursos del sistema..."
ssh ${VPS_USER}@${VPS_IP} "free -h | grep Mem" | awk '{print "   💾 RAM: " $3 " usados / " $2 " total (" $7 " disponibles)"}'
ssh ${VPS_USER}@${VPS_IP} "df -h / | tail -1" | awk '{print "   💿 Disco: " $3 " usados / " $2 " total (" $5 " uso)"}'
echo ""

# 5. Verificar endpoints públicos
echo "5️⃣  Verificando endpoints públicos..."

# Health check FastAPI
if curl -s -f -m 5 "https://${DOMAIN}/health" &>/dev/null; then
    echo "   ✅ https://${DOMAIN}/health"
else
    echo "   ❌ https://${DOMAIN}/health (no responde)"
fi

# Llama.cpp models
if curl -s -f -m 5 "https://${DOMAIN}/v1/models" &>/dev/null; then
    echo "   ✅ https://${DOMAIN}/v1/models"
else
    echo "   ❌ https://${DOMAIN}/v1/models (no responde)"
fi
echo ""

# 6. Verificar modelo cargado
echo "6️⃣  Verificando modelo Salamandra..."
MODEL_INFO=$(ssh ${VPS_USER}@${VPS_IP} "curl -s http://127.0.0.1:8080/v1/models" 2>/dev/null)
if echo "$MODEL_INFO" | grep -q "salamandra"; then
    MODEL_SIZE=$(echo "$MODEL_INFO" | grep -o '"size":[0-9]*' | head -1 | cut -d: -f2)
    MODEL_SIZE_GB=$(echo "scale=1; $MODEL_SIZE / 1024 / 1024 / 1024" | bc)
    echo "   ✅ Modelo: salamandra-7b-instruct-Q4_K_M.gguf"
    echo "   📦 Tamaño: ${MODEL_SIZE_GB} GB"
else
    echo "   ❌ Modelo no detectado"
fi
echo ""

# 7. Verificar procesos
echo "7️⃣  Procesos activos..."
LLAMA_PID=$(ssh ${VPS_USER}@${VPS_IP} "pgrep -f llama-server" 2>/dev/null || echo "")
if [ -n "$LLAMA_PID" ]; then
    LLAMA_MEM=$(ssh ${VPS_USER}@${VPS_IP} "ps -p $LLAMA_PID -o rss= | awk '{print \$1/1024/1024}'")
    echo "   ✅ llama-server (PID: $LLAMA_PID, RAM: ${LLAMA_MEM} GB)"
else
    echo "   ❌ llama-server no está corriendo"
fi

UVICORN_PID=$(ssh ${VPS_USER}@${VPS_IP} "pgrep -f 'uvicorn.*salamandra'" 2>/dev/null || echo "")
if [ -n "$UVICORN_PID" ]; then
    echo "   ✅ salamandra-api (PID: $UVICORN_PID)"
else
    echo "   ❌ salamandra-api no está corriendo"
fi
echo ""

# 8. Test funcional básico
echo "8️⃣  Test funcional (health check)..."
HEALTH_RESPONSE=$(curl -s "https://${DOMAIN}/health" 2>/dev/null || echo "{}")
if echo "$HEALTH_RESPONSE" | grep -q "ok"; then
    echo "   ✅ API responde correctamente"
    echo "   📄 Respuesta: $HEALTH_RESPONSE"
else
    echo "   ⚠️  API responde pero formato inesperado"
    echo "   📄 Respuesta: $HEALTH_RESPONSE"
fi
echo ""

echo "================================"
echo "✅ Verificación completada"
echo ""
echo "📋 Comandos útiles:"
echo "   ssh ${VPS_USER}@${VPS_IP}"
echo "   ssh ${VPS_USER}@${VPS_IP} 'systemctl status llama-server.service'"
echo "   ssh ${VPS_USER}@${VPS_IP} 'journalctl -u salamandra-api.service -n 50'"
echo "   curl https://${DOMAIN}/docs"
