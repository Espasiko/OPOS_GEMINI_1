# INVESTIGACIÓN DE MATERIALES - ACADEMIAS (30/03) 🕵️‍♂️

Este documento recopila de forma sistemática las "trampas", "villancicos" y puntos de confusión detectados en los materiales de las academias para su posterior integración en el `catalogo_trampas.yaml` y el motor de generación V14.5.

## 📊 Metodología de Extracción
1. **Lectura profunda** de los archivos de texto extraídos (10MB+).
2. **Identificación de patrones** en supuestos prácticos reales (Exámenes AGE 2011-2023).
3. **Aislamiento de la "Trampa"**: El giro legal que invalida la respuesta lógica pero incorrecta.

---

## 🏗️ Bloque I: Gestión de Personal y Regímenes (Líneas 34800-35500)

### 1. La Trampa del "Funcionario de la S.S. vs MUFACE"
*   **Origen**: Supuesto Conv. PI C1 AGE 2013 - Pregunta 9.
*   **La Trampa**: Se presenta a un funcionario que pertenece a un cuerpo de la **Administración de la Seguridad Social** solicitando entrar en **MUFACE/Clases Pasivas**.
*   **El Engaño**: El opositor tiende a pensar que al ser "Administración General del Estado" (en sentido amplio), tiene derecho al régimen especial de funcionarios.
*   **Realidad Legal**: Los funcionarios de la Administración de la Seguridad Social están **EXCLUIDOS** de MUFACE/Clases Pasivas (quedan en Régimen General).
*   **Aplicación V14.5**: Generar personajes que trabajen en la TGSS o INSS y pregunten por su régimen; la respuesta correcta siempre debe ser Régimen General.

### 2. La Trampa del "Examen vs Formación"
*   **Origen**: Pregunta 8 (34809).
*   **La Trampa**: Un empleado pide permiso para un examen de carrera universitaria.
*   **El Engaño**: Confundir "tiempo indispensable" con "día completo".
*   **Realidad Legal**: El permiso es solo por el **tiempo indispensable** para la realización. No incluye el día anterior ni posterior por desplazamiento (a menos que el convenio específico diga otra cosa, pero en general es la trampa).

### 3. La Trampa del Reingreso desde Excedencia por Cuidado de Hijos
*   **Origen**: Pregunta R2 (35022).
*   **La Trampa**: El funcionario agota los 3 años y no pide el reingreso.
*   **El Engaño**: Pensar que se le abre expediente por abandono de servicio o que se le avisa.
*   **Realidad Legal**: Se le declara **de oficio** en excedencia voluntaria por interés particular. No hay "aviso previo" ni "expediente disciplinario" automático por el simple fin del plazo.

### 4. La Trampa de la IT y la Situación Administrativa
*   **Origen**: Pregunta R903 (35031).
*   **La Trampa**: ¿En qué situación está un funcionario de carrera durante una IT (Incapacidad Temporal)?
*   **El Engaño**: Pensar que es "Suspensión de funciones" o "Excedencia por enfermedad".
*   **Realidad Legal**: Sigue en **Servicio Activo** (con licencia por enfermedad). Es vital para el cómputo de trienios y grado.

---

## 🏗️ Bloque II: Incompatibilidades y Consolidación de Grado (Líneas 35100-35300)

### 5. La Trampa de la Comisión de Servicios y el Grado
*   **Origen**: Pregunta 10 (35242).
*   **La Trampa**: Funcionario A1 (grado 24) en comisión de servicios 2 años en nivel 28.
*   **El Engaño**: Pensar que consolida el 28 o que consolida el 26 (por salto).
*   **Realidad Legal**: **No consolida grado alguno** en comisión de servicios (en la normativa general de la AGE, el grado se consolida en puesto obtenido por concurso o libre designación, salvo excepciones muy específicas de "reserva de grado"). *Nota: Verificar si esto ha cambiado en el último RD de 2024, pero en los exámenes de academia es la trampa reina.*

---

---

## 🏗️ Bloque III: Encuadramiento y Relaciones Familiares (Líneas 97700-97900)

