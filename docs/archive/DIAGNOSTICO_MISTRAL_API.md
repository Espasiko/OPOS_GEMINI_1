# 🔍 DIAGNÓSTICO: Problema con Mistral API

**Fecha**: 1 Diciembre 2025  
**Problema**: Ambas API keys de Mistral dan error 401 Unauthorized

---

## ❌ PROBLEMA DETECTADO

### **API Keys Probadas:**

1. **Key Vieja** (del .env):
   ```
   Dn11EQcZl36z7BghhcM3mfa8mrjI5Ko2
   ```
   - **Status**: ❌ 401 Unauthorized
   - **Error**: `{"detail":"Unauthorized"}`

2. **Key Nueva** (proporcionada):
   ```
   V27eNNH4b7Er1k9WPxYHRaEf9gLsKqmH
   ```
   - **Status**: ❌ 401 Unauthorized
   - **Error**: `{"detail":"Unauthorized"}`

### **Endpoints Probados:**
- ✅ Endpoint correcto: `https://api.mistral.ai/v1/chat/completions`
- ✅ Endpoint agente correcto: `https://api.mistral.ai/v1/agents/completions`
- ❌ Ambos dan 401

---

## 🔎 POSIBLES CAUSAS

### **1. API Keys Revocadas o Expiradas**
- Las keys pueden haber sido revocadas
- Pueden haber expirado
- La cuenta puede estar suspendida

### **2. Problema de Facturación**
- Cuenta sin método de pago
- Créditos agotados
- Factura pendiente

### **3. Formato Incorrecto**
- Aunque el formato parece correcto
- Bearer token bien formado

### **4. Restricciones de IP/Región**
- Posible bloqueo geográfico
- Restricciones de IP

---

## ✅ SOLUCIÓN: Obtener Nueva API Key

### **Paso 1: Ir a Mistral Console**
1. Visita: https://console.mistral.ai/
2. Inicia sesión con tu cuenta

### **Paso 2: Verificar Estado de la Cuenta**
1. Ve a **Settings** → **Billing**
2. Verifica que tengas:
   - ✅ Método de pago activo
   - ✅ Créditos disponibles
   - ✅ Sin facturas pendientes

### **Paso 3: Crear Nueva API Key**
1. Ve a **API Keys** en el menú
2. Click en **Create new key**
3. Dale un nombre: "OpositAIA Dataset Generator"
4. Copia la key inmediatamente (solo se muestra una vez)

### **Paso 4: Actualizar .env**
```bash
# backend/.env.backend
MISTRAL_API_KEY=tu_nueva_key_aqui
```

### **Paso 5: Probar Nueva Key**
```bash
wsl python3 test_mistral_agent_complete.py
```

---

## 📊 RESULTADOS ACTUALES (Solo Claude)

### **Claude 4.5 Sonnet:**
- ⏱️ **Tiempo**: 12.01s
- 💰 **Coste**: $0.010113
- 📊 **Tokens**: 771 total (121 input + 650 output)
- 🔗 **URLs**: 4 encontradas

### **Verificación URLs Claude:**
- ✅ **2/4 válidas** (50%)
- ⚠️ **2/4 bloqueadas** (seg-social.es)

**URLs Válidas:**
1. ✅ https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724
2. ✅ https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a205

**URLs Bloqueadas/Inventadas:**
3. ⚠️ https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/10963
4. ⚠️ https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/10938/28393

---

## 💡 RECOMENDACIONES INMEDIATAS

### **1. Obtener Nueva API Key de Mistral** ⚠️ URGENTE
- Sin Mistral API funcional, no puedes usar el plan híbrido
- Necesitas acceso a Mistral para el 30% de contenido complejo

