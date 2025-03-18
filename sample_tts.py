#!/usr/bin/env python3
"""
Sample script to demonstrate F5-TTS usage.
This can be run inside the Docker container.
"""

import os
import subprocess

# Output directory
OUTPUT_DIR = "/workspace/data/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    print("Running F5-TTS text-to-speech synthesis...")
    
    # Text to synthesize
    text = "Hello! This is a demonstration of F5-TTS text-to-speech synthesis running in Docker on MacOS M3."
    output_file = os.path.join(OUTPUT_DIR, "sample_output.wav")
    
    # Run F5-TTS CLI command
    cmd = [
        "f5-tts_infer-cli",
        "--gen_text", text,
        "--output_file", output_file,
        "--model", "F5TTS_v1_Base"  # Use the default model
    ]
    
    print(f"Generating speech for: '{text}'")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Speech generated successfully! Output saved to: {output_file}")
        print("You can find this file in the './data/output' directory on your host machine.")
    else:
        print("Error generating speech:")
        print(result.stderr)

if __name__ == "__main__":
    main() 