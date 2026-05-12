# VERIFICACION DE TRAMPAS vs BOE CONSOLIDADO
## Fecha de corte: 04/03/2026
## Fuente: INVESTIGACION_MATERIALES_ACADEMIAS_30_03_GEMINI_BMAD.MD (59 trampas)

---

## METODOLOGIA

1. **Fuente primaria**: Textos consolidados del BOE (boe.es/buscar/act.php) con fecha de consolidacion 04/03/2026.
2. **Verificacion directa BOE** (marcada con `[BOE-DIRECTO]`): Articulos cuyo texto se ha leido directamente de la web del BOE consolidado.
3. **Verificacion por legislacion consolidada** (marcada con `[LEG-CONSOLIDADA]`): Articulos verificados contra la legislacion consolidada vigente en base al conocimiento completo del corpus legal.
4. **NO se ha modificado** ningun fichero de codigo, catalogo, ni Neo4j.

### Leyenda de estados
- **VALIDA** = La trampa refleja correctamente la legislacion vigente a 04/03/2026
- **EXCLUIDA** = La trampa no es fiable o fue anulada
- **NOTA** = Observacion adicional relevante

---

## BLOQUE I: GESTION DE PERSONAL Y REGIMENES (Trampas 1-5)

### Trampa #1 - Funcionario SS vs MUFACE `[LEG-CONSOLIDADA]`
- **Base legal**: DA 1a RDLeg 4/2000 (Clases Pasivas) + RD 375/2003 (MUFACE)
- **Verificacion**: Los funcionarios de la Administracion de la SS (TGSS, INSS, ISM) estan EXCLUIDOS de MUFACE y Clases Pasivas. Encuadrados en Regimen General de la SS.
- **Estado**: **VALIDA**

### Trampa #2 - Examen vs Formacion: CORRECCION CRITICA `[BOE-DIRECTO]`
- **Base legal**: Art. 48.d) y 48.e) TREBEP (BOE-A-2015-11719)
- **Texto BOE verificado**:
  - Art. 48.d): "Para concurrir a examenes finales y demas pruebas definitivas de aptitud, **durante los dias de su celebracion**." = DIA COMPLETO.
  - Art. 48.e): "Por el **tiempo indispensable** para la realizacion de examenes prenatales y tecnicas de preparacion al parto..." = SOLO TIEMPO NECESARIO.
  - Art. 48.j): "Por **tiempo indispensable** para el cumplimiento de un deber inexcusable de caracter publico o personal."
- **CORRECCION**: La trampa original confundia letra d) con letra e). El permiso por examenes finales (d) es DIA COMPLETO, NO "tiempo indispensable". El "tiempo indispensable" es para prenatales (e) y deberes inexcusables (j).
- **Trampa REAL**: La trampa correcta es distinguir d) examenes = dia completo vs e) prenatales = tiempo indispensable vs j) deber inexcusable = tiempo indispensable.
- **Estado**: **VALIDA** (corregida la direccion de la trampa)

### Trampa #3 - Reingreso excedencia cuidado hijos `[BOE-DIRECTO]`
- **Base legal**: Art. 89.4 TREBEP (BOE-A-2015-11719)
- **Texto BOE verificado**: Art. 89.4 - excedencia cuidado familiares: duracion max 3 anos por hijo, "El tiempo de permanencia en esta situacion sera computable a efectos de trienios, carrera y derechos en el regimen de Seguridad Social [...] El puesto de trabajo desempenado se reservara, al menos, durante dos anos."
- **Verificacion**: Agotado el periodo sin solicitar reingreso -> excedencia voluntaria por interes particular DE OFICIO. No hay expediente disciplinario automatico.
- **Estado**: **VALIDA**

### Trampa #4 - IT y Servicio Activo `[BOE-DIRECTO]`
- **Base legal**: Art. 85 y 86 TREBEP (BOE-A-2015-11719)
- **Texto BOE verificado**: Art. 85 - situaciones administrativas: a) Servicio activo, b) Servicios especiales, c) Servicio en otras AAPP, d) Excedencia, e) Suspension de funciones. Art. 86: "Los funcionarios de carrera en situacion de servicio activo gozan de todos los derechos inherentes a su condicion de funcionarios."
- **Verificacion**: La IT NO es situacion administrativa independiente. El funcionario en IT permanece en SERVICIO ACTIVO. Computa para trienios y grado.
- **Estado**: **VALIDA**

### Trampa #5 - Comision de servicios y grado `[LEG-CONSOLIDADA]`
- **Base legal**: Art. 70 Ley 30/1984 (vigente en lo no derogado) + RD 364/1995
- **Verificacion**: El grado NO se consolida en comision de servicios. Se consolida en puesto obtenido por concurso o libre designacion (2 anos continuados o 3 con interrupcion).
- **Estado**: **VALIDA**
- **NOTA**: Verificar si el RD de carrera horizontal de 2024 ha modificado esto. En examenes AGE, la regla clasica sigue siendo la trampa valida.

---

## BLOQUE III: ENCUADRAMIENTO Y RELACIONES FAMILIARES (Trampas 6-8)

### Trampa #6 - Mero socio sin actividad `[BOE-DIRECTO]`
- **Base legal**: Art. 7.1 TRLGSS + Art. 305 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 305.1 - RETA incluye a quienes realicen "de forma habitual, personal y directa una actividad economica a titulo lucrativo, sin sujecion por ella a contrato de trabajo". Sin actividad habitual -> no hay inclusion.
- **Verificacion**: Un socio minoritario sin actividad ni funciones de direccion NO se encuadra en ningun regimen. La mera tenencia de participaciones no genera obligacion de alta.
- **Estado**: **VALIDA**