### 6. La Trampa del "Mero Socio" (Genaro)
*   **Origen**: Supuesto 2022 C1 PI - Pregunta 1.
*   **La Trampa**: Socio con 20% del capital que no trabaja ni dirige.
*   **El Engaño**: Pensar que debe estar en el RETA o General por ser socio.
*   **Realidad Legal**: **No procede el alta**. La mera administración del patrimonio no es actividad laboral.
*   **Aplicación V14.5**: Insertar personajes "inversores" en las tramas para forzar al opositor a descartar su alta.

### 7. La Trampa del "Familiar que no convive" (Luis)
*   **Origen**: Pregunta 2 (97838).
*   **La Trampa**: Hijo de 27 años que trabaja en la empresa de los padres pero **no convive** con ellos.
*   **El Engaño**: Aplicar automáticamente la exclusión de familiares del Art. 12 TRLGSS.
*   **Realidad Legal**: Al no convivir, es **Régimen General** (trabajador por cuenta ajena puro). Si conviviera y fuera menor de 30, podría ser General pero sin desempleo (Disposición Adicional 10ª LETA).

### 8. La Trampa de "Servicios Domésticos vía Empresa" (Marcos)
*   **Origen**: Pregunta 3 (97860) - Marcada como "PGTA. TRAMPA".
*   **La Trampa**: Marcos limpia la casa del jefe, pero el contrato lo hace la **empresa** (SL).
*   **El Engaño**: Encuadrarlo en el Sistema Especial de Empleados de Hogar.
*   **Realidad Legal**: **Régimen General**. Si el empleador es una persona jurídica (empresa), no es Empleados de Hogar, aunque la labor sea doméstica.

---

## 🏗️ Bloque IV: Cotización y Gestión Recaudatoria (Líneas 97500-97700)

### 9. La Trampa de la "Base Mínima del Grupo 1"
*   **Origen**: Pregunta 6 (97548).
*   **La Trampa**: Trabajadora grupo 1 con salario de 1000€ + prorrata extras.
*   **El Engaño**: Calcular la base sobre el salario real (aprox 1166€).
*   **Realidad Legal**: Debe cotizar por la **Base Mínima del Grupo 1** (1.629,30€ en 2022), que es muy superior a su salario real.
*   **Aplicación V14.5**: El motor de cálculo debe validar que si el salario + prorrata < base_min_grupo, se inyecta la base_min_grupo.

### 10. La Trampa del "Alta Previa" (Plazos)
*   **Origen**: Pregunta 5 (97535).
*   **La Trampa**: ¿Con cuánta antelación se puede solicitar el alta?
*   **El Engaño**: Confundir los 60 días con 30 o 3.
*   **Realidad Legal**: Hasta **60 días naturales antes**. (Ojo: Antes eran menos, la trampa es el cambio normativo reciente).

### 11. La Trampa de los Empleados de Hogar < 60h (Novedad 2023)
*   **Origen**: Pregunta 4 (97911).
*   **La Trampa**: Contrato de 6 horas semanales. ¿Quién ingresa las cuotas?
*   **El Engaño**: Pensar que el trabajador puede seguir ingresándolas él mismo (como antes de 2023).
*   **Realidad Legal**: Desde el 1/01/2023, el **empleador es siempre el responsable**, sin importar las horas. Se acabó la opción de que el trabajador < 60h asuma la cotización.

---

---

## 🏗️ Bloque V: Pensiones y Beneficios (Líneas 99050-99090)

### 12. La Trampa de la "Jubilación Demorada" (4% vs 2%)
*   **Origen**: Pregunta 8 (99063).
*   **La Trampa**: Laura decide jubilarse en 2024 (después de su edad ordinaria).
*   **El Engaño**: Aplicar porcentajes antiguos (2% o 3%) basándose en años de carencia.
*   **Realidad Legal**: Tras la reforma, es un **4% adicional fijo** por cada año completo de demora (o pago único, a elección).
*   **Aplicación V14.5**: El blueprint de Jubilación debe forzar el cálculo al 4% para casos "post-reforma".

### 13. La Trampa del "Complemento de Brecha de Género"
*   **Origen**: Pregunta 7 (99052).
*   **La Trampa**: Laura tiene 1 hijo y dejó de trabajar para cuidarlo.
*   **El Engaño**: Pensar que se necesitan 2 hijos (como el antiguo "Complemento de Maternidad").
*   **Realidad Legal**: El nuevo complemento se da desde el **primer hijo**, siempre que se acredite el perjuicio en la carrera (lagunas de cotización o cese).
*   **Ojo al Dato**: Si el hombre quiere pedirlo, tiene requisitos mucho más duros que la mujer.

