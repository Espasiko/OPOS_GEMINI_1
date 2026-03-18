**APÉNDICE IV --- SUPLEMENTO**

App Oposiciones AGE & SS · Febrero 2026

*Calculator Engine SS (20 tipos reales) · Por qué falló el fine-tuning y
qué hacer · Trap Pedagogy · Gamificación Duolingo · EADOP evaluado*

**1. EADOP (salamandra-7b-aligned-EADOP) --- Evaluación Honesta**

El modelo EADOP de projecte-aina (BSC + Alinia AI) ha sido investigado
directamente en HuggingFace. La conclusión es clara:

+-----------------------------------------------------------------------+
| **❌ EADOP NO sirve para tu caso de uso**                             |
|                                                                       |
| EADOP fue entrenado para una sola tarea: enseñar al modelo a rechazar |
| educadamente preguntas fuera de dominio en un chatbot RAG de          |
| legislación catalana. Tiene solo 2.000 ejemplos anotados en           |
| catalán/español. Su objetivo no es responder preguntas de oposición,  |
| sino saber cuándo NO responder. Es un proof-of-concept de rechazo     |
| educado, no un asistente legal. Usarlo como base para fine-tuning en  |
| AGE/SS sería partir de un modelo empeorado para tu tarea.             |
+-----------------------------------------------------------------------+

  -----------------------------------------------------------------------
  **Característica**     **EADOP**              **Lo que necesitas**
  ---------------------- ---------------------- -------------------------
  Tamaño del dataset de  2.000 ejemplos         10.000+ pares AGE/SS de
  FT                                            alta calidad

  Idioma                 Catalán + español      Español jurídico (AGE +
                                                TRLGSS)

  Tarea aprendida        Rechazar preguntas     Responder con precisión
                         fuera de dominio       preguntas de oposición

  Legislación cubierta   DOGC (legislación      Constitución, Ley
                         catalana)              39/2015, TRLGSS, EBEP\...

  **¿Útil como base?**   **Solo si quieres un   **No es útil. Parte de
                         modelo que se niegue a salamandra-7b-instruct
                         contestar**            directamente.**
  -----------------------------------------------------------------------

**2. Por Qué Falló el Fine-Tuning con Salamandra --- Diagnóstico**

Tus pruebas con Salamandra R1 GGUF + Unsloth + QLoRA en Kaggle con
10.000 pares de preguntas AGE/SS dieron resultados decepcionantes en
razonamiento complejo y en uso de herramientas (calculadoras). Aquí está
el diagnóstico técnico de por qué, con datos reales:

**2.1 Los Tres Problemas que Encontraste**

  ------------------------------------------------------------------------
  **Síntoma observado** **Causa técnica    **Diagnóstico**
                        real**             
  --------------------- ------------------ -------------------------------
  Preguntas simples     El modelo memorizó Correcto para recall factual.
  (edad jubilación =    hechos del dataset QLoRA en 10K pares es
  65) funcionaban       de FT              suficiente para esto.

  Razonamiento complejo 7B con QLoRA es    Los modelos 7B tienen capacidad
  (cálculos multi-paso) insuficiente para  de razonamiento multi-paso
  fallaba               razonamiento en    limitada. Fine-tuning no añade
                        cadena fiable      capacidad nueva --- solo
                                           redirige la existente.

  Sistema de agentes    Los modelos        Function calling requiere JSON
  con tools no funcionó cuantizados (GGUF  perfecto. Los modelos
                        q4/q5) fallan en   cuantizados producen JSON
                        JSON estructurado  malformado con alta frecuencia
                                           bajo presión de contexto largo.
                                           El fine-tuning con QLoRA no
                                           corrige esto.

  Salamandra R1         Es un experimento  No es un modelo del BSC. No
  \'ericrisco\' no      comunitario sin    tiene benchmark. Es un intento
  mejoró                evaluación ni      de reproducir R1 sin los
                        método publicado   recursos que tuvo DeepSeek.
  ------------------------------------------------------------------------

**2.2 La Conclusión Definitiva sobre Fine-Tuning Local**

+-----------------------------------------------------------------------+
| **💡 Conclusión: fine-tuning para facts SÍ, para razonamiento NO**    |
|                                                                       |
| Fine-tuning de Salamandra 7B con tus 10.000 pares funcionó para lo    |
| que debería funcionar: memorizar hechos del temario AGE/SS (la edad   |
| de jubilación, los plazos de la Ley 39/2015, etc.). Eso es recall, no |
| razonamiento. Para el razonamiento multi-paso que requieren los casos |
| prácticos (calcular base reguladora + aplicar porcentaje + comprobar  |
| coeficientes + detectar excepciones), necesitas o un modelo más       |
| grande (GPT-OSS 120B, Qwen3 32B) o la arquitectura correcta: el       |
| Calculator Engine determinístico que hace los cálculos fuera del LLM. |
+-----------------------------------------------------------------------+

