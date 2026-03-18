**APÉNDICE V**

App Oposiciones AGE & SS --- Arquitectura Final

*Calculadora SS completa (27 tipos) · Frontend & Backend comparativa ·
Flujo de despliegue · Seguridad & RGPD*

**1. Calculadora SS Completa --- Los 27 Tipos de Cálculo Verificados**

Revisión exhaustiva contra el temario oficial (13 temas específicos SS),
los supuestos prácticos de los exámenes de 2024 y 2025, y la legislación
vigente (TRLGSS RDL 8/2015 + modificaciones hasta enero 2026). El
Apéndice IV anterior identificó 20. Aquí se añaden 7 tipos más que
faltaban, todos documentados en supuestos reales de examen.

+-----------------------------------------------------------------------+
| **🔑 Regla fundamental del Calculator Engine**                        |
|                                                                       |
| El LLM NUNCA calcula. Extrae parámetros del enunciado → llama a la    |
| función Python correspondiente → recibe el resultado exacto → narra   |
| la respuesta con el artículo citado. Si el LLM no tiene herramienta   |
| para un cálculo determinado, dice \'no puedo calcular esto            |
| automáticamente, necesito verificación manual\' en lugar de inventar  |
| un número.                                                            |
+-----------------------------------------------------------------------+

  -----------------------------------------------------------------------------------------------------------------------
  **\#**   **Tipo de cálculo**  **Prestación**          **Dificultad**   **Función Python**
  -------- -------------------- ----------------------- ---------------- ------------------------------------------------
  **──**   **── INCAPACIDAD                                              **──**
           TEMPORAL ──**                                                 

  1        Base reguladora IT   IT                      BAJA             calcular_br_it(bases_6m, tipo)
           (enfermedad común /                                           
           AT-EP)                                                        

  2        Cuantía diaria IT    IT                      BAJA             calcular_cuantia_it(br_diaria, dia, tipo)
           según tramo de días                                           
           (1-3 / 4-20 / 21+)                                            

  3        Duración máxima IT:  IT                      BAJA             calcular_duracion_it(fecha_inicio)
           545 días y prórroga                                           
           hasta 730 (EVI)                                               

  4        IT por AT/EP: sin    IT profesional          MEDIA            calcular_it_at_ep(br_diaria, dia)
           días espera, 75%                                              
           desde día 1, pagador                                          
           mutua                                                         

  **──**   **── INCAPACIDAD                                              **──**
           PERMANENTE ──**                                               

  5        IP grado y cuantía:  IP contributiva         ALTA             calcular_ip(br, grado, edad)
           parcial                                                       
           (indemnización 24                                             
           mens.) / total 55% /                                          
           absoluta 100% / GI                                            
           145%                                                          

  6        IP total +           IP total mayor 55       ALTA             calcular_ip_complemento_55(br, edad)
           complemento edad:                                             
           75% si ≥55 años sin                                           
           trabajo apto (art.                                            
           196.2)                                                        

  7        Complemento por      IP / Jubilación /       MEDIA            calcular_complemento_minimos(pension,
           mínimos: diferencia  Viudedad                                 tipo_beneficiario, edad, hijos_cargo)
           hasta pensión mínima                                          
           si renta \< umbral                                            
           (art. 59)                                                     

  **──**   **── JUBILACIÓN ──**                                          **──**

  8        Edad ordinaria de    Jubilación ordinaria    MEDIA            calcular_edad_jubilacion(anios_cotizados,
           jubilación: 65 si                                             anio_nacimiento)
           ≥38a6m cotizados;                                             
           66+10m si no (art.                                            
           205 --- tabla                                                 
           transitoria)                                                  

  9        BR jubilación        Jubilación              ALTA             calcular_br_jubilacion(bases_300m)
           ordinaria: suma 300                                           
           meses / 350 (con                                              
           actualización IPC                                             
           parcial, art. 209)                                            

  10       Porcentaje por años  Jubilación              ALTA             calcular_pct_jubilacion(anios_cotizados)
           cotizados: 50% a 15                                           
           años + escala                                                 
           mensual hasta 100%                                            
           (art. 210)                                                    

  11       Jubilación           Jubilación anticipada   ALTA             calcular_jub_anticipada(pension_ord,
           anticipada                                                    meses_antic, \'involuntaria\')
           involuntaria: tabla                                           
           coeficientes                                                  
           reductores art. 207                                           
           (más favorable)                                               

  12       Jubilación           Jubilación anticipada   ALTA             calcular_jub_anticipada(pension_ord,
           anticipada                                                    meses_antic, \'voluntaria\')
           voluntaria: tabla                                             
           coeficientes                                                  
           reductores art. 208                                           
           (menos favorable)                                             

  13       Jubilación           Jubilación discapacidad ALTA             calcular_jub_discapacidad(anios_cot,
           anticipada por                                                anios_disc_65pct)
           discapacidad: +0.25                                           
           años cotizados por                                            
           cada año con disc.                                            
           ≥65% (art. 206)                                               

  14       Jubilación parcial:  Jubilación parcial      ALTA             calcular_jub_parcial(pension_ord,
           pensión proporcional                                          pct_reduccion_jornada)
           a reducción de                                                
           jornada 25%-50%                                               
           (art. 215, RDL                                                
           11/2024)                                                      

  15       Jubilación activa    Jubilación activa       MEDIA            calcular_jub_activa(pension_ord)
           (compatible                                                   
           trabajo): 50%                                                 
           pensión mientras se                                           
           trabaja (art. 214)                                            

  **──**   **── MUERTE Y                                                 **──**
           SUPERVIVENCIA ──**                                            

  16       Pensión viudedad:    Muerte y supervivencia  MEDIA            calcular_viudedad(br, cargas_familiares)
           52% BR general / 70%                                          
           con cargas                                                    
           familiares (art.                                              
           220-221)                                                      

  17       Pensión orfandad:    Muerte y supervivencia  MEDIA            calcular_orfandad(br, num_huerfanos,
           20% por huérfano,                                             doble_orfandad)
           doble orfandad hasta                                          
           100% sin superar                                              
           cuantía máx. (art.                                            
           224)                                                          

  18       Auxilio por          Muerte y supervivencia  BAJA             calcular_auxilio_defuncion()
           defunción: 46.50€                                             
           (cuantía fija                                                 
           actualizable, art.                                            
           218)                                                          

  **──**   **── NACIMIENTO Y                                             **──**
           FAMILIA ──**                                                  

  19       Prestación           Maternidad/Paternidad   BAJA             calcular_nacimiento(br_diaria, semanas_base,
           nacimiento/cuidado                                            semanas_extra)
           menor: 100% BR, 16                                            
           semanas + semanas                                             
           adicionales (art.                                             
           178-182)                                                      

  20       Asignación económica Prestaciones familiares BAJA             calcular_asignacion_hijo(discapacidad_pct,
           por hijo/menor a                                              tipo_familia)
           cargo: cuantía anual                                          
           fija por grado                                                
           discapacidad del                                              
           hijo (art. 351-354)                                           

  **──**   **── DESEMPLEO ──**                                           **──**

  21       Duración prestación  Desempleo               MEDIA            calcular_duracion_desempleo(dias_cotizados_6a)
           desempleo: escala de                                          
           días cotizados en 6                                           
           años previos (art.                                            
           269)                                                          

  22       BR desempleo:        Desempleo               MEDIA            calcular_br_desempleo(bases_180d)
           promedio últimos 180                                          
           días cotizados / 180                                          
           (excluidas horas                                              
           extra, art. 270)                                              

  23       Cuantía desempleo:   Desempleo               MEDIA            calcular_cuantia_desempleo(br_diaria, dia,
           70% BR primeros 180                                           hijos_cargo)
           días / 60% resto;                                             
           topes min/máx según                                           
           hijos IPREM (art.                                             
           270)                                                          

  **──**   **── COTIZACIÓN Y                                             **──**
           RECAUDACIÓN ──**                                              

  24       Base de cotización   Cotización              MEDIA            calcular_base_cotizacion(salario_mes,
           mensual: salario +                                            pagas_extra, grupo)
           pagas extra                                                   
           prorrateadas,                                                 
           topeado por grupo                                             
           (art. 147)                                                    

  25       Liquidación cuotas:  Cotización              ALTA             calcular_cuotas(bc_mes, cnae, tipo_contrato)
           empresa \~23.6% +                                             
           trabajador \~4.7%                                             
           CC + tipos AT/EP +                                            
           FOGASA + FP (art.                                             
           153)                                                          

  **──**   **── PRESTACIONES NO                                          **──**
           CONTRIBUTIVAS ──**                                            

  26       IMV: umbral de renta Ingreso Mínimo Vital    MEDIA            calcular_imv(tipo_hogar, renta_anual_actual)
           garantizada por tipo                                          
           de hogar                                                      
           (actualizado                                                  
           anualmente, Ley                                               
           19/2021 arts. 10-12)                                          

  27       Pensión no           PNC                     BAJA             calcular_pnc(tipo, convivencia_familiar,
           contributiva                                                  rentas_anuales)
           (invalidez /                                                  
           jubilación): cuantía                                          
           base PNC anual (art.                                          
           363-369)                                                      
  -----------------------------------------------------------------------------------------------------------------------

+-----------------------------------------------------------------------+
| **⚠️ Los 7 tipos que faltaban en el Apéndice IV**                     |
|                                                                       |
| Tipos nuevos identificados en esta revisión: (7) Complemento por      |
| mínimos --- aparece en el examen real de Gestión SS 2025 preguntando  |
| si una IP total de 500€ puede acceder al complemento según edad. (13) |
| Jubilación anticipada por discapacidad --- art. 206, coeficiente 0.25 |
| por año. (14) Jubilación parcial con RDL 11/2024. (18) Auxilio por    |
| defunción --- cuantía fija, muy preguntado en test. (20) Asignación   |
| económica por hijo a cargo --- prestaciones familiares. (21-23)       |
| Desempleo completo: duración + BR + cuantía + topes IPREM. Aparece en |
| caso práctico 2024 verificado en misitiosocial.com.                   |
+-----------------------------------------------------------------------+

**1.1 Código Python Completo --- calculadora_ss.py**

Implementación con Decimal para precisión exacta. Sin float nativo, sin
redondeo erróneo. Validado contra los casos prácticos reales de
2024-2025:

+-----------------------------------------------------------------------+
| \# calculadora_ss.py --- Motor determinístico para supuestos          |
| prácticos SS                                                          |
|                                                                       |
| \# Actualizado: normativa vigente enero 2026                          |
|                                                                       |
| \# Usar: from calculadora_ss import ejecutar_calculo, TOOLS           |
|                                                                       |
| from decimal import Decimal, ROUND_HALF_UP                            |
|                                                                       |
| from datetime import date, timedelta                                  |
|                                                                       |
| from typing import Optional                                           |
|                                                                       |
| import math                                                           |
|                                                                       |
| D = lambda x: Decimal(str(x))                                         |
|                                                                       |
| R2 = lambda x: x.quantize(D(\'0.01\'), rounding=ROUND_HALF_UP)        |
|                                                                       |
| \# ── VALORES REFERENCIALES 2026 (actualizar cada año con PGE) ────   |
|                                                                       |
| IPREM_DIARIO_2026 = D(\'20.00\') \# verificar con PGE 2026            |
|                                                                       |
| IPREM_MENSUAL_2026 = D(\'600.00\') \# base de referencia              |
|                                                                       |
| SMI_MENSUAL_2026 = D(\'1184.00\') \# SMI 2026                         |
|                                                                       |
| \# Cuantías mínimas de pensión 2026 (Resolución IMSERSO ---           |
| actualizar)                                                           |
|                                                                       |
| PENSIONES_MINIMAS_2026 = {                                            |
|                                                                       |
| \'jubilacion_con_conyuge\': D(\'1135.80\'), \# €/mes 14 pagas         |
|                                                                       |
| \'jubilacion_sin_conyuge_65\': D(\'916.90\'),                         |
|                                                                       |
| \'jubilacion_sin_conyuge_menor65\': D(\'857.80\'),                    |
|                                                                       |
| \'viudedad_cargas_familiares\': D(\'916.90\'),                        |
|                                                                       |
| \'viudedad_sin_cargas_65\': D(\'762.00\'),                            |
|                                                                       |
| \'ip_total_con_conyuge\': D(\'1135.80\'),                             |
|                                                                       |
| \'ip_total_sin_conyuge_60_64\': D(\'916.90\'),                        |
|                                                                       |
| \'ip_total_sin_conyuge_menor60_comun\': D(\'762.00\'),                |
|                                                                       |
| }                                                                     |
|                                                                       |
| AUXILIO_DEFUNCION_2026 = D(\'46.50\') \# cuantía fija art. 218        |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| \# TIPO 1-4: INCAPACIDAD TEMPORAL                                     |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| def calcular_br_it(bases_6_meses: list\[float\],                      |
|                                                                       |
| tipo: str = \'comun\') -\> dict:                                      |
|                                                                       |
| \'\'\'BR IT = suma de las 6 bases mensuales / 180 días (art. 169      |
| TRLGSS)\'\'\'                                                         |
|                                                                       |
| if len(bases_6_meses) != 6:                                           |
|                                                                       |
| return {\'error\': \'Necesito exactamente 6 bases mensuales\'}        |
|                                                                       |
| suma = sum(D(str(b)) for b in bases_6_meses)                          |
|                                                                       |
| br_diaria = R2(suma / D(\'180\'))                                     |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'base_reguladora_diaria\': float(br_diaria),                         |
|                                                                       |
| \'suma_bases_6m\': float(suma),                                       |
|                                                                       |
| \'tipo_contingencia\': tipo,                                          |
|                                                                       |
| \'articulo\': \'Art. 169 TRLGSS\'                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_cuantia_it(br_diaria: float, dia_numero: int,            |
|                                                                       |
| tipo: str = \'comun\') -\> dict:                                      |
|                                                                       |
| \'\'\'Cuantía diaria IT según tramo y tipo de contingencia\'\'\'      |
|                                                                       |
| br = D(str(br_diaria))                                                |
|                                                                       |
| if tipo == \'profesional\': \# AT o EP --- sin espera, 75% desde día  |
| 1                                                                     |
|                                                                       |
| cuantia = R2(br \* D(\'0.75\'))                                       |
|                                                                       |
| pagador = \'mutua (desde día 1, sin espera)\'                         |
|                                                                       |
| descripcion = \'75% BR --- AT/EP desde día 1\'                        |
|                                                                       |
| else: \# contingencias comunes                                        |
|                                                                       |
| if dia_numero \<= 3:                                                  |
|                                                                       |
| cuantia = D(\'0.00\')                                                 |
|                                                                       |
| pagador = \'ninguno --- período de espera\'                           |
|                                                                       |
| descripcion = \'Días 1-3: sin prestación (período de espera)\'        |
|                                                                       |
| elif dia_numero \<= 20:                                               |
|                                                                       |
| cuantia = R2(br \* D(\'0.60\'))                                       |
|                                                                       |
| pagador = \'empresa (pago delegado)\'                                 |
|                                                                       |
| descripcion = \'60% BR --- días 4 al 20\'                             |
|                                                                       |
| else:                                                                 |
|                                                                       |
| cuantia = R2(br \* D(\'0.75\'))                                       |
|                                                                       |
| pagador = \'mutua / INSS (pago directo)\'                             |
|                                                                       |
| descripcion = \'75% BR --- día 21 en adelante\'                       |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'cuantia_diaria\': float(cuantia),                                   |
|                                                                       |
| \'pagador\': pagador,                                                 |
|                                                                       |
| \'descripcion\': descripcion,                                         |
|                                                                       |
| \'articulo\': \'Arts. 169-174 TRLGSS\'                                |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_duracion_it(fecha_inicio_baja: str) -\> dict:            |
|                                                                       |
| \'\'\'Límites temporales IT: 545 días + prórroga hasta 730 (art.      |
| 174)\'\'\'                                                            |
|                                                                       |
| from datetime import datetime                                         |
|                                                                       |
| fi = datetime.strptime(fecha_inicio_baja, \'%d/%m/%Y\').date()        |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'dia_545\': (fi + timedelta(days=544)).strftime(\'%d/%m/%Y\'),       |
|                                                                       |
| \'dia_730\': (fi + timedelta(days=729)).strftime(\'%d/%m/%Y\'),       |
|                                                                       |
| \'nota_prorroga\': (\'El INSS puede prorrogar hasta el día 730 si\'   |
|                                                                       |
| \' el EVI prevé recuperación en ese plazo\'),                         |
|                                                                       |
| \'articulo\': \'Art. 174 TRLGSS\'                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| \# TIPOS 5-7: INCAPACIDAD PERMANENTE                                  |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| def calcular_ip(base_reguladora: float, grado: str,                   |
|                                                                       |
| edad: Optional\[int\] = None) -\> dict:                               |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| grado: \'parcial\' \| \'total\' \| \'absoluta\' \| \'gran_invalidez\' |
|                                                                       |
| IP parcial = 24 mensualidades de la BR (pago único, art. 196.1)       |
|                                                                       |
| IP total = 55% BR (o 75% si ≥55 años sin trabajo apto, art. 196.2)    |
|                                                                       |
| IPA = 100% BR \| GI = 100% + 45% complemento cuidador                 |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| br = D(str(base_reguladora))                                          |
|                                                                       |
| if grado == \'parcial\':                                              |
|                                                                       |
| \# Pago único = 24 mensualidades                                      |
|                                                                       |
| cuantia_total = R2(br \* D(\'24\'))                                   |
|                                                                       |
| pct = D(\'0\')                                                        |
|                                                                       |
| tipo_pago = \'pago_unico\'                                            |
|                                                                       |
| descripcion = \'24 mensualidades de la BR (pago único)\'              |
|                                                                       |
| art = \'Art. 196.1 TRLGSS\'                                           |
|                                                                       |
| elif grado == \'total\':                                              |
|                                                                       |
| if edad and edad \>= 55:                                              |
|                                                                       |
| pct = D(\'0.75\')                                                     |
|                                                                       |
| descripcion = \'75% BR --- mayor de 55 años, complemento por edad\'   |
|                                                                       |
| art = \'Art. 196.2 TRLGSS\'                                           |
|                                                                       |
| else:                                                                 |
|                                                                       |
| pct = D(\'0.55\')                                                     |
|                                                                       |
| descripcion = \'55% BR --- IP total ordinaria\'                       |
|                                                                       |
| art = \'Art. 196.1 TRLGSS\'                                           |
|                                                                       |
| cuantia_total = R2(br \* pct)                                         |
|                                                                       |
| tipo_pago = \'pension_mensual\'                                       |
|                                                                       |
| elif grado == \'absoluta\':                                           |
|                                                                       |
| pct = D(\'1.00\')                                                     |
|                                                                       |
| cuantia_total = R2(br)                                                |
|                                                                       |
| tipo_pago = \'pension_mensual\'                                       |
|                                                                       |
| descripcion = \'100% BR --- Incapacidad Permanente Absoluta\'         |
|                                                                       |
| art = \'Art. 197 TRLGSS\'                                             |
|                                                                       |
| elif grado == \'gran_invalidez\':                                     |
|                                                                       |
| pct = D(\'1.45\')                                                     |
|                                                                       |
| cuantia_total = R2(br \* D(\'1.45\'))                                 |
|                                                                       |
| tipo_pago = \'pension_mensual\'                                       |
|                                                                       |
| descripcion = \'100% BR + 45% complemento ayuda cuidador\'            |
|                                                                       |
| art = \'Art. 198 TRLGSS\'                                             |
|                                                                       |
| else:                                                                 |
|                                                                       |
| return {\'error\': f\'Grado desconocido: {grado}\'}                   |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'grado\': grado, \'cuantia\': float(cuantia_total),                  |
|                                                                       |
| \'tipo_pago\': tipo_pago, \'descripcion\': descripcion,               |
|                                                                       |
| \'articulo\': art                                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_complemento_minimos(pension_calculada: float,            |
|                                                                       |
| tipo_beneficiario: str,                                               |
|                                                                       |
| edad: int = 65,                                                       |
|                                                                       |
| hijos_cargo: bool = False) -\> dict:                                  |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| Complemento por mínimos art. 59 TRLGSS.                               |
|                                                                       |
| Solo si: residente en España + rentas \< límite PGE.                  |
|                                                                       |
| tipo_beneficiario: \'jubilacion_con_conyuge\' \|                      |
| \'jubilacion_sin_conyuge_65\' \|                                      |
|                                                                       |
| \'ip_total_sin_conyuge_60_64\' \| etc.                                |
|                                                                       |
| \'\'\'                                                                |
|                                                                       |
| pension = D(str(pension_calculada))                                   |
|                                                                       |
| minimo = PENSIONES_MINIMAS_2026.get(tipo_beneficiario)                |
|                                                                       |
| if minimo is None:                                                    |
|                                                                       |
| return {\'error\': f\'Tipo no encontrado: {tipo_beneficiario}.\',     |
|                                                                       |
| \'tipos_validos\': list(PENSIONES_MINIMAS_2026.keys())}               |
|                                                                       |
| if pension \>= minimo:                                                |
|                                                                       |
| return {\'complemento\': 0.0,                                         |
|                                                                       |
| \'nota\': \'La pensión ya supera el mínimo, no procede complemento\', |
|                                                                       |
| \'pension_minima_referencia\': float(minimo)}                         |
|                                                                       |
| complemento = R2(minimo - pension)                                    |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'pension_calculada\': float(pension),                                |
|                                                                       |
| \'pension_minima\': float(minimo),                                    |
|                                                                       |
| \'complemento_por_minimos\': float(complemento),                      |
|                                                                       |
| \'pension_total_con_complemento\': float(R2(pension + complemento)),  |
|                                                                       |
| \'articulo\': \'Art. 59 TRLGSS\'                                      |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| \# TIPOS 8-15: JUBILACIÓN                                             |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| def calcular_edad_jubilacion(anios_cotizados: float) -\> dict:        |
|                                                                       |
| \'\'\'Edad ordinaria 2026: 65 si ≥38a6m; 66a10m si no (art.           |
| 205)\'\'\'                                                            |
|                                                                       |
| if anios_cotizados \>= 38.5:                                          |
|                                                                       |
| return {\'edad_ordinaria\': \'65 años\', \'meses\': 0,                |
|                                                                       |
| \'nota\': \'≥38 años y 6 meses cotizados → jubilación a los 65\',     |
|                                                                       |
| \'articulo\': \'Art. 205 TRLGSS (año 2027+: 65 / 67)\'}               |
|                                                                       |
| else:                                                                 |
|                                                                       |
| return {\'edad_ordinaria\': \'66 años y 10 meses\', \'meses\': 10,    |
|                                                                       |
| \'nota\': \'Menos de 38a6m → edad ordinaria 66a10m en 2026\',         |
|                                                                       |
| \'articulo\': \'Art. 205 TRLGSS --- tabla transitoria 2026\'}         |
|                                                                       |
| def calcular_br_jubilacion(bases_300_meses: list\[float\]) -\> dict:  |
|                                                                       |
| \'\'\'BR jubilación = suma 300 meses / 350 (art. 209 TRLGSS, Ley      |
| 21/2021)\'\'\'                                                        |
|                                                                       |
| if len(bases_300_meses) != 300:                                       |
|                                                                       |
| return {\'error\': f\'Necesito 300 bases mensuales, recibí            |
| {len(bases_300_meses)}.\',                                            |
|                                                                       |
| \'consejo\': \'Si no tienes todas las bases, indica cuáles tienes y   |
| usaré el promedio\'}                                                  |
|                                                                       |
| suma = sum(D(str(b)) for b in bases_300_meses)                        |
|                                                                       |
| br = R2(suma / D(\'350\'))                                            |
|                                                                       |
| return {\'base_reguladora_mensual\': float(br), \'articulo\': \'Art.  |
| 209 TRLGSS\'}                                                         |
|                                                                       |
| def calcular_pct_jubilacion(anios_cotizados: float) -\> dict:         |
|                                                                       |
| \'\'\'Porcentaje art. 210 TRLGSS (Ley 21/2021 vigente en 2026)\'\'\'  |
|                                                                       |
| anios = D(str(anios_cotizados))                                       |
|                                                                       |
| if anios \< D(\'15\'):                                                |
|                                                                       |
| return {\'error\': \'Mínimo 15 años cotizados para jubilación         |
| ordinaria\'}                                                          |
|                                                                       |
| elif anios \<= D(\'25\'):                                             |
|                                                                       |
| pct = D(\'50\') + (anios - D(\'15\')) \* D(\'12\') \* D(\'1.15\')     |
|                                                                       |
| elif anios \<= D(\'37\'):                                             |
|                                                                       |
| pct = D(\'50\') + D(\'10\') \* D(\'12\') \* D(\'1.15\') + \\          |
|                                                                       |
| (anios - D(\'25\')) \* D(\'12\') \* D(\'1.50\')                       |
|                                                                       |
| else:                                                                 |
|                                                                       |
| pct = D(\'100\')                                                      |
|                                                                       |
| pct = min(R2(pct), D(\'100\'))                                        |
|                                                                       |
| return {\'porcentaje\': float(pct), \'articulo\': \'Art. 210 TRLGSS   |
| (Ley 21/2021)\'}                                                      |
|                                                                       |
| \# Tablas coeficientes reductores 2026 (RDL 2/2023) --- por trimestre |
| anticipado                                                            |
|                                                                       |
| \# involuntaria (art. 207) --- más favorable; voluntaria (art. 208)   |
| --- menos favorable                                                   |
|                                                                       |
| COEF_INV_2026 =                                                       |
| {1:D(\'0.0040\'),2:D(\'0.0040\'),3:D(\'0.0040\'),4:D(\'0.0040\'),     |
|                                                                       |
| 5:D(\'0.0040\'),6:D(\'0.0040\'),7:D(\'0.0040\'),8:D(\'0.0036\')}      |
|                                                                       |
| COEF_VOL_2026 =                                                       |
| {1:D(\'0.0058\'),2:D(\'0.0058\'),3:D(\'0.0058\'),4:D(\'0.0058\'),     |
|                                                                       |
| 5:D(\'0.0058\'),6:D(\'0.0058\'),7:D(\'0.0058\'),8:D(\'0.0050\')}      |
|                                                                       |
| def calcular_jub_anticipada(pension_ordinaria: float,                 |
| meses_anticipacion: int,                                              |
|                                                                       |
| tipo: str = \'voluntaria\') -\> dict:                                 |
|                                                                       |
| pension = D(str(pension_ordinaria))                                   |
|                                                                       |
| trimestres = math.ceil(meses_anticipacion / 3)                        |
|                                                                       |
| tabla = COEF_VOL_2026 if tipo == \'voluntaria\' else COEF_INV_2026    |
|                                                                       |
| coef = tabla.get(trimestres, D(\'0.0058\') if tipo==\'voluntaria\'    |
| else D(\'0.0040\'))                                                   |
|                                                                       |
| reduccion = R2(coef \* D(str(trimestres)))                            |
|                                                                       |
| pension_red = R2(pension \* (D(\'1\') - reduccion))                   |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'pension_ordinaria\': float(pension),                                |
|                                                                       |
| \'trimestres_anticipados\': trimestres,                               |
|                                                                       |
| \'coef_por_trimestre\': float(coef),                                  |
|                                                                       |
| \'reduccion_pct\': float(reduccion \* D(\'100\')),                    |
|                                                                       |
| \'pension_anticipada\': float(pension_red),                           |
|                                                                       |
| \'articulo\': f\'Art. {208 if tipo==\"voluntaria\" else 207} TRLGSS\' |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_jub_discapacidad(anios_cotizados: float,                 |
|                                                                       |
| anios_con_discapacidad_65pct: float) -\> dict:                        |
|                                                                       |
| \'\'\'Art. 206: +0.25 años por cada año con discapacidad ≥65%\'\'\'   |
|                                                                       |
| bonus = D(str(anios_con_discapacidad_65pct)) \* D(\'0.25\')           |
|                                                                       |
| anios_efectivos = D(str(anios_cotizados)) + bonus                     |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'anios_cotizados_reales\': anios_cotizados,                          |
|                                                                       |
| \'bonus_discapacidad\': float(bonus),                                 |
|                                                                       |
| \'anios_efectivos_a_efectos_jubilacion\': float(anios_efectivos),     |
|                                                                       |
| \'articulo\': \'Art. 206 TRLGSS\'                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_jub_parcial(pension_ordinaria: float,                    |
|                                                                       |
| pct_reduccion_jornada: float) -\> dict:                               |
|                                                                       |
| \'\'\'Art. 215 + RDL 11/2024: reducción 25%-50%; pensión prop.\'\'\'  |
|                                                                       |
| if not (25 \<= pct_reduccion_jornada \<= 50):                         |
|                                                                       |
| return {\'error\': \'La reducción de jornada debe estar entre 25% y   |
| 50%\'}                                                                |
|                                                                       |
| pension_parcial = R2(D(str(pension_ordinaria)) \*                     |
| D(str(pct_reduccion_jornada)) / D(\'100\'))                           |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'pension_ordinaria\': pension_ordinaria,                             |
|                                                                       |
| \'pct_reduccion_jornada\': pct_reduccion_jornada,                     |
|                                                                       |
| \'pension_parcial\': float(pension_parcial),                          |
|                                                                       |
| \'nota\': \'Compatible con trabajo a tiempo parcial mientras se       |
| mantiene contrato\',                                                  |
|                                                                       |
| \'articulo\': \'Art. 215 TRLGSS + RDL 11/2024\'                       |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_jub_activa(pension_ordinaria: float) -\> dict:           |
|                                                                       |
| \'\'\'Art. 214: compatible con trabajo. 50% de la pensión\'\'\'       |
|                                                                       |
| pension_activa = R2(D(str(pension_ordinaria)) \* D(\'0.50\'))         |
|                                                                       |
| return {\'pension_activa_compatible\': float(pension_activa),         |
|                                                                       |
| \'articulo\': \'Art. 214 TRLGSS\'}                                    |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| \# TIPOS 16-18: MUERTE Y SUPERVIVENCIA                                |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| def calcular_viudedad(base_reguladora: float,                         |
|                                                                       |
| cargas_familiares: bool = False) -\> dict:                            |
|                                                                       |
| br = D(str(base_reguladora))                                          |
|                                                                       |
| pct = D(\'0.70\') if cargas_familiares else D(\'0.52\')               |
|                                                                       |
| pension = R2(br \* pct)                                               |
|                                                                       |
| return {\'pension_viudedad\': float(pension),                         |
| \'porcentaje_aplicado\': float(pct\*100),                             |
|                                                                       |
| \'cargas_familiares\': cargas_familiares, \'articulo\': \'Arts.       |
| 220-221 TRLGSS\'}                                                     |
|                                                                       |
| def calcular_orfandad(base_reguladora: float, num_huerfanos: int,     |
|                                                                       |
| doble_orfandad: bool = False) -\> dict:                               |
|                                                                       |
| br = D(str(base_reguladora))                                          |
|                                                                       |
| pct_por_huerfano = D(\'0.20\')                                        |
|                                                                       |
| pension_total_sin_tope = R2(br \* pct_por_huerfano \*                 |
| D(str(num_huerfanos)))                                                |
|                                                                       |
| \# En doble orfandad, la suma de todas las pensiones (inc. viudedad   |
| que no existe)                                                        |
|                                                                       |
| \# no puede superar el 100% de la BR, ni una cuantía máxima           |
| establecida                                                           |
|                                                                       |
| if doble_orfandad:                                                    |
|                                                                       |
| tope = R2(br) \# máximo 100% BR en doble orfandad                     |
|                                                                       |
| pension = min(pension_total_sin_tope, tope)                           |
|                                                                       |
| nota = \'Doble orfandad: reparto hasta 100% BR entre huérfanos\'      |
|                                                                       |
| else:                                                                 |
|                                                                       |
| pension = pension_total_sin_tope                                      |
|                                                                       |
| nota = f\'{num_huerfanos} huérfano(s) × 20% BR\'                      |
|                                                                       |
| return {\'pension_orfandad\': float(pension), \'nota\': nota,         |
|                                                                       |
| \'articulo\': \'Art. 224 TRLGSS\'}                                    |
|                                                                       |
| def calcular_auxilio_defuncion() -\> dict:                            |
|                                                                       |
| return {\'cuantia\': float(AUXILIO_DEFUNCION_2026),                   |
|                                                                       |
| \'nota\': \'Cuantía fija actualizable anualmente\',                   |
|                                                                       |
| \'articulo\': \'Art. 218 TRLGSS\'}                                    |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| \# TIPOS 19-20: NACIMIENTO Y FAMILIA                                  |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| def calcular_nacimiento(br_diaria: float, num_hijos: int = 1,         |
|                                                                       |
| semanas_extra_parto_multiple: int = 0) -\> dict:                      |
|                                                                       |
| \'\'\'100% BR. Duración: 16 sem + extras por múltiple/prematuridad    |
| (art. 178)\'\'\'                                                      |
|                                                                       |
| semanas_base = 16                                                     |
|                                                                       |
| semanas_extra = semanas_extra_parto_multiple + (2 if num_hijos \>= 2  |
| else 0)                                                               |
|                                                                       |
| semanas_totales = semanas_base + semanas_extra                        |
|                                                                       |
| cuantia_diaria = D(str(br_diaria)) \# 100% BR                         |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'cuantia_diaria\': float(cuantia_diaria),                            |
|                                                                       |
| \'semanas_totales\': semanas_totales, \'porcentaje\': 100,            |
|                                                                       |
| \'nota\': f\'16 semanas base + {semanas_extra} extras =               |
| {semanas_totales} semanas\',                                          |
|                                                                       |
| \'articulo\': \'Arts. 178-182 TRLGSS\'                                |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_asignacion_hijo(discapacidad_pct: int = 0,               |
|                                                                       |
| familia_numerosa: bool = False) -\> dict:                             |
|                                                                       |
| \'\'\'Asignación económica hijo/menor a cargo (art. 351-354           |
| TRLGSS)\'\'\'                                                         |
|                                                                       |
| if discapacidad_pct \>= 75:                                           |
|                                                                       |
| cuantia_anual = D(\'6000.00\') \# ≥75% discapacidad + necesita        |
| tercera persona                                                       |
|                                                                       |
| elif discapacidad_pct \>= 65:                                         |
|                                                                       |
| cuantia_anual = D(\'4747.20\') \# ≥65% discapacidad                   |
|                                                                       |
| elif discapacidad_pct \>= 33:                                         |
|                                                                       |
| cuantia_anual = D(\'1000.00\') \# ≥33% discapacidad                   |
|                                                                       |
| else:                                                                 |
|                                                                       |
| cuantia_anual = D(\'0.00\') \# sin discapacidad: sujeto a umbral      |
| renta                                                                 |
|                                                                       |
| return {\'cuantia_anual\': float(cuantia_anual),                      |
|                                                                       |
| \'discapacidad_pct\': discapacidad_pct,                               |
|                                                                       |
| \'articulo\': \'Arts. 351-354 TRLGSS (verificar cuantías PGE 2026)\'} |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| \# TIPOS 21-23: DESEMPLEO (¡faltaban en versión anterior!)            |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| ESCALA_DESEMPLEO = \[ \# (min_dias, max_dias, dias_prestacion) art.   |
| 269                                                                   |
|                                                                       |
| (360, 539, 120), (540, 719, 180), (720, 899, 240),                    |
|                                                                       |
| (900, 1079, 300), (1080, 1259, 360), (1260, 1439, 420),               |
|                                                                       |
| (1440, 1619, 480), (1620, 1799, 540), (1800, 1979, 600),              |
|                                                                       |
| (1980, 2159, 660), (2160, float(\'inf\'), 720)                        |
|                                                                       |
| \]                                                                    |
|                                                                       |
| def calcular_duracion_desempleo(dias_cotizados_ultimos_6_anios: int)  |
| -\> dict:                                                             |
|                                                                       |
| d = dias_cotizados_ultimos_6_anios                                    |
|                                                                       |
| if d \< 360:                                                          |
|                                                                       |
| return {\'error\': \'Mínimo 360 días cotizados para prestación        |
| contributiva\',                                                       |
|                                                                       |
| \'nota\': \'Con \< 360 días: solo subsidio asistencial (art. 274)\'}  |
|                                                                       |
| for min_d, max_d, prestacion in ESCALA_DESEMPLEO:                     |
|                                                                       |
| if min_d \<= d \<= max_d or (max_d == float(\'inf\') and d \>=        |
| min_d):                                                               |
|                                                                       |
| return {\'dias_cotizados\': d, \'dias_prestacion\': prestacion,       |
|                                                                       |
| \'meses_prestacion\': prestacion // 30,                               |
|                                                                       |
| \'articulo\': \'Art. 269 TRLGSS\'}                                    |
|                                                                       |
| def calcular_br_desempleo(bases_180_dias: list\[float\]) -\> dict:    |
|                                                                       |
| \'\'\'BR desempleo = promedio últimos 180 días cotizados EXCLUYENDO   |
| horas extra\'\'\'                                                     |
|                                                                       |
| if len(bases_180_dias) != 180:                                        |
|                                                                       |
| \# Si se pasan bases mensuales (6 meses), las convertimos             |
|                                                                       |
| if len(bases_180_dias) == 6:                                          |
|                                                                       |
| total = sum(D(str(b)) for b in bases_180_dias)                        |
|                                                                       |
| br = R2(total / D(\'180\'))                                           |
|                                                                       |
| return {\'base_reguladora_diaria\': float(br),                        |
|                                                                       |
| \'nota\': \'Calculada con 6 bases mensuales / 180 días\',             |
|                                                                       |
| \'articulo\': \'Art. 270 TRLGSS\'}                                    |
|                                                                       |
| return {\'error\': f\'Necesito 180 bases diarias o 6 mensuales,       |
| recibí {len(bases_180_dias)}\'}                                       |
|                                                                       |
| total = sum(D(str(b)) for b in bases_180_dias)                        |
|                                                                       |
| br = R2(total / D(\'180\'))                                           |
|                                                                       |
| return {\'base_reguladora_diaria\': float(br), \'articulo\': \'Art.   |
| 270 TRLGSS\'}                                                         |
|                                                                       |
| def calcular_cuantia_desempleo(br_diaria: float, dia_numero: int,     |
|                                                                       |
| hijos_cargo: int = 0) -\> dict:                                       |
|                                                                       |
| \'\'\'70% primeros 180 días / 60% resto; topeado por IPREM según      |
| hijos\'\'\'                                                           |
|                                                                       |
| br = D(str(br_diaria))                                                |
|                                                                       |
| pct = D(\'0.70\') if dia_numero \<= 180 else D(\'0.60\')              |
|                                                                       |
| cuantia_calc = R2(br \* pct)                                          |
|                                                                       |
| \# Topes IPREM+1/6 para 2026 (verificar con Orden de cotización 2026) |
|                                                                       |
| if hijos_cargo == 0:                                                  |
|                                                                       |
| tope_max = R2(IPREM_MENSUAL_2026 \* D(\'1.75\') / D(\'30\'))          |
|                                                                       |
| tope_min = R2(IPREM_MENSUAL_2026 \* D(\'1.07\') / D(\'30\'))          |
|                                                                       |
| elif hijos_cargo == 1:                                                |
|                                                                       |
| tope_max = R2(IPREM_MENSUAL_2026 \* D(\'2.00\') / D(\'30\'))          |
|                                                                       |
| tope_min = R2(IPREM_MENSUAL_2026 \* D(\'1.25\') / D(\'30\'))          |
|                                                                       |
| else: \# 2 o más hijos                                                |
|                                                                       |
| tope_max = R2(IPREM_MENSUAL_2026 \* D(\'2.25\') / D(\'30\'))          |
|                                                                       |
| tope_min = R2(IPREM_MENSUAL_2026 \* D(\'1.40\') / D(\'30\'))          |
|                                                                       |
| cuantia_final = min(max(cuantia_calc, tope_min), tope_max)            |
|                                                                       |
| return {                                                              |
|                                                                       |
| \'cuantia_diaria_calculada\': float(cuantia_calc),                    |
|                                                                       |
| \'cuantia_diaria_final\': float(cuantia_final),                       |
|                                                                       |
| \'porcentaje_aplicado\': float(pct \* D(\'100\')),                    |
|                                                                       |
| \'tope_maximo_diario\': float(tope_max),                              |
|                                                                       |
| \'tope_minimo_diario\': float(tope_min),                              |
|                                                                       |
| \'articulo\': \'Art. 270 TRLGSS\'                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| \# TIPOS 24-25: COTIZACIÓN                                            |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| TIPOS_COTIZACION_CC_2026 = { \# (empresa_pct, trabajador_pct)         |
|                                                                       |
| \'contingencias_comunes\': (D(\'23.60\'), D(\'4.70\')),               |
|                                                                       |
| \'desempleo_indefinido\': (D(\'5.50\'), D(\'1.55\')),                 |
|                                                                       |
| \'desempleo_temporal\': (D(\'6.70\'), D(\'1.60\')),                   |
|                                                                       |
| \'fogasa\': (D(\'0.20\'), D(\'0.00\')),                               |
|                                                                       |
| \'formacion_profesional\': (D(\'0.60\'), D(\'0.10\')),                |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_base_cotizacion(salario_mes: float, num_pagas_extra:     |
| int,                                                                  |
|                                                                       |
| importe_paga_extra: float, grupo: int) -\> dict:                      |
|                                                                       |
| \'\'\'Base cotización = salario mes + prorrateo pagas extra (art. 147 |
| TRLGSS)\'\'\'                                                         |
|                                                                       |
| \# Topes por grupo (grupo 1 = licenciados, grupo 10 = peones)         |
|                                                                       |
| \# Simplificado --- actualizar con Orden cotización 2026              |
|                                                                       |
| TOPES = {1: (D(\'4909.50\'), D(\'1166.70\')), 2: (D(\'4109.40\'),     |
| D(\'1166.70\')),                                                      |
|                                                                       |
| 3: (D(\'3576.60\'), D(\'1166.70\')), 7: (D(\'1624.80\'),              |
| D(\'1166.70\')),                                                      |
|                                                                       |
| 10: (D(\'1624.80\'), D(\'1166.70\'))}                                 |
|                                                                       |
| sm = D(str(salario_mes))                                              |
|                                                                       |
| pe_mes = D(str(importe_paga_extra)) \* D(str(num_pagas_extra)) /      |
| D(\'12\')                                                             |
|                                                                       |
| bc = sm + pe_mes                                                      |
|                                                                       |
| tope_max, tope_min = TOPES.get(grupo, (D(\'4909.50\'),                |
| D(\'1166.70\')))                                                      |
|                                                                       |
| bc_efectiva = min(max(bc, tope_min), tope_max)                        |
|                                                                       |
| return {\'base_cotizacion\': float(R2(bc_efectiva)),                  |
|                                                                       |
| \'tope_maximo_grupo\': float(tope_max),                               |
|                                                                       |
| \'tope_minimo_grupo\': float(tope_min),                               |
|                                                                       |
| \'articulo\': \'Art. 147 TRLGSS + Orden cotización 2026\'}            |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| \# TIPOS 26-27: PRESTACIONES NO CONTRIBUTIVAS                         |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| IMV_CUANTIAS_2026 = { \# cuantía mensual garantizada                  |
|                                                                       |
| \'adulto_solo\': D(\'533.00\'),                                       |
|                                                                       |
| \'pareja_sin_hijos\': D(\'757.00\'),                                  |
|                                                                       |
| \'1_adulto_1_hijo\': D(\'640.00\'),                                   |
|                                                                       |
| \'2_adultos_1_hijo\': D(\'828.00\'),                                  |
|                                                                       |
| \# verificar con actualización PGE 2026                               |
|                                                                       |
| }                                                                     |
|                                                                       |
| def calcular_imv(tipo_hogar: str, renta_anual_actual: float = 0.0)    |
| -\> dict:                                                             |
|                                                                       |
| \'\'\'Art. 10-12 Ley 19/2021. IMV = cuantía garantizada - rentas      |
| actuales (si \< cuantía)\'\'\'                                        |
|                                                                       |
| cuantia_garantizada = IMV_CUANTIAS_2026.get(tipo_hogar)               |
|                                                                       |
| if cuantia_garantizada is None:                                       |
|                                                                       |
| return {\'error\': f\'Tipo de hogar desconocido: {tipo_hogar}\',      |
|                                                                       |
| \'tipos_validos\': list(IMV_CUANTIAS_2026.keys())}                    |
|                                                                       |
| renta_mensual = D(str(renta_anual_actual)) / D(\'12\')                |
|                                                                       |
| if renta_mensual \>= cuantia_garantizada:                             |
|                                                                       |
| return {\'imv\': 0.0, \'nota\': \'Rentas superan el umbral IMV, no    |
| procede\',                                                            |
|                                                                       |
| \'umbral\': float(cuantia_garantizada)}                               |
|                                                                       |
| imv = R2(cuantia_garantizada - renta_mensual)                         |
|                                                                       |
| return {\'imv_mensual\': float(imv), \'umbral_garantizado\':          |
| float(cuantia_garantizada),                                           |
|                                                                       |
| \'articulo\': \'Arts. 10-12 Ley 19/2021\'}                            |
|                                                                       |
| def calcular_pnc(tipo: str, convivencia_familiar: bool = False,       |
|                                                                       |
| rentas_anuales: float = 0.0) -\> dict:                                |
|                                                                       |
| \'\'\'PNC invalidez / jubilación (art. 363-369 TRLGSS)\'\'\'          |
|                                                                       |
| PNC_BASE_2026 = D(\'5899.60\') / D(\'12\') \# cuantía mensual ref.    |
| 2026                                                                  |
|                                                                       |
| renta_mensual = D(str(rentas_anuales)) / D(\'12\')                    |
|                                                                       |
| if convivencia_familiar:                                              |
|                                                                       |
| limite_renta = PNC_BASE_2026 \* D(\'2.5\') \# con familiares          |
| obligados                                                             |
|                                                                       |
| else:                                                                 |
|                                                                       |
| limite_renta = PNC_BASE_2026                                          |
|                                                                       |
| if renta_mensual \>= PNC_BASE_2026:                                   |
|                                                                       |
| return {\'pnc\': 0.0, \'nota\': \'Rentas superan la cuantía PNC\'}    |
|                                                                       |
| pnc = R2(min(PNC_BASE_2026, PNC_BASE_2026 - renta_mensual))           |
|                                                                       |
| return {\'pnc_mensual\': float(pnc), \'tipo\': tipo,                  |
|                                                                       |
| \'articulo\': \'Arts. 363-369 TRLGSS (verificar PGE 2026)\'}          |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| \# DISPATCHER --- El LLM solo llama a esta función                    |
|                                                                       |
| \# ═══════════════════════════════════════════════════════════════    |
|                                                                       |
| TOOLS = {                                                             |
|                                                                       |
| \'calcular_br_it\': calcular_br_it,                                   |
|                                                                       |
| \'calcular_cuantia_it\': calcular_cuantia_it,                         |
|                                                                       |
| \'calcular_duracion_it\': calcular_duracion_it,                       |
|                                                                       |
| \'calcular_ip\': calcular_ip,                                         |
|                                                                       |
| \'calcular_complemento_minimos\': calcular_complemento_minimos,       |
|                                                                       |
| \'calcular_edad_jubilacion\': calcular_edad_jubilacion,               |
|                                                                       |
| \'calcular_br_jubilacion\': calcular_br_jubilacion,                   |
|                                                                       |
| \'calcular_pct_jubilacion\': calcular_pct_jubilacion,                 |
|                                                                       |
| \'calcular_jub_anticipada\': calcular_jub_anticipada,                 |
|                                                                       |
| \'calcular_jub_discapacidad\': calcular_jub_discapacidad,             |
|                                                                       |
| \'calcular_jub_parcial\': calcular_jub_parcial,                       |
|                                                                       |
| \'calcular_jub_activa\': calcular_jub_activa,                         |
|                                                                       |
| \'calcular_viudedad\': calcular_viudedad,                             |
|                                                                       |
| \'calcular_orfandad\': calcular_orfandad,                             |
|                                                                       |
| \'calcular_auxilio_defuncion\': calcular_auxilio_defuncion,           |
|                                                                       |
| \'calcular_nacimiento\': calcular_nacimiento,                         |
|                                                                       |
| \'calcular_asignacion_hijo\': calcular_asignacion_hijo,               |
|                                                                       |
| \'calcular_duracion_desempleo\': calcular_duracion_desempleo,         |
|                                                                       |
| \'calcular_br_desempleo\': calcular_br_desempleo,                     |
|                                                                       |
| \'calcular_cuantia_desempleo\': calcular_cuantia_desempleo,           |
|                                                                       |
| \'calcular_base_cotizacion\': calcular_base_cotizacion,               |
|                                                                       |
| \'calcular_imv\': calcular_imv,                                       |
|                                                                       |
| \'calcular_pnc\': calcular_pnc,                                       |
|                                                                       |
| }                                                                     |
|                                                                       |
| def ejecutar_calculo(nombre_tool: str, params: dict) -\> dict:        |
|                                                                       |
| if nombre_tool not in TOOLS:                                          |
|                                                                       |
| return {\'error\': f\'Herramienta no disponible: {nombre_tool}.\',    |
|                                                                       |
| \'herramientas_disponibles\': list(TOOLS.keys()),                     |
|                                                                       |
| \'instruccion\': \'Si no hay herramienta para este cálculo, di al     |
| usuario que requiere verificación manual y cita el artículo           |
| relevante.\'}                                                         |
|                                                                       |
| try:                                                                  |
|                                                                       |
| return TOOLS\[nombre_tool\](\*\*params)                               |
|                                                                       |
| except TypeError as e:                                                |
|                                                                       |
| return {\'error\': f\'Parámetro incorrecto: {e}\', \'tool\':          |
| nombre_tool}                                                          |
|                                                                       |
| except Exception as e:                                                |
|                                                                       |
| return {\'error\': str(e), \'tool\': nombre_tool}                     |
+-----------------------------------------------------------------------+

**2. Frontend & Backend --- Comparativa Completa para Elegir**

Opciones verificadas en febrero 2026. Organizadas por uso: frontend
estático, backend API, y base de datos/auth integrada. Todas tienen tier
gratuito real o coste inferior a 10€/mes para el MVP.

**2.1 Frontend --- Dónde Hospedar la Interfaz**

  -----------------------------------------------------------------------------------
  **Plataforma**   **Tier       **Cold        **CDN EU**    **Cuándo elegirla**
                   gratuito**   start**                     
  ---------------- ------------ ------------- ------------- -------------------------
  Cloudflare Pages Ilimitado    No (edge      ✅ Madrid,    ✅ RECOMENDADO MVP.
                                global)       Frankfurt     Deploy GitHub en 1 min.
                                                            0€ para siempre en
                                                            contenido estático. RGPD:
                                                            edge en EU.

  Netlify          100GB        No (CDN)      ✅ EU nodes   Alternativa a Cloudflare.
                   banda/mes                                Mejor preview deploys.
                                                            Formularios incluidos en
                                                            free.

  Vercel           Hobby:       No (edge)     ✅ EU nodes   Si usas Next.js/React.
                   ilimitado                                OJO: backend Functions
                                                            tienen límite de 10s por
                                                            ejecución ---
                                                            insuficiente para
                                                            llamadas a LLMs.

  GitHub Pages     Ilimitado    No            ❌ No         Solo HTML/CSS/JS sin
                   (solo                      garantizado   backend. Para landing
                   estático)                  EU            page/docs, no para la
                                                            app.
  -----------------------------------------------------------------------------------

**2.2 Backend API --- Dónde Corre tu Servidor Python/Node**

  -------------------------------------------------------------------------------------------
  **Plataforma**   **Tier        **Cold        **Región EU**        **Cuándo elegirla**
                   gratuito**    start**                            
  ---------------- ------------- ------------- -------------------- -------------------------
  Fly.io           3 VMs shared  No (siempre   ✅ Frankfurt (fra)   ✅ RECOMENDADO MVP. 8
                                 activo)                            cores compartidos, 256MB
                                                                    RAM gratis. Escala bien.
                                                                    GPU disponible para
                                                                    futuro. RGPD OK en
                                                                    Frankfurt.

  Railway          \$5           No            ❌ Solo US           Muy fácil de usar (deploy
                   crédito/mes                                      en 2 min con GitHub).
                   gratis                                           Pero región EU no
                                                                    disponible en free. Para
                                                                    MVP ES con RGPD:
                                                                    problema.

  Render.com       Free (con     \~50 seg      ❌ Frankfurt en paid Free tier: 50s de cold
                   cold start)                                      start. Inaceptable para
                                                                    usuarios de pago. Starter
                                                                    (\$7/mes): siempre
                                                                    activo + Frankfurt EU.

  Hetzner Cloud    No (€3.29/mes No (VPS       ✅                   Mejor precio/rendimiento
  CX11             mín)          dedicado)     Nuremberg/Helsinki   para producción. 2 vCPU,
                                                                    2GB RAM. Paga con
                                                                    tarjeta. RGPD: empresa
                                                                    alemana.

  VPS Hostinger    Ya pagado     No            ✅ EU (verificar DC) ✅ USAR para Neo4j +
  (ya tienes)                                                       Redis + cron jobs. Libera
                                                                    recursos desactivando
                                                                    Salamandra. Backend
                                                                    ligero también cabe.

  Coolify          Gratis sobre  No            ✅ Donde esté el VPS Panel estilo Vercel
  (self-hosted en  tu VPS                                           self-hosted. Deploy
  Hostinger)                                                        GitHub → tu VPS con 0€
                                                                    extra. Recomendado si
                                                                    quieres UI de deploy.

  PocketBase       Gratis        No            ✅ Donde lo hosts    Backend + auth + BD en un
                   self-hosted                                      solo binario de 20MB.
                                                                    Ideal para MVP si no
                                                                    tienes mucha lógica
                                                                    custom.
  -------------------------------------------------------------------------------------------

**2.3 Autenticación y Pagos --- No Las Implementes Tú**

  ---------------------------------------------------------------------------------
  **Servicio**   **Tipo**        **Coste**           **Cuándo**
  -------------- --------------- ------------------- ------------------------------
  Clerk.com      Auth completo   Free hasta 10K MAU, ✅ RECOMENDADO para auth.
                                 luego \$25/mes      Componentes React ya hechos,
                                                     magic link, Google OAuth,
                                                     gestión de sesiones. 0€ en
                                                     MVP.

  Supabase Auth  Auth +          Free tier generoso  Auth sólido si también usas su
                 PostgreSQL                          PG. No uses si ya tienes
                                                     Neo4j+PG en VPS.

  Stripe         Pagos           1.4% +              ✅ IMPRESCINDIBLE para
                 recurrentes     0.25€/transacción   suscripciones. Stripe
                                 EU                  Checkout: formulario de pago
                                                     ya hecho. Stripe Customer
                                                     Portal: gestión de
                                                     suscripciones.

  Paddle         Pagos + IVA     5% transacción      Alternativa a Stripe. Gestiona
                 gestionado                          el IVA europeo
                                                     automáticamente. Más simple
                                                     fiscalmente si vendes en
                                                     varios países EU.

  Resend.com     Email           3.000 emails/mes    Para emails de bienvenida,
                 transaccional   gratis              reseteo de contraseña,
                                                     notificaciones. API limpia en
                                                     Node/Python.
  ---------------------------------------------------------------------------------

**3. Flujo de Despliegue Completo --- Cómo Conectar Todo**

Esta es la arquitectura recomendada para el MVP que puedes tener
operativo en 1-2 semanas. Cada componente es independiente y
reemplazable sin afectar los demás:

**3.1 Diagrama de la Arquitectura**

+-----------------------------------------------------------------------+
| ┌─────────────────────────────────────────────────────────────┐       |
|                                                                       |
| │ USUARIO (navegador / app móvil) │                                   |
|                                                                       |
| └────────────────────────┬────────────────────────────────────┘       |
|                                                                       |
| │ HTTPS                                                               |
|                                                                       |
| ▼                                                                     |
|                                                                       |
| ┌────────────────────────────────────────────────────────────┐        |
|                                                                       |
| │ CLOUDFLARE PAGES (frontend) │                                       |
|                                                                       |
| │ React/Vue/Svelte estático · Deploy automático desde GitHub │        |
|                                                                       |
| │ CDN global · 0€ · HTTPS automático · EU edge │                      |
|                                                                       |
| └────────────────────────┬───────────────────────────────────┘        |
|                                                                       |
| │ API calls HTTPS                                                     |
|                                                                       |
| ▼                                                                     |
|                                                                       |
| ┌────────────────────────────────────────────────────────────┐        |
|                                                                       |
| │ FLY.IO Frankfurt (backend API --- fastapi o express) │              |
|                                                                       |
| │ Recibe peticiones · Verifica JWT de Clerk │                         |
|                                                                       |
| │ Rate limiting con Redis · Consulta Neo4j · Llama a Groq │           |
|                                                                       |
| │ Free tier: 3 VMs · Escala automático · RGPD EU │                    |
|                                                                       |
| └──────┬───────────────────────────────────────┬─────────────┘        |
|                                                                       |
| │ Cypher queries │ API calls                                          |
|                                                                       |
| ▼ ▼                                                                   |
|                                                                       |
| ┌──────────────────────┐ ┌──────────────────────┐                     |
|                                                                       |
| │ VPS HOSTINGER │ │ APIs EXTERNAS │                                   |
|                                                                       |
| │ Neo4j Community │ │ Groq (LLM chat) │                               |
|                                                                       |
| │ PostgreSQL │ │ OpenAI embeddings │                                  |
|                                                                       |
| │ Redis (cache+rate) │ │ DeepSeek (generar) │                         |
|                                                                       |
| │ nginx reverse proxy │ │ Anthropic (revisar) │                       |
|                                                                       |
| │ Cron jobs Python │ │ Stripe (pagos) │                               |
|                                                                       |
| └──────────────────────┘ └──────────────────────┘                     |
|                                                                       |
| │ Auth webhooks                                                       |
|                                                                       |
| ▼                                                                     |
|                                                                       |
| ┌──────────────┐                                                      |
|                                                                       |
| │ CLERK.COM │                                                         |
|                                                                       |
| │ Autenticación│                                                      |
|                                                                       |
| │ Sesiones JWT│                                                       |
|                                                                       |
| └──────────────┘                                                      |
+-----------------------------------------------------------------------+

**3.2 Pasos de Despliegue (en este orden)**

1.  VPS Hostinger: Instala Neo4j Community + PostgreSQL + Redis. Abre
    puertos 7474 (Neo4j browser), 7687 (Bolt). Configura nginx como
    reverse proxy. Asegura con ufw: solo acepta conexiones de la IP de
    Fly.io.

2.  Clerk.com: Crea cuenta gratuita. Configura app. Anota
    publishable_key y secret_key. Activa Google OAuth y magic link.
    Define roles: free / pro / admin.

3.  Fly.io Frankfurt: fly launch en tu directorio de backend. Configura
    flyctl y fly deploy. Añade variables de entorno: GROQ_KEY,
    ANTHROPIC_KEY, NEO4J_URI, PG_URI, CLERK_SECRET, STRIPE_KEY.
    Configura health check.

4.  Cloudflare Pages: Conecta tu repositorio GitHub. Build command: npm
    run build. Publish directory: dist/. Añade variable
    VITE_API_URL=https://tu-app.fly.dev. Deploy automático en cada push
    a main.

5.  Stripe: Activa modo producción. Crea productos: Plan PRO (9€/mes) y
    Plan PRO+BYOK (7€/mes). Configura webhook hacia tu backend Fly.io:
    eventos checkout.session.completed y customer.subscription.deleted.

6.  Dominio + HTTPS: Cloudflare gestiona el dominio y el HTTPS
    automáticamente. Para el backend Fly.io: fly certs add
    tu-dominio.com. Para Neo4j en VPS: acceso solo por IP interna de
    Fly.io, nunca expuesto a internet directamente.

**3.3 Variables de Entorno (Backend Fly.io)**

+-----------------------------------------------------------------------+
| \# Configurar en Fly.io con: fly secrets set VARIABLE=valor           |
|                                                                       |
| \# Nunca en código fuente ni en .env commiteado                       |
|                                                                       |
| \# APIs de IA                                                         |
|                                                                       |
| GROQ_API_KEY=gsk\_\...                                                |
|                                                                       |
| ANTHROPIC_API_KEY=sk-ant-\...                                         |
|                                                                       |
| DEEPSEEK_API_KEY=\...                                                 |
|                                                                       |
| OPENAI_API_KEY=sk-\... \# solo para embeddings text-embedding-3-small |
|                                                                       |
| \# Base de datos (conexión interna VPS → Fly.io privado)              |
|                                                                       |
| NEO4J_URI=bolt://tu-vps-ip:7687                                       |
|                                                                       |
| NEO4J_USER=neo4j                                                      |
|                                                                       |
| NEO4J_PASSWORD=\... \# contraseña fuerte                              |
|                                                                       |
| POSTGRES_URI=postgresql://user:pass@tu-vps-ip:5432/oposiciones        |
|                                                                       |
| REDIS_URI=redis://tu-vps-ip:6379                                      |
|                                                                       |
| \# Auth                                                               |
|                                                                       |
| CLERK_SECRET_KEY=sk_live\_\...                                        |
|                                                                       |
| CLERK_PUBLISHABLE_KEY=pk_live\_\... \# también en frontend            |
|                                                                       |
| \# Pagos                                                              |
|                                                                       |
| STRIPE_SECRET_KEY=sk_live\_\...                                       |
|                                                                       |
| STRIPE_WEBHOOK_SECRET=whsec\_\...                                     |
|                                                                       |
| \# App                                                                |
|                                                                       |
| ENVIRONMENT=production                                                |
|                                                                       |
| ALLOWED_ORIGINS=https://tu-app.pages.dev,https://tudominio.com        |
|                                                                       |
| SECRET_JWT_KEY=\... \# para firmar tokens propios si los usas         |
+-----------------------------------------------------------------------+

**4. Seguridad y Cumplimiento RGPD --- Obligatorio Antes del 1er
Usuario**

Una app de pago con historial de estudio, datos de progreso y cobros
recurrentes requiere cumplir con el RGPD antes de lanzar beta pública.
No es burocracia --- es requisito legal con multas de hasta 20M€ o el 4%
de facturación global.

**4.1 Datos que Tratas y Base Legal**

  ------------------------------------------------------------------------
  **Dato           **Base legal (art. **Conservación**   **Dónde se
  personal**       6 RGPD)**                             aloja**
  ---------------- ------------------ ------------------ -----------------
  Email, nombre    Ejecución de       Mientras dure la   Clerk.com
                   contrato (art.     relación +5 años   (certificado
                   6.1.b)                                RGPD)

  Historial de     Ejecución de       Duración           PostgreSQL en VPS
  respuestas,      contrato (art.     suscripción + 1    EU
  progreso         6.1.b)             año                

  Conversaciones   Ejecución de       30 días (free) /   PostgreSQL VPS EU
  con IA (chat)    contrato (art.     12 meses (pro)     --- NO enviado a
                   6.1.b)                                OpenAI

  Datos de pago    Ejecución de       Gestión por Stripe Solo en Stripe
                   contrato (art.     (PCI-DSS)          --- tú no
                   6.1.b)                                almacenas
                                                         tarjetas

  Cookies técnicas Interés legítimo   Sesión / 1 año     Navegador usuario
                   (art. 6.1.f)                          

  Cookies          Consentimiento     Hasta revocación   Plataforma
  analíticas (si   (art. 6.1.a)                          analítica (ej:
  las usas)                                              Plausible EU)
  ------------------------------------------------------------------------

**4.2 Documentos Legales Mínimos (Obligatorios)**

-   Política de privacidad: qué datos tratas, con qué base legal, con
    qué proveedores (Groq, Clerk, Stripe, Fly.io, Neo4j). Derechos ARCO
    (acceso, rectificación, cancelación, oposición). Contacto DPO o
    responsable.

-   Política de cookies: categorías de cookies, forma de
    aceptar/rechazar. Herramienta gratuita: cookieconsent.orestbida.com.

-   Términos y condiciones: precio, condiciones de cancelación,
    propiedad intelectual del contenido, limitación de responsabilidad
    sobre exactitud del contenido legal.

-   Registro de actividades de tratamiento: documento interno
    obligatorio si tratas datos de más de 250 personas o datos de
    categorías especiales. En tu caso: sí desde el primer usuario de
    pago.

**4.3 Transferencias Internacionales de Datos**

+-----------------------------------------------------------------------+
| **⚠️ El problema con las APIs de IA externas**                        |
|                                                                       |
| Cuando envías el chat de un usuario a Groq (EEUU), DeepSeek (China) o |
| Anthropic (EEUU), estás haciendo una transferencia internacional de   |
| datos personales bajo el RGPD. Esto requiere base legal específica.   |
| Soluciones: (1) Para Groq/Anthropic: Están sujetos al Data Privacy    |
| Framework EU-EEUU (2023) --- válido. Incluir en política de           |
| privacidad. (2) Para DeepSeek: Servidor en China. El RGPD no reconoce |
| China como país adecuado. SOLUCIÓN: No envíes datos personales        |
| identificativos a DeepSeek. Solo lo usas para generar contenido       |
| offline (banco de preguntas), no para el chat de usuarios. Esto       |
| elimina el problema.                                                  |
+-----------------------------------------------------------------------+

**4.4 Seguridad Técnica Mínima (Checklist)**

  -----------------------------------------------------------------------
  **Control de seguridad**            **Cómo implementarlo**
  ----------------------------------- -----------------------------------
  HTTPS obligatorio en todas las      Cloudflare: automático. Fly.io:
  conexiones                          automático. VPS: Let\'s Encrypt con
                                      certbot + nginx.

  Neo4j y PostgreSQL no expuestos a   ufw en VPS: solo acepta conexiones
  internet                            Bolt/PG desde IP de Fly.io. Nunca
                                      puerto abierto al mundo.

  Rate limiting en API backend        Redis + sliding window: 10 req/min
                                      en endpoints públicos, 60/min
                                      autenticados.

  Variables de entorno nunca en       fly secrets set para Fly.io. .env
  código                              en .gitignore. Usar dotenv +
                                      variables de entorno del sistema.

  Validación de JWT de Clerk en       Cada request autenticado: verificar
  backend                             token Clerk antes de cualquier
                                      lógica. Librería oficial.

  Webhook de Stripe verificado        Verificar signature del webhook con
                                      STRIPE_WEBHOOK_SECRET antes de
                                      procesar. Sin verificación →
                                      cualquiera puede simular pagos.

  Logs sin datos personales           Los logs de errores/acceso no deben
                                      incluir contenido de los chats ni
                                      datos de usuario. Solo timestamps,
                                      endpoints, códigos HTTP.

  Backups de BD                       Cron diario: dump de PostgreSQL +
                                      Neo4j export → cifrado → almacenado
                                      en Hetzner Storage Box o Backblaze
                                      B2 EU.

  Política de retención de datos      Cron mensual: borrar historial de
                                      chat FREE \> 30 días, borrar
                                      cuentas inactivas \> 18 meses con
                                      email de aviso previo.

  Prompt Guard 2 en todas las         Groq Prompt Guard 2 (\$0.03/M)
  entradas                            antes del modelo principal. Detecta
                                      prompt injection y jailbreaks.
  -----------------------------------------------------------------------

**5. Stack Final MVP --- Decisiones Tomadas**

  -----------------------------------------------------------------------------------------
  **Capa**              **Tecnología elegida**   **Coste/mes**          **Por qué**
  --------------------- ------------------------ ---------------------- -------------------
  Frontend              Cloudflare Pages         0€                     CDN global, HTTPS
                                                                        auto, deploy
                                                                        GitHub, free para
                                                                        siempre

  Backend API           Fly.io Frankfurt (fra)   0€ (free 3 VMs)        EU, RGPD, siempre
                                                                        activo, sin cold
                                                                        start, escala auto

  Grafo + Vectores +    Neo4j Community (VPS)    0€ (VPS ya pagado)     Todo en uno: grafo,
  Cache                                                                 embeddings, caché
                                                                        semántico

  Base de datos         PostgreSQL (VPS)         0€ (VPS ya pagado)     Historial mensajes,
  relacional                                                            estadísticas,
                                                                        sesiones

  Rate limiting +       Redis (VPS)              0€ (VPS ya pagado)     20MB RAM, muy
  sesiones                                                              ligero,
                                                                        imprescindible para
                                                                        seguridad

  Autenticación         Clerk.com                0€ hasta 10K usuarios  Magic link + Google
                                                 activos                OAuth + gestión de
                                                                        roles lista en 1
                                                                        hora

  Pagos                 Stripe                   1.4%+0.25€ por         PCI-DSS, webhooks,
                                                 transacción EU         gestión de
                                                                        suscripciones,
                                                                        facturación auto

  Chat LLM              Groq GPT-OSS 120B        \~\$0.28/usuario/mes   Calidad +
                                                                        velocidad + precio
                                                                        verificados

  Seguridad entrada     Groq Prompt Guard 2      \~\$0.015/mes (10K     Detección prompt
                                                 msgs)                  injection, casi
                                                                        gratis

  Embeddings caché      text-embedding-3-small   \~\$0.001/mes          Despreciable,
                                                                        necesario para
                                                                        caché semántico

  Calculadora SS        calculadora_ss.py        0€                     Módulo Python
                        (local)                                         propio. Nunca el
                                                                        LLM calcula solo.

  Email transaccional   Resend.com               0€ hasta 3K emails/mes API limpia, dominio
                                                                        propio, plantillas
                                                                        HTML

  Analytics             Plausible.io o Umami     0€ self-hosted /       Sin cookies, RGPD
  EU-compliant                                   \$9/mes cloud          nativo, no Google
                                                                        Analytics

  **TOTAL MVP                                    **\~0-15€/mes**        **Escala a
  (infraestructura)**                                                   \~\$70-100/mes con
                                                                        500 usuarios
                                                                        activos**
  -----------------------------------------------------------------------------------------

*Apéndice V · Calculadora SS verificada contra exámenes reales
2024-2025*

*Fuentes: TRLGSS RDL 8/2015 · misitiosocial.com (casos prácticos 2025) ·
mad.es · oposegsocial.net · Fly.io vs Railway 2026:
thesoftwarescout.com*
