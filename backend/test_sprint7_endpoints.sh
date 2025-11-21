#!/bin/bash
# Script de verificación rápida de endpoints Sprint 7
# Ejecutar: bash backend/test_sprint7_endpoints.sh

echo "🧪 Testing Sprint 7 Endpoints"
echo "================================"
echo ""

BASE_URL="http://localhost:8000"

# Test 1: Root endpoint
echo "1️⃣ Testing root endpoint..."
curl -s $BASE_URL/ | python3 -m json.tool
echo ""

# Test 2: Health check general
echo "2️⃣ Testing general health..."
curl -s $BASE_URL/health | python3 -m json.tool
echo ""

# Test 3: Chat health
echo "3️⃣ Testing chat health..."
curl -s $BASE_URL/chat/health | python3 -m json.tool
echo ""

# Test 4: Upload health
echo "4️⃣ Testing upload health..."
curl -s $BASE_URL/upload/health | python3 -m json.tool
echo ""

# Test 5: RAG health
echo "5️⃣ Testing RAG health..."
curl -s $BASE_URL/api/v2/rag/health | python3 -m json.tool
echo ""

echo "✅ All health checks completed!"
echo ""
echo "📝 To test chat endpoint:"
echo 'curl -X POST $BASE_URL/chat/message -H "Content-Type: application/json" -d '"'"'{"message":"test","conversation_id":"test","use_rag":false}'"'"''
echo ""
echo "📝 To test upload endpoint:"
echo 'echo "test content" > test.txt && curl -X POST $BASE_URL/upload/file -F "file=@test.txt"'