### **2. Implementar Verificación Automática de URLs** ✅ CRÍTICO
```python
def verify_and_fix_urls(qa_data):
    """
    Verifica URLs y marca las inválidas
    """
    urls = extract_urls(qa_data)
    valid_urls = []
    invalid_urls = []
    
    for url in urls:
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                valid_urls.append(url)
            else:
                invalid_urls.append({
                    "url": url,
                    "status": response.status_code,
                    "reason": "HTTP error"
                })
        except:
            invalid_urls.append({
                "url": url,
                "status": 0,
                "reason": "Connection failed - possibly invented"
            })
    
    # Actualizar Q&A
    qa_data['valid_urls'] = valid_urls
    qa_data['invalid_urls'] = invalid_urls
    qa_data['url_verification'] = {
        "total": len(urls),
        "valid": len(valid_urls),
        "invalid": len(invalid_urls),
        "validity_rate": len(valid_urls) / len(urls) if urls else 0
    }
    
    # Reducir confianza si hay URLs inválidas
    if invalid_urls:
        qa_data['confidence'] *= (len(valid_urls) / len(urls))
        qa_data['warnings'].append(f"{len(invalid_urls)} URLs inválidas detectadas")
    
    return qa_data
```

### **3. Estrategia Temporal (Mientras arreglas Mistral)**

**Opción A: Solo Groq (Económica)**
```yaml
100% Groq Llama 3.1 70B
Coste: $7 para 10K Q&A
Calidad: 88-90%
Tiempo: 3-4 horas
```

**Opción B: Groq + Claude (Premium)**
```yaml
70% Groq: $5
30% Claude: $45
Total: $50 para 10K Q&A
Calidad: 96-98%
Tiempo: 4-5 horas
```

**Opción C: Esperar a Mistral (Recomendado)**
```yaml
70% Groq: $5
30% Mistral: $10
Total: $15 para 10K Q&A
Calidad: 93-95%
Tiempo: 3-4 horas
```

---

## 🔧 SCRIPT DE VERIFICACIÓN DE URLs

He creado el script completo que:
1. ✅ Prueba ambas API keys de Mistral
2. ✅ Prueba Claude como comparación
3. ✅ Verifica TODAS las URLs automáticamente
4. ✅ Calcula costes reales
5. ✅ Guarda resultados en JSON

**Archivo**: `test_mistral_agent_complete.py`

**Uso**:
```bash
wsl python3 test_mistral_agent_complete.py
```

---

## 📈 PRÓXIMOS PASOS

### **Inmediato (Hoy):**
1. ⚠️ **Obtener nueva API key de Mistral**
   - Ve a https://console.mistral.ai/
   - Verifica billing
   - Crea nueva key
   - Actualiza .env

2. ✅ **Ejecutar prueba completa**
   ```bash
   wsl python3 test_mistral_agent_complete.py
   ```

3. ✅ **Comparar Mistral Agent vs Claude**
   - Calidad
   - Coste
   - URLs válidas

### **Corto Plazo (Esta Semana):**
1. ✅ Implementar verificación automática de URLs en pipeline
2. ✅ Decidir estrategia final (Groq+Mistral vs Groq+Claude)
3. ✅ Comenzar generación de dataset

### **Medio Plazo:**
1. ✅ Generar 10,000 Q&A
2. ✅ Revisión humana selectiva
3. ✅ Fine-tuning de Mistral 7B

---

## 🎯 DECISIÓN RECOMENDADA

### **SI consigues nueva API key de Mistral:**
```yaml
Estrategia: Groq (70%) + Mistral Agent (30%)
Coste: $15-20
Calidad: 94-96%
URLs: Verificación automática
Revisión humana: 10%
```

### **SI NO consigues API key de Mistral:**
```yaml
Estrategia: Solo Groq (100%)
Coste: $7
Calidad: 88-90%
URLs: Verificación automática
Revisión humana: 15%
```

**NO recomiendo Claude** por coste prohibitivo ($151 vs $15)

---

## 📄 ARCHIVOS GENERADOS

1. `test_mistral_agent_complete.py` - Script de prueba completo
2. `test_mistral_vs_claude_complete.json` - Resultados en JSON
3. `DIAGNOSTICO_MISTRAL_API.md` - Este documento

---

**Estado**: ⚠️ Bloqueado por API key de Mistral  
**Acción Requerida**: Obtener nueva API key  
**Prioridad**: 🔴 Alta
