# 🐶 Bark Modell Cheatsheet

## 1. Grundlegende Initialisierung
```python
import os
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import numpy as np

# GPU-RAM Optimierungen
os.environ["SUNO_OFFLOAD_CPU"] = "True"     # CPU Offloading aktivieren
os.environ["SUNO_USE_SMALL_MODELS"] = "True" # Kleine Modelle verwenden

# Modelle laden
preload_models()
```

## 2. Einfache Audiogenerierung
```python
# Basis Audio Generation
text = "Hallo, das ist ein Test."
audio_array = generate_audio(text)
write_wav("output.wav", SAMPLE_RATE, audio_array)

# Mit spezifischer Stimme
audio_array = generate_audio(text, history_prompt="v2/de_speaker_0")

# Mit Sprachauswahl
audio_array = generate_audio(text, language="de")
```

## 3. Spezialeffekte und Notation
```python
# Lachen und Geräusche
text_with_effects = """
[laughter] Das ist lustig! [laughs]
[sighs] Okay, weiter geht's...
[gasps] Das ist überraschend!
[clears throat] Nun zum nächsten Punkt.
"""

# Musik und Gesang
music_text = "♪ In der Nacht, wenn alles schläft ♪"

# Betonungen und Pausen
emphasis_text = """
Das ist SEHR wichtig!
Lass uns nachdenken... und weitermachen.
Ein Moment der Stille—dann geht es weiter.
"""

# Geschlechts-Bias
male_text = "[MAN] Dies ist eine männliche Stimme."
female_text = "[WOMAN] Dies ist eine weibliche Stimme."
```

## 4. Langform-Generierung
```python
import nltk
nltk.download('punkt')

def generate_long_form(text, voice_preset="v2/de_speaker_0"):
    sentences = nltk.sent_tokenize(text)
    silence = np.zeros(int(0.25 * SAMPLE_RATE))
    pieces = []
    
    for sentence in sentences:
        audio_array = generate_audio(sentence, history_prompt=voice_preset)
        pieces += [audio_array, silence.copy()]
    
    return np.concatenate(pieces)
```

## 5. Verfügbare Sprachen
```python
SUPPORTED_LANGUAGES = {
    "Englisch": "en",
    "Deutsch": "de",
    "Spanisch": "es",
    "Französisch": "fr",
    "Hindi": "hi",
    "Italienisch": "it",
    "Japanisch": "ja",
    "Koreanisch": "ko",
    "Polnisch": "pl",
    "Portugiesisch": "pt",
    "Russisch": "ru",
    "Türkisch": "tr",
    "Chinesisch": "zh"
}
```

## 6. Streaming Generation
```python
def stream_generator(text, chunk_size=20, overlap_length=1024):
    wav_chunks = []
    is_end = False
    
    while not is_end:
        chunk = generate_audio(text[:chunk_size])
        wav_chunks.append(chunk)
        text = text[chunk_size:]
        is_end = len(text) == 0
        
    return wav_chunks
```

## 7. Memory Optimierung
```python
# Minimaler Speicherverbrauch (~2GB VRAM)
os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

# Mittlerer Speicherverbrauch (~8GB VRAM)
os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "False"

# Maximale Leistung (~12GB VRAM)
os.environ["SUNO_OFFLOAD_CPU"] = "False"
os.environ["SUNO_USE_SMALL_MODELS"] = "False"
```

## 8. Voice Preset Handling
```python
# Standard Stimmen-Format
VOICE_PRESET_FORMAT = "v2/{sprache}_speaker_{nummer}"

# Beispiele für Stimmen
VOICE_PRESETS = {
    "Deutsch": [
        "v2/de_speaker_0",
        "v2/de_speaker_1",
        "v2/de_speaker_2"
    ],
    "Englisch": [
        "v2/en_speaker_0",
        "v2/en_speaker_1",
        # ... bis en_speaker_9
    ]
}
```

## 9. Fortgeschrittene Parameter
```python
def advanced_generation(
    text,
    temperature=0.7,
    waveform_temp=0.7,
    min_eos_p=0.05,
    history_prompt=None,
    language=None
):
    semantic_tokens = generate_text_semantic(
        text,
        history_prompt=history_prompt,
        temp=temperature,
        min_eos_p=min_eos_p
    )
    
    audio_array = semantic_to_waveform(
        semantic_tokens,
        history_prompt=history_prompt,
        temp=waveform_temp
    )
    return audio_array
```

## 10. Performance Profiling
```python
PERFORMANCE_METRICS = {
    "GPU (Enterprise)": "Echtzeit-Generation",
    "GPU (Consumer)": "~1.5x Echtzeit",
    "CPU": "~10x Echtzeit",
    "Chunk Größe": "~13-14 Sekunden optimal",
    "RAM Nutzung": {
        "Minimum": "16GB empfohlen",
        "VRAM (Full)": "12GB",
        "VRAM (Small)": "8GB",
        "VRAM (Minimal)": "2GB mit CPU Offloading"
    }
}
```

## Spezielle Features & Tipps

### Nicht-verbale Sounds
- `[laughter]` - Lachen
- `[laughs]` - Kurzes Lachen
- `[sighs]` - Seufzen
- `[music]` - Musik
- `[gasps]` - Nach Luft schnappen
- `[clears throat]` - Räuspern

### Text Formatierung
- `—` oder `...` für Zögern/Pausen
- `♪` für Liedtexte
- GROSSBUCHSTABEN für Betonung
- `[MAN]` und `[WOMAN]` für Geschlechter-Bias

### Beste Praktiken
1. Text in 13-14 Sekunden Chunks aufteilen
2. Konsistente Stimme über history_prompt beibehalten
3. Temperatur für Kreativität/Stabilität anpassen
4. Pausen zwischen Sätzen für natürliche Sprache
5. GPU-Speicher durch Offloading optimieren

### Fehlerbehandlung
```python
try:
    audio = generate_audio(text)
except Exception as e:
    if "CUDA out of memory" in str(e):
        os.environ["SUNO_OFFLOAD_CPU"] = "True"
        audio = generate_audio(text)
    else:
        raise e
```
