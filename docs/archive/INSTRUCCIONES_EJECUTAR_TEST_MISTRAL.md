# 🔧 INSTRUCCIONES: Ejecutar Test Agente Mistral

## ❌ PROBLEMA ACTUAL:

El Agent ID está incorrecto:
```
Agent ID usado: ag:019ad601:20241201:untitled-agent:e5b1e3d5
Error: "Agent not found"
```

## ✅ SOLUCIÓN:

### 1. Obtener Agent ID Correcto

Ve a https://console.mistral.ai/ y:
1. Login
2. Agents → Tu agente
3. Copia el Agent ID (formato: `ag:XXXXXXXX:YYYYMMDD:nombre:ZZZZZZZZ`)

### 2. Actualizar el Test

Edita `test_mistral_agent_tools.py` línea 13:
```python
# CAMBIAR ESTO:
AGENT_ID = "ag:019ad601:20241201:untitled-agent:e5b1e3d5"

# POR TU AGENT ID REAL:
AGENT_ID = "tu_agent_id_aqui"
```

### 3. Ejecutar Test

```bash
wsl bash -c "source elemplos_leyes_info/venv/bin/activate && python3 test_mistral_agent_tools.py"
```

## 📋 QUÉ VERÁS:

Si funciona correctamente:
```
TEST 1: Web Search
✓ Respuesta del agente
🔧 HERRAMIENTAS USADAS:
  - web_search
  - ...

TEST 2: Code Execution
✓ Respuesta del agente
🔧 HERRAMIENTAS USADAS:
  - code_interpreter
  - ...
```

## 🎯 PRÓXIMO PASO:

**Dame el Agent ID correcto y lo actualizo inmediatamente** 🚀

---

**Nota**: La API key de Mistral ya está configurada en `.env`
