
# 🚀 Plan de Fine-Tuning: "Operación V8 Midnight"

**Objetivo:** Entrenar Mistral 7B (v0.3) con el Dataset V8 Omni (11.5k items).
**Infraestructura:** Google Colab (Free Tier - GPU T4).
**Tiempo Estimado:** ~3-4 Horas.

---

## 1. 📋 Requisitos Previos (Hazlo Ahora)

1.  **Dataset V8:**
    *   Descarga el archivo local: `dataset_generator/MASTER_DATASET_v8_OMNI.jsonl`
    *   Súbelo a tu **Google Drive** en la raíz.
    *   *Ruta esperada:* `/content/drive/MyDrive/MASTER_DATASET_v8_OMNI.jsonl`

    > **💎 OPCIONAL (Recomendado): Quality Gate con Cohere**
    > Si quieres asegurar la máxima calidad antes de subir:
    > 1.  Consigue una API Key en [Cohere Dashboard](https://dashboard.cohere.com/api-keys) (Gratis para pruebas).
    > 2.  Edita `dataset_generator/filter_quality_cohere.py` y pon tu clave.
    > 3.  Ejecuta localmente: `python3 dataset_generator/filter_quality_cohere.py`
    > 4.  Esto generará `MASTER_DATASET_v9_GOLD_OPTIMIZED.jsonl` (ordenado por calidad).
    > 5.  Usa ESE archivo en lugar del V8 y cambia el nombre en el notebook.

2.  **Notebook:**
    *   He creado el archivo: `fine_tuning_v8_ready.ipynb`
    *   Súbelo también a tu Drive o ábrelo directamente en Colab (File -> Upload notebook).

---

## 2. ⚙️ Configuración del Entrenamiento

He pre-configurado el notebook con estos valores optimizados para el dataset de 11.500 items:

| Parámetro | Valor | Razón |
|:---|:---|:---|
| **Modelo Base** | `unsloth/mistral-7b-v0.3-bnb-4bit` | Cabe en 12GB VRAM (Colab Free). |
| **Épocas** | `1` (aprox. 1440 pasos) | Suficiente para que vea todo el dataset una vez sin sobreajustar (overfitting). |
| **Batch Size** | `2` (Grad Accum: 4) | Efectivo = 8. Balance entre velocidad y memoria. |
| **LoRA Rank** | `16` | Estándar para capturar matices legales. |
| **Warmup** | `100 pasos` | Estabilidad inicial. |

---

## 3. 🚦 Pasos de Ejecución (Paso a Paso)

1.  **Abrir Colab:** Lanza el notebook `fine_tuning_v8_ready.ipynb`.
2.  **Runtime:** Asegúrate de estar en `Entorno de ejecución -> Cambiar tipo -> T4 GPU`.
3.  **Montar Drive:** Ejecuta la celda 0 y autoriza el acceso a Drive.
4.  **Instalar:** Ejecuta Celda 1 (Unsloth). Tardará ~2 min.
5.  **Cargar:** Ejecuta hasta la Celda 3.
    *   *Check:* Debería decir que ha cargado 11.516 filas. Si da error, revisa la ruta del archivo.
6.  **ENTRENAR (Celda 4):**
    *   Dale al Play.
    *   Vigila la barra de progreso. Debería tardar unas 3 horas.
    *   *Importante:* Mantén la pestaña activa (o usa un auto-clicker/reproductor de música de fondo) para que Colab no te desconecte por inactividad.

---

## 4. 💾 Resultado Final

Al terminar, la Celda 5 exportará el modelo a formato **GGUF** (cuantizado q4_k_m).
*   **Archivo:** `mistral_7b_v8_omni_final.gguf`
*   **Ubicación:** Se guardará automáticamente en tu carpeta `/OpositaIA_Models/` en Drive.

Este archivo es el que luego cargaremos en `ollama` o `LM Studio` para probarlo localmente.

**¡Buena suerte esta noche! 🌙**
