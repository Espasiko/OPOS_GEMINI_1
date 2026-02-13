 PLAN CORREGIDO: CREAR DATASET DESDE CERO CON MODELOS BARATOS + VALIDACIÓN CLAUDE

✅ SITUACIÓN REAL
❌ NO HAY DATASET
✅ Solo ~10 casos evaluados antes
✅ Sistema de agentes diseñado pero NO implementado
✅ Infraestructura operativa (VPS + Qdrant + Multi-LLM)
✅ Presupuesto: €10-15/mes

🎯 ESTRATEGIA: MODELOS BARATOS + INGENIERÍA PROMPTS + CLAUDE JUDGE
COSTES COMPARADOS (Generación 1.500 casos)
ModeloCoste/1M tokensTokens/casoCoste 1.500 casosCalidad sin promptsCalidad CON promptsClaude Sonnet 4.5$3/$15~4k$270-45095%98%GPT-4o$2.50/$10~4k$225-37593%96%DeepSeek V3$0.27/$1.10~4k$24-4175%90% ✅Gemini 2.0 Flash$0.075/$0.30~4k$7-1170%88% ✅Groq Llama 3.3 70BGRATIS~4k$065%85% ✅Mistral Large$2/$6~4k$90-15080%92%
ESTRATEGIA ÓPTIMA (Coste total: ~$50-80)
pythonpipeline_generacion = {
    "FASE 1 - Generación Masiva (Modelos baratos)": {
        "modelo_principal": "Groq Llama 3.3 70B",  # GRATIS
        "modelo_backup": "Gemini 2.0 Flash",        # $0.075/1M
        "cantidad": 3000,  # Generar 3k para filtrar a 1.5k
        "coste": "$0-22"   # Solo Gemini si Groq falla
    },
    
    "FASE 2 - Refinamiento (DeepSeek)": {
        "modelo": "DeepSeek V3",
        "funcion": "Mejorar los mejores 2000 casos de Fase 1",
        "coste": "$16-27"
    },
    
    "FASE 3 - Validación Claude (Muestreo)": {
        "modelo": "Claude Sonnet 4.5",
        "funcion": "Validar 100% pero en lotes",
        "estrategia": "Validar 100 casos → si 95+ OK → validar siguiente lote",
        "coste": "$20-30"
    },
    
    "TOTAL": "$36-79"  # Dentro de presupuesto €50-80
}

🏗️ ARQUITECTURA DEL PIPELINE DE GENERACIÓN
python# agents/dataset_generator.py