---

## 🏗️ Bloque VI: Procedimiento Recaudatorio y Subastas (Líneas 98350-98430)

### 14. La Trampa de los "Recargos por Ingreso Fuera de Plazo"
*   **Origen**: Pregunta 4 (99033).
*   **La Trampa**: Empresa presenta liquidación (L00) pero no paga a tiempo.
*   **El Engaño**: Aplicar el 20% o 35% indiscriminadamente.
*   **Realidad Legal**: 
    - 10% si paga en el mes siguiente al plazo.
    - 20% si paga después del primer mes natural siguiente.
    - **OJO**: Si NI SIQUIERA presentó los datos de cotización (liquidación), el recargo sube al **20% directo** (desde el día 1 de retraso) o **35%** si es tras reclamación/acta.

### 15. La Trampa de las "Posturas en Subasta"
*   **Origen**: Preguntas 12 y 14 (98376, 98417).
*   **La Trampa**: ¿Cuánto hay que depositar para pujar?
*   **El Engaño**: Confundir el 25% del tipo con el 30%.
*   **Realidad Legal**: El depósito para licitar es el **25% del tipo de enajenación**.
*   **Posturas verbales**: Solo si superan el **75% del tipo** (si hubo sobre cerrado previo).

---

---

## 🏗️ Bloque VII: Supuesto Práctico 1 (Pág. 1330) - Casos Cruzados

### 16. La Trampa de la "Maternidad en Desempleo"
*   **Origen**: Supuesto Marta (Preguntas 9 y 10).
*   **La Trampa**: Marta es despedida y está cobrando el paro. Da a luz a su hijo Álvaro.
*   **El Engaño**: Pensar que sigue cobrando el 70% u 80% del desempleo.
*   **Realidad Legal**: El desempleo **se suspende**. Pasa a cobrar la prestación por Nacimiento y Cuidado de Menor al **100% de su base reguladora** (abonada por el INSS, no por el SEPE). Al terminar las 16 semanas, se reanuda el paro por el tiempo que quedaba.
*   **OJO**: El tiempo de maternidad **no se descuenta** del paro.

### 17. La Trampa de la "Viudedad y Orfandad sin Carencia"
*   **Origen**: Supuesto Roberto (Pregunta 11).
*   **La Trampa**: Roberto fallece por **enfermedad común** estando en alta.
*   **El Engaño**: Pensar que no hace falta carencia (como en Accidente).
*   **Realidad Legal**: Al ser enfermedad común, se exigen **500 días cotizados** en los 5 años anteriores.
*   **Trampa del Orfanato**: Si el fallecimiento es por Accidente (sea de trabajo o no), **NO se exige carencia**. En el examen suelen poner "enfermedad común" para pillar a quien no compruebe los 500 días.

### 18. La Trampa del "Descuento de Cuota Obrera Olvidado"
*   **Origen**: Pregunta 3 (100407).
*   **La Trampa**: La empresa olvida descontar la cuota al trabajador en febrero. Quiere hacerlo en marzo.
*   **El Engaño**: Pensar que puede hacerlo "cuando se de cuenta".
*   **Realidad Legal**: El descuento DEBE hacerse en el momento de abonar las percepciones. Si no se hace, el empresario queda obligado a ingresar el total a su **exclusivo cargo**. **PROHIBIDO** descontarlo después.

---

---

## 🏗️ Bloque VIII: Supuesto Práctico 2 (Pág. 1334) - Socios y Administradores

### 19. La Trampa del "Control Efectivo Familiar" (Miguel)
*   **Origen**: Supuesto Miguel (Pregunta 4, 100699).
*   **La Trampa**: Miguel tiene el 37%, su hermana Caridad el 53% y su esposa el 10%. Conviven.
*   **El Engaño**: Pensar que como Miguel tiene < 50% individual (solo 37%), va al Régimen General.
*   **Realidad Legal**: Se suma el capital de los familiares con los que convive. 37% (Miguel) + 53% (hermana) + 10% (esposa) = **100% familiar**. Miguel tiene control efectivo por suma de participaciones familiares. Va al **RETA**.

