#!/usr/bin/env bash
# Run LoRA fine-tuning on CPU using mistral-finetune repo
# Usage: bash run_finetune_cpu.sh /absolute/path/to/mistral-finetune

set -euo pipefail
ROOT_DIR="${1:-$HOME/mistral-finetune}"
CONFIG="$(pwd)/tools/finetune/7B_cpu.yaml"

echo "Root mistral-finetune dir: $ROOT_DIR"
echo "Using config: $CONFIG"

# create venv and install deps if needed
if [ ! -d "$ROOT_DIR" ]; then
  echo "mistral-finetune repo not found at $ROOT_DIR"
  echo "Clone it: git clone https://github.com/mistralai/mistral-finetune.git $ROOT_DIR"
  exit 1
fi

cd "$ROOT_DIR"
python3 -m venv venv || true
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || true

# export threading env to use CPU cores efficiently (adjust as needed)
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-8}
export NUMEXPR_NUM_THREADS=${NUMEXPR_NUM_THREADS:-8}

# Validate dataset
python -m utils.validate_data --train_yaml "$CONFIG" || true

# Run training (CPU). The exact entrypoint may vary; try train module then fallback to train.py
if python -m train "$CONFIG"; then
  echo "Training completed (module)"
else
  echo "Module entry failed, trying train.py"
  python train.py "$CONFIG"
fi

echo "Done. Check run_dir in the YAML for checkpoints." 
