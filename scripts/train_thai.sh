#!/bin/bash

# Thai Language Training Script for DIA-Multilingual TTS

MANIFEST_PATH="configs/thai_train_manifest.json"
LANG_VOCAB_PATH="configs/lang_vocab.json"
DATA_ROOT="data/"
OUTPUT_DIR="checkpoints/thai"
EPOCHS=50
BATCH_SIZE=8
LEARNING_RATE=1e-4
NUM_WORKERS=4

echo "Starting Thai language training..."
echo "Manifest: $MANIFEST_PATH"
echo "Language vocab: $LANG_VOCAB_PATH"
echo "Output directory: $OUTPUT_DIR"

python3 scripts/train_dia.py \
  --manifest $MANIFEST_PATH \
  --lang_vocab $LANG_VOCAB_PATH \
  --data_root $DATA_ROOT \
  --output_dir $OUTPUT_DIR \
  --epochs $EPOCHS \
  --batch_size $BATCH_SIZE \
  --lr $LEARNING_RATE \
  --num_workers $NUM_WORKERS

echo "Training completed!"
echo "Model checkpoints saved in: $OUTPUT_DIR"