### 20. La Trampa de la "Cuñada Administradora"
*   **Origen**: Contexto SP2 (100627).
*   **La Trampa**: La cuñada tiene el 10%, es administradora y trabaja 4 horas.
*   **El Engaño**: Al ser administradora, enviarla al RETA directamente.
*   **Realidad Legal**: Al tener solo el 10% (y no convivir con Miguel/Caridad en el mismo domicilio, según se deduzca del caso), no tiene control efectivo. Va al **Régimen General como 'Asimilada'** (sin desempleo ni FOGASA) por ser administradora sin control.

### 21. La Trampa de la "Base de Cotización Grupo 1" (José)
*   **Origen**: Pregunta 12 (100780).
*   **La Trampa**: José tiene sueldo 1200€, antigüedad 100€, 2 pagas extras y seguro accidentes 20€.
*   **El Engaño**: Olvidar que el seguro de accidentes (si es para cubrir riesgos de la empresa) **COTIZA** desde 2014.
*   **Cálculo Correcto**: 
    - Remuneración mensual: 1200 + 100 + 20(seguro) = 1320€.
    - Prorrata extras: (1200+100)*2 / 12 = 216,66€.
    - Base: 1536,66€.
*   **OJO**: El seguro de accidentes para el personal cotiza si es una mejora de la SS voluntaria (desde 2014).

---

## 🏗️ Bloque IX: Examen PI 2023 - Gaps Recuperados (22-27)

### 22. La Trampa del Plazo de Amparo (Judicial)
*   **Origen**: Pregunta 22 (99830).
*   **La Trampa**: Plazo para interponer recurso de amparo ante el TC por actos del Poder Judicial.
*   **El Engaño**: Confundir con los 20 días (actos administrativos) o 3 meses (actos parlamentarios).
*   **Realidad Legal**: Son **30 días** naturales (Art 44.2 LOTC).

### 23. La Trampa de la Formalización del Personal Laboral
*   **Origen**: Pregunta 23 (99834).
*   **La Trampa**: Requisito esencial para ser considerado personal laboral en la Administración.
*   **El Engaño**: Pensar que basta con el nombramiento o el alta en SS.
*   **Realidad Legal**: Precisa de **contrato de trabajo formalizado por escrito**. (Art 11 EBEP).

### 24. La Trampa de la Convocatoria de Reuniones (Legitimación)
*   **Origen**: Pregunta 24 (99842).
*   **La Trampa**: ¿Quién puede convocar una reunión fuera de horas de trabajo?
*   **El Engaño**: Pensar que basta con el 30% del personal.
*   **Realidad Legal**: Se requiere un número no inferior al **40 por ciento** del colectivo convocado (Art 46 EBEP). Las Juntas de Personal y Comités de Empresa sí tienen legitimación directa.

### 25. La Trampa de las Inclusiones Expresas (RGSS)
*   **Origen**: Pregunta 25 (99847).
*   **La Trampa**: ¿Quién entra "por decreto" en el Régimen General?
*   **El Engaño**: Socios de cooperativas (están si lo eligen los estatutos, no es "expreso" por ley).
*   **Realidad Legal**: Los **conductores de vehículos de turismo** al servicio de particulares son inclusión expresa (Art 136.2 LGSS).

### 26. La Trampa de la BR de Nacimiento (Días)
*   **Origen**: Pregunta 26 (99854).
*   **La Trampa**: Cálculo de la Base Reguladora para Nacimiento y Cuidado de Menor.
*   **El Engaño**: Usar el promedio de los últimos 6 meses (eso es en RETA).
*   **Realidad Legal**: Es la BC por CC del **mes anterior al del hecho causante**, dividida por el número de días a que dicha cotización se refiera (Art 179 LGSS).

### 27. La Trampa de la Aportación Farmacéutica (Anulada)
*   **Origen**: Pregunta 27 (99862).
*   **Contexto**: Funcionarios de MUFACE/ISFAS.
*   **Realidad**: Pregunta anulada en el examen real, pero sirve para recordar que su régimen de aportación es distinto (generalmente 30% sin topes, saldo crónicos).

---

## 🏗️ Bloque X: Examen PI 2023 - Gaps Recuperados (42-49)

### 42. La Trampa de la "No Condición de Salario" (Traslados)
*   **Origen**: Pregunta 42 (100067).
*   **La Trampa**: ¿Qué percepciones no son salario?
*   **Realidad Legal**: Las **indemnizaciones correspondientes a traslados, suspensiones o despidos** NO tienen condición de salario (Art 26.2 ET).