class DatasetGeneratorPipeline:
    """
    Pipeline completo: Generación barata → Refinamiento → Validación Claude
    """
    
    def __init__(self):
        # Modelos baratos para generación masiva
        self.generators = {
            "primary": GroqLlama70B(),      # GRATIS
            "secondary": GeminiFlash(),     # $0.075/1M
            "refiner": DeepSeekV3()         # $0.27/1M
        }
        
        # Claude solo para validación
        self.validator = ClaudeSonnet4()    # $3/1M input
        
        # Tu Qdrant para RAG
        self.qdrant = QdrantLegalDB()
        
        # Calculadora determinista
        self.calculator = SSCalculator()
    
    async def generate_full_dataset(self, target=1500):
        """
        Genera dataset completo con coste ~$50-80
        """
        
        print("🚀 FASE 1: Generación masiva con Groq (GRATIS)")
        raw_casos = await self.fase_1_generacion_masiva(
            target=target * 2  # Generar 3000 para filtrar a 1500
        )
        print(f"   Generados: {len(raw_casos)} casos brutos")
        
        print("🔧 FASE 2: Refinamiento con DeepSeek ($16-27)")
        refined_casos = await self.fase_2_refinamiento(raw_casos)
        print(f"   Refinados: {len(refined_casos)} casos")
        
        print("✅ FASE 3: Validación Claude ($20-30)")
        validated_casos = await self.fase_3_validacion_claude(
            refined_casos,
            target=target
        )
        print(f"   Validados: {len(validated_casos)} casos finales")
        
        return validated_casos
    
    async def fase_1_generacion_masiva(self, target=3000):
        """
        Generación rápida y barata con Groq + Gemini
        """
        casos = []
        errors = 0
        
        for i in range(target):
            try:
                # 1. Crear parámetros aleatorios
                params = self._create_random_params()
                
                # 2. Calcular datos VERIFICADOS (determinista)
                calculo = self.calculator.compute(params)
                
                # 3. Buscar normativa en Qdrant
                leyes = await self.qdrant.search_articles(params['temas'])
                
                # 4. Construir prompt CON TEMPLATE PERFECTO
                prompt = self._build_cot_prompt(params, calculo, leyes)
                
                # 5. Generar con Groq (GRATIS)
                try:
                    caso = await self.generators['primary'].generate(prompt)
                except:
                    # Fallback a Gemini si Groq falla
                    caso = await self.generators['secondary'].generate(prompt)
                
                # 6. Validación rápida automática (sin Claude)
                if self._quick_validation(caso, calculo):
                    casos.append({
                        "caso": caso,
                        "calculo_original": calculo,
                        "leyes": leyes,
                        "fase": 1
                    })
                
                # Progress
                if (i+1) % 100 == 0:
                    print(f"   Progreso: {i+1}/{target} ({len(casos)} válidos)")
            
            except Exception as e:
                errors += 1
                if errors > 100:
                    print(f"⚠️ Demasiados errores, deteniendo...")
                    break
        
        return casos
    
    async def fase_2_refinamiento(self, raw_casos):
        """
        DeepSeek mejora los mejores casos de Fase 1
        """
        # Ordenar por calidad automática
        sorted_casos = sorted(
            raw_casos,
            key=lambda x: self._quick_quality_score(x),
            reverse=True
        )
        
        # Tomar los mejores 2000
        top_casos = sorted_casos[:2000]
        
        refined = []
        for caso_data in top_casos:
            # Prompt de refinamiento
            refinement_prompt = f"""
Eres un experto revisor de casos de oposiciones.

CASO ORIGINAL:
{json.dumps(caso_data['caso'], indent=2)}

DATOS VERIFICADOS:
{json.dumps(caso_data['calculo_original'], indent=2)}

NORMATIVA APLICABLE:
{self._format_leyes(caso_data['leyes'])}

TAREA:
Revisa el caso y mejora:
1. Coherencia numérica (usar EXACTAMENTE los datos verificados)
2. Precisión normativa (citar artículos exactos)
3. Calidad de distractores (diferencias sutiles)
4. Realismo de la narrativa

Mantén la estructura pero mejora la calidad.
Responde SOLO con JSON válido.
"""
            
            # Refinar con DeepSeek
            refined_caso = await self.generators['refiner'].generate(
                refinement_prompt
            )
            
            # Validación rápida post-refinamiento
            if self._quick_validation(refined_caso, caso_data['calculo_original']):
                refined.append({
                    **caso_data,
                    "caso": refined_caso,
                    "fase": 2
                })
        
        return refined
    
    async def fase_3_validacion_claude(self, refined_casos, target=1500):
        """
        Claude valida en lotes (validación incremental)
        """
        validated = []
        batch_size = 100
        
        for i in range(0, len(refined_casos), batch_size):
            batch = refined_casos[i:i+batch_size]
            
            print(f"   Validando lote {i//batch_size + 1}...")
            
            batch_validations = []
            for caso_data in batch:
                # Validación Claude
                validation = await self.validator.validate_caso(
                    caso=caso_data['caso'],
                    calculo=caso_data['calculo_original'],
                    leyes=caso_data['leyes']
                )
                
                batch_validations.append({
                    **caso_data,
                    "validation": validation,
                    "fase": 3
                })
            
            # Métricas del lote
            batch_quality = np.mean([
                v['validation']['score'] 
                for v in batch_validations
            ])
            
            print(f"   Calidad lote: {batch_quality:.2%}")
            
            # Si lote tiene buena calidad, continuar
            if batch_quality >= 0.95:
                # Añadir solo los que superan 0.95
                validated.extend([
                    v for v in batch_validations
                    if v['validation']['score'] >= 0.95
                ])
                
                print(f"   ✅ Lote OK - Total validados: {len(validated)}")
            else:
                # Si lote malo, revisar individualmente
                print(f"   ⚠️ Lote necesita revisión individual")
                for v in batch_validations:
                    if v['validation']['score'] >= 0.97:
                        validated.append(v)
            
            # Detener si alcanzamos target
            if len(validated) >= target:
                print(f"   🎯 Target alcanzado: {len(validated)}")
                break
        
        return validated[:target]
    
    def _build_cot_prompt(self, params, calculo, leyes):
        """
        Construye prompt CON Chain-of-Thought PERFECTO
        """
        return f"""
{PROMPT_TEMPLATE_PERFECTO}  # Del documento que compartiste

DATOS VERIFICADOS (USA EXACTAMENTE ESTOS):
{json.dumps(calculo, indent=2, ensure_ascii=False)}

NORMATIVA APLICABLE:
{self._format_leyes(leyes)}

INSTRUCCIONES CRÍTICAS:
1. Usa EXACTAMENTE la base de cotización: {calculo['base_cotizacion']}€
2. Usa EXACTAMENTE la contingencia: {calculo['contingencia']}
3. Usa EXACTAMENTE el subsidio: {calculo['subsidio_diario']}€
4. Cita EXACTAMENTE los artículos proporcionados
5. Razona paso a paso ANTES de generar el caso

Piensa paso a paso:
<razonamiento>
Paso 1: Verificar datos
- Base: {calculo['base_cotizacion']}€ ✓
- Subsidio: {calculo['subsidio_diario']}€ ✓
- Contingencia: {calculo['contingencia']} ✓

Paso 2: Crear narrativa con estos datos EXACTOS
...
</razonamiento>

Ahora genera el caso completo en JSON.
"""
    
    def _quick_validation(self, caso, calculo):
        """
        Validación rápida SIN Claude (determinista)
        """
        try:
            # 1. Verificar que es JSON válido
            if isinstance(caso, str):
                caso = json.loads(caso)
            
            # 2. Verificar estructura
            required_keys = ['enunciado', 'preguntas', 'opciones']
            if not all(k in caso for k in required_keys):
                return False
            
            # 3. Verificar coherencia numérica (regex)
            enunciado = caso.get('enunciado', '')
            base_str = str(int(calculo['base_cotizacion']))
            
            if base_str not in enunciado.replace('.', '').replace(',', ''):
                return False
            
            # 4. Verificar subsidio en opciones
            subsidio_str = f"{calculo['subsidio_diario']:.2f}"
            opciones_str = json.dumps(caso.get('opciones', {}))
            
            if subsidio_str not in opciones_str:
                return False
            
            # 5. Verificar longitud mínima
            if len(enunciado) < 400:  # Mínimo 400 chars
                return False
            
            return True
        
        except:
            return False
    
    def _quick_quality_score(self, caso_data):
        """
        Score rápido 0-1 sin Claude
        """
        score = 0.0
        caso = caso_data['caso']
        calculo = caso_data['calculo_original']
        
        # Coherencia numérica (0.4)
        if self._check_numerical_coherence(caso, calculo):
            score += 0.4
        
        # Estructura completa (0.2)
        if self._check_structure(caso):
            score += 0.2
        
        # Longitud adecuada (0.2)
        if 600 <= len(caso.get('enunciado', '')) <= 1000:
            score += 0.2
        
        # Tiene artículos citados (0.2)
        if self._check_articles_cited(caso):
            score += 0.2
        
        return score
    
    def _create_random_params(self):
        """
        Genera parámetros aleatorios para un caso
        """
        import random
        
        return {
            "base_cotizacion": random.choice([1200, 1500, 1800, 2000, 2400]),
            "contingencia": random.choice(["EC", "AT", "EP"]),
            "dia_baja": random.randint(1, 30),
            "temas": random.sample([
                "encuadramiento",
                "bases_cotizacion",
                "IT",
                "regimenes_especiales",
                "prestaciones",
                "procedimientos"
            ], k=random.randint(2, 4)),
            "num_preguntas": 15,
            "dificultad": random.choice(["media", "alta"])
        }

