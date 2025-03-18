# F5-TTS Examples

This document provides examples for using F5-TTS in the Docker container.

## Basic Text-to-Speech

Run the basic TTS example:

```bash
./run_sample.sh
```

This will:

1. Generate speech from simple text: `simple_output.wav`
2. Generate speech from complex multilingual text with mathematical notation: `complex_output.wav`

The complex text example includes:

- Multilingual text (Spanish, Japanese, Arabic, Greek, Korean)
- Mathematical notation (equations, symbols)
- Special characters (musical notation, phonetic symbols)
- Different formatting styles

## Voice Cloning Demo

Run the voice cloning demo:

```bash
./demo_tts.sh
```

This will:

1. Download a sample reference audio to `data/reference/`
2. Create a Python script in the data directory
3. Run voice cloning using the reference audio
4. Save the output to `data/output/voice_cloned_output.wav`

## Web Interface

The F5-TTS web interface is available at http://localhost:8000 and provides:

1. Text-to-speech generation
2. Voice cloning with reference audio
3. Multi-speaker synthesis
4. Real-time parameter adjustment

## Using the F5-TTS CLI

You can run F5-TTS commands directly in the container:

```bash
# Basic TTS
docker exec f5-tts-f5-tts-1 f5-tts_infer-cli --gen_text "Your text here" --output_file /workspace/data/output/output.wav

# Voice cloning
docker exec f5-tts-f5-tts-1 f5-tts_infer-cli \
  --ref_audio /workspace/data/reference/your_reference.wav \
  --ref_text "Transcript of the reference audio" \
  --gen_text "Text to synthesize with the cloned voice" \
  --output_file /workspace/data/output/cloned_voice.wav

# Complex text with enhanced quality settings
docker exec f5-tts-f5-tts-1 f5-tts_infer-cli \
  --gen_text "Complex multilingual text here" \
  --output_file /workspace/data/output/enhanced_output.wav \
  --nfe_step 32 \
  --cfg_strength 2.5
```

## CLI Parameters

Key parameters for the F5-TTS CLI:

- `--model` - Model to use (default: F5TTS_v1_Base)
- `--ref_audio` - Reference audio file for voice cloning
- `--ref_text` - Transcript of the reference audio
- `--gen_text` - Text to synthesize
- `--output_file` - Output WAV file
- `--target_rms` - Audio loudness (default: 0.1)
- `--nfe_step` - Denoising steps (default: 32, lower for faster processing)
- `--speed` - Playback speed (default: 1.0)
- `--cfg_strength` - Classifier-free guidance strength (default: 2.0)

For a complete list of options, run:

```bash
docker exec f5-tts-f5-tts-1 f5-tts_infer-cli --help
```

## Text Formatting Tips

F5-TTS supports various formatting features:

### Speech Styles

- `{Whisper}` - Whispered speech
- `{Excited}` - Excited, energetic speech
- `{Sad}` - Sad, melancholic speech

### Special Handling for Complex Text

- Mathematical symbols and equations are usually read aloud
- For multilingual text, make sure your text is properly UTF-8 encoded
- Special characters like musical notation may be handled differently depending on the model
