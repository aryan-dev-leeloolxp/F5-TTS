#!/bin/bash

# Create directories
mkdir -p data/reference
mkdir -p data/output

# Download a sample reference audio
echo "Downloading sample reference audio..."
curl -L "https://github.com/pytorch/audio/raw/main/examples/audio_data/tutorial_assets/english.wav" -o data/reference/english.wav

# Create a script to run inside the Docker container
cat > data/run_demo.py << 'EOF'
#!/usr/bin/env python3
"""
Complete demonstration of F5-TTS with reference audio.
"""
import os
import subprocess

# Paths
REF_AUDIO = "/workspace/data/reference/english.wav"
REF_TEXT = "This is a reference audio sample for voice cloning."
OUTPUT_DIR = "/workspace/data/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    print("Running F5-TTS with reference audio for voice cloning...")
    
    # Text to synthesize with the cloned voice
    text = "Hello! I'm synthesizing this using F5-TTS with voice cloning. This is running on macOS M3 through Docker."
    output_file = os.path.join(OUTPUT_DIR, "voice_cloned_output.wav")
    
    # Run F5-TTS CLI command with reference audio
    cmd = [
        "f5-tts_infer-cli",
        "--ref_audio", REF_AUDIO,
        "--ref_text", REF_TEXT,
        "--gen_text", text,
        "--output_file", output_file,
        "--model", "F5TTS_v1_Base",
        "--target_rms", "0.2",
        "--nfe_step", "20"  # Lower for faster processing
    ]
    
    print(f"Reference audio: {REF_AUDIO}")
    print(f"Reference text: {REF_TEXT}")
    print(f"Generating speech for: '{text}'")
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode == 0:
        print(f"Success! Voice-cloned speech saved to: {output_file}")
        print("You can find this file in the './data/output' directory on your host machine.")
    else:
        print("Error generating speech:")
        print(process.stderr)

if __name__ == "__main__":
    main()
EOF

# Make the script executable
chmod +x data/run_demo.py

# Run the demo inside the container
echo "Running voice cloning demo inside the container..."
docker exec f5-tts-f5-tts-1 python /workspace/data/run_demo.py

echo ""
echo "Demo complete! Check the data/output directory for the generated audio file."
echo "You can also access the web interface at http://localhost:8000 to try more examples." 