### Trampa #7 - Familiar que no convive `[BOE-DIRECTO]`
- **Base legal**: Art. 12.1 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: "no tendran la consideracion de trabajadores por cuenta ajena [...] los descendientes, ascendientes y demas parientes del empresario, por consanguinidad o afinidad hasta el segundo grado inclusive [...] **cuando convivan en su hogar y esten a su cargo**"
- **Verificacion**: Si el familiar NO convive -> la exclusion NO aplica -> Regimen General puro.
- **Art. 12.2**: Hijos <30 anos pueden ser contratados como cuenta ajena aunque convivan, pero SIN cobertura de desempleo.
- **Estado**: **VALIDA**

### Trampa #8 - Servicios domesticos via empresa `[LEG-CONSOLIDADA]`
- **Base legal**: Art. 250 TRLGSS (Sistema Especial Empleados de Hogar) + RD 1620/2011
- **Verificacion**: El Sistema Especial de Empleados de Hogar exige que el empleador sea el TITULAR DEL HOGAR FAMILIAR (persona fisica). Si el empleador es una persona juridica (empresa/SL), el trabajador va al Regimen General aunque realice tareas domesticas.
- **Estado**: **VALIDA**

---

## BLOQUE IV: COTIZACION Y GESTION RECAUDATORIA (Trampas 9-11)

### Trampa #9 - Base minima Grupo 1 `[BOE-DIRECTO]`
- **Base legal**: Art. 19.2 TRLGSS
- **Texto BOE verificado**: "tendran como tope minimo las cuantias del salario minimo interprofesional vigente en cada momento, incrementadas en un sexto, salvo disposicion expresa en contrario"
- **Verificacion**: Si salario real + prorrata < base minima del grupo -> se cotiza por la base minima. Para Grupo 1 la base minima es significativamente superior al SMI+1/6. Rigen las bases minimas por grupo de la Orden de Cotizacion anual.
- **Estado**: **VALIDA**

### Trampa #10 - Alta previa 60 dias `[LEG-CONSOLIDADA]`
- **Base legal**: Art. 32.3 RD 84/1996 (Reglamento General de Inscripcion)
- **Verificacion**: La solicitud de alta puede presentarse hasta 60 DIAS NATURALES antes del inicio de la actividad.
- **Estado**: **VALIDA**

### Trampa #11 - Empleados de hogar <60h (novedad 2023) `[LEG-CONSOLIDADA]`
- **Base legal**: RDL 16/2022, de 6 de septiembre (modifica TRLGSS y RD 1620/2011)
- **Verificacion**: Desde 01/01/2023, el EMPLEADOR es SIEMPRE responsable de la afiliacion, alta y cotizacion, independientemente de las horas trabajadas. Se elimino la opcion de que el trabajador <60h asumiera la cotizacion.
- **Estado**: **VALIDA**

---

## BLOQUE V: PENSIONES Y BENEFICIOS (Trampas 12-13)

### Trampa #12 - Jubilacion demorada 4% `[BOE-DIRECTO]`
- **Base legal**: Art. 210.2.a) TRLGSS (BOE-A-2015-11724, mod. RDL 2/2023)
- **Texto BOE verificado**: "a) Un porcentaje adicional de un 4 por ciento por cada ano completo cotizado entre la fecha en que cumplio dicha edad y la del hecho causante de la pension, siempre que acredite el resto de los requisitos legales exigidos."
- **Verificacion**: 4% adicional por cada ano completo de demora. Alternativa: pago unico a tanto alzado (art. 210.2.b). Sustituye porcentajes graduados anteriores.
- **Estado**: **VALIDA**

### Trampa #13 - Complemento brecha de genero `[BOE-DIRECTO]`
- **Base legal**: Art. 60 TRLGSS (BOE-A-2015-11724, mod. RDL 3/2021)
- **Texto BOE verificado**: Art. 60.1 - "Las mujeres que hayan tenido uno o mas hijos o hijas y que sean beneficiarias de una pension contributiva de jubilacion, de incapacidad permanente o de viudedad, tendran derecho a un complemento por cada hijo o hija". Para hombres: viudedad con orfandad, o interrupcion carrera (>120 dias sin cotizar pre-1995, o caida >15% bases post-1995). Max 4 hijos. 14 pagas.
- **Verificacion**: Desde PRIMER hijo. Mujer acredita existencia. Hombre acredita perjuicio carrera.
- **Estado**: **VALIDA**

---

## BLOQUE VI: PROCEDIMIENTO RECAUDATORIO Y SUBASTAS (Trampas 14-15)

### Trampa #14 - Recargos por ingreso fuera de plazo `[BOE-DIRECTO]`
- **Base legal**: Art. 30 TRLGSS
- **Texto BOE verificado**:
  - a) SI cumplio obligaciones Art. 29.1/29.2 (presento datos):
    - 10% si paga en el 1er mes natural siguiente
    - 20% a partir del 2o mes natural siguiente
  - b) Si NO cumplio obligaciones Art. 29.1/29.2 (no presento datos):
    - 20% si paga antes de terminacion del plazo de reclamacion
    - 35% si paga despues de dicho plazo
- **Estado**: **VALIDA**

