  - (Recomendado) `llama-cpp-python` para usar modelos GGUF directamente
  # Instalar llama-cpp-python (para inferencia con GGUF)
  pip install llama-cpp-python
    
## Opción Rápida: Usar Modelo GGUF Pre-cuantizado (SIN fine-tuning)

Si solo quieres probar inferencia local sin entrenar, usa el modelo GGUF directamente:

```bash
# 1. Descargar Mistral 7B Instruct Q4 GGUF (4.1GB)
mkdir -p ~/mistral_models
cd ~/mistral_models
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf \
   -O mistral-7b-instruct-q4.gguf

# 2. Instalar llama-cpp-python
pip install llama-cpp-python

# 3. Probar inferencia
python backend/agents/mistral_gguf_local.py
```

**Ventajas del enfoque GGUF**:
- ✅ No necesita fine-tuning (listo para usar)
- ✅ 4.1GB (vs 7GB Ollama formato)
- ✅ Usa `llama-cpp-python` (más eficiente en CPU que Ollama)
- ✅ Mismo rendimiento que Ollama pero menor overhead
- ✅ Descarga directa desde Hugging Face (sin timeouts de Cloudflare R2)

**Wrapper Python creado**: `backend/agents/mistral_gguf_local.py`

```python
from backend.agents.mistral_gguf_local import generate, chat

# Uso simple
response = generate("¿Qué es el recurso de casación?", max_tokens=150)
print(response)

# Formato chat (compatible con OpenAI/Gemini)
response = chat([
  {"role": "user", "content": "¿Qué es el recurso de casación?"}
])
print(response)
```

---

Finetune LoRA (CPU) - Quick guide

Objetivo: ejecutar un fine-tuning LoRA en CPU (muy lento pero gratuito). Este README contiene los pasos mínimos y recomendaciones.

1) Requisitos
- Espacio suficiente (tens/hundreds GB para checkpoints si hacer muchos steps).
- Python 3.9+
- Repositorio `mistral-finetune` clonado en el sistema.

2) Pasos (copy-paste)

# Clonar repo (si no lo tienes)
cd $HOME
git clone https://github.com/mistralai/mistral-finetune.git

# Ajustar paths en YAML (tools/finetune/7B_cpu.yaml)
# - model_id_or_path -> ruta con el modelo base descargado
# - data.* -> rutas a tus jsonl de train/eval
# - run_dir -> donde guardar checkpoints

# Ejecutar script (desde la raíz del repo OPOS_GEMINI_1)
cd /home/espasiko/OPOS_GEMINI_1
bash tools/finetune/run_finetune_cpu.sh $HOME/mistral-finetune

3) Consejos útiles
- Empieza con max_steps=100 para validar que todo funciona.
- Si aparece OOM, baja seq_len a 256 o baja rank en lora.
- Revisa logs en run_dir especificado en YAML.

4) Qué esperar
- En CPU un run puede tardar mucho (horas/días). Si confirmas que config y paths funcionan, puedes dejarlo ejecutando en background (screen/tmux).

5) Después del entrenamiento
- Si `save_adapters: True`, encontrarás `lora.safetensors` en el checkpoint.
- Para inferencia en VPS/host sin fusionar:
  pip install mistral_inference
  mistral-chat /ruta/a/base/model --instruct --lora_path /ruta/a/lora.safetensors

6) Si quieres que haga la ejecución de prueba (max_steps=10) aquí, dímelo y lo ejecuto (nota: el entorno local del runner actual puede no tener modelos ni repo clonado).