### 43. La Trampa de la Prelación en Cobros Parciales
*   **Origen**: Pregunta 43 (100072).
*   **La Trampa**: La empresa paga solo una parte de la deuda apremiada.
*   **Realidad Legal**: Se aplica **PRIMERO A LAS COSTAS** y luego a los títulos más antiguos (Art 32 LGSS).

### 44. La Trampa de la Interpretación de Convenio (Conflicto)
*   **Origen**: Pregunta 44 (100082).
*   **Realidad Legal**: Deberá intervenir previamente la **comisión paritaria** del convenio (Art 91 ET).

### 45. La Trampa del Cambio de Nombre IP -> Jubilación (2027)
*   **Origen**: Pregunta 45 (100088).
*   **Realidad Legal**: A partir de los **67 años** (Disposición Transitoria 7ª LGSS, horizonte 2027).

### 46. La Trampa de las Modalidades de Función Interventora
*   **Origen**: Pregunta 46 (100092).
*   **Realidad Legal**: Se ejerce en las modalidades de **intervención formal e intervención material** (RD 706/1997).

### 47. La Trampa de la Jubilación Activa al 100% (RETA)
*   **Origen**: Pregunta 47 (100095).
*   **Realidad Legal**: Autónomo que contrata a un trabajador. La cuantía de la pensión compatible alcanza el **100 por ciento** (Art 214.2 LGSS).

### 48. La Trampa de la Comunicación de Coeficientes (Minería)
*   **Origen**: Pregunta 48 (100099).
*   **Realidad Legal**: **Al solicitar el alta** del trabajador (Art 50 RD 84/1996).

### 49. La Trampa del Reconocimiento Médico EP
*   **Origen**: Pregunta 49 (100148).
*   **Realidad Legal**: **PREVIAMENTE a la admisión** (Art 243 LGSS).

---

### 28. La Trampa del Límite del 100% en Concurrencia (Viudedad + Orfandad)
*   **Origen**: Anexo3059A4 - Carlos Hernández (Art. 229).

### 29. La Trampa del "Crowding Out" (Huérfanos limitados por Viudedad alta)
*   **Origen**: Anexo3059A4 - Pág 42.
*   **La Trampa**: Si Viudedad = 70%, los huérfanos solo pueden aspirar al 30% restante?
*   **Realidad Legal**: No. Si Viudedad > 52%, los huérfanos tienen un límite **total del 48%** (aunque individualmente sigan limitados al 20%). Esto permite que la suma llegue al **118%** (70+48).

### 30. La Trampa del Incremento de Orfandad Absoluta (52% vs 70%)
*   **Origen**: Anexo3059A4 - Art. 224.
*   **La Trampa**: Al huérfano absoluto se le suma el porcentaje de viudedad.
*   **El Engaño**: Pensar que se suma el 70% si el fallecido tenía cargas.
*   **Realidad Legal**: Se incrementa en un **52% fijo** (el porcentaje ordinario de viudedad).
*   **Variación Divorcio**: Si el otro progenitor vive pero no tiene derecho a viudedad (ej. no era beneficiario), el huérfano **NO** recibe el incremento de orfandad absoluta (porque no hay orfandad absoluta, el padre vive). Pero si el padre muere después, sí.

### 31. La Trampa de la Orfandad por Violencia de Género (Art. 233)
*   **Origen**: Anexo3059A4 - Ley 3/2019.
*   **La Trampa**: Huérfanos de madre asesinada por el padre.
*   **Realidad Legal**: Se consideran huérfanos absolutos ipso facto. 
*   **El Giro**: El incremento puede llegar al **70%** (en vez de 52%) si la renta familiar es < 75% SMI. 
*   **Garantía**: La suma nunca será < Pensión mínima de viudedad con cargas.

### 32. La Trampa de los 12 Meses Garantizados (Extinción)
*   **Origen**: Anexo3059A4 - Pág 42.
*   **La Trampa**: El huérfano se casa o cumple la edad a los 3 meses de empezar a cobrar.
*   **Realidad Legal**: Se le debe abonar la diferencia hasta completar **12 mensualidades**. Es decir, cobra una "indemnización" final por lo que falte hasta los 12 meses.