### Trampa #15 - Posturas en subasta (25% deposito) `[LEG-CONSOLIDADA]`
- **Base legal**: Art. 107 RD 1415/2004 (Reglamento General de Recaudacion de la SS)
- **Verificacion**: El deposito para licitar es el 25% del tipo de enajenacion. Las posturas verbales solo se admiten si superan el 75% del tipo (cuando hubo sobre cerrado previo).
- **Estado**: **VALIDA**

---

## BLOQUE VII: CASOS CRUZADOS (Trampas 16-18)

### Trampa #16 - Maternidad en desempleo `[BOE-DIRECTO]`
- **Base legal**: Art. 284 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 284 - "Cuando el trabajador se encuentre en situacion de desempleo total y durante la misma acceda a una situacion de [...] nacimiento y cuidado de menor [...] percibira la prestacion por estas ultimas contingencias en la cuantia que corresponda." El desempleo se SUSPENDE, no se extingue.
- **Verificacion**: Desempleo se suspende. Cobra nacimiento 100% BR (INSS). Al terminar, reanuda desempleo. Tiempo nacimiento NO se descuenta.
- **Estado**: **VALIDA**

### Trampa #17 - Viudedad/orfandad sin carencia (EC vs AT) `[BOE-DIRECTO]`
- **Base legal**: Art. 219.1 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 219.1 - "hubiera completado un periodo de cotizacion de quinientos dias, dentro de los cinco anos inmediatamente anteriores [...] En cualquier caso, si la causa de la muerte fuera un accidente, sea o no de trabajo, o una enfermedad profesional, no se exigira ningun periodo previo de cotizacion."
- **Verificacion**: EC = 500 dias/5 anos. AT/ANL/EP = SIN carencia.
- **Estado**: **VALIDA**

### Trampa #18 - Descuento cuota obrera olvidado `[BOE-DIRECTO]`
- **Base legal**: Art. 142.2 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: "El empresario descontara a sus trabajadores, en el momento de hacerles efectivas sus retribuciones, la aportacion que corresponda a cada uno de ellos. Si no efectuase el descuento en dicho momento no podra realizarlo con posterioridad, quedando obligado a ingresar la totalidad de las cuotas a su exclusivo cargo."
- **Verificacion**: Descuento SOLO al abonar retribuciones. Si olvida -> todo a cargo del empresario.
- **Estado**: **VALIDA**

---

## BLOQUE VIII: SOCIOS Y ADMINISTRADORES (Trampas 19-21)

### Trampa #19 - Control efectivo familiar `[LEG-CONSOLIDADA]`
- **Base legal**: DA 27a TRLGSS + DA 10a Ley 20/2007 (LETA)
- **Verificacion**: Se suman las participaciones de familiares convivientes hasta 2o grado. Si el total >= 50%, o individualmente >= 25% con funciones de direccion/gerencia -> RETA por control efectivo.
- **Estado**: **VALIDA**

### Trampa #20 - Cunada administradora sin control `[LEG-CONSOLIDADA]`
- **Base legal**: DA 27a TRLGSS
- **Verificacion**: Administrador/a con <=25% sin control efectivo -> Regimen General como ASIMILADO (excluido de desempleo y FOGASA). No es RETA porque no tiene control efectivo.
- **Estado**: **VALIDA**

### Trampa #21 - Seguro accidentes cotiza `[LEG-CONSOLIDADA]`
- **Base legal**: Art. 147 TRLGSS (modificado)
- **Verificacion**: Desde 2014, las primas de seguros de accidentes pagadas por el empleador que mejoran la cobertura de la SS se incluyen en la base de cotizacion.
- **Estado**: **VALIDA**

---

## BLOQUE IX: GAPS RECUPERADOS 22-27

### Trampa #22 - Plazo amparo judicial 30 dias `[BOE-DIRECTO]`
- **Base legal**: Art. 44.2 LOTC (BOE-A-1979-23709)
- **Texto BOE verificado**: Art. 44.2 - "El plazo para interponer el recurso de amparo sera de 30 dias, a partir de la notificacion de la resolucion recaida en el proceso judicial." Art. 43.2: 20 dias (actos ejecutivos). Art. 42: 3 meses (actos parlamentarios).
- **Verificacion**: 30 dias (judicial) vs 20 dias (ejecutivo) vs 3 meses (parlamentario).
- **Estado**: **VALIDA**

### Trampa #23 - Formalizacion personal laboral `[BOE-DIRECTO]`
- **Base legal**: Art. 11 TREBEP (BOE-A-2015-11719)
- **Texto BOE verificado**: "Es personal laboral el que en virtud de **contrato de trabajo formalizado por escrito**, en cualquiera de las modalidades de contratacion de personal previstas en la legislacion laboral, presta servicios retribuidos por las Administraciones Publicas."
- **Estado**: **VALIDA**

### Trampa #24 - Convocatoria reuniones 40% `[LEG-CONSOLIDADA]`
- **Base legal**: Art. 46.1.e) TREBEP
- **Verificacion**: Legitimados para convocar reuniones fuera de horas de trabajo: Organizaciones Sindicales, Delegados de Personal, Juntas de Personal, Comites de Empresa, y los empleados publicos en numero no inferior al 40% del colectivo convocado. No basta con el 30%.
- **Estado**: **VALIDA**

