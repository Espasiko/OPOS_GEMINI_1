# 🎯 PLAN: RAG 3 Capas con JSON del BOE + Agente Mistral Mejorado

**Fecha**: 4 Diciembre 2025  
**Objetivo**: Mejorar RAG con JSON del BOE, eliminar PDFs, implementar 3 capas con búsqueda logarítmica/semántica, caché y ahorro de tokens

---

## 📊 CONTEXTO: Problemas Actuales

### ❌ Problema 1: Agente Mistral Inventa URLs
- Cita artículos pero URLs son de ayuntamientos, no del BOE
- No verifica contenido real del documento
- Empieza siempre con "Según el artículo X..."

### ❌ Problema 2: RAG Actual Usa PDFs
- PDFs mal parseados, texto sucio
- Sin estructura (artículos mezclados)
- Metadata pobre: `norma: "N/A"`
- Capa 1 mal indexada (447 docs incorrectos)

### ❌ Problema 3: Sin Optimización de Tokens
- No hay caché
- No hay búsqueda logarítmica
- Envía mucho contexto innecesario

---

## ✅ SOLUCIÓN: RAG 3 Capas con JSON del BOE

### Arquitectura Propuesta

```
┌─────────────────────────────────────────────────────────────┐
│                  MISTRAL AGENT STUDIO                        │
│  - Instrucciones mejoradas (sin "según el artículo...")     │
│  - Verificación de URLs con contenido                       │
│  - Generación de 1 pregunta con 4 opciones (A,B,C,D)        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Function Calling
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐         ┌──────────────┐
│  buscar_rag   │         │ verificar_url│
│  (3 capas)    │         │  (contenido) │
└───────┬───────┘         └──────────────┘
        │
        │ Búsqueda Optimizada
        │
        ▼
┌─────────────────────────────────────────┐
│         QDRANT LOCAL (Nueva)             │
│  Collection: leyes_boe_json_3_capas      │
│                                          │
│  CAPA 1: Leyes BOE (JSON) ~5K chunks    │
│  ├─ Búsqueda logarítmica por artículo   │
│  ├─ Metadata rica (BOE JSON)            │
│  └─ Caché de artículos frecuentes       │
│                                          │
│  CAPA 2: Jurisprudencia ~500 chunks     │
│  └─ (Futuro)                             │
│                                          │
│  CAPA 3: Materiales ~550 chunks         │
│  └─ Ya indexados correctamente          │
│                                          │
│  Total: ~6K chunks (vs 7.8K actual)     │
│  Embeddings: BGE-M3 (1024 dims)         │
└─────────────────────────────────────────┘
```

---

## 📋 FASE 1: Limpiar y Preparar (30 min)

### 1.1 Eliminar Colección Actual