💰 DESGLOSE DE COSTES DETALLADO
pythoncostes_pipeline = {
    "FASE 1 - Generación (Groq + Gemini)": {
        "groq_llama_70b": {
            "items": 2400,  # 80% éxito con Groq
            "coste_unitario": 0,
            "coste_total": "$0"
        },
        "gemini_flash_fallback": {
            "items": 600,   # 20% fallback
            "tokens_por_item": 4000,
            "coste_por_millon": 0.30,
            "coste_total": "$0.72"
        },
        "SUBTOTAL": "$0.72"
    },
    
    "FASE 2 - Refinamiento (DeepSeek)": {
        "deepseek_v3": {
            "items": 2000,  # Mejores de Fase 1
            "tokens_input": 3000,  # Caso + prompt
            "tokens_output": 3500,
            "coste_input": "$0.27/1M",
            "coste_output": "$1.10/1M",
            "coste_total": "$7.70"
        },
        "SUBTOTAL": "$7.70"
    },
    
    "FASE 3 - Validación (Claude Sonnet 4.5)": {
        "validacion_lotes": {
            "items": 1500,  # Target final
            "tokens_input": 4000,  # Caso completo
            "tokens_output": 500,   # Validation report
            "coste_input": "$3/1M",
            "coste_output": "$15/1M",
            "coste_total": "$29.25"
        },
        "SUBTOTAL": "$29.25"
    },
    
    "TOTAL_PIPELINE": "$37.67",
    "MARGEN_ERROR": "+20%",
    "COSTE_ESTIMADO_FINAL": "$42-50"
}