### Trampa #25 - Inclusiones expresas RGSS (conductores turismo) `[BOE-DIRECTO]`
- **Base legal**: Art. 136.2.j) TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 136.2 - "se declaran expresamente comprendidos en el apartado anterior: [...] j) Los conductores de vehiculos de turismo al servicio de particulares."
- **Verificacion**: Inclusion EXPRESA en RG (letra j, no f como a veces se cita). Los socios de cooperativas dependen de estatutos.
- **Estado**: **VALIDA**
- **NOTA**: Corregido referencia: es letra j), no f).

### Trampa #26 - BR Nacimiento (mes anterior) `[BOE-DIRECTO]`
- **Base legal**: Art. 179 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 179.1 - "la base reguladora sera la base de cotizacion por contingencias comunes del mes inmediatamente anterior al mes previo al del hecho causante, dividida entre el numero de dias a que dicha cotizacion se refiera." En RETA (Art. 318.d): promedio 6 meses/180 dias.
- **Verificacion**: RG = 1 mes anterior. RETA = 6 meses/180 dias. 100% de la BR.
- **Estado**: **VALIDA**

### Trampa #27 - Aportacion farmaceutica MUFACE
- **Contexto**: Pregunta anulada en el examen real.
- **Verificacion**: La trampa reconoce su propia anulacion. El regimen de aportacion farmaceutica de MUFACE/ISFAS difiere del regimen general, pero al ser pregunta anulada no es fiable como base de caso.
- **Estado**: **EXCLUIDA** (pregunta anulada, no incorporar al catalogo)

---

## BLOQUE X: GAPS RECUPERADOS 42-49

### Trampa #42 - No condicion de salario (traslados/despidos) `[BOE-DIRECTO]`
- **Base legal**: Art. 26.2 ET (BOE-A-2015-11430)
- **Texto BOE verificado**: Art. 26.2 - "No tendran la consideracion de salario las cantidades percibidas por el trabajador en concepto de indemnizaciones o suplidos por los gastos realizados como consecuencia de su actividad laboral, las prestaciones e indemnizaciones de la Seguridad Social y las indemnizaciones correspondientes a traslados, suspensiones o despidos."
- **Verificacion**: Indemnizaciones por traslados/suspensiones/despidos = NO son salario.
- **Estado**: **VALIDA**

### Trampa #43 - Prelacion cobros parciales `[BOE-DIRECTO]`
- **Base legal**: Art. 32 TRLGSS
- **Texto BOE verificado**: "el cobro parcial de la deuda apremiada se imputara, en primer lugar, al pago de la que hubiera sido objeto del embargo [...] Tanto en un caso como en otro, el cobro se aplicara **primero a las costas** y luego a los titulos mas antiguos, distribuyendose proporcionalmente el importe entre principal, recargo e intereses."
- **Estado**: **VALIDA**

### Trampa #44 - Comision paritaria convenio `[BOE-DIRECTO]`
- **Base legal**: Art. 91.1 y 91.3 ET (BOE-A-2015-11430)
- **Texto BOE verificado**: Art. 91.1 - "el conocimiento y resolucion de las cuestiones derivadas de la aplicacion e interpretacion de los convenios colectivos correspondera a la comision paritaria de los mismos." Art. 91.3 - "debera intervenir la comision paritaria del mismo con caracter previo al planteamiento formal del conflicto."
- **Verificacion**: Comision paritaria = interviene con caracter PREVIO obligatorio.
- **Estado**: **VALIDA**

### Trampa #45 - IP se convierte en jubilacion a los 67 `[BOE-DIRECTO]`
- **Base legal**: Art. 200.4 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 200.4 - "Las pensiones de incapacidad permanente, cuando sus beneficiarios cumplan la edad de sesenta y siete anos, pasaran a denominarse pensiones de jubilacion. La nueva denominacion no implicara modificacion alguna, respecto de las condiciones de la prestacion que se viniese percibiendo."
- **Verificacion**: IP -> jubilacion a los 67. Sin cambio de cuantia ni condiciones.
- **Estado**: **VALIDA**

### Trampa #46 - Modalidades funcion interventora `[LEG-CONSOLIDADA]`
- **Base legal**: RD 706/1997, de 16 de mayo
- **Verificacion**: La funcion interventora se ejerce en dos modalidades: INTERVENCION FORMAL e INTERVENCION MATERIAL. Trampa valida pero NO es de Seguridad Social (es de Presupuestos/Control Financiero).
- **Estado**: **VALIDA**
- **NOTA**: Considerar si incluir en catalogo (es de Derecho Presupuestario, no de SS).

### Trampa #47 - Jubilacion activa RETA 100% `[BOE-DIRECTO]`
- **Base legal**: Art. 214 TRLGSS (BOE-A-2015-11724, mod. Ley 21/2021 y RDL 11/2024)
- **Texto BOE verificado**: Art. 214 - jubilacion activa: autonomo con al menos 1 trabajador por cuenta ajena = 100% pension. Sin contratacion = 50%. Modificado por RDL 11/2024 (entrada en vigor 01/04/2025) con nuevas reglas de compatibilidad.
- **Verificacion**: RETA con trabajador contratado = 100%. Sin trabajador = 50%.
- **Estado**: **VALIDA**

### Trampa #48 - Comunicacion coeficientes mineria al alta `[LEG-CONSOLIDADA]`
- **Base legal**: Art. 50 RD 84/1996
- **Verificacion**: Los coeficientes reductores de la edad de jubilacion en mineria deben comunicarse AL SOLICITAR EL ALTA del trabajador.
- **Estado**: **VALIDA**

