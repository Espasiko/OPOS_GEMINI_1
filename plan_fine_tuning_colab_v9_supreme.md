
# 💎 Plan de Fine-Tuning: "Protocolo Calidad Suprema (V9)"

**Status:** ✅ FINALIZADO (28/12/2025)
**Dataset:** `MASTER_DATASET_v9_GOLD_OPTIMIZED.jsonl` (11.516 Items).
**Mejora V9:** **Quality Reranking**. Los mejores items (según Cohere) están al principio del archivo para que el modelo los aprenda primero y con mayor impacto.

---

## 1. 📂 El Kit "Supreme" (Descargas)

Necesitas descargar estos 2 archivos de tu entorno local:

1.  **Dataset V9:** `dataset_generator/MASTER_DATASET_v9_GOLD_OPTIMIZED.jsonl`
2.  **Notebook V9:** `fine_tuning_v9_supreme.ipynb`

---

## 2. 🚀 Instrucciones de Vuelo (Google Colab)

1.  **Subir a Drive:**
    *   Sube el `.jsonl` y el `.ipynb` a la raíz de tu Google Drive (o la carpeta que uses).
    *   *Ruta esperada:* `/content/drive/MyDrive/MASTER_DATASET_v9_GOLD_OPTIMIZED.jsonl`

2.  **Abrir Notebook:**
    *   Abre `fine_tuning_v9_supreme.ipynb` en Colab.
    *   **Runtime:** GPU T4 (Gratis).

3.  **Ejecutar:**
    *   Ejecuta todas las celdas secuencialmente.
    *   **Duración:** ~3 Horas (1 Época).

---

## 3. 🔍 Informe de Calidad (Transparencia)

Durante el proceso `filter_quality_cohere.py`:
*   **Total Items:** 11.516
*   **Ranking:** Se intentó puntuar todos los items contra "Pregunta técnica de oposición".
*   **Incidencia:** Debido a límites de la API Gratuita (Trial Key), algunos bloques dieron error 429.
*   **Solución Segura:** **NO SE BORRÓ NADA**. Los items fallidos se conservaron al final.
*   **Resultado V9:** Es un dataset **Híbrido Optimizado**.
    *   🔝 **Top:** Lo mejor de lo mejor (Items puntuados altos).
    *   ⬇️ **Bottom:** El resto (Backup).
    *   Esto actúa como un *Curriculum Learning* natural (Calidad primero).

**¡Estás listo para entrenar el modelo definitivo!** 🎓🤖
