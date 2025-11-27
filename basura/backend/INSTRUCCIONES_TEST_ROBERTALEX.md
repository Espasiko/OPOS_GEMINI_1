# 🧪 Instrucciones: Test RoBERTalex Local

## Objetivo

Probar RoBERTalex localmente para:
1. Comparar calidad vs all-minilm
2. Medir tiempo de inferencia
3. Verificar que funciona en tu PC
4. Decidir si usar local o HuggingFace API

---

## Paso 1: Activar entorno virtual

```bash
# Opción A: Si tienes venv en backend
cd backend
.\venv\Scripts\activate

# Opción B: Si tienes venv en elemplos_leyes_info
cd elemplos_leyes_info
.\venv\Scripts\activate
```

## Paso 2: Instalar dependencias

```bash
pip install sentence-transformers numpy
```

## Paso 3: Ejecutar test

```bash
cd backend
python test_robertalex_local.py
```

---

## Qué esperar

### Primera ejecución (lenta):
```
🔹 TEST 2: RoBERTalex (modelo legal español)
Descargando RoBERTalex desde HuggingFace...
⚠️  Esto puede tardar ~5 minutos la primera vez (420 MB)
✅ Cargado en 300.00s
```

### Ejecuciones posteriores (rápido):
```
✅ Cargado en 5.00s
✅ Embeddings generados en 2.00s
```

---

## Resultados esperados

### all-minilm (modelo genérico):
```
📊 Similitudes para query: 'Diferencia entre incapacidad permanente total y absoluta según LGSS'
   1. 0.6234 - Art. 194 LGSS: Incapacidad permanente total...
   2. 0.5891 - Art. 195 LGSS: Incapacidad permanente absoluta...
   3. 0.3456 - Art. 208 LGSS: Jubilación anticipada...
```

### RoBERTalex (modelo legal español):
```
📊 Similitudes para query: 'Diferencia entre incapacidad permanente total y absoluta según LGSS'
   1. 0.8123 - Art. 194 LGSS: Incapacidad permanente total...
   2. 0.7956 - Art. 195 LGSS: Incapacidad permanente absoluta...
   3. 0.2134 - Art. 208 LGSS: Jubilación anticipada...
```

**Diferencia**: RoBERTalex debería tener scores más altos y mejor separación entre relevantes e irrelevantes.

---

## Interpretación

### Si RoBERTalex es mejor:
- ✅ Scores más altos (>0.7 vs >0.6)
- ✅ Mejor separación (relevantes vs irrelevantes)
- ✅ Encuentra documentos correctos más consistentemente

### Si all-minilm es similar:
- ⚠️ Puede que el dataset de prueba sea muy simple
- ⚠️ Probar con queries más complejas

---

## Decisión

Después del test, decidir:

### Usar RoBERTalex local si:
- ✅ Calidad significativamente mejor
- ✅ Tiempo de inferencia aceptable (<5s)
- ✅ Tienes RAM suficiente (7.7 GB es suficiente)

### Usar HuggingFace API si:
- ✅ Quieres ahorrar RAM local
- ✅ Prefieres no gestionar el modelo
- ✅ Free tier es suficiente (lo es)

---

## Próximos pasos

Una vez decidido, actualizar:
1. `backend/.env` con modelo elegido
2. `backend/agents/rag_agent.py` con configuración
3. `docs/DECISIONES_CLAVE.md` con la decisión