### 33. La Trampa de la Recaída en IT (Competencia INSS vs SNS)
*   **Origen**: Anexo3058A1 - Alfonso Hidalgo.
*   **La Trampa**: Recaída dentro de los 180 días tras el alta.
*   **El Engaño**: Ir al médico de cabecera (SNS) para la nueva baja.
*   **Realidad Legal**: Si el alta anterior fue emitida por el **INSS**, solo el **INSS** puede emitir la nueva baja por recaída. El SNS no tiene competencia en esos 180 días.

### 34. La Trampa del Límite de Edad en IP (Incapacidad Permanente)
*   **Origen**: Anexo3058A2 - Alfonso Hidalgo (Art. 196).
*   **La Trampa**: Trabajador de 66 años pide IP.
*   **Realidad Legal**: No procede si tiene la edad ordinaria de jubilación y cumple los requisitos para la pensión de jubilación (salvo si la IP deriva de AT/EP, en cuyo caso sí puede). 
*   **Confusión**: Muchos piensan que la IP es "antes de los 65" siempre. Es "antes de la edad ordinaria" aplicada a su caso.

### 35. La Trampa de la Carencia en IP Parcial (EC)
*   **Origen**: Anexo3058A2.
*   **La Trampa**: Calcular los 1.800 días en los últimos 5 años (como en jubilación o viudedad).
*   **Realidad Legal**: Son 1.800 días en los últimos **10 años** inmediatamente anteriores a la extinción de la IT.

### 36. La Trampa de la Revisión de Grado (Pensión a Tanto Alzado)
*   **Origen**: Anexo3058A2 - Alfonso Hidalgo.
*   **La Trampa**: Un pensionista de IP Total mejora y le dan IP Parcial (indemnización 24 meses).
*   **El Engaño**: Cobrar los 24 meses íntegros.
*   **Realidad Legal**: Se **deduce** lo ya percibido en concepto de pensión. Si ya cobró más de lo que vale la indemnización, no cobra nada (pero no devuelve).

### 37. La Trampa de las LPNI (Baremo)
*   **Origen**: Anexo3058A2.
*   **La Trampa**: ¿Se puede cobrar LPNI por una enfermedad común?
*   **Realidad Legal**: **NUNCA**. Las Lesiones Permanentes No Invalidantes son exclusivas de **AT y EP** (Contingencias Profesionales).

### 38. La Trampa de la Indemnización Especial AT/EP (Padres)
*   **Origen**: Anexo3059A4 - Carlos Hernández (Art. 227).
*   **La Trampa**: Fallece trabajador por AT, no hay viuda ni huérfanos. Solo viven los padres a su cargo.
*   **Realidad Legal**: Cobran una indemnización de **9 mensualidades** (si es 1 padre) o **12 mensualidades** (si son los 2). 
*   **OJO**: Deben vivir a expensas del fallecido (ingresos < SMI).

### 39. La Trampa de la Presunción de Muerte por AT/EP
*   **Origen**: Anexo3059A4 (Art. 217).
*   **La Trampa**: Fallece un pensionista de IP Absoluta por AT.
*   **Realidad Legal**: Se presume **IURIS ET DE IURE** (sin prueba en contra) que la muerte es debida a esa contingencia profesional. No hay que demostrar nexo causal.

### 40. La Trampa del Plazo para demostrar Muerte por AT
*   **Origen**: Anexo3059A4.
*   **La Trampa**: El accidente fue hace 10 años, el trabajador muere ahora.
*   **Realidad Legal**: Si es AT -> la prueba solo se admite si la muerte ocurre dentro de los **5 años** siguientes al accidente. Si es EP -> **sin límite de tiempo**.

### 41. La Trampa del Recálculo por Suspensión de Orfandad
*   **Origen**: Anexo3059A4 - Carlos Hernández.
*   **La Trampa**: Un huérfano empieza a trabajar y supera el SMI. Le suspenden la pensión.
*   **Realidad Legal**: Se **recanculan** las pensiones de los otros huérfanos (si estaban limitadas por el 100%/118%), PERO solo si el suspendido ya había cobrado las **12 mensualidades garantizadas**.

---