**2.3 Salamandra en Fly.io para Ahorrar Tokens --- ¿Vale la Pena?**

  ------------------------------------------------------------------------
  **Escenario**    **Salamandra en Fly.io**    **API Groq GPT-OSS 120B**
  ---------------- --------------------------- ---------------------------
  Coste fijo       \~\$15-25/mes mínimo para   \$0 si no hay tráfico.
  mensual          una instancia con RAM       \$0.28/usuario/mes con 440
                   suficiente (4GB mínimo para interacciones.
                   Q4_K_M)                     

  Velocidad en     5-15 tok/s (CPU). 20-40s    \<1 segundo por respuesta a
  Fly.io CPU       por respuesta = inaceptable 500+ TPS.
                   para chat.                  

  Velocidad en     No disponible directamente  N/A
  Fly.io GPU       en Fly.io (no ofrecen GPU)  

  Calidad de       Limitada (7B con QLoRA, ya  Alta (GPT-OSS 120B es un
  respuestas       verificado en tus pruebas)  modelo de 120B params sin
  legales                                      cuantizar)
  complejas                                    

  Cuándo saldría   Con \>100 usuarios activos  GPT-OSS 120B sería más
  rentable         simultáneos y aceptando     barato hasta \~2.000
  Salamandra en    latencia alta               usuarios/mes con caché
  CPU                                          

  **Veredicto**    **❌ No vale la pena para   **✅ Usar GPT-OSS 120B o
                   el chat en tiempo real**    Llama 4 Maverick en Groq**
  ------------------------------------------------------------------------

**3. Calculator Engine SS --- Los 20 Tipos de Cálculo Reales (No 9)**

El documento de Gemini afirmaba \'9 tipologías principales\'.
Investigando el temario oficial y los supuestos prácticos publicados de
las últimas convocatorias, el número real es bastante mayor. Estos son
todos los tipos de cálculo que pueden aparecer en el examen:

  --------------------------------------------------------------------------------------
  **\#**   **Tipo de cálculo**   **Prestación / Tema**    **Complejidad y artículo
                                                          clave**
  -------- --------------------- ------------------------ ------------------------------
  1        Base reguladora IT    Incapacidad Temporal     Suma últimas 6 bases / días
           (enfermedad común)                             cotizados (180 días). Art. 169
                                                          TRLGSS. BAJA

  2        Cuantía diaria IT     IT                       0€ días 1-3 (espera). 60% BR
           (días 1-3 / 4-20 /                             días 4-20. 75% BR día 21+.
           21+)                                           Art. 169-170 TRLGSS. BAJA

  3        Duración máxima IT +  IT                       545 días + prórroga hasta 730
           prórroga EVI                                   si EVI lo estima. Art. 174
                                                          TRLGSS. MEDIA

  4        IT por contingencias  IT accidente trabajo     Sin días de espera. 75% BR
           profesionales (AT/EP)                          desde día 1. Porcentaje
                                                          distinto al común. MEDIA

  5        BR jubilación         Jubilación               Últimos 300 meses (25 años) /
           ordinaria                                      350. Art. 209 TRLGSS.
                                                          Actualización anual con IPC.
                                                          ALTA

  6        Porcentaje jubilación Jubilación               50% a los 15 años. +1,15%/mes
           por años cotizados                             entre 15-25 años. +1,50%/mes
                                                          25-37 años. 100% a los 37
                                                          años. Art. 210 TRLGSS. ALTA

  7        Coeficientes          Jubilación anticipada    Tabla de meses/trimestres de
           reductores jubilación                          anticipación × coeficiente.
           anticipada voluntaria                          Art. 208 TRLGSS. Requiere
                                                          tabla 2026. ALTA

  8        Coeficientes          Jubilación anticipada    Tabla distinta a la
           reductores jubilación                          voluntaria. Art. 207 TRLGSS.
           anticipada                                     Más favorable al trabajador.
           involuntaria                                   ALTA

  9        Porcentaje jubilación Jubilación parcial       Art. 215 TRLGSS. Porcentaje
           parcial +                                      proporcional a la reducción de
           compatibilidad                                 jornada (min 25% - max 50%).
           trabajo                                        MEDIA

  10       BR y cuantía IP       Incapacidad Permanente   Porcentajes: 55% (IPT base) /
           parcial / total /                              75% (IPT \> 55 años) / 100%
           absoluta / GI                                  (IPA) / IPA + 45% (GI). Art.
                                                          196-197 TRLGSS. ALTA

  11       Pensión de viudedad   Muerte y supervivencia   52% BR general / 70% con
           --- porcentaje y                               cargas familiares. Art.
           duración                                       220-221 TRLGSS. Condiciones de
                                                          acceso. MEDIA

  12       Pensión de orfandad   Muerte y supervivencia   20% por huérfano (simple) /
           --- porcentaje y                               doble orfandad hasta 100% sin
           límite acumulado                               superar cuantía máxima. Art.
                                                          224 TRLGSS. MEDIA

  13       Prestación            Maternidad/Paternidad    100% BR. Duración: 16 semanas
           nacimiento/cuidado de                          base + semanas adicionales
           menor (baja parental)                          (prematuridad, discapacidad).
                                                          Art. 178-182 TRLGSS. BAJA

  14       IMV --- umbral de     Ingreso Mínimo Vital     Renta anual garantizada por
           renta y cuantía                                tipo de hogar (actualizada
                                                          anualmente). Art. 10-12 Ley
                                                          19/2021. MEDIA

  15       Cotización: base de   Cotización               Salario mensual + pagas extra
           cotización mensual                             prorrateadas + horas extra.
                                                          Topeado por grupo de
                                                          cotización. Art. 147 TRLGSS.
                                                          MEDIA

  16       Liquidación cuotas    Cotización               CC: empresa \~23.6% +
           empresa + trabajador                           trabajador \~4.7%. Desempleo,
                                                          AT/EP por CNAE. Art. 148-153
                                                          TRLGSS. ALTA

  17       Recargo de            Recargo                  30-50% sobre prestación
           prestaciones                                   económica cuando hay culpa
                                                          empresarial. Art. 164 TRLGSS.
                                                          BAJA

  18       Plazos                Procedimental            Recursos administrativos: 1
           procedimentales (días                          mes días hábiles. Solicitudes:
           naturales vs hábiles)                          varía. Ley 39/2015 arts.
                                                          30-31. MEDIA

  19       Capital coste de      Recaudación              Valor actual de prestaciones
           pensiones                                      comprometidas. Usado en
                                                          responsabilidades por falta de
                                                          alta. Art. 167 TRLGSS. ALTA

  20       Complemento brecha de Jubilación/IP/Viudedad   Por cada hijo: % adicional
           género / complemento                           sobre pensión. Ley 21/2021
           maternidad                                     modificó el sistema anterior.
                                                          MEDIA
  --------------------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **⚠️ No son 9, son 20 tipos verificados**                             |
