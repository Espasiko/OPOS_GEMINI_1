# 🎓 SPRINT 5: Capa 3 - Materiales de Estudio

**Fecha**: 2025-11-18  
**Estado**: ⏳ EN PROGRESO  
**Objetivo**: Indexar materiales de academia (tests, temarios, casos)

---

## 📚 Archivos a Indexar

### 1. Tests con Respuestas (Prioridad ALTA)
- ✅ `Test_Admtvos_AGE_1contestando.pdf` (273 páginas) - **COMPLETADO** (391 chunks)
- ⏳ `Test_Admtvos_AGE_2contestando.pdf` (321 páginas) - EN PROGRESO
- **Total tests**: ~600 páginas

### 2. Temarios de Academia
- ⏸️ `SS Temario Unificado - Parte específica (1).pdf` (989 páginas)
- ⏸️ `Temario1_Administrativos_Acceso_Libre_AGE.pdf`
- ⏸️ `Temario2_Administrativos_Acceso_Libre_AGE.pdf`
- **Total temarios**: ~2,000 páginas

### 3. Casos Prácticos
- ⏸️ `C1-AGE-SUPUESTOS-PRACTICOS-ADMINISTRATIVO-DEL-ESTADO.pdf`
- **Total casos**: ~100 páginas

---

## 🎯 Metadata de Capa 3

Cada chunk incluye:
- `layer`: 3 (Materiales de Estudio)
- `nivel_jerarquia`: 3
- `tipo`: "test", "temario", "caso_practico"
- `fuente`: "Academia"
- `material_nombre`: Nombre del archivo
- `material_descripcion`: Descripción del contenido
- `tiene_respuestas`: true/false
- `page_num`: Número de página
- `text`: Contenido del chunk

---

## ⏱️ Progreso Estimado

### Completado:
- ✅ Test 1: 391 chunks (~13 minutos)

### En progreso:
- ⏳ Test 2: ~500 chunks estimados (~15 minutos)

### Pendiente:
- ⏸️ Temarios: ~4,000 chunks estimados (~2 horas)
- ⏸️ Casos: ~200 chunks estimados (~10 minutos)

**Total estimado**: ~5,000 chunks nuevos | 2-3 horas

---

## 🎓 Valor de Capa 3

### Para Estudiantes:
- ✅ Tests reales con respuestas correctas
- ✅ Temarios completos de academia
- ✅ Casos prácticos resueltos
- ✅ Material de práctica auténtico

### Para el Sistema RAG:
- ✅ Ejemplos de preguntas tipo examen
- ✅ Formato de respuestas esperadas
- ✅ Contexto de aplicación práctica
- ✅ Complemento perfecto a normativa (Capa 1)

---

## 📊 Arquitectura Final (3 Capas)

```
Sistema RAG OpositaIA:
├── Capa 1: Normativa Oficial (2,016 chunks) ✅
│   ├── Constitución, LGSS, Leyes, RDs
│   └── Jerarquía: 1 (máxima autoridad)
│
├── Capa 2: Jurisprudencia (OMITIDA) ⏸️
│   └── RoBERTalex ya entrenado con jurisprudencia
│
└── Capa 3: Materiales de Estudio (~5,000 chunks) ⏳
    ├── Tests con respuestas
    ├── Temarios de academia
    ├── Casos prácticos
    └── Jerarquía: 3 (material de apoyo)
```

**Total proyectado**: ~7,000 chunks | ~20 MB

---

## 🚀 Próximos Pasos

### Después de Sprint 5:
1. **Verificar calidad** de búsquedas en Capa 3
2. **Implementar reranking** por jerarquía (Capa 1 > Capa 3)
3. **Integrar con backend** FastAPI
4. **Testing end-to-end** con las 3 capas

### Opcional (Capa 2):
- Scraping legal de CENDOJ (respetando términos)
- O simplemente confiar en RoBERTalex pre-entrenado

---

## 💡 Decisión sobre Capa 2

**Razones para OMITIR Capa 2 por ahora**:
1. ✅ RoBERTalex ya entrenado con jurisprudencia española
2. ✅ CENDOJ no tiene API pública
3. ✅ Scraping masivo prohibido por términos de uso
4. ✅ Capa 1 (normativa) + Capa 3 (práctica) = valor completo
5. ✅ Podemos agregar Capa 2 más adelante si es necesario

**Alternativa futura**:
- Recopilar manualmente Top 20-30 sentencias clave
- Usar bases de datos comerciales (vLex, Aranzadi)
- Scraping legal y respetuoso de CENDOJ (1-2 sentencias/día)

---

**🎉 Sistema RAG con 2 capas operativas será suficiente para MVP!**
