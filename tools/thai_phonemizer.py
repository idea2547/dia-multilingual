#!/usr/bin/env python3
"""
Thai Phonemizer for DIA-Multilingual TTS

This module provides Thai text-to-phoneme conversion for TTS training.
"""

import re
from typing import List, Optional

class ThaiPhonemizer:
    """Thai text to phoneme converter"""
    
    def __init__(self):
        self.setup_mappings()
    
    def setup_mappings(self):
        """Setup Thai character to phoneme mappings"""
        
        # Thai consonants to IPA
        self.consonants = {
            'ก': 'k', 'ข': 'kʰ', 'ค': 'kʰ', 'ง': 'ŋ',
            'จ': 'tʃ', 'ฉ': 'tʃʰ', 'ช': 'tʃʰ', 'ซ': 's', 'ฌ': 'tʃʰ',
            'ญ': 'j', 'ด': 'd', 'ต': 't', 'ถ': 'tʰ', 'ท': 'tʰ', 'ธ': 'tʰ',
            'น': 'n', 'บ': 'b', 'ป': 'p', 'ผ': 'pʰ', 'ฝ': 'f', 'พ': 'pʰ',
            'ฟ': 'f', 'ภ': 'pʰ', 'ม': 'm', 'ย': 'j', 'ร': 'r', 'ล': 'l',
            'ว': 'w', 'ศ': 's', 'ษ': 's', 'ส': 's', 'ห': 'h', 'ฬ': 'l',
            'อ': 'ʔ', 'ฮ': 'h'
        }
        
        # Thai vowels to IPA
        self.vowels = {
            'ะ': 'a', 'า': 'aː', 'ิ': 'i', 'ี': 'iː', 'ึ': 'ɯ', 'ื': 'ɯː',
            'ุ': 'u', 'ู': 'uː', 'เ': 'e', 'แ': 'ɛː', 'โ': 'oː', 'ใ': 'aj',
            'ไ': 'aj', 'ำ': 'am', 'อ': 'ɔː', 'ั': 'a', 'ิ': 'i'
        }
        
        # Tone marks
        self.tones = {
            '่': '1',  # mai ek (low tone)
            '้': '2',  # mai tho (falling tone)
            '๊': '3',  # mai tri (high tone)
            '๋': '4'   # mai chattawa (rising tone)
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and prepare Thai text"""
        # Remove non-Thai characters except spaces
        text = re.sub(r'[^\u0E00-\u0E7F\s]', '', text)
        # Normalize spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def segment_syllables(self, text: str) -> List[str]:
        """Basic Thai syllable segmentation"""
        # This is a simplified approach
        # For production, use proper Thai word segmentation tools
        syllables = []
        current_syllable = ""
        
        for char in text:
            if char == ' ':
                if current_syllable:
                    syllables.append(current_syllable)
                    current_syllable = ""
            else:
                current_syllable += char
                # Simple heuristic: if we hit a consonant after vowels, start new syllable
                if (char in self.consonants and 
                    len(current_syllable) > 1 and 
                    any(c in self.vowels for c in current_syllable[:-1])):
                    syllables.append(current_syllable[:-1])
                    current_syllable = char
        
        if current_syllable:
            syllables.append(current_syllable)
        
        return syllables
    
    def syllable_to_phonemes(self, syllable: str) -> str:
        """Convert Thai syllable to phonemes"""
        phonemes = []
        i = 0
        
        while i < len(syllable):
            char = syllable[i]
            
            # Handle consonants
            if char in self.consonants:
                phonemes.append(self.consonants[char])
            
            # Handle vowels
            elif char in self.vowels:
                phonemes.append(self.vowels[char])
            
            # Handle tone marks
            elif char in self.tones:
                if phonemes:
                    phonemes[-1] += self.tones[char]
            
            # Handle special vowel combinations
            elif char == 'เ' and i + 1 < len(syllable):
                next_char = syllable[i + 1]
                if next_char in ['า', 'อ']:
                    phonemes.append('aw')
                    i += 1  # Skip next character
                else:
                    phonemes.append('e')
            
            i += 1
        
        return ' '.join(phonemes)
    
    def text_to_phonemes(self, text: str) -> str:
        """Convert Thai text to phonemes"""
        # Clean text
        text = self.clean_text(text)
        
        # Segment into syllables
        syllables = self.segment_syllables(text)
        
        # Convert each syllable to phonemes
        phoneme_syllables = []
        for syllable in syllables:
            phonemes = self.syllable_to_phonemes(syllable)
            if phonemes:
                phoneme_syllables.append(phonemes)
        
        return ' '.join(phoneme_syllables)
    
    def __call__(self, text: str) -> str:
        """Make the class callable"""
        return self.text_to_phonemes(text)

# Global instance
thai_phonemizer = ThaiPhonemizer()

def phonemize_thai(text: str) -> str:
    """Convenience function for Thai phonemization"""
    return thai_phonemizer(text)

if __name__ == "__main__":
    # Test the phonemizer
    test_texts = [
        "สวัสดี",
        "ขอบคุณ",
        "ยินดีที่ได้รู้จัก",
        "สวัสดีครับ ผมชื่อโจ"
    ]
    
    for text in test_texts:
        phonemes = phonemize_thai(text)
        print(f"Text: {text}")
        print(f"Phonemes: {phonemes}")
        print("---")