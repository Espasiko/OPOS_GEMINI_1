#!/bin/bash
echo "Testing Ollama..."
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "mistral:latest", "prompt": "Di hola en una palabra", "stream": false}' \
  2>&1 | head -30
