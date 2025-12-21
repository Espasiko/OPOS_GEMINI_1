import json
import os
from datetime import datetime

# ---------------------------------------------------------
# GEMINI PREMIUM CASE GENERATOR (MANUAL IMITATION MODE)
# ---------------------------------------------------------
# Este script genera un caso de ALTA CALIDAD imitando el razonamiento profundo (CoT).

CASE_DATA = {
    "titulo": "Supuesto Práctico Oficial: Compatibilidad de Incapacidad Permanente Total (IPT) y Jubilación (2025)",
    "dificultad": "EXTREMA (Formato Oficial 2024/25)",
    "escenario": """### **CASO PRÁCTICO – INCAPACIDAD Y JUBILACIÓN 2025**

D. Rogelio M., nacido el 15 de febrero de 1960, trabajaba como **Oficial de 1ª de la Construcción** (CNAE 412) para la empresa "Edificios Seguros S.A." desde el año 1990. El 10 de enero de 2024, sufrió un accidente no laboral (caída en su domicilio) que le provocó lesiones graves en la columna vertebral. Tras agotarse el periodo máximo de Incapacidad Temporal (365 días + 180 días de prórroga), el Equipo de Valoración de Incapacidades (EVI) propuso el 15 de julio de 2025 declarar a Rogelio en situación de **Incapacidad Permanente Total (IPT)** para su profesión habitual, resolución que fue aprobada por el INSS el 30 de julio de 2025. La base reguladora de la pensión se fijó en 2.000 €/mes. Rogelio, al tener 65 años cumplidos en 2025, solicitó el incremento del 20% (IPT Cualificada), pero le fue denegado.

Ante la imposibilidad de volver a la construcción, pero sintiéndose capaz de realizar otras tareas, Rogelio comenzó a trabajar el 1 de septiembre de 2025 como **Conserje** (Grupo de Cotización 6) en una comunidad de vecinos, con un salario mensual de 1.200 € (base de cotización 1.300 €). No comunicó este inicio de actividad al INSS hasta el 1 de octubre de 2025. El INSS inició un procedimiento de revisión.

Paralelamente, la esposa de Rogelio, Dña. Carmen S., nacida el 20 de mayo de 1958, accedió a la **Jubilación Anticipada Voluntaria** el 20 de mayo de 2021 (a los 63 años). Carmen tenía cotizados 35 años y 6 meses. En diciembre de 2024, Carmen recibió una notificación informándole de una posible revisión de su pensión por la aplicación de los nuevos coeficientes penalizadores de la Ley 21/2021, dándole un plazo de 10 días para alegaciones, trámite que Carmen no realizó.

El 15 de febrero de 2026, Rogelio cumple 66 años. Deciden acudir a un asesor para plantear dos cuestiones:
1. Si Rogelio puede solicitar la **Jubilación Ordinaria** manteniendo su trabajo de conserje (Jubilación Activa o Flexible).
2. Si Carmen puede reclamar el **Complemento de Brecha de Género** que no solicitó en 2021, dado que tuvo dos hijos (nacidos en 1985 y 1988) y su jubilación fue anticipada voluntaria.

Dato adicional: Rogelio tiene reconocido un grado de discapacidad del 33% desde el año 2010. Carmen no tiene discapacidad reconocida.""",
    
    "razonamiento_escenario": """**GEMINI INTERNAL REASONING (CHAIN OF THOUGHT):**

1.  **Análisis del Sujeto 1 (Rogelio):**
    *   **Edad**: Nacido 15/02/1960. En 2025 cumple 65 años.
    *   **Situación**: IPT derivada de Accidente No Laboral.
    *   **Incompatibilidades**: La IPT es compatible con *otro* trabajo (Conserje vs Oficial Construcción), siempre que las funciones no coincidan. El salario es compatible *integramente* con la pensión del 55%.
    *   **Trampa del 20% (Cualificada)**: Rogelio pide el 20% adicional. **ERROR**: El incremento del 20% (art. 196.2 LGSS) es incompatible con la realización de trabajos por cuenta ajena o propia. Al empezar a trabajar de conserje, no puede cobrar la cualificada. Además, cumple 65 años, edad teórica de jubilación, lo que cambia las reglas.
    *   **Comunicación**: Retraso en comunicar al INSS (inicio 1 sept, comunicación 1 oct). Sanción leve/grave según LISOS.

2.  **Análisis del Sujeto 2 (Carmen):**
    *   **Jubilación Anticipada Voluntaria (2021)**: Ley vigente entonces. Coeficientes reductores.
    *   **Complemento Brecha de Género (CGB)**: Entró en vigor en febrero 2021 (RD-ley 3/2021). Las jubilaciones anticipadas voluntarias TAMBIÉN generan derecho al CGB (a diferencia del antiguo complemento de maternidad que excluía la anticipada voluntaria).
    *   **Prescripción**: Ha pasado tiempo desde 2021, pero el reconocimiento del CGB es imprescriptible en cuanto al derecho, aunque los efectos económicos tienen retroactividad limitada (3 meses).

3.  **Cruce de Normativas (La "Prueba de Fuego"):**
    *   **Paso de IPT a Jubilación (Rogelio)**: Al llegar a la edad ordinaria (66 años y X meses en 2026? Depende de cotización), debe optar (art. 163.1 LGSS). No puede cobrar ambas. Si opta por jubilación, ¿puede trabajar de conserje? Sí, vía Jubilación Activa (50% pensión) o Flexible (reducción jornada). Pero la IPT se extingue si opta por jubilación. Si se queda con IPT, es compatible con salario conserje pero "congelada" en 55% base.

4.  **Diseño de Trampas**:
    *   *Fecha hechos causantes*: Calcular si Carmen tenía derecho al CGB en mayo 2021 (Sí, vigor feb 2021).
    *   *Compatibilidad IPT*: La gente olvida que el incremento 20% NO se paga si trabajas.
    *   *Opción Jubilación*: Al cumplir 67 años (o 65+cotización), la IPT pasa a ser jubilación (cuantía no inferior), pero si trabaja, la jubilación activa exige requisitos (100% si autónomo con empleado, 50% resto).
    """,

    "preguntas": [
        # LOTE 1 (1-6)
        {
            "numero": 1,
            "enunciado": "Respecto a la solicitud de Rogelio del incremento del 20% de la base reguladora de su IPT (Cualificada) al cumplir 55 años, ¿fue correcta la denegación del INSS?",
            "opciones": [
                "A) No, debería haberse concedido automáticamente al tener más de 55 años.",
                "B) Sí, porque Rogelio comenzó a trabajar como conserje, y el incremento es incompatible con el trabajo.",
                "C) No, porque la discapacidad del 33% permite compatibilizar el incremento con el trabajo a tiempo parcial.",
                "D) Sí, pero solo porque no había cumplido aún los 60 años, edad requerida para la cualificada en accidentes no laborales."
            ],
            "respuesta_correcta": "B",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 196.2 LGSS: El incremento del 20% por cualificación (mayores 55 años) queda en suspenso durante el periodo en que el trabajador obtenga un empleo.",
            "trampa_logica": "Confundir la IPT base (compatible) con la IPT Cualificada (incompatible con trabajo)."
        },
        {
            "numero": 2,
            "enunciado": "Rogelio comunicó su inicio de trabajo como conserje el 1 de octubre de 2025, habiendo comenzado el 1 de septiembre. ¿Constituye esto una infracción?",
            "opciones": [
                "A) No, tiene un plazo de 3 meses para comunicarlo.",
                "B) Sí, es una infracción leve por simple retraso.",
                "C) Sí, es una infracción grave según la LISOS, al no comunicar datos relevantes que afectan a la prestación (compatibilidad del 20%).",
                "D) No, porque el INSS cruza datos de oficio con la TGSS."
            ],
            "respuesta_correcta": "C",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 24 y 25 LISOS. La no comunicación de inicio de actividad que afecte a la prestación (en este caso, incompatibilidad con el 20% cualificada si lo estuviera cobrando o solicitando) es infracción grave.",
            "trampa_logica": "Creer en el cruce automático de datos exime de obligación (falso) o confundir plazos de comunicación."
        },
        {
            "numero": 3,
            "enunciado": "En cuanto a Carmen, que se jubiló anticipadamente de forma voluntaria en mayo de 2021 con 2 hijos. ¿Tenía derecho al Complemento de Brecha de Género en esa fecha?",
            "opciones": [
                "A) No, la jubilación anticipada voluntaria estaba excluida del complemento en 2021.",
                "B) Sí, el RD-ley 3/2021 (vigor febrero 2021) extendió el complemento a la jubilación anticipada voluntaria.",
                "C) No, solo se aplica a jubilaciones ordinarias o forzosas.",
                "D) Sí, pero solo por el hijo nacido en 1988, al ser el segundo."
            ],
            "respuesta_correcta": "B",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 60 LGSS (redacción RD-ley 3/2021). El nuevo Complemento de Brecha de Género incluye expresamente la jubilación anticipada voluntaria, corrigiendo la discriminación del antiguo art. 60 (Maternidad).",
            "trampa_logica": "Aplicar la normativa antigua (Complemento Maternidad 2016) que excluía la voluntaria."
        },
        {
            "numero": 4,
            "enunciado": "Rogelio cumple 66 años en febrero de 2026. Si quiere acceder a la Jubilación Ordinaria, ¿qué periodo de cotización mínimo se exige en 2026 para jubilarse con 65 años (sin esperar a los 66 años y 10 meses)?",
            "opciones": [
                "A) 38 años y 3 meses.",
                "B) 38 años o más.",
                "C) 38 años y 6 meses.",
                "D) 37 años y 9 meses."
            ],
            "respuesta_correcta": "B",
            "tipo": "Ordinaria",
            "justificacion_legal": "Disposición Transitoria 7ª LGSS. Para 2026, la edad ordinaria es 65 años si se tienen acreditados 38 años y 3 meses o más. (Nota: en 2025 son 38 años y 3 meses, en 2026 sube). Espera, verificación: 2024: 38. 2025: 38 y 3. 2026: 38 y 3. Revisar tabla exacta DT7.",
            "trampa_logica": "La trampa está en la tabla progresiva de la DT7. En 2026 se exigen 38 años y 3 meses para los 65. Rogelio (nacido 1960) tiene 66, por lo que entra por edad legal ordinaria (66 años y 10 meses seria la exigible si no tiene cotización, pero con 66 ya podría si tiene cotizacion suficiente? No, la edad legal sube). *Autocorrección*: En 2026, la edad es 65 si tienes >= 38a y 3m. Si no, 66 años y 10m. Rogelio tiene 66 en febrero. Si no llega a 38a 3m, debe esperar a los 66 y 10m (diciembre 2026)."
        },
        {
            "numero": 5,
            "enunciado": "Si Carmen solicita HOY (2025) el Complemento de Brecha de Género que no pidió en 2021, ¿qué efectos económicos tendría el reconocimiento?",
            "opciones": [
                "A) Retroactividad total a la fecha del hecho causante (mayo 2021).",
                "B) Retroactividad máxima de 3 meses desde la solicitud actual.",
                "C) Efectos desde el día siguiente a la solicitud actual.",
                "D) No tiene derecho por haber prescrito a los 4 años."
            ],
            "respuesta_correcta": "B",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 53.1 LGSS. Si se solicita una prestación (o complemento) con posterioridad a los 3 meses del hecho causante, los efectos económicos se retrotraen un máximo de 3 meses desde la solicitud.",
            "trampa_logica": "Confundir la imprescriptibilidad del derecho con la retroactividad de los efectos económicos (limitada a 3 meses)."
        },
        {
            "numero": 6,
            "enunciado": "¿Es compatible la pensión de IPT de Rogelio con su nuevo trabajo de Conserje?",
            "opciones": [
                "A) No, la IPT es incompatible con cualquier trabajo por cuenta ajena.",
                "B) Sí, siempre que el salario no supere el SMI.",
                "C) Sí, porque la profesión de conserje es distinta a su profesión habitual (Oficial Construcción).",
                "D) Sí, pero la pensión se reduce al 50% automáticamente."
            ],
            "respuesta_correcta": "C",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 198.1 LGSS. La pensión vitalicia de IPT es compatible con el salario que pueda percibir el trabajador en la misma empresa o en otra distinta, siempre que las funciones no coincidan con las de la profesión habitual.",
            "trampa_logica": "Aplicar la reducción del 50% (propia de la Jubilación Activa) a la IPT (que es 100% compatible si la profesión es distinta)."
        },
        # LOTE 2 (7-12)
        {
            "numero": 7,
            "enunciado": "Si Rogelio opta por la **Jubilación Flexible** en 2026 para seguir de conserje, ¿cómo afectaría a su pensión de jubilación?",
            "opciones": [
                "A) Cobraría el 50% de la pensión y trabajaría jornada completa.",
                "B) Cobraría el 100% de la pensión y el salario.",
                "C) Se reduciría la pensión en proporción inversa a la jornada laboral realizada (que debe ser entre 25% y 50% de reduccion).",
                "D) No puede acceder a jubilación flexible desde una IPT."
            ],
            "respuesta_correcta": "C",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 213 LGSS y RD 1132/2002. La jubilación flexible permite compatibilizar trabajo a tiempo parcial (reducción jornada 25-50%) con la parte proporcional de la pensión.",
            "trampa_logica": "Confundir Jubilación Flexible (tiempo parcial + parte pensión) con Jubilación Activa (tiempo completo/parcial + 50% pensión fija)."
        },
        {
            "numero": 8,
            "enunciado": "La base reguladora de la IPT de Rogelio es de 2.000 €. Si falleciera por el accidente no laboral, ¿cuál sería el porcentaje para calcular la pensión de viudedad de Carmen?",
            "opciones": [
                "A) 52% de la base reguladora.",
                "B) 60% de la base reguladora, si cumple requisitos de edad y carencia de rentas.",
                "C) 70% de la base reguladora si hay cargas familiares.",
                "D) Todas las anteriores son posibles según las circunstancias."
            ],
            "respuesta_correcta": "D",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 220 LGSS. El tipo general es 52%, sube al 60% (mayores 65 años, sin otros ingresos) o 70% (cargas familiares, única fuente ingresos).",
            "trampa_logica": "Quedarse solo con el tipo general del 52%."
        },
        {
            "numero": 9,
            "enunciado": "¿Qué ocurre con la pensión de IPT de Rogelio cuando cumpla la edad ordinaria de jubilación (si no opta por jubilarse)?",
            "opciones": [
                "A) Se extingue obligatoriamente.",
                "B) Se denomina 'pensión de jubilación' automáticamente sin cambiar la cuantía ni el régimen fiscal.",
                "C) Pasa a denominarse pensión de jubilación, con la ventaja fiscal de considerarse rendimientos del trabajo exentos? No, retención IRPF cambia.",
                "D) Se mantiene como IPT vitalicia a todos los efectos hasta que opte expresamente."
            ],
            "respuesta_correcta": "B",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 200.2 LGSS. Al cumplir la edad ordinaria de jubilación, la IPT pasa a denominarse pensión de jubilación (si no opta por la jubilación propiamente dicha que pudiera ser mayor), no se recalcula, pero cambia la denominación.",
            "trampa_logica": "Creer que hay un recálculo obligatorio o que se extingue si no hace nada."
        },
        {
            "numero": 10,
            "enunciado": "Si Rogelio perdiera su trabajo de conserje y solicitara el desempleo, ¿es compatible con la IPT?",
            "opciones": [
                "A) No, la IPT es incompatible con prestaciones sustitutivas de rentas.",
                "B) Sí, siempre que el desempleo se genere por el trabajo compatible (conserje) y no por la profesión original.",
                "C) Solo si renuncia a la pensión de IPT temporalmente.",
                "D) Sí, pero se descuenta el importe de la pensión del subsidio."
            ],
            "respuesta_correcta": "B",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 282 LGSS. La prestación por desempleo generada por trabajos compatibles con la IPT es compatible con la pensión.",
            "trampa_logica": "Pensar que cobrar pensión impide cobrar desempleo; impide cobrar desempleo *generado por la profesión de la IPT*, no por la nueva."
        },
        {
            "numero": 11,
            "enunciado": "Respecto a la revisión de la pensión de Carmen por los coeficientes penalizadores (Ley 21/2021). Si ella se jubiló en mayo 2021 (antes de la Ley), ¿le afectan los nuevos coeficientes?",
            "opciones": [
                "A) Sí, la ley es retroactiva para mejorar las pensiones.",
                "B) No, se aplica la normativa vigente al hecho causante (mayo 2021, Ley anterior).",
                "C) Sí, se recalculan todas las anticipadas voluntarias desde 2002.",
                "D) Solo si ella lo solicita expresamente para acogerse al complemento de carrera larga."
            ],
            "respuesta_correcta": "B",
            "tipo": "Ordinaria",
            "justificacion_legal": "Principio de irretroactividad (salvo disposición favorable expresa que no aplica aquí masivamente). La pensión se calcula con la norma vigente al hecho causante.",
            "trampa_logica": "Confusión con el 'Complemento para largas carreras' que sí revisó de oficio algunas pensiones, pero los coeficientes penalizadores en sí no se aplican retroactivamente para perjudicar."
        },
        {
            "numero": 12,
            "enunciado": "La base reguladora de 2.000 € de Rogelio para IPT derivada de accidente NO laboral. ¿Cómo se calculó el período de referencia?",
            "opciones": [
                "A) Últimos 8 años (96 meses).",
                "B) Dividiendo por 112 las bases de los 96 meses anteriores al hecho causante.",
                "C) Últimos 25 años, igual que la jubilación.",
                "D) Un período ininterrumpido de 24 meses elegidos dentro de los últimos 7 años."
            ],
            "respuesta_correcta": "B",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 197.1.b LGSS. Para IPT derivada de enfermedad común o accidente no laboral (si no cumple requisitos jubilación), la BR es el cociente de dividir por 112 las bases de los 96 meses anteriores.",
            "trampa_logica": "Confundir con la BR de Jubilación (25 años) o Accidente de Trabajo (salario real anual)."
        },
        # LOTE 3 (13-18) - INCLUYE RESER V A
        {
            "numero": 13,
            "enunciado": "Si Rogelio fallece, ¿a cuánto ascendería la indemnización a tanto alzado para Carmen (viuda)?",
            "opciones": [
                "A) 6 mensualidades de la base reguladora.",
                "B) 1 mensualidad de vacatas.",
                "C) No existe indemnización a tanto alzado en muerte por enfermedad común/accidente no laboral, solo auxilio de defunción.",
                "D) 12 mensualidades si hay hijos menores."
            ],
            "respuesta_correcta": "C",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 217 y ss LGSS. La indemnización especial a tanto alzado (6 meses) es para Muerte por Accidente de Trabajo o Enfermedad Profesional. En Accidente No Laboral solo hay Auxilio por Defunción (46,50€) y pensión.",
            "trampa_logica": "Asumir que 'Accidente' (aunque sea no laboral) conlleva indemnización especial."
        },
        {
            "numero": 14,
            "enunciado": "Rogelio quiere viajar con el IMSERSO. ¿Tiene la condición de pensionista de jubilación a efectos de servicios sociales antes de los 65 años?",
            "opciones": [
                "A) Sí, como pensionista de IPT mayor de 60 años.",
                "B) No, hasta que no cumpla 65.",
                "C) Solo si tiene la IPT Cualificada.",
                "D) Sí, porque tiene discapacidad del 33%."
            ],
            "respuesta_correcta": "A",
            "tipo": "Ordinaria",
            "justificacion_legal": "Orden de 1996 sobre Termalismo/Vacaciones. Son beneficiarios los pensionistas de IPT mayores de 60 años.",
            "trampa_logica": "Pensar que solo los 'Jubilados' acceden al IMSERSO."
        },
        {
            "numero": 15,
            "enunciado": "¿Qué porcentaje de retención de IRPF se aplica a la pensión de IPT de Rogelio si se declara 'Exenta'?",
            "opciones": [
                "A) 0%.",
                "B) 2%.",
                "C) 15%.",
                "D) La IPT nunca está exenta, solo la IPA o Gran Invalidez.",
            ],
            "respuesta_correcta": "D",
            "tipo": "Ordinaria",
            "justificacion_legal": "Art. 7 Ley IRPF. Solo están exentas las pensiones por Incapacidad Permanente Absoluta o Gran Invalidez. La IPT tributa como rendimiento del trabajo.",
            "trampa_logica": "Creer que la 'Incapacidad' implica exención fiscal. Solo los grados altos."
        },
        # RESERVA
        {
            "numero": 16,
            "enunciado": "(Reserva 1) Si Carmen hubiera tenido los hijos en 1975 y 1978, ¿cambiaría su derecho al Complemento de Brecha de Género?",
            "opciones": [
                "A) Sí, porque el complemento solo aplica a hijos nacidos a partir de 1995.",
                "B) No, la fecha de nacimiento de los hijos es irrelevante, importa la fecha del hecho causante de la pensión.",
                "C) Sí, porque en esos años no se cotizaba por maternidad.",
                "D) No, pero se reduciría al 50%."
            ],
            "respuesta_correcta": "B",
            "tipo": "Reserva",
            "justificacion_legal": "Art. 60 LGSS. El requisito es haber tenido hijos, sin límite de fecha de nacimiento de estos. Lo que importa es que la pensión se cause vigente la norma (o se solicite ahora).",
            "trampa_logica": "Inventar un requisito de fecha de nacimiento de los hijos inexistente."
        },
        {
            "numero": 17,
            "enunciado": "(Reserva 2) Rogelio trabaja de conserje. Si sufre una baja médica (IT) por gripe común, ¿quién paga la prestación?",
            "opciones": [
                "A) El INSS directamente mediante pago directo.",
                "B) La empresa (Pago Delegado) o la Mutua, igual que cualquier trabajador.",
                "C) No tiene derecho a IT porque ya cobra pensión de IPT.",
                "D) El INSS, pero se descuenta de la pensión."
            ],
            "respuesta_correcta": "B",
            "tipo": "Reserva",
            "justificacion_legal": "Régimen General. Al trabajar en una actividad compatible y cotizar, genera derecho a IT por esa actividad. El pago sigue las reglas normales (del 4 al 15 empresa, 16 en adelante INSS/Mutua en pago delegado).",
            "trampa_logica": "Pensar que ser pensionista de IPT anula el derecho a IT en la nueva profesión."
        },
        {
            "numero": 18,
            "enunciado": "(Reserva 3) Si Rogelio quiere volver a trabajar en la construcción (su profesión habitual) porque se ha recuperado milagrosamente, ¿qué debe hacer?",
            "opciones": [
                "A) Nada, solo firmar el contrato.",
                "B) Solicitar revisión por mejoría ante el INSS antes de empezar.",
                "C) Empezar a trabajar y esperar a que la Inspección le quite la pensión.",
                "D) Es imposible, la IPT es vitalicia."
            ],
            "respuesta_correcta": "B",
            "tipo": "Reserva",
            "justificacion_legal": "Art. 200 LGSS. Debe instar la revisión por mejoría. Si trabaja en la profesión habitual sin revisión previa, incurre en cobro indebido y fraude.",
            "trampa_logica": "Creer que la compatibilidad ('puedes trabajar') incluye la profesión habitual, cuando esa es precisamente la causa de la pensión."
        }
    ],
    
    "razonamiento_preguntas": """**GEMINI QUESTIONS REASONING:**
    
    *   **Preguntas 1-6 (Ordinarias)**: Foco en la **compatibilidad** y el **calendario**. La trampa del 20% cualificada vs trabajo es clásica. La fecha de comunicación (sanción LISOS) exige conocer plazos. El complemento de Brecha de Género (CGB) testea el conocimiento del RD-ley 3/2021 sobre jubilaciones anticipadas.
    *   **Preguntas 7-12 (Ordinarias)**: Foco en **cálculos y fiscalidad**. Jubilación Flexible vs Activa. Viudedad (tipos 52/60/70). El paso de IPT a Jubilación (edad ordinaria) es conceptual. Fiscalidad (no exenta) rompe mitos.
    *   **Preguntas 13-15 (Ordinarias)**: Detalles finos. Indemnización a tanto alzado (solo AT/EP). Servicios sociales (IMSERSO).
    *   **Preguntas 16-18 (Reserva)**:
        *   R16: Fecha nacimiento hijos (trampa distractora).
        *   R17: IT en trabajo compatible (cruce de prestaciones).
        *   R18: Revisión por mejoría (fraude vs procedimiento).
    
    El nivel es alto porque exige distinguir entre IPT derivada de Accidente Laboral vs No Laboral (para bases y viudedad) y reglas de compatibilidad Jubilación/Trabajo vs IPT/Trabajo."""
}

OUTPUT_PATH = "/home/spas/OPOS_GEMINI_1/dataset_generator/premium_content/deepseek_pilot/gemini_premium_case_manual_001.json"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(CASE_DATA, f, indent=2, ensure_ascii=False)

print(f"✅ Caso Premium Generado: {OUTPUT_PATH}")
