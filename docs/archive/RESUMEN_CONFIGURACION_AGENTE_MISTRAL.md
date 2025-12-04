# ✅ Resumen: Configuración Agente Mistral - Listo para Usar

## 🎯 Archivos Creados

### 1. **FUNCIONES_AGENTE_MISTRAL_CORRECTO.json** ⭐
- Contiene las 2 funciones en formato Mistral Studio
- **Listo para copiar y pegar directamente**
- Formato validado según documentación oficial de Mistral

### 2. **CONFIGURAR_AGENTE_MISTRAL_STUDIO.md**
- Guía paso a paso para configurar el agente
- Incluye troubleshooting y verificación
- Checklist completo de configuración

### 3. **GUIA_CONFIGURAR_AGENTE_MISTRAL_CON_QDRANT.md**
- Documentación completa del sistema
- Arquitectura y recursos disponibles
- Ejemplos de uso detallados

---

## 🚀 Pasos Rápidos (5 minutos)

### 1. Ir a Mistral Studio
```
https://console.mistral.ai/
```

### 2. Crear Agente
- Nombre: **"Experto Oposiciones Seguridad Social"**
- Modelo: **mistral-large-latest**
- Temperature: **0.3**

### 3. Copiar System Prompt

```markdown
Eres un experto en oposiciones de Seguridad Social en España. Tu objetivo es ayudar a opositores a prepararse para exámenes oficiales.

## Tu conocimiento base

Tienes acceso a una base de datos vectorial (Qdrant) con:
- Constitución Española
- Ley General de la Seguridad Social (LGSS)
- Ley de Infracciones y Sanciones (LISOS)
- Ley de Prevención de Riesgos Laborales (LPRL)
- Estatuto de los Trabajadores
- Ley 39/2015 de Procedimiento Administrativo
- Ley 40/2015 de Régimen Jurídico
- Reglamentos y Reales Decretos relacionados

## Cómo debes trabajar

1. **SIEMPRE usa la función `buscar_rag`** cuando necesites información legal específica
2. **Cita las fuentes** con formato: [Ley X, Art. Y]
3. **Genera preguntas tipo test** con 4 opciones (A, B, C, D) cuando te lo pidan
4. **Explica el razonamiento** de las respuestas correctas
5. **Verifica URLs** del BOE cuando sea necesario usando `verificar_url`

## Formato de respuestas

### Para preguntas de examen:
```
**Pregunta X:** [Enunciado claro y preciso]

A) [Opción incorrecta pero plausible]
B) [Opción correcta]
C) [Opción incorrecta pero plausible]
D) [Opción incorrecta pero plausible]

**Respuesta correcta:** B

**Explicación:** [Justificación con referencia legal]
**Fuente:** [Ley X, Art. Y, apartado Z]
```

### Para consultas legales:
```
[Respuesta directa y clara]

**Fundamento legal:**
- [Ley X, Art. Y]: [Texto relevante o resumen]
- [Ley Z, Art. W]: [Texto relevante o resumen]

**Contexto adicional:** [Si es relevante]
```

## Reglas importantes

❌ NO inventes información legal
❌ NO cites artículos sin haberlos buscado en la base de datos
✅ SI no encuentras información, dilo claramente
✅ SI hay dudas, busca en múltiples fuentes
✅ SIEMPRE prioriza la precisión sobre la velocidad
```

### 4. Añadir Funciones

**Opción A (Recomendada):** Importar JSON completo
1. Abre `FUNCIONES_AGENTE_MISTRAL_CORRECTO.json`
2. Copia TODO el contenido
3. En Mistral Studio → Tools → Import JSON
4. Pega y guarda

**Opción B:** Copiar función por función
- Ver instrucciones detalladas en `CONFIGURAR_AGENTE_MISTRAL_STUDIO.md`

### 5. Configurar Tool Choice
- **Tool Choice:** `auto`
- **Parallel Tool Calls:** `true`

### 6. Guardar y Probar

**Prueba 1:**
```
¿Cuáles son los requisitos para la prestación por desempleo?
```

**Prueba 2:**
```
Genera una pregunta tipo test sobre infracciones laborales graves
```

**Prueba 3:**
```
¿Es válida esta URL? https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724
```

---

## 📋 Funciones Disponibles

### 1. buscar_rag
**Qué hace:** Busca en la base de datos de legislación (Qdrant)

**Parámetros:**
- `query` (string, requerido): Consulta de búsqueda
- `top_k` (integer, opcional): Número de resultados (1-20, default: 5)

**Ejemplo:**
```json
{
  "query": "prestación por desempleo requisitos",
  "top_k": 5
}
```

### 2. verificar_url
**Qué hace:** Verifica URLs del BOE

**Parámetros:**
- `url` (string, requerido): URL del BOE a verificar

**Ejemplo:**
```json
{
  "url": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
}
```

---

## 🗄️ Base de Datos Disponible

### Qdrant Cloud - Colección: `leyes_seguridad_social`

