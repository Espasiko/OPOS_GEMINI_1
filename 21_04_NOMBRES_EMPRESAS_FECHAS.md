# AUDITORÍA DE ENTIDADES, EMPRESAS Y FECHAS (Catálogo Trampas v2)

Este documento consolida la extracción manual (línea a línea) de todas las entidades, casos ficticios y fechas específicas contenidas en `trampas_unificadas_v2_CURADO.yaml`.

> [!IMPORTANT]
> **ESTADO DE LA AUDITORÍA:** 100% Completada (Líneas 1-4082).
> **VERIFICACIÓN AGENTES:** Todos los agentes en carpeta `bmad` están operativos y verificados para el proyecto OPOS_GEMINI_1.

## 1. PERSONAS Y CASOS (ENTIDADES INDIVIDUOS)

| Nombre | Rol / Contexto | Trampa Asociada |
| :--- | :--- | :--- |
| **Miguel** | Socio con 37% capital (conviviente) | A13 (RETA por control familiar) |
| **Caridad** | Hermana de Miguel (53% capital) | A13 (RETA por control familiar) |
| **Esposa de Miguel** | 10% capital (conviviente) | A13 (RETA por control familiar) |
| **Cuñada de Miguel** | Administradora (10% capital, no convive) | A14 (RG Asimilada sin desempleo) |
| **Andrés** | Autónomo embargado (garaje) | Marca 5 (Entrelazamiento causal) |
| **Roberto** | Fallecido por Enfermedad Común | J15 (Carencia 500 días / 5 años) |
| **Leandro** | Socio Cooperativa con deuda | R11 (Responsabilidad Solidaria) |
| **Genaro** | Mero socio inversor (20%, no trabaja) | A11 (No procede alta) |
| **Sofía** | Jubilada con 36a 4m cotizados | CA1 (Cálculo mes a mes exacto) |
| **Irene** | Asesora laboral (comete errores) | I8 (Error con Mutua) |
| **Víctor** | Cliente de Irene | I8 |
| **Javier** | Autónomo RETA (alta 18 oct) | H7 (Ventanas efectos RETA) |
| **Pedro** | Trabajador en empresa con impagos | N1 (Automaticidad absoluta) |

## 2. EMPRESAS Y ENTIDADES JURÍDICAS

*   **GAVIOTAS DEL SUR S.COOPV:** (Caso R11) Cooperativa de Trabajo Asociado. Responsabilidad solidaria.
*   **BODEGAS DIONISIOS:** (Bloque 1) Empresa con deudas.
*   **CARNICERÍA APOCALIPTO S.L.:** (Bloque 1) Ejemplo de alta fuera de plazo.
*   **MC MUTUAL:** (Bloque 2) Entidad gestora mencionada en el error de Irene.

## 3. FECHAS, PLAZOS Y FORMATOS ESPECÍFICOS

### A. Fechas Clave (Vigor 2025/2026)
*   **01/04/2025:** Entrada en vigor RDL 11/2024 (Jubilación activa, fijos discontinuos, etc.).
*   **19/04/2026:** Fecha de verificación literal del BOE para todo el catálogo.
*   **01/01/2026:** Inicio nueva regla BR Jubilación (302/352,33).
*   **11/02/2026:** Fecha de la sentencia STS 158/2026 (Parejas de hecho).
*   **24/12/2024:** Fecha de reforma RDL 11/2024 en el BOE.
*   **01/10/2023:** Derogación definitiva del coeficiente de parcialidad (RDL 2/2023).
*   **01/01/2023:** Vigor RDL 16/2022 (SE Hogar <60h cotiza empleador).

### B. Formatos Detectados en Texto Narrativo
*   **Formatos Mes:** "18 oct", "1 nov", "julio", "agosto", "septiembre".
*   **Formatos Numéricos:** "01/04/2025", "25/10/2017", "11/02/2026".
*   **Plazos Críticos:**
    *   **48 horas:** Plazo TGSS SLD (Art. 18.2.e).
    *   **10 días naturales:** Rechazo notificación electrónica.
    *   **30 días naturales:** Recurso de Amparo.
    *   **60 días naturales:** Plazo ingreso tras notificación.
    *   **15 días:** Para presentar valoración contradictoria (URE).
    *   **180 días:** Especial competencia INSS recaídas; Período base desempleo.
    *   **273 días:** Factor base reguladora AT/EP (días laborables).

## 4. TOPES Y CIFRAS ECONÓMICAS 2026 (CURADO)

*   **Base Máxima:** 5.101,20 €
*   **Pensión Máxima:** 3.359,60 €
*   **Cuota Fija ≤ 8 días:** 32,60 €
*   **Patrimonio PNC IP:** 26.409,60 € (Vivienda habitual EXCLUIDA).
*   **Umbral 20%:** Diferencia tasación para TERCER PERITO.
*   **Umbral 25%:** Suelo absoluto subasta bienes inmuebles.
*   **19 Semanas:** Permiso nacimiento funcionarios (32 monoparental).

## 5. REGLAS DE CÁLCULO "FINAS" (MANUAL AUDIT)

1.  **Viudedad AT/EP:** Divisor pluses = Días efectivamente trabajados. Multiplicador = **273**.
2.  **Jubilación Activa RETA (con empleado):**
    *   Demora 1-3 años: **75%**.
    *   Demora 4 años: **80%**.
    *   Demora 5+ años: **100%**.
3.  **Cese Actividad RETA:** Topes IPREM **puros** (175%/107%). No usar IPREM+1/6.
4.  **Recargos:** Escala 10%, 20%, 35% (Pre-apremio / Post-vencimiento / Providencia).

---
**Nota Final:** El catálogo v2 está totalmente alineado con la normativa vigente en 2026. Se recomienda usar estos nombres (Zacarias, Caridad, Miguel) en todos los nuevos simulacros para mantener la coherencia narrativa del sistema.