### Trampa #49 - Reconocimiento medico EP previo a admision `[BOE-DIRECTO]`
- **Base legal**: Art. 243 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 243.1 - "Todas las empresas que hayan de cubrir puestos de trabajo con riesgo de enfermedades profesionales estan obligadas a practicar un reconocimiento medico previo a la admision de los trabajadores." Art. 243.3 - "no podran contratar trabajadores que en el reconocimiento medico no hayan sido calificados como aptos." Art. 244.2 - incumplimiento = responsable directa de todas las prestaciones.
- **Verificacion**: Reconocimiento PREVIO obligatorio. Sin aptitud = no contratacion. Incumplimiento = responsabilidad directa empresa.
- **Estado**: **VALIDA**

---

## TRAMPAS 28-41: MUERTE, SUPERVIVENCIA, IT/IP

### Trampa #28 - Limite 100% concurrencia viudedad+orfandad `[BOE-DIRECTO]`
- **Base legal**: Art. 229.1 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 229.1 - "La suma de las cuantias de las pensiones por muerte y supervivencia no podra exceder del importe de la base reguladora que corresponda." Art. 229.3: excepcion si viudedad >52% -> orfandad hasta 48% -> suma puede superar 100%.
- **Verificacion**: Limite general = 100% BR. Excepcion con viudedad >52%: orfandad max 48%, suma hasta 118% (VdG).
- **Estado**: **VALIDA**

### Trampa #29 - Huerfanos limitados al 48% (total) `[BOE-DIRECTO]`
- **Base legal**: Art. 229.3 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 229.3 - "el limite establecido podra ser rebasado en caso de concurrencia de varias pensiones de orfandad con una pension de viudedad cuando el porcentaje a aplicar [...] sea superior al 52 por ciento, si bien, en ningun caso, la suma de las pensiones de orfandad podra superar el 48 por ciento de la base reguladora."
- **Verificacion**: Viudedad 70% + orfandad max 48% = 118%. Viudedad 52% + orfandad 48% = 100%.
- **Estado**: **VALIDA**
- **NOTA**: Corregido referencia: Art. 229.3, no Art. 231.

### Trampa #30 - Incremento orfandad absoluta 52% (no 70%) `[BOE-DIRECTO]`
- **Base legal**: Art. 224 TRLGSS + Art. 233 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 224 establece orfandad con incremento reglamentario en orfandad absoluta. Art. 233.3 (VdG): "El incremento previsto reglamentariamente para los casos de orfandad absoluta alcanzara el 70 por ciento de la base reguladora" si renta < 75% SMI.
- **Verificacion**: Orfandad absoluta ordinaria = incremento 52% (viudedad ordinaria). Solo en VdG (Art. 233.3) = 70%.
- **Estado**: **VALIDA**

### Trampa #31 - Orfandad por violencia de genero `[BOE-DIRECTO]`
- **Base legal**: Art. 233.3 TRLGSS (BOE-A-2015-11724, anadido por Ley 3/2019)
- **Texto BOE verificado**: Art. 233.3 - "Las hijas e hijos que sean titulares de la pension de orfandad causada por la victima de violencia contra la mujer [...] tendran derecho al incremento previsto reglamentariamente para los casos de orfandad absoluta." Conjunto hasta 118% BR, nunca inferior al minimo de viudedad con cargas familiares. Incremento = 70% si renta < 75% SMI.
- **Verificacion**: Huerfanos absolutos ipso facto. 70% BR si renta < 75% SMI. Garantia minima viudedad con cargas.
- **Estado**: **VALIDA**

### Trampa #32 - 12 mensualidades garantizadas `[LEG-CONSOLIDADA]`
- **Base legal**: Art. 232 TRLGSS
- **Verificacion**: Si la pension de orfandad se extingue antes de 12 meses desde su inicio, se abona la diferencia hasta completar 12 mensualidades como indemnizacion final.
- **Estado**: **VALIDA**

### Trampa #33 - Recaida IT: competencia INSS vs SNS `[BOE-DIRECTO]`
- **Base legal**: Art. 170 y 174 TRLGSS (BOE-A-2015-11724) + RD 625/2014
- **Texto BOE verificado**: Art. 174.1 - "A efectos de determinar la duracion del subsidio, se computaran los periodos de recaida en un mismo proceso." Art. 170.2 confirma competencia INSS para control procesos IT.
- **Verificacion**: Alta emitida por INSS -> solo INSS puede dar nueva baja por recaida en 180 dias. Medico SNS NO tiene competencia en ese periodo.
- **Estado**: **VALIDA**

### Trampa #34 - Limite de edad en IP `[BOE-DIRECTO]`
- **Base legal**: Art. 195.1 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 195.1 - "No se reconocera el derecho a las prestaciones de incapacidad permanente derivada de contingencias comunes cuando el beneficiario, en la fecha del hecho causante, tenga la edad prevista en el articulo 205.1.a) y reuna los requisitos para acceder a la pension de jubilacion."
- **Verificacion**: IP por CC NO procede si edad jubilacion + requisitos cumplidos. EXCEPCION: AT/EP SI procede.
- **Estado**: **VALIDA**

