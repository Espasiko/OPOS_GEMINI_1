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