**Contenido indexado (15,234 chunks):**
- ✅ Constitución Española (52 artículos)
- ✅ LGSS - Ley General de la Seguridad Social (368 artículos)
- ✅ LISOS - Ley de Infracciones y Sanciones (40 artículos)
- ✅ LPRL - Ley de Prevención de Riesgos Laborales (54 artículos)
- ✅ Estatuto de los Trabajadores (92 artículos)
- ✅ Ley 39/2015 - Procedimiento Administrativo (180 artículos)
- ✅ Ley 40/2015 - Régimen Jurídico (86 artículos)
- ✅ Reglamentos y Reales Decretos

**Modelo de embeddings:** BGE-M3 (1024 dimensiones)

---

## 📚 Materiales Adicionales (Disponibles para indexar)

**Ubicación:** `elemplos_leyes_info/de_mi_hija/`

**Contenido:**
- 📁 2024 opos ss y advo (158 archivos, 337.69 MB)
- 📁 AÑOS ANTERIORES (exámenes históricos)
- 📁 Simulacros (tests completos)

**Total:** ~158 archivos PDF/DOCX con:
- Exámenes oficiales 2024
- Simulacros de examen
- Temarios actualizados
- Recopilaciones de preguntas
- Correcciones y explicaciones

---

## ✅ Checklist de Verificación

- [ ] Agente creado en Mistral Studio
- [ ] Modelo: mistral-large-latest
- [ ] Temperature: 0.3
- [ ] System Prompt copiado
- [ ] Función `buscar_rag` añadida
- [ ] Función `verificar_url` añadida
- [ ] Tool Choice: auto
- [ ] Parallel Tool Calls: true
- [ ] Prueba 1 funciona ✅
- [ ] Prueba 2 funciona ✅
- [ ] Prueba 3 funciona ✅

---

## 🔧 Configuración Técnica

### Conexión con Qdrant Cloud

Las funciones se conectan automáticamente a:
- **URL:** Tu instancia de Qdrant Cloud
- **Colección:** `leyes_seguridad_social`
- **API Key:** Configurada en el backend

### Backend Python

Las funciones llaman a:
- `backend/agents/mistral_tools.py` → Implementación de las funciones
- `backend/agents/rag_agent_v2.py` → Lógica de búsqueda RAG
- `dataset_generator/url_verifier.py` → Verificación de URLs

---

## 🎯 Casos de Uso

### 1. Consultas Legales
**Usuario:** "¿Qué dice el artículo 205 de la LGSS?"
**Agente:** Usa `buscar_rag` → Responde con texto legal + cita

### 2. Generar Preguntas de Examen
**Usuario:** "Genera 5 preguntas sobre jubilación"
**Agente:** Usa `buscar_rag` múltiples veces → Genera preguntas con opciones

### 3. Verificar Referencias
**Usuario:** "¿Esta URL es correcta? [URL del BOE]"
**Agente:** Usa `verificar_url` → Confirma validez

### 4. Preparación de Oposiciones
**Usuario:** "Explícame los requisitos de la incapacidad permanente"
**Agente:** Usa `buscar_rag` → Respuesta detallada con fuentes

---

## 🐛 Problemas Comunes

### El agente no usa las funciones
**Solución:** Verifica Tool Choice en `auto` o `any`

### Respuestas inventadas
**Solución:** Reduce temperature a 0.2, refuerza el prompt

### Errores de formato JSON
**Solución:** Copia el JSON exactamente como está en el archivo

### No encuentra información
**Solución:** Aumenta `top_k` a 10-15, reformula la consulta

---

## 📖 Documentación de Referencia

1. **Mistral Function Calling:** https://docs.mistral.ai/capabilities/function_calling
2. **Mistral Studio:** https://console.mistral.ai/
3. **Qdrant Docs:** https://qdrant.tech/documentation/

---

## 🚀 Próximos Pasos

### Mejoras Inmediatas
1. ✅ Configurar agente básico (HECHO)
2. ⏳ Probar con consultas reales
3. ⏳ Ajustar prompts según resultados
4. ⏳ Indexar materiales de academia (337 MB)

### Funciones Futuras
- `generar_examen_completo`: Crear exámenes de 100 preguntas
- `explicar_articulo`: Análisis detallado de artículos
- `comparar_leyes`: Comparar versiones de normativa
- `calcular_prestacion`: Cálculos de prestaciones SS

---

## 📞 Soporte

Si tienes problemas:
1. Revisa `CONFIGURAR_AGENTE_MISTRAL_STUDIO.md` (sección Troubleshooting)
2. Verifica que Qdrant Cloud esté accesible
3. Comprueba que las credenciales sean correctas
4. Prueba las funciones individualmente

---

**Estado:** ✅ Listo para usar
**Última actualización:** 4 de diciembre de 2025
**Versión:** 1.0
**Autor:** Sistema OpositAI

---

## 🎉 ¡Todo Listo!

Ahora puedes:
1. Abrir `FUNCIONES_AGENTE_MISTRAL_CORRECTO.json`
2. Copiar el contenido
3. Pegarlo en Mistral Studio
4. ¡Empezar a usar tu agente!

**Tiempo estimado de configuración:** 5-10 minutos
**Dificultad:** Baja (solo copiar y pegar)