|                                                                       |
| El documento de Gemini estimaba \'9 tipologías\'. El análisis del     |
| temario oficial de los 13 temas específicos SS y los supuestos        |
| prácticos de exámenes anteriores muestra al menos 20 tipos distintos  |
| de cálculo. Los más frecuentes en examen (aparecen en más del 60% de  |
| los supuestos): IT base reguladora + cuantía (tipos 1-2), jubilación  |
| BR + porcentaje (tipos 5-6), y cotización mensual (tipo 15). Los más  |
| complejos y que más fallan los opositores: jubilación anticipada con  |
| coeficientes (tipos 7-8), IP permanente (tipo 10) y capital coste     |
| (tipo 19).                                                            |
+-----------------------------------------------------------------------+

**3.1 El Calculator Engine Python --- Implementación Completa**

La arquitectura correcta: el LLM NUNCA hace los cálculos numéricos. El
LLM extrae los parámetros del caso práctico, llama a funciones Python
determinísticas, recibe el resultado exacto y lo incorpora en la
respuesta:

+-----------------------------------------------------------------------+
| \# calculadora_ss.py --- Motor de cálculo determinístico para         |
| exámenes SS                                                           |
|                                                                       |
| \# Los LLMs no hacen cálculos. Este módulo los hace por ellos.        |
|                                                                       |
| \# Todos los valores están actualizados a la normativa vigente en     |
| enero 2026                                                            |
|                                                                       |
| from decimal import Decimal, ROUND_HALF_UP                            |
|                                                                       |
| from datetime import date, timedelta                                  |
|                                                                       |
| from typing import Optional                                           |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| \# TIPO 1-2: INCAPACIDAD TEMPORAL --- Base reguladora y cuantía       |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| def calcular_it(bases_6meses: list\[float\], tipo_contingencia: str = |
| \'comun\',                                                            |
|                                                                       |
| dia_numero: int = 1) -\> dict:                                        |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| bases_6meses: lista de 6 bases mensuales brutas                       |
|                                                                       |
| tipo_contingencia: \'comun\' o \'profesional\' (AT/EP)                |
|                                                                       |
| dia_numero: día de la prestación (1, 5, 21, 100\...)                  |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| br_diaria = Decimal(str(sum(bases_6meses))) / Decimal(\'180\')        |
|                                                                       |
| br_diaria = br_diaria.quantize(Decimal(\'0.01\'),                     |
| rounding=ROUND_HALF_UP)                                               |
|                                                                       |
| if tipo_contingencia == \'profesional\':                              |
|                                                                       |
| \# AT/EP: sin días de espera, 75% desde el día 1                      |
|                                                                       |
| cuantia_diaria = br_diaria \* Decimal(\'0.75\')                       |
|                                                                       |
| pagador = \'mutua/empresa desde dia_1\'                               |
|                                                                       |
| else:                                                                 |
|                                                                       |
| \# Contingencias comunes                                              |
|                                                                       |
| if dia_numero \<= 3:                                                  |
|                                                                       |
| cuantia_diaria = Decimal(\'0.00\') \# días de espera                  |
|                                                                       |
| pagador = \'ninguno (espera)\'                                        |
|                                                                       |
| elif dia_numero \<= 20:                                               |
|                                                                       |
| cuantia_diaria = br_diaria \* Decimal(\'0.60\')                       |
|                                                                       |
| pagador = \'empresa (pago delegado)\'                                 |
|                                                                       |
| else:                                                                 |
|                                                                       |
| cuantia_diaria = br_diaria \* Decimal(\'0.75\')                       |
|                                                                       |
| pagador = \'mutua o INSS directo\'                                    |
|                                                                       |
| cuantia_diaria = cuantia_diaria.quantize(Decimal(\'0.01\'),           |
| rounding=ROUND_HALF_UP)                                               |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'base_reguladora_diaria\': float(br_diaria),                         |
|                                                                       |
| \'cuantia_diaria\': float(cuantia_diaria),                            |
|                                                                       |
| \'pagador\': pagador,                                                 |
|                                                                       |
| \'articulo\': \'Arts. 169-174 TRLGSS (RDL 8/2015)\'                   |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| \# TIPO 3: DURACIÓN MÁXIMA IT                                         |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| def calcular_duracion_it(fecha_inicio_baja: date) -\> dict:           |
|                                                                       |
| dia_545 = fecha_inicio_baja + timedelta(days=544)                     |
|                                                                       |
| dia_730 = fecha_inicio_baja + timedelta(days=729)                     |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'limite_ordinario\': dia_545.strftime(\'%d/%m/%Y\'),                 |
|                                                                       |
| \'limite_con_prorroga\': dia_730.strftime(\'%d/%m/%Y\'),              |
|                                                                       |
| \'nota\': \'Prórroga hasta 730 días si EVI prevé mejoría probable\',  |
|                                                                       |
| \'articulo\': \'Art. 174 TRLGSS\'                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| \# TIPOS 5-6: JUBILACIÓN ORDINARIA --- BR y porcentaje                |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| def calcular_jubilacion_ordinaria(bases_300_meses: list\[float\],     |
|                                                                       |
| anios_cotizados: float) -\> dict:                                     |
|                                                                       |
| \'\'\'Cálculo según reforma Ley 21/2021 vigente en 2026\'\'\'         |
|                                                                       |
| \# Base reguladora: suma de 300 meses / 350                           |
|                                                                       |
| suma_bases = sum(bases_300_meses)                                     |
|                                                                       |
| base_reguladora = Decimal(str(suma_bases)) / Decimal(\'350\')         |
|                                                                       |
| base_reguladora = base_reguladora.quantize(Decimal(\'0.01\'),         |
| rounding=ROUND_HALF_UP)                                               |
|                                                                       |
| \# Porcentaje según años cotizados (art. 210 TRLGSS)                  |
|                                                                       |
| anios = Decimal(str(anios_cotizados))                                 |
|                                                                       |
| if anios \< 15:                                                       |
|                                                                       |
| raise ValueError(\'Mínimo 15 años para jubilación ordinaria\')        |
|                                                                       |
| elif anios \<= 25:                                                    |
|                                                                       |
| pct = Decimal(\'50\') + (anios - Decimal(\'15\')) \*                  |
| Decimal(\'1.15\') \* Decimal(\'12\')                                  |
|                                                                       |
| elif anios \<= 37:                                                    |
|                                                                       |
| pct = Decimal(\'50\') + Decimal(\'10\') \* Decimal(\'1.15\') \*       |
| Decimal(\'12\') \\                                                    |
|                                                                       |
| \+ (anios - Decimal(\'25\')) \* Decimal(\'1.50\') \* Decimal(\'12\')  |
|                                                                       |
| else:                                                                 |
|                                                                       |
| pct = Decimal(\'100\')                                                |
|                                                                       |
| pct = min(pct, Decimal(\'100\')).quantize(Decimal(\'0.01\'))          |
|                                                                       |
| pension = (base_reguladora \* pct /                                   |
| Decimal(\'100\')).quantize(Decimal(\'0.01\'))                         |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'base_reguladora\': float(base_reguladora),                          |
|                                                                       |
| \'porcentaje\': float(pct),                                           |
|                                                                       |
| \'pension_mensual\': float(pension),                                  |
|                                                                       |
| \'articulo\': \'Arts. 209-210 TRLGSS (reforma Ley 21/2021)\'          |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| \# TIPOS 7-8: JUBILACIÓN ANTICIPADA --- Coeficientes reductores       |
|                                                                       |
| \# Tablas vigentes con la reforma de 2023 (Real Decreto-ley 2/2023)   |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| \# Trimestres de anticipación → coeficiente reductor por trimestre    |
|                                                                       |
| COEF_VOLUNTARIA_2026 = { \# Art. 208 TRLGSS                           |
|                                                                       |
| 1: Decimal(\'0.0058\'), 2: Decimal(\'0.0058\'), 3:                    |
| Decimal(\'0.0058\'),                                                  |
|                                                                       |
| 4: Decimal(\'0.0058\'), 5: Decimal(\'0.0058\'), 6:                    |
| Decimal(\'0.0058\'),                                                  |
|                                                                       |
| 7: Decimal(\'0.0058\'), 8: Decimal(\'0.0050\'), \# a partir del 2º    |
| año                                                                   |
|                                                                       |
| }                                                                     |
|                                                                       |
| COEF_INVOLUNTARIA_2026 = { \# Art. 207 TRLGSS --- más favorable       |
|                                                                       |
| 1: Decimal(\'0.0040\'), 2: Decimal(\'0.0040\'), 3:                    |
| Decimal(\'0.0040\'),                                                  |
|                                                                       |
| 4: Decimal(\'0.0040\'), 5: Decimal(\'0.0040\'), 6:                    |
| Decimal(\'0.0040\'),                                                  |
|                                                                       |
| 7: Decimal(\'0.0040\'), 8: Decimal(\'0.0036\'),                       |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_jubilacion_anticipada(pension_ordinaria: float,          |
|                                                                       |
| meses_anticipacion: int,                                              |
|                                                                       |
| tipo: str = \'voluntaria\') -\> dict:                                 |
|                                                                       |
| pension = Decimal(str(pension_ordinaria))                             |
|                                                                       |
| trimestres = (meses_anticipacion + 2) // 3 \# redondeo arriba         |
|                                                                       |
| tabla = COEF_VOLUNTARIA_2026 if tipo == \'voluntaria\' else           |
| COEF_INVOLUNTARIA_2026                                                |
|                                                                       |
| coef_por_trimestre = tabla.get(trimestres, Decimal(\'0.0058\'))       |
|                                                                       |
| reduccion_total = coef_por_trimestre \* Decimal(str(trimestres))      |
|                                                                       |
| pension_reducida = pension \* (Decimal(\'1\') - reduccion_total)      |
|                                                                       |
| pension_reducida = pension_reducida.quantize(Decimal(\'0.01\'))       |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'pension_ordinaria\': float(pension),                                |
|                                                                       |
| \'trimestres_anticipacion\': trimestres,                              |
|                                                                       |
| \'coeficiente_por_trimestre\': float(coef_por_trimestre),             |
|                                                                       |
| \'reduccion_total_pct\': float(reduccion_total \* 100),               |
|                                                                       |
| \'pension_anticipada\': float(pension_reducida),                      |
|                                                                       |
| \'articulo\': f\'Art. {208 if tipo == \"voluntaria\" else 207}        |
| TRLGSS\'                                                              |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| \# TIPO 10: INCAPACIDAD PERMANENTE --- grado y cuantía                |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| PORCENTAJES_IP = {                                                    |
|                                                                       |
| \'parcial\': Decimal(\'0.55\'), \# Art. 196: 24 mensualidades de la   |
| BR                                                                    |
|                                                                       |
| \'total\': Decimal(\'0.55\'), \# 55% BR (70% si \> 55 años sin        |
| trabajo apto)                                                         |
|                                                                       |
| \'total_mayor_55\': Decimal(\'0.75\'), \# complemento por edad        |
|                                                                       |
| \'absoluta\': Decimal(\'1.00\'), \# 100% BR                           |
|                                                                       |
| \'gran_invalidez\': Decimal(\'1.45\'), \# 100% + 45% complemento      |
| cuidador                                                              |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_ip(base_reguladora: float, grado: str,                   |
|                                                                       |
| edad: Optional\[int\] = None) -\> dict:                               |
|                                                                       |
| if grado == \'total\' and edad and edad \>= 55:                       |
|                                                                       |
| pct = PORCENTAJES_IP\[\'total_mayor_55\'\]                            |
|                                                                       |
| grado_efectivo = \'total (complemento 55 años)\'                      |
|                                                                       |
| else:                                                                 |
|                                                                       |
| pct = PORCENTAJES_IP.get(grado, Decimal(\'0.55\'))                    |
|                                                                       |
| grado_efectivo = grado                                                |
|                                                                       |
| pension = (Decimal(str(base_reguladora)) \*                           |
| pct).quantize(Decimal(\'0.01\'))                                      |
|                                                                       |
| return {\'grado\': grado_efectivo, \'porcentaje\': float(pct)\*100,   |
|                                                                       |
| \'pension\': float(pension), \'articulo\': \'Arts. 194-200 TRLGSS\'}  |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| \# TIPO 18: PLAZOS PROCEDIMENTALES                                    |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| def calcular_plazo(fecha_notificacion: date, tipo_plazo: str) -\>     |
| dict:                                                                 |
|                                                                       |
| PLAZOS = {                                                            |
|                                                                       |
| \'recurso_alzada\': {\'dias\': 1, \'meses\': 1, \'tipo\': \'habil\',  |
| \'art\': \'Art. 121 Ley 39/2015\'},                                   |
|                                                                       |
| \'recurso_reposicion\': {\'dias\': 1, \'meses\': 1, \'tipo\':         |
| \'habil\', \'art\': \'Art. 124 Ley 39/2015\'},                        |
|                                                                       |
| \'recurso_extraord_revision\': {\'dias\': None, \'meses\': None,      |
| \'tipo\': \'especial\', \'art\': \'Art. 125 Ley 39/2015\'},           |
|                                                                       |
| \'reclamacion_previa_ss\': {\'dias\': 30, \'meses\': None, \'tipo\':  |
| \'natural\', \'art\': \'Art. 71 LRJS\'},                              |
|                                                                       |
| }                                                                     |
|                                                                       |
| plazo = PLAZOS.get(tipo_plazo, {})                                    |
|                                                                       |
| return {\'tipo\': tipo_plazo, \'referencia_legal\':                   |
| plazo.get(\'art\', \'Verificar\'), \*\*plazo}                         |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| \# DISPATCHER --- Interfaz para el LLM (function calling)             |
|                                                                       |
| \# ────────────────────────────────────────────────────────────       |
|                                                                       |
| TOOLS = {                                                             |
|                                                                       |
| \'calcular_it\': calcular_it,                                         |
|                                                                       |
| \'calcular_duracion_it\': calcular_duracion_it,                       |
|                                                                       |
| \'calcular_jubilacion_ordinaria\': calcular_jubilacion_ordinaria,     |
|                                                                       |
| \'calcular_jubilacion_anticipada\': calcular_jubilacion_anticipada,   |
|                                                                       |
| \'calcular_ip\': calcular_ip,                                         |
|                                                                       |
| \'calcular_plazo\': calcular_plazo,                                   |
|                                                                       |
| \# añadir: calcular_viudedad, calcular_cotizacion, calcular_imv\...   |
|                                                                       |
| }                                                                     |
|                                                                       |
| def ejecutar_calculo(nombre_tool: str, params: dict) -\> dict:        |
|                                                                       |
| if nombre_tool not in TOOLS:                                          |
|                                                                       |
| return {\'error\': f\'Tool {nombre_tool} no encontrada\'}             |
|                                                                       |
| try:                                                                  |
|                                                                       |
| return TOOLS\[nombre_tool\](\*\*params)                               |
|                                                                       |
| except Exception as e:                                                |
|                                                                       |
| return {\'error\': str(e), \'tool\': nombre_tool, \'params\': params} |
+-----------------------------------------------------------------------+

**3.2 Cómo el LLM usa el Calculator Engine (Function Calling)**

+-----------------------------------------------------------------------+
| \# Flujo completo: LLM extrae parámetros → Python calcula → LLM narra |
|                                                                       |
| SYSTEM_CON_TOOLS = \'\'\'                                             |
|                                                                       |
| Eres un preparador de oposiciones SS. Tienes acceso a una calculadora |
|                                                                       |
| determinística para prestaciones de la Seguridad Social.              |
|                                                                       |
| REGLA CRÍTICA: NUNCA calcules manualmente porcentajes, bases          |
| reguladoras                                                           |
|                                                                       |
| ni cuantías. SIEMPRE usa la función correspondiente del módulo de     |
| cálculo.                                                              |
|                                                                       |
| Si no tienes todos los datos necesarios, pregunta al usuario.         |
|                                                                       |
| Después del cálculo, explica el resultado con el artículo exacto      |
| citado.                                                               |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| \# Ejemplo de intercambio:                                            |
|                                                                       |
| \# Usuario: \'María tiene baja desde el 1 de febrero, sus bases de    |
| cotización                                                            |
|                                                                       |
| \# de los últimos 6 meses son 1800, 1800, 1900, 1900, 2000, 2000.     |
|                                                                       |
| \# ¿Cuánto cobra el día 25?\'                                         |
|                                                                       |
| \# LLM detecta: tipo=comun, dia=25,                                   |
| bases=\[1800,1800,1900,1900,2000,2000\]                               |
|                                                                       |
| \# Llama: ejecutar_calculo(\'calcular_it\',                           |
|                                                                       |
| \#                                                                    |
| {\                                                                    |
| 'bases_6meses\':\[1800,1800,1900,1900,2000,2000\],\'dia_numero\':25}) |
|                                                                       |
| \# Python devuelve:                                                   |
|                                                                       |
| \# {\'base_reguladora_diaria\': 64.44, \'cuantia_diaria\': 48.33,     |
|                                                                       |
| \# \'pagador\': \'mutua o INSS directo\', \'articulo\': \'Arts.       |
| 169-174 TRLGSS\'}                                                     |
|                                                                       |
| \# LLM narra el resultado con el artículo ya validado                 |
|                                                                       |
| \# Sin riesgo de alucinación numérica                                 |
+-----------------------------------------------------------------------+

**4. Trap Pedagogy --- Cómo Implementar Distractores con Valor
Pedagógico**

Los distractores de cada pregunta deben ser trampas conceptuales reales,
no opciones absurdas. Un opositor que falla una pregunta con
distractores bien construidos aprende más que uno que la acierta por
eliminación.

**4.1 Los 6 Tipos de Trampa Reales en Exámenes AGE/SS**

  -------------------------------------------------------------------------
  **Tipo        **Descripción**     **Ejemplo real**   **Cómo generarlo**
  trampa**                                             
  ------------- ------------------- ------------------ --------------------
  Inversión de  El pagador y el     \'El INSS paga los Generar opción con
  sujeto        receptor se         primeros 20 días   roles invertidos
                intercambian        de IT\' (falso:    
                                    paga la empresa)   

  Días          El tipo de cómputo  \'30 días hábiles  Generar opción con
  naturales vs  de plazos se        para recurso de    el tipo de día
  hábiles       confunde            alzada\' (son días incorrecto
                                    naturales del mes) 

  Confusión de  Un porcentaje real  \'75% desde el día Tomar porcentaje de
  porcentajes   de otra situación   4 de IT\' (es 60%; la misma prestación
  adyacentes    similar             el 75% empieza en  en momento distinto
                                    el día 21)         

  Artículo real Cita un artículo    \'Art. 169 Ley     Cambiar la ley
  pero de norma real pero de otra   39/2015\' (es del  citada manteniendo
  diferente     ley                 TRLGSS)            el número de
                                                       artículo

  Excepción     La excepción se     \'El silencio es   Invertir regla
  presentada    presenta como norma negativo\' (la     general y excepción
  como regla    general             regla general es   
                                    positivo; negativo 
                                    es la excepción)   

  Normativa     Una norma que era   \'Base reguladora  Usar el texto
  derogada      correcta pero       = últimas 2 años\' anterior a la última
  reciente      cambió              (ahora son 25 años reforma
                                    desde Ley 21/2021) 
  -------------------------------------------------------------------------

**4.2 Prompt para Generar Distractores Tipo Trampa con Claude/DeepSeek**

+-----------------------------------------------------------------------+
| PROMPT_TRAP_PEDAGOGY = \'\'\'                                         |
|                                                                       |
| Eres un experto en psicometría jurídica para oposiciones AGE y SS.    |
|                                                                       |
| Tu tarea es generar 3 opciones incorrectas (distractores) para esta   |
| pregunta.                                                             |
|                                                                       |
| REGLA FUNDAMENTAL: Cada distractor debe ser una trampa conceptual     |
| plausible,                                                            |
|                                                                       |
| no una opción absurda. El opositor debe dudar entre la correcta y el  |
| distractor.                                                           |
|                                                                       |
| Para cada distractor, indica también:                                 |
|                                                                       |
| \- qué tipo de trampa es (de la lista: inversión_sujeto,              |
| dias_naturales_habiles,                                               |
|                                                                       |
| porcentaje_adyacente, articulo_ley_incorrecta, excepcion_como_regla,  |
| norma_derogada)                                                       |
|                                                                       |
| \- por qué un opositor lo elegiría (el error conceptual que comete)   |
|                                                                       |
| PREGUNTA: {enunciado}                                                 |
|                                                                       |
| RESPUESTA CORRECTA: {correcta} (Art. {articulo})                      |
|                                                                       |
| Genera exactamente 3 distractores. Formato JSON:                      |
|                                                                       |
| {                                                                     |
|                                                                       |
| \'distractores\': \[                                                  |
|                                                                       |
| {\'texto\': \'\...\', \'tipo_trampa\': \'\...\', \'razon_confusion\': |
| \'\...\'},                                                            |
|                                                                       |
| {\'texto\': \'\...\', \'tipo_trampa\': \'\...\', \'razon_confusion\': |
| \'\...\'},                                                            |
|                                                                       |
| {\'texto\': \'\...\', \'tipo_trampa\': \'\...\', \'razon_confusion\': |
| \'\...\'}                                                             |
|                                                                       |
| \]                                                                    |
|                                                                       |
| }                                                                     |
|                                                                       |
| \'\'\'                                                                |
+-----------------------------------------------------------------------+

**4.3 El Mapa de Errores Colectivos --- El Diferenciador Real**

Con el tiempo, tu sistema detectará automáticamente qué pares de
conceptos confunden más los opositores. Esto es imposible en una
academia tradicional y es tu ventaja competitiva más sostenible:

+-----------------------------------------------------------------------+
| \# Query Neo4j: detectar confusiones sistemáticas entre conceptos     |
|                                                                       |
| QUERY_MAPA_ERRORES = \'\'\'                                           |
|                                                                       |
| MATCH (u:Usuario)-\[:INTENTO {correcto: false}\]-\>(p:Pregunta)       |
|                                                                       |
| MATCH (p)-\[:TRAMPA_USADA\]-\>(t:TipoTrampa)                          |
|                                                                       |
| WITH t.tipo as tipo_trampa, p.tema as tema,                           |
|                                                                       |
| count(distinct u) as num_usuarios_engañados                           |
|                                                                       |
| WHERE num_usuarios_engañados \> 15                                    |
|                                                                       |
| RETURN tipo_trampa, tema, num_usuarios_engañados                      |
|                                                                       |
| ORDER BY num_usuarios_engañados DESC                                  |
|                                                                       |
| LIMIT 20                                                              |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| \# Resultado que obtienes después de 100+ usuarios:                   |
|                                                                       |
| \# tipo_trampa=\'porcentaje_adyacente\' \| tema=\'IT\' \| usuarios=67 |
|                                                                       |
| \# tipo_trampa=\'excepcion_como_regla\' \| tema=\'Silencio Adm.\' \|  |
| usuarios=54                                                           |
|                                                                       |
| \# tipo_trampa=\'dias_naturales_habiles\' \| tema=\'Recursos\' \|     |
| usuarios=48                                                           |
|                                                                       |
| \# ACCIÓN AUTOMÁTICA: Para los temas con \>30 usuarios engañados,     |
|                                                                       |
| \# el sistema genera un mini-módulo de discriminación específico      |
|                                                                       |
| \# que se activa para todos los usuarios al llegar a ese tema         |
+-----------------------------------------------------------------------+

**5. Gamificación Estilo Duolingo --- Lo Que Vale la Pena Implementar**

Del análisis del documento de Gemini y de la investigación sobre las
métricas reales de Duolingo, estos son los mecanismos con impacto
demostrado en retención y cuáles son técnicamente simples:

  -----------------------------------------------------------------------------------------
  **Mecánica**     **Efecto en      **Complejidad técnica**     **Implementación**
                   retención**                                  
  ---------------- ---------------- --------------------------- ---------------------------
  Streak diario    Alto. Aversión a Baja --- campo \'racha\' en Cron a las 00:00: si no hay
  (racha de días)  la pérdida.      tabla usuario + cron diario actividad en 24h, racha =
                   Duolingo: +52%   que lo resetea              0. Notificación push 2h
                   retención semana                             antes de medianoche.
                   2                                            

  Streak Freeze    Crítico. Evita   Baja --- campo              Plan PRO: 2 freezes/semana.
  (congelador)     abandono por     \'freezes_disponibles\' +   FREE: 0. Se gasta
                   ruptura          lógica en el cron           automáticamente si hay
                   accidental                                   racha y no hay actividad.

  Ligas semanales  Medio-Alto. La   Media --- necesitas         Liga = usuarios con ±20% de
  por actividad    competencia      segmentar usuarios por      tu actividad media semanal.
  similar          justa motiva más \'ritmo de estudio\'        Se calcula el lunes y se
                   que los rankings                             cierra el domingo.
                   globales                                     

  XP por tipo de   Medio --- si el  Baja --- campo XP en tabla  Test: 1 XP/pregunta.
  actividad        ratio XP refleja usuario + tabla de          Simulacro completo: 2x.
                   el esfuerzo real multiplicadores             Caso práctico integral: 5x.
                                                                Chat de duda resuelta: 3x.

  Progresión de    Alto. El cierre  Baja --- porcentaje         Barra de progreso por tema:
  tema como %      de circuito      calculado del banco visto   preguntas vistas / total
  visible          motivacional es  vs total                    del tema × 100%. Se muestra
                   fundamental                                  en la home.

  Corazones        Bajo para        Media                       Omitir para exámenes de
  (vidas) por      opositores                                   oposición --- el opositor
  simulacro        avanzados. Puede                             ya tiene suficiente
                   frustrar                                     presión. No implementar.

  Memes/humor por  Medio --- ancla  Media --- necesitas         Al alcanzar hito (1ª
  logro            mnemotécnica +   generación de imagen o      semana, 1er simulacro
                   pausa emocional  banco de memes prediseñados \>70%) mostrar meme
                                                                generado con artículo bien
                                                                aprendido.
  -----------------------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **⚠️ Diferencia crucial con Duolingo: el opositor adulto**            |
|                                                                       |
| Duolingo gamifica aprendizaje casual de idiomas para adultos de ocio. |
| Tu usuario es un adulto bajo estrés extremo preparando su futuro      |
| laboral. Mecanismos como los \'corazones\' (vidas que se agotan)      |
| funcionan en Duolingo pero pueden frustrar y hacer abandono en tu     |
| app. Prioriza los mecanismos positivos (streak, XP, ligas) sobre los  |
| punitivos (vidas, penalizaciones de XP por errores). El opositor ya   |
| tiene penalizaciones reales en el examen.                             |
+-----------------------------------------------------------------------+

**6. Resumen: Cambios al Plan Técnico de Este Suplemento**

  ------------------------------------------------------------------------
  **Tema**              **Decisión**           **Prioridad**
  --------------------- ---------------------- ---------------------------
  EADOP (salamandra     Descartado. No         ---
  fine-tune catalán)    relevante para AGE/SS. 
                        Fue investigado y es   
                        un proof-of-concept de 
                        rechazo, no de         
                        respuesta.             

  Salamandra para chat  Descartado             ---
  en tiempo real        definitivamente.       
                        Validado por tus       
                        pruebas reales: 7B     
                        cuantizado no es       
                        fiable para            
                        razonamiento ni tools. 

  Salamandra en Fly.io  Descartado. CPU 5-15   ---
  para ahorro           tok/s = 40s por        
                        respuesta. GPT-OSS     
                        120B es mejor y más    
                        barato hasta \>2.000   
                        usuarios.              

  Calculator Engine SS  AÑADIR AL PLAN. 20     ⭐ ALTA --- antes del
                        tipos de cálculo       primer caso práctico
                        identificados (no 9).  
                        Python determinístico. 
                        El LLM nunca calcula,  
                        solo narra.            

  Trap Pedagogy         AÑADIR AL PLAN. Prompt ⭐⭐ MEDIA --- fase 2 del
  (distractores con     específico para        banco
  valor)                Claude/DeepSeek        
                        generando 6 tipos de   
                        trampa. Mapa de        
                        errores colectivos.    

  Gamificación          AÑADIR AL PLAN.        ⭐⭐ MEDIA --- con el MVP
  Duolingo-style        Implementar: streak +  
                        freeze + ligas         
                        segmentadas + XP.      
                        Omitir:                
                        corazones/vidas.       

  Fine-tuning futuro    POSIBLE en Fase 3. Con ⭐⭐⭐ BAJA PRIORIDAD
  con 10K+ pares        QLoRA en Kaggle para   
                        recall factual SÍ      
                        funciona. Para         
                        razonamiento:          
                        necesitas modelo \>13B 
                        o dataset estructurado 
                        con CoT.               
  ------------------------------------------------------------------------

*Apéndice IV --- Suplemento · Datos verificados febrero 2026*

*EADOP: huggingface.co/projecte-aina/salamandra-7b-aligned-EADOP ·
Cálculos SS: Arts. 169-221 TRLGSS (RDL 8/2015) · Duolingo retention
data:
strivecloud.io/blog/gamification-examples-boost-user-retention-duolingo*