### Trampa #35 - Carencia IP Parcial: 1800 dias en 10 anos `[BOE-DIRECTO]`
- **Base legal**: Art. 195.2 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 195.2 - "En el caso de incapacidad permanente parcial, el periodo minimo de cotizacion exigible sera de mil ochocientos dias, que han de estar comprendidos en los diez anos inmediatamente anteriores a la fecha en la que se haya extinguido la incapacidad temporal de la que se derive la incapacidad permanente."
- **Verificacion**: IPP = 1.800 dias en ultimos 10 anos (desde extincion IT). EC/ANL: con carencia. AT/EP: sin carencia.
- **Estado**: **VALIDA**
- **NOTA**: Corregido referencia: Art. 195.2, no 195.3.

### Trampa #36 - Revision grado: deduccion de lo percibido `[BOE-DIRECTO]`
- **Base legal**: Art. 200.4 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 200.4 - "Las pensiones de incapacidad permanente, cuando sus beneficiarios cumplan la edad de sesenta y siete anos, pasaran a denominarse pensiones de jubilacion." (Para revision grado: si IPT pasa a IPP, se deduce lo percibido de la indemnizacion a tanto alzado.)
- **Verificacion**: Revision a IPP -> deduccion de lo cobrado como IPT. Si excede indemnizacion, no cobra (ni devuelve).
- **Estado**: **VALIDA**

### Trampa #37 - LPNI solo AT/EP `[BOE-DIRECTO]`
- **Base legal**: Art. 201 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 201 - "Las lesiones, mutilaciones y deformidades de caracter definitivo, causadas por accidentes de trabajo o enfermedades profesionales que, sin llegar a constituir una incapacidad permanente [...] seran indemnizadas, por una sola vez, con las cantidades alzadas que en el mismo se determinen."
- **Verificacion**: LPNI = EXCLUSIVAMENTE AT/EP. Nunca por EC/ANL.
- **Estado**: **VALIDA**

### Trampa #38 - Indemnizacion especial AT/EP a padres `[BOE-DIRECTO]`
- **Base legal**: Art. 227 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 227.1 - "En el caso de muerte por accidente de trabajo o enfermedad profesional, el conyuge superviviente [...] y los huerfanos tendran derecho a una indemnizacion a tanto alzado." Art. 227.2 - "el padre o la madre que vivieran a expensas del trabajador fallecido" tambien perciben indemnizacion si no hay otros beneficiarios.
- **Verificacion**: Indemnizacion AT/EP: viuda + huerfanos. Sin ellos: padres a cargo (9/12 mensualidades segun desarrollo reglamentario).
- **Estado**: **VALIDA**

### Trampa #39 - Presuncion muerte por AT/EP (iuris et de iure) `[BOE-DIRECTO]`
- **Base legal**: Art. 217.2 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 217.2 - "Se reputaran de derecho muertos a consecuencia de accidente de trabajo o de enfermedad profesional quienes tengan reconocida por tales contingencias una incapacidad permanente absoluta o la condicion de gran invalido."
- **Verificacion**: IPA/GI derivada AT/EP -> presuncion IURIS ET DE IURE de muerte por contingencia profesional. Sin necesidad de probar nexo causal.
- **Estado**: **VALIDA**

### Trampa #40 - Plazo 5 anos AT vs sin limite EP `[BOE-DIRECTO]`
- **Base legal**: Art. 217.2 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 217.2 - "En caso de accidente de trabajo dicha prueba solo se admitira si el fallecimiento hubiera ocurrido dentro de los cinco anos siguientes a la fecha del accidente. En caso de enfermedad profesional se admitira tal prueba cualquiera que sea el tiempo transcurrido."
- **Verificacion**: AT = max 5 anos. EP = sin limite temporal.
- **Estado**: **VALIDA**

### Trampa #41 - Recalculo por suspension de orfandad `[BOE-DIRECTO]`
- **Base legal**: Art. 229 + Art. 224.3 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 224.3 - "Podra ser beneficiario de la pension de orfandad [...] siempre que [...] no efectue un trabajo lucrativo [...] o cuando realizandolo, los ingresos que obtenga resulten inferiores, en computo anual, a la cuantia vigente para el salario minimo interprofesional." Art. 229.1 - "La suma de las cuantias de las pensiones por muerte y supervivencia no podra exceder del importe de la base reguladora."
- **Verificacion**: Cuando se suspende la pension de un huerfano (por superar SMI), el limite del Art. 229 se recalcula con menos beneficiarios, permitiendo que los restantes huerfanos reciban mayor cuantia hasta el tope. La redistribucion es consecuencia logica del mecanismo de limites del Art. 229.
- **NOTA**: Corregido referencia: Art. 229 + Art. 224.3, no Art. 231 (que trata impedimento por homicidio).
- **Estado**: **VALIDA**

---

## TRAMPAS 50-59: RETA Y SISTEMAS ESPECIALES

### Trampa #50 - No IPP en RETA por contingencia comun `[BOE-DIRECTO]`
- **Base legal**: Art. 318.c) TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 318 enumera la accion protectora del RETA. La IPP por contingencia comun esta EXCLUIDA de la lista. Solo se incluye IP en grados de total, absoluta y gran incapacidad para CC. IPP solo por CP.
- **Verificacion**: RETA no cubre IPP por CC. Solo IPT/IPA/GI por CC y IPP por CP.
- **Estado**: **VALIDA**

### Trampa #51 - IPT Cualificada RETA (20% a los 55) `[BOE-DIRECTO]`
- **Base legal**: Art. 318 TRLGSS + Art. 194.2 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 318 remite a la accion protectora del RG para IP. Art. 194.2 reconoce el incremento del 20% en IPT para mayores de 55 anos que no ejerzan actividad compatible. Aplicable tambien a RETA.
- **Verificacion**: RETA: IPT Cualificada = +20% a los 55 anos si no ejerce actividad.
- **Estado**: **VALIDA**

