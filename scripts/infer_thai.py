#!/usr/bin/env python3
"""
Thai Language Inference Script for DIA-Multilingual TTS
"""

import argparse
import json
import torch
import torchaudio
from pathlib import Path
from dia.model import DiaModel
import subprocess

def thai_phonemizer(text):
    """
    Simple Thai phonemizer - replace with proper G2P
    This is a placeholder implementation
    """
    # For production, use proper Thai G2P tools like:
    # - PyThaiNLP's phonemization
    # - Custom Thai phoneme dictionary
    # - Thai IPA conversion tools
    
    # Simplified character-level approach
    return list(text.replace(" ", ""))

def main():
    parser = argparse.ArgumentParser(description="Thai TTS Inference")
    parser.add_argument("--model_path", required=True, help="Path to trained model")
    parser.add_argument("--lang_vocab", required=True, help="Language vocabulary JSON")
    parser.add_argument("--text", required=True, help="Thai text to synthesize")
    parser.add_argument("--output_dir", default="outputs/", help="Output directory")
    parser.add_argument("--reference_wav", help="Reference audio for style cloning")
    parser.add_argument("--sample_rate", type=int, default=22050, help="Sample rate")
    
    args = parser.parse_args()
    
    # Load language vocabulary
    lang_vocab = json.load(open(args.lang_vocab))
    
    # Load model
    model = DiaModel.load_from_checkpoint(args.model_path, map_location="cpu")
    model.eval()
    
    # Thai language setup
    lang = "th"
    lang_token = f"<{lang}>"
    lang_token_id = lang_vocab.get(lang_token, 0)
    
    print(f"Input text: {args.text}")
    print(f"Language: {lang} (token_id: {lang_token_id})")
    
    # Get phonemes for Thai
    phonemes = thai_phonemizer(args.text)
    print(f"Phonemes: {phonemes}")
    
    # Build character vocabulary (should match training)
    char_vocab = {c: i+10 for i, c in enumerate(sorted(set(phonemes)))}
    char_vocab["<pad>"] = 0
    char_vocab["<unk>"] = 1
    
    # Convert to token IDs
    phoneme_ids = [char_vocab.get(c, 1) for c in phonemes]
    input_ids = torch.tensor([lang_token_id] + phoneme_ids).unsqueeze(0)
    
    print(f"Input shape: {input_ids.shape}")
    
    # Reference audio (optional)
    ref_audio = None
    if args.reference_wav:
        wav, sr = torchaudio.load(args.reference_wav)
        if sr != args.sample_rate:
            wav = torchaudio.functional.resample(wav, sr, args.sample_rate)
        ref_audio = wav.squeeze(0).unsqueeze(0)
        print(f"Using reference audio: {args.reference_wav}")
    
    # Generate audio
    print("Generating Thai speech...")
    with torch.no_grad():
        audio = model.infer(input_ids=input_ids, ref_audio=ref_audio)
    
    # Save output
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output_dir) / f"thai_tts_{hash(args.text) % 10000}.wav"
    torchaudio.save(str(output_path), audio.cpu(), args.sample_rate)
    
    print(f"✅ Thai speech generated: {output_path}")
    return output_path

if __name__ == "__main__":
    main()