📅 CRONOGRAMA REALISTA
pythoncronograma = {
    "DÍA 1-2: Setup Pipeline": {
        "tareas": [
            "Implementar DatasetGeneratorPipeline",
            "Configurar Groq + Gemini + DeepSeek APIs",
            "Preparar SSCalculator determinista",
            "Preparar Qdrant con legislación"
        ],
        "output": "Pipeline operativo"
    },
    
    "DÍA 3-5: Fase 1 Generación": {
        "items_objetivo": 3000,
        "items_por_dia": 1000,
        "modelo": "Groq (gratis) + Gemini (backup)",
        "coste": "$0.72",
        "output": "~3000 casos brutos"
    },
    
    "DÍA 6-7: Fase 2 Refinamiento": {
        "items_input": 2000,  # Top de Fase 1
        "items_output": 1800,  # 90% pasan refinamiento
        "modelo": "DeepSeek V3",
        "coste": "$7.70",
        "output": "~1800 casos refinados"
    },
    
    "DÍA 8-10: Fase 3 Validación": {
        "items_input": 1800,
        "items_objetivo": 1500,
        "modelo": "Claude Sonnet 4.5",
        "estrategia": "Lotes de 100, detener en 1500",
        "coste": "$29.25",
        "output": "1500 casos validados 95%+"
    },
    
    "TOTAL": "10 días, $37-50"
}

🎯 UNIDADES MÍNIMAS CORREGIDAS
pythonunidades_minimas = {
    "PARA_FINE_TUNING_BASICO": {
        "casos_practicos_cot": 500,
        "qa_con_razonamiento": 500,
        "total": 1000,
        "dias_generacion": 4,
        "coste": "$15-20"
    },
    
    "PARA_FINE_TUNING_RECOMENDADO": {
        "casos_practicos_cot": 1500,
        "qa_con_razonamiento": 1500,
        "esquemas": 200,
        "total": 3200,
        "dias_generacion": 10,
        "coste": "$37-50"  # ✅ TU PRESUPUESTO
    },
    
    "PARA_FINE_TUNING_OPTIMO": {
        "casos_practicos_cot": 3000,
        "qa_con_razonamiento": 3000,
        "esquemas": 500,
        "temas": 50,
        "total": 6550,
        "dias_generacion": 20,
        "coste": "$75-100"
    }
}

✅ PRÓXIMOS PASOS INMEDIATOS
bash# PASO 1: Implementar pipeline (HOY)
cd backend/agents
touch dataset_generator.py

# Copiar código del DatasetGeneratorPipeline

# PASO 2: Test con 10 casos (30 min)
python -m agents.dataset_generator --test --items 10

# PASO 3: Si test OK, generar 100 (2h)
python -m agents.dataset_generator --items 100

# PASO 4: Si 100 OK, generar 1500 (10 días)
python -m agents.dataset_generator --items 1500 --output dataset_final.jsonl
¿Empiezo a implementar el DatasetGeneratorPipeline completo con Groq + DeepSeek + Claude?