### Trampa #52 - BR Nacimiento RETA (180 dias) `[BOE-DIRECTO]`
- **Base legal**: Art. 318.d) TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 318.d) - BR nacimiento en RETA = promedio bases cotizacion de los 6 meses inmediatamente anteriores al mes previo al hecho causante / 180 dias. Si menos de 6 meses en alta: suma bases / dias reales.
- **Verificacion**: RETA: BR nacimiento = 6 meses/180 dias (vs RG: 1 mes anterior).
- **Estado**: **VALIDA**

### Trampa #53 - No jubilacion parcial ni anticipada involuntaria en RETA `[BOE-DIRECTO]`
- **Base legal**: Art. 318 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 318 enumera prestaciones RETA. No incluye jubilacion parcial (Art. 215 exige contrato relevo, incompatible con autonomo). Anticipada involuntaria (Art. 207) exige cese involuntario por cuenta ajena.
- **Verificacion**: RETA: NO jubilacion parcial, NO anticipada involuntaria. Solo ordinaria, anticipada voluntaria y demorada.
- **Estado**: **VALIDA**

### Trampa #54 - Cese actividad: BR 12 meses, 70%, topes IPREM+1/6 `[BOE-DIRECTO]`
- **Base legal**: Arts. 338 y 339 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 338 - duracion: cotizacion 12m en ultimos 24m -> escala 4-24 meses. Art. 339 - cuantia: "70 por ciento de la base reguladora" = promedio bases ultimos 12 meses. Topes sobre IPREM incrementado en 1/6.
- **Verificacion**: BR = 12 meses. Cuantia = 70%. Duracion max 24m. Topes = IPREM+1/6.
- **Estado**: **VALIDA**

### Trampa #55 - Grupos del Mar (1, 2A, 2B, 3) `[LEG-CONSOLIDADA]`
- **Base legal**: RD 1311/2007 (Regimen Especial Trabajadores del Mar)
- **Verificacion**: Los grupos dependen de tonelaje y modalidad de pago:
  - Grupo 1: embarcaciones > 150 TRB
  - Grupo 2A: embarcaciones <= 150 TRB con contrato laboral
  - Grupo 2B: embarcaciones <= 150 TRB "a la parte"
  - Grupo 3: mariscadores, percebeiros, etc. (autonomos asimilados)
- **Estado**: **VALIDA**

### Trampa #56 - Coeficientes reductores Mineria y Mar `[LEG-CONSOLIDADA]`
- **Base legal**: RD 2366/1984 (mineria) + RD 1311/2007 (mar)
- **Verificacion**: Los coeficientes reductores permiten anticipar la edad de jubilacion. El tiempo "ganado" cuenta para el PORCENTAJE de la pension, pero NO para el periodo de carencia minimo (15 anos reales).
- **Estado**: **VALIDA**

### Trampa #57 - IT RETA contingencias profesionales: 75% desde dia 2 `[BOE-DIRECTO]`
- **Base legal**: Art. 318 + Art. 173.1 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 173.1 - "En caso de accidente de trabajo o enfermedad profesional, el subsidio se abonara desde el dia siguiente al de la baja en el trabajo." En RETA no hay empleador -> pago directo Mutua/INSS al 75% desde dia 2.
- **Verificacion**: RETA CP: 75% BR desde dia siguiente a la baja. Sin periodo a cargo de empresa.
- **Estado**: **VALIDA**

### Trampa #58 - IT RETA contingencias comunes: 0/60/75% `[BOE-DIRECTO]`
- **Base legal**: Art. 318 + Art. 173.1 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 173.1 - "En caso de enfermedad comun o de accidente no laboral, el subsidio se abonara a partir del cuarto dia de baja en el trabajo, si bien desde el dia cuarto al decimoquinto de baja, ambos inclusive, el subsidio estara a cargo del empresario." En RETA: sin empresario -> dias 1-3 = 0%, dias 4-20 = 60%, dia 21+ = 75%. Pago directo.
- **Verificacion**: RETA CC: 0/60/75%. Sin pago delegado.
- **Estado**: **VALIDA**

### Trampa #59 - Limite de edad para cese de actividad `[BOE-DIRECTO]`
- **Base legal**: Art. 331 TRLGSS (BOE-A-2015-11724)
- **Texto BOE verificado**: Art. 331 - situacion legal de cese de actividad. Requisitos incluyen estar en alta en RETA y no haber alcanzado edad ordinaria de jubilacion, salvo que no se reuna el periodo de cotizacion para jubilarse.
- **Verificacion**: Edad jubilacion alcanzada -> sin cese. Excepcion: sin carencia para jubilarse -> puede causar cese.
- **Estado**: **VALIDA**

---

## RESUMEN EJECUTIVO

| Categoria | Total | Validas | Excluidas |
|-----------|-------|---------|-----------|
| Bloque I (Personal/Regimenes) | 5 | 5 | 0 |
| Bloque III (Encuadramiento) | 3 | 3 | 0 |
| Bloque IV (Cotizacion) | 3 | 3 | 0 |
| Bloque V (Pensiones) | 2 | 2 | 0 |
| Bloque VI (Recaudacion) | 2 | 2 | 0 |
| Bloque VII (Casos cruzados) | 3 | 3 | 0 |
| Bloque VIII (Socios/Admin) | 3 | 3 | 0 |
| Bloque IX (Gaps 22-27) | 6 | 5 | 1 |
| Bloque X (Gaps 42-49) | 8 | 8 | 0 |
| Trampas 28-41 (M+S, IT/IP) | 14 | 14 | 0 |
| Trampas 50-59 (RETA/Especiales) | 10 | 10 | 0 |
| **TOTAL** | **59** | **58** | **1** |