**50. La (NO) Protección de la IPP en RETA:**
*   **La Trampa:** Por contingencia común, el RETA **NO protege la Incapacidad Permanente Parcial (IPP)**. Solo se protege si deriva de contingencia profesional (accidente de trabajo o enf. profesional).
*   **Pivote Legal:** En un examen, si el autónomo tiene una IPP por enfermedad común -> "No tiene derecho a prestación".

**51. La "Cualificada" en RETA (Incremento del 20%):**
*   **La Trampa:** Los autónomos tienen derecho al incremento del 20% en la IPT (Incapacidad Permanente Total) al cumplir 55 años, igual que en el Régimen General.
*   **Pivote Legal:** Se exige que no se ejerza actividad por cuenta propia ni ajena compatible con la IPT.

**52. Base Reguladora de Nacimiento en RETA (Regla de los 180 días):**
*   **La Trampa:** No es la base del mes anterior (como en General). Es el promedio de las bases de los **6 meses anteriores** al mes previo al hecho causante (dividido por 180).
*   **Pivote Legal:** Si lleva menos de 6 meses en alta, se divide la suma de bases por los días de alta.

**53. Jubilación "Prohibida" en RETA:**
*   **La Trampa:** En el RETA **NO existe la jubilación parcial ni la jubilación anticipada involuntaria**.
*   **Pivote Legal:** Solo cabe la ordinaria, la anticipada voluntaria (35 años cotizados y 2 años antes de la edad legal) y la demorada.

**54. El Cese de Actividad (El "Paro" del Autónomo):**
*   **La Trampa:** La BR es el promedio de los últimos **12 meses**. La cuantía es siempre el **70%**.
*   **Pivote Legal:** Los topes (mínimo y máximo) se calculan sobre el **IPREM + 1/6**. Muchos fallan al usar el IPREM mensual a secas.

**55. Los Grupos del Mar (1, 2A, 2B y 3):**
*   **La Trampa:** La diferencia entre grupos depende del tonelaje (TRB) y si van "a la parte" o "a salario".
*   **Pivote Legal:** Grupo 3 (Mariscadores, percebeiros) son siempre autónomos asimilados. En el examen suelen preguntar por el umbral de las **150 TRB** (Grupo 1 vs 2A).

**56. Coeficientes Reductores en Minería y Mar:**
*   **La Trampa:** Permiten jubilarse antes de los 65/67. El tiempo "ganado" cuenta como cotizado solo para el **porcentaje** de la pensión, no para el periodo de carencia.
*   **Pivote Legal:** Un picador de mina con coeficiente 0.50 que trabaja 20 años tiene 10 años "extra" de cotización teórica.

**57. IT en RETA (Contingencias Profesionales):**
*   **La Trampa:** Se cobra el **75% desde el día siguiente a la baja**. 
*   **Pivote Legal:** No hay días de "cargo a la empresa" (porque no hay empresa). Se cobra desde el día 2 de la baja de forma directa.

**58. IT en RETA (Contingencias Comunes):**
*   **La Trampa:** Días 1-3 (0%), días 4-20 (60%), día 21 en adelante (75%).
*   **Pivote Legal:** Es idéntico al Régimen General, pero el pago siempre es de la Mutua/INSS (Pago directo).

**59. El Límite de Edad para Cese de Actividad:**
*   **La Trampa:** No se puede causar derecho al cese de actividad si se tiene la **edad ordinaria de jubilación**.
*   **Pivote Legal:** Salvo que no se tenga el periodo de carencia para jubilarse, en cuyo caso sí puede seguir protegiéndole el cese.

---

# ✅ Conclusión de la Investigación (Actualizado 30/03)

Hemos catalogado un total de **59 trampas críticas** extraídas de:
1.  **Exámenes Reales (2011-2023)**.
2.  **Supuestos Prácticos de Academias (Las Cortes, SP1 y SP2)**.
3.  **Materiales de Esquemas (Sara Domínguez)**.
4.  **Monográficos de Muerte y Supervivencia (Carlos Hernández)**.
5.  **Esquemas de IT/IP (Alfonso Hidalgo)**.

Estas trampas se inyectarán en el `catalogo_trampas.yaml` para asegurar que el **CaseSchemaBuilder V14.5** genere casos que no solo sean legales, sino que "puncen" en los puntos donde los opositores suelen fallar.

**Próximo Paso**: Sincronizar este MD con el YAML y proceder a la refactorización del Builder con el Architect.






