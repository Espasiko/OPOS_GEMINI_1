# Clasificación Técnica de Cálculos - Seguridad Social (Mayo 2026)

Este documento clasifica y detalla la lógica matemática exigible para el Cuerpo Administrativo de la Seguridad Social (C1) y Gestión (A2). Se basa exclusivamente en la normativa vigente en Neo4j y las constantes de 2026.

---

## 📈 Rama 1: Acción Protectora (Pensiones y Subsidios)
Bloque principal que requiere cálculos de Bases Reguladoras (BR) y aplicación de porcentajes.

### A) Incapacidad Temporal (IT)
*   **Fuentes en Neo4j:** Art. 169-176 TRLGSS.
*   **Operación:** 
    *   Enfermedad Común: (Base cotización mes anterior / 30). Días 1-3 (0%), 4-15 (60% empresa), 16-20 (60% INSS/Mutua), 21+ (75%).
    *   Accidente Trabajo: (Base cotización mes anterior - Horas Extras / 30) + (Promedio horas extras año anterior / 365). Pago del 75% desde el día siguiente al hecho.

### B) Jubilación Ordinaria (Modelo 2026)
*   **Fuentes en Neo4j:** Art. 204-210 TRLGSS.
*   **Operación:** Cálculo de la BR dual (Elección de oficio de la más favorable):
    1.  Últimos 25 años (300 bases / 350).
    2.  Últimos 29 años descartando los 24 meses peores (324 bases / 378 aprox).

---

## 🌳 Rama 2: Cotización y Recaudación (Mora y Gestión)
Bloque centrado en cálculos de recargos e intereses financieros. Crucial para temas de Tesorería General (TGSS).

### A) Recargos por Ingreso Fuera de Plazo (Art. 27 TRLGSS)
*   **Escenario 1 (Presentación en plazo):**
    *   Pago en el mes natural siguiente: **10%**.
    *   Pago a partir del segundo mes: **20%**.
*   **Escenario 2 (NO presentación en plazo):**
    *   Pago antes de finalizar el plazo de la reclamación de deuda: **20%**.
    *   Pago tras finalizar el plazo de la reclamación/acta: **35%**.

---

## ⚖️ Rama 3: Infracciones y Sanciones (LISOS)
Cuantías de multas administrativas según el Art. 40 de la LISOS (Actualización 2026).

### A) Cuantías Seguridad Social (General)
*   **Leves:** 70€ a 910€ (según grados).
*   **Graves:** 911€ a 9.273€ (según grados).
*   **Muy Graves:** 9.274€ a 225.018€ (según grados).

---

## 🎯 BLOQUE 4: CATÁLOGO VERIFICADO DE TRAMPAS Y CASOS CRÍTICOS C1

Este catálogo ha sido auditado contra la normativa real para eliminar errores doctrinales.

### 4.1. Recaudación y Procedimiento
1.  **Competencia Orgánica (Trampa INSS vs TGSS):** La TGSS gestiona la afiliación y el dinero (recaudación). El INSS gestiona el reconocimiento del derecho a la prestación.
2.  **Silencio Administrativo (Art. 129 TRLGSS):** En materia de prestaciones de la Seguridad Social, el silencio tiene efectos **desestimatorios** (negativos) una vez transcurrido el plazo máximo para resolver.
3.  **Intereses de Demora:** Se devengan desde el día siguiente al vencimiento del plazo reglamentario, pero solo se exigen tras 15 días de la providencia de apremio.
4.  **Conceptos Excluidos de Cotización:** Se restan de la base el exceso de dietas, gastos de locomoción justificados e indemnizaciones por despido (hasta el límite legal).
5.  **Sujeto Responsable:** El empresario es el único responsable del ingreso de la cuota obrera si no la descontó en el momento del pago del salario.

### 4.2. Acción Protectora (Validado)
6.  **Recaída en IT:** Se considera el mismo proceso si la recaída ocurre antes de 180 días. No hay nuevo periodo de carencia (los 3 primeros días ya se cumplieron).
7.  **Pérdida/Suspensión de IT (Causas Ampliadas):** 
    *   Actuar fraudulentamente para obtener o conservar el subsidio.
    *   Trabajar por cuenta propia o ajena.
    *   Rechazar o abandonar el tratamiento médico sin causa justa.
    *   Incomparecencia injustificada a reconocimientos médicos de la Mutua/INSS.
8.  **Carencia Específica en Jubilación:** Exigencia de que al menos 2 años de los 15 mínimos estén dentro de los 15 años inmediatamente anteriores al hecho causante.
9.  **Cuidado de Menores (CUME):** La reducción de jornada debe ser de al menos el 50%. Si la reducción es menor, el derecho es inexistente.
10. **Maternidad Gemelar (Especial 2026):** El periodo se amplía a **21 semanas** en caso de gemelos (16 base + 1 adicional por hijo + 4 semanas por parto múltiple/discapacidad según RDL 11/2024).
11. **Compromiso de Actividad (Desempleo):** El incumplimiento conlleva la pérdida de la prestación (infracción grave).
12. **Auxilio por Defunción:** Cuantía fija e invariable de **46,50€**. No depende de bases de cotización.
13. **Prescripción:** Plazo general de 5 años para reclamar prestaciones. La caducidad para el cobro de mensualidades es de 1 año.

---
*Documento auditado y corregido - 14 de Mayo de 2026.*