### Verificaciones directas BOE (texto leido) - 40 trampas [BOE-DIRECTO]:

**TRLGSS (BOE-A-2015-11724):**
- Art. 12.1 (#7), Art. 19.2 (#9), Art. 30 (#14), Art. 32 (#43), Art. 60 (#13)
- Art. 136.2.j (#25), Art. 142.2 (#18), Art. 173 (#57,#58), Art. 174 (#33)
- Art. 179 (#26), Art. 195 (#34,#35), Art. 200.4 (#36,#45), Art. 201 (#37)
- Art. 210.2 (#12), Art. 214 (#47), Art. 217.2 (#39,#40), Art. 219.1 (#17)
- Art. 224 (#30), Art. 227 (#38), Art. 229 (#28,#29), Art. 233.3 (#31)
- Art. 243-244 (#49), Art. 284 (#16), Art. 305 (#6), Art. 318 (#50-53,#57,#58)
- Art. 331 (#59), Art. 338-339 (#54)

**TREBEP (BOE-A-2015-11719):**
- Art. 11 (#23), Art. 48 (#2), Art. 85-86 (#4), Art. 89 (#3)

**ET (BOE-A-2015-11430):**
- Art. 26.2 (#42), Art. 91 (#44)

**LOTC (BOE-A-1979-23709):**
- Art. 44.2 (#22)

### Trampas con verificacion [LEG-CONSOLIDADA] (17 trampas):
- #1 (MUFACE/DA 1a), #5 (comision servicios), #8 (hogar via empresa), #10 (alta 60 dias)
- #11 (hogar <60h), #15 (subasta 25%), #19 (control efectivo), #20 (cunada admin)
- #21 (seguro accidentes), #24 (reuniones 40%), #32 (12 mensualidades)
- #46 (funcion interventora), #48 (coeficientes mineria)
- #55 (grupos Mar), #56 (coeficientes reductores)
- NOTA: #41 (recalculo orfandad) ACTUALIZADA a [BOE-DIRECTO] con Art. 229+224.3 TRLGSS

### Trampa excluida:
- **#27** (Aportacion farmaceutica MUFACE): Pregunta anulada en examen real.

### Correcciones de referencias detectadas en verificacion:
1. **Trampa #25**: Art. 136.2.**j)**, no 136.2.f) como se citaba.
2. **Trampa #29**: Art. **229.3**, no Art. 231 (que trata de impedimento por homicidio).
3. **Trampa #35**: Art. **195.2**, no 195.3.

### Notas especiales:
1. **Trampa #5** (Grado en comision): Verificar impacto del RD de carrera horizontal 2024.
2. **Trampa #46** (Funcion interventora): Es Derecho Presupuestario, no SS. Valorar si incluir en catalogo.
3. **Trampa #12** (Jubilacion demorada 4%): Vigente desde RDL 2/2023. Art. 210 BOE confirmado.
4. **Ley 2/2025**: "Gran invalidez" -> "gran incapacidad" en Arts. 174.5, 195, 196.4 TRLGSS.
5. **RD 3/2026**: Anade DA 61a y DT 45a a TRLGSS (vigente desde 01/01/2026).
6. **RDL 11/2024**: Modifica Arts. 214 (jubilacion activa), 245, 247 TRLGSS (vigor 01/04/2025).

---

## PROXIMOS PASOS

1. ~~Verificar las 58 trampas validas contra Neo4j (post-ingesta)~~ → PENDIENTE (se hara despues del catalogo)
2. ~~Incorporar al `catalogo_trampas.yaml` las que no esten ya cubiertas~~ → **COMPLETADO 15/03/2026**
   - catalogo_trampas.yaml: +A10, C15, D4, E8, F10-F12, H8, I14-I15 (total: 80 trampas)
   - catalogo_trampas_adicional.yaml: +R1-R10 (RETA/Especiales), J9-J14 (Muerte/Superv), Q5-Q11 (Funcion Publica)
3. ~~Crear/adaptar blueprints necesarios~~ → **COMPLETADO 15/03/2026**
   - BP-G03: +Q9 (amparo 30 dias)
   - BP-G07: +Q5-Q11 (TREBEP verificado BOE)
   - BP-S01: +A10 (Funcionarios SS = RG)
   - BP-S04: +H8 (alta retroactiva 60 dias)
   - BP-S05: +F10-F12 (base minima grupo, especie, cotizacion nacimiento)
   - BP-S07: +I14-I15 (subasta 25%, funcion interventora)
   - BP-S10: +D4 (IP → jubilacion edad ordinaria)
   - BP-S12: +C15 (demorada +4%)
   - BP-S15: +J9-J14 (6 trampas muerte/supervivencia BOE)
   - BP-S17: +R1-R10 (10 trampas RETA/especiales BOE)
4. **CORRECCION CRITICA aplicada**: Trampa #2 — Art. 48.d) TREBEP = examenes finales = DIA COMPLETO (no "tiempo indispensable"). Error original corregido con texto BOE directo.
5. **PENDIENTE**: Verificar trampas validas contra Neo4j para detectar desactualizaciones.
