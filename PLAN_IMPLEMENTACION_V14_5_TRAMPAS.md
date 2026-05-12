# 📝 PLAN DE IMPLEMENTACIÓN V14.5: INTEGRACIÓN DE TRAMPAS FILTRADAS Y REFACTORIZACIÓN DEL MOTOR

## 🎯 Objetivo
Sincronizar las **59 trampas legales** extraídas de los materiales de la academia (Sara Domínguez) con el catálogo maestro y preparar el motor de generación `CaseSchemaBuilder.py` para manejar las nuevas complejidades de los Sistemas Especiales (Mar, Minería, Agrario) y las reglas RETA 2024-2026.

---

## 🏗️ 1. Sincronización del Catálogo de Trampas (YAML)

Se añadirán las nuevas trampas detectadas a `academias/1_casos_recientes_2026_DM/catalogo_trampas.yaml` y su versión adicional.

### 🧩 Nuevas Categorías y Trampas Críticas:
*   **Categoría R (RETA Avanzado):**
    *   `R1`: No protección de IPP en contingencias comunes (RETA).
    *   `R2`: Regla de los 180 días para Base Reguladora de Nacimiento (Base 6 meses anteriores / 180).
    *   `R3`: Umbral de control efectivo (25% con funciones de dirección vs 33% socio).
*   **Categoría S (Sistemas Especiales):**
    *   `S1`: Coeficientes reductores en Minería del Carbón (Edad de jubilación < 65).
    *   `S2`: Clasificación de Trabajadores del Mar (Grupos 1, 2A, 2B, 3) según TRB y retribución "a la parte".
    *   `S3`: Exclusión de Accidentes in Itinere en ciertos tramos del Régimen Marítimo.
*   **Categoría T (Cese de Actividad):**
    *   `T1`: Tope de prestación basado en IPREM + 1/6 (prorrateo de pagas).
    *   `T2`: Cómputo de los 12 meses de cotización mínima para acceso.

---

## 🛠️ 2. Refactorización del CaseSchemaBuilder V14.5

El motor debe evolucionar para que el "blueprint" pueda inyectar datos realistas de estos nuevos sistemas.

### [MODIFY] `backend/v14/case_schema_builder.py`
1.  **Extensión de `PersonajeSchema`**: Añadir campos `sistema_especial` y `grupo_cotizacion_mar`.
2.  **Mejora de `_generar_datos_personaje`**:
    *   Si el rol es "marino": Generar TRB (Tonelaje de Registro Bruto) y tipo de retribución.
    *   Si el rol es "minero": Generar años en interior vs exterior para el coeficiente reductor.
    *   Si el rol es "autónomo" (RETA): Aplicar la lógica del 25% de participaciones sociales si es administrador.
3.  **Lógica de Multiactividad**: Permitir que un personaje tenga simultáneamente `rol="trabajador"` y un flag `secuencia_reta=True` para generar conflictos de bases máximas y carencias cruzadas.

---

## 🧪 3. Creación de Nuevos Blueprints de Alta Densidad Legal

Para "activar" las nuevas trampas, crearemos blueprints específicos que el `CaseSchemaBuilder` consumirá:

### [NEW] `backend/v14/blueprints/bp_s17_mar_mineria.py`
*   **Enfoque**: Supuestos de trabajadores del mar y mineros.
*   **Trampas**: S1, S2, S3.
*   **Calculadora**: Integrar coeficientes reductores de edad.

### [NEW] `backend/v14/blueprints/bp_s18_cese_actividad_reta.py`
*   **Enfoque**: Autónomos que cierran negocio o piden nacimiento con la nueva BR.
*   **Trampas**: R1, R2, T1, T2.

---

## ✅ 4. Plan de Verificación

1.  **Actualización de Neo4j**: Sincronizar los artículos del BOE citados en las nuevas 59 trampas (ej. Art. 305 y ss TRLGSS para RETA).
2.  **Test E2E Completo**: Ejecutar `python3 test_e2e_completo_v14_5.py` forzando el uso de los nuevos blueprints.
3.  **Auditoría de Prosa**: Validar que el `LLM Narrator` (Mistral Large) no ignore los datos técnicos (ej. el TRB del barco) al redactar el supuesto.

---

> [!IMPORTANT]
> **Consistencia de Datos**: No se modificarán las trampas existentes (A-G) para mantener la compatibilidad con el dataset de entrenamiento previo, solo se extenderán con las nuevas categorías R, S y T.
