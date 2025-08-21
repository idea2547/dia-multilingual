# 🇹🇭 Thai Language Training Guide for DIA-Multilingual TTS

This guide explains how to train the DIA-Multilingual TTS model for Thai language support.

## 📋 Prerequisites

1. **Thai Audio Dataset**: Prepare Thai speech data with transcriptions
2. **Dependencies**: Install Thai NLP tools
3. **Hardware**: GPU recommended for training

## 🚀 Quick Start

### 1. Install Thai Dependencies
```bash
pip install -r requirements_thai.txt
```

### 2. Prepare Thai Dataset
Create your training manifest in `configs/thai_train_manifest.json`:
```json
[
  {
    "audio": "data/th/clips/sample1.wav",
    "text": "สวัสดีครับ",
    "phonemes": "s a w a t d i k r a p",
    "lang": "th"
  }
]
```

### 3. Train Thai Model
```bash
./scripts/train_thai.sh
```

### 4. Generate Thai Speech
```bash
python scripts/infer_thai.py \
  --model_path checkpoints/thai/epoch49.pt \
  --lang_vocab configs/lang_vocab.json \
  --text "สวัสดีครับ" \
  --output_dir outputs/
```

## 📊 Dataset Requirements

### Audio Format
- **Sample Rate**: 22,050 Hz
- **Channels**: Mono
- **Format**: WAV
- **Duration**: 1-10 seconds per clip
- **Quality**: Clean, noise-free recordings

### Text Requirements
- **Language**: Thai script (Unicode)
- **Content**: Natural Thai sentences
- **Length**: 5-50 words per sentence
- **Coverage**: Diverse vocabulary and phonemes

### Recommended Datasets
1. **Common Voice Thai** - Mozilla's open dataset
2. **LOTUS Corpus** - Thai speech corpus
3. **NECTEC Thai Speech** - Academic datasets
4. **Custom Recordings** - Record your own data

## 🔧 Advanced Configuration

### Thai Phonemizer Options
The system includes a custom Thai phonemizer (`tools/thai_phonemizer.py`) that:
- Converts Thai script to IPA phonemes
- Handles tone marks and vowel combinations
- Supports syllable segmentation

### Training Parameters
Adjust training parameters in `scripts/train_thai.sh`:
- **Batch Size**: Start with 8, increase based on GPU memory
- **Learning Rate**: 1e-4 (default) or 5e-5 for fine-tuning
- **Epochs**: 50-100 depending on dataset size
- **Sample Rate**: 22,050 Hz (default)

### Model Architecture
The model uses:
- **Language Token**: `<th>` for Thai
- **Phoneme Encoding**: Custom Thai phoneme vocabulary
- **Speaker Embedding**: 192-dimensional speaker vectors
- **Diffusion Steps**: StyleTTS2-based generation

## 📈 Training Tips

### Data Preparation
1. **Clean Audio**: Remove background noise and normalize volume
2. **Accurate Transcriptions**: Ensure text matches audio exactly
3. **Diverse Speakers**: Include multiple speakers for better generalization
4. **Balanced Dataset**: Cover various phonemes and tones

### Training Strategy
1. **Start Small**: Begin with 100-500 samples to test pipeline
2. **Monitor Loss**: Training loss should decrease steadily
3. **Validation**: Use held-out data to check overfitting
4. **Checkpointing**: Save models every 10 epochs

### Common Issues
- **Memory Errors**: Reduce batch size or sequence length
- **Poor Quality**: Check audio preprocessing and phoneme accuracy
- **Slow Training**: Use mixed precision or smaller model variants

## 🎯 Evaluation

### Objective Metrics
- **MOS Score**: Mean Opinion Score from human listeners
- **WER**: Word Error Rate with ASR systems
- **Phoneme Accuracy**: Compare generated vs. target phonemes

### Subjective Evaluation
- **Naturalness**: How natural does the speech sound?
- **Intelligibility**: Can listeners understand the content?
- **Speaker Similarity**: Does it match reference speaker?

## 🔄 Fine-tuning Existing Models

To fine-tune an existing multilingual model for Thai:

1. **Load Pre-trained Model**:
```python
model = DiaModel.from_pretrained("nari-labs/Dia-1.6B")
```

2. **Add Thai Language Token**:
Update the language vocabulary to include `<th>`.

3. **Prepare Thai Data**:
Use the same format as training data.

4. **Fine-tune**:
```bash
python scripts/train_dia.py \
  --manifest configs/thai_train_manifest.json \
  --pretrained_model checkpoints/pretrained.pt \
  --epochs 20 \
  --lr 5e-5
```

## 🛠️ Troubleshooting

### Common Errors

**"Thai not supported" in espeak-ng**:
- Use the custom Thai phonemizer instead
- Install additional Thai language packs

**Out of Memory**:
- Reduce batch size
- Use gradient accumulation
- Enable mixed precision training

**Poor Audio Quality**:
- Check sample rate consistency
- Verify audio preprocessing pipeline
- Ensure proper phoneme alignment

### Performance Optimization

**Speed Up Training**:
- Use multiple GPUs with DataParallel
- Enable mixed precision (FP16)
- Optimize data loading with more workers

**Improve Quality**:
- Increase model size
- Add more training data
- Use speaker embeddings
- Apply audio augmentation

## 📚 Resources

### Thai NLP Libraries
- **PyThaiNLP**: Comprehensive Thai NLP toolkit
- **AttaCut**: Thai word segmentation
- **DeepCut**: Neural Thai tokenization

### Datasets
- **Common Voice**: https://commonvoice.mozilla.org/th
- **OpenSLR**: http://www.openslr.org/
- **NECTEC**: Thai language resources

### Papers
- "StyleTTS 2: Towards Human-Level Text-to-Speech through Style Diffusion and Adversarial Training with Large Speech Language Models"
- "DIA: A Dialogue-based Text-to-Speech Model"
- Thai TTS research papers from NECTEC and universities

## 🤝 Contributing

To contribute Thai language improvements:
1. Fork the repository
2. Add Thai language features
3. Test with Thai datasets
4. Submit pull request with documentation

## 📄 License

This Thai language extension follows the same license as the main DIA project.