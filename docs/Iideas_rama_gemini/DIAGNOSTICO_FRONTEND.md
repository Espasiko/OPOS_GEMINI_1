# 🔍 Diagnóstico Frontend - Problema con Modelos

**Fecha:** 25 Noviembre 2025  
**Problema:** Los modelos no aparecen en el desplegable y no son clicables

---

## ✅ Problemas Identificados y Corregidos

### 1. ❌ Error Crítico en `ModelContext.tsx`

**Problema:**
```typescript
// ANTES (INCORRECTO)
interface ModelContextType {
  selectedModel: string;
  setSelectedModel: () => void;  // ❌ Sin parámetro
}
```

**Solución:**
```typescript
// DESPUÉS (CORRECTO)
interface ModelContextType {
  selectedModel: string;
  setSelectedModel: (value: string) => void;  // ✅ Con parámetro
}
```

**Impacto:** Este error impedía que el selector pudiera cambiar el modelo seleccionado.

---

## 🔍 Checklist de Diagnóstico

### Backend
- [ ] Backend corriendo en `http://localhost:8000`
- [ ] Endpoint `/chat/providers` responde
- [ ] Endpoint `/health` responde
- [ ] Variables de entorno cargadas desde `.env.backend`

### Frontend
- [ ] Frontend corriendo en `http://localhost:3000`
- [ ] `ModelContext.tsx` corregido
- [ ] `ModelSelector.tsx` carga providers
- [ ] Console del navegador sin errores

---

## 🧪 Comandos de Verificación

### 1. Verificar Backend
```bash
# Arrancar backend
wsl bash -c "cd backend && source venv/bin/activate && python -m uvicorn main:app --host 0.0.0.0 --port 8000"

# En otra terminal, verificar health
curl http://localhost:8000/health

# Verificar providers
curl http://localhost:8000/chat/providers
```

**Respuesta esperada de `/chat/providers`:**
```json
{
  "providers": [
    {
      "id": "groq-8b",
      "provider": "groq",
      "model": "Llama 3.1 8B",
      "speed": "ultra",
      "cost": "free",
      "configured": true
    },
    ...
  ]
}
```

### 2. Verificar Frontend
```bash
# Arrancar frontend
npm run dev

# Abrir navegador
# http://localhost:3000
```

**En Console del navegador (F12):**
- No debe haber errores de tipo `setSelectedModel is not a function`
- Debe aparecer: `Loading providers...` → Lista de modelos

---

## 🐛 Errores Comunes

### Error 1: "Cannot connect to backend"
**Causa:** Backend no está corriendo  
**Solución:** Arrancar backend con el comando de arriba

### Error 2: "setSelectedModel is not a function"
**Causa:** Error en `ModelContext.tsx`  
**Solución:** ✅ Ya corregido

### Error 3: "Providers array is empty"
**Causa:** Backend no tiene API keys configuradas  
**Solución:** Verificar `.env.backend` tiene las keys

### Error 4: "CORS error"
**Causa:** Backend no permite requests desde frontend  
**Solución:** Verificar CORS en `main.py`

---

## 📝 Próximos Pasos

1. **Arrancar backend** y verificar que responde
2. **Arrancar frontend** y verificar console
3. **Probar selector** de modelos
4. **Reportar** cualquier error que aparezca en console

---

## 🔧 Archivos Modificados

- ✅ `contexts/ModelContext.tsx` - Corregido tipo de `setSelectedModel`

---

## 📊 Estado Actual

**Backend:** ⏳ Pendiente verificación  
**Frontend:** ✅ Código corregido  
**Integración:** ⏳ Pendiente prueba  

---

**Siguiente acción:** Arrancar backend y verificar endpoint `/chat/providers`
