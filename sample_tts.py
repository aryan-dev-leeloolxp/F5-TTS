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

def run_tts(text, output_filename, model="F5TTS_v1_Base", extra_args=None):
    """Run F5-TTS with the given text and save to the given output file."""
    output_file = os.path.join(OUTPUT_DIR, output_filename)
    
    # Base command
    cmd = [
        "f5-tts_infer-cli",
        "--gen_text", text,
        "--output_file", output_file,
        "--model", model
    ]
    
    # Add any extra arguments
    if extra_args:
        cmd.extend(extra_args)
    
    print(f"Generating speech for text to: {output_filename}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Speech generated successfully! Output saved to: {output_file}")
        return True
    else:
        print("Error generating speech:")
        print(result.stderr)
        return False

def main():
    print("Running F5-TTS text-to-speech synthesis...")
    
    # Example 1: Simple text
    simple_text = "{Whisper} Hello! This is a demonstration of F5-TTS text-to-speech synthesis running in Docker on MacOS M3."
    run_tts(simple_text, "simple_output.wav")
    
    # Example 2: Complex multilingual text with mathematical notation
    complex_text = """
Prof. María Gutiérrez-López¹ and Dr. 山田 健一 (Yamada Ken'ichi)² presented at IEEE's Q2 2024 conference — groundbreaking results!
Their paper "θ-Optimization Analysis in Music & Physics" examined:
    > The correlation between Bach's compositions and quantum states
    > demonstrates remarkable harmonic patterns in ℝ² space.
    > — Advanced Theory Quarterly, Vol. III
Core equations studied:
• H = -ℏ²/2m ∇² + V
• ∫(x²+2x+1)dx = x³/3 + x² + x + C
• F = ma = m(d²x/dt²)
Key findings (p≤0.05, χ² test):
1. Algorithm complexity: O(n²) → O(n log n)
2. Set theory: A ∩ B ⊆ C where ||x|| ≤ ε
3. Vector field: ∇ × B = -∂E/∂t
4. Statistics: μ = 3.5 ± 2σ
Bach's Toccata (BWV 565):
* Key: D♭ major, C₄ range
* Time: 6/8 at ♩=120
* Dynamics: pp → mf → ff (sfz)
* Articulation: staccato • → legato ‿
* Chords: Cmaj7 → F⁷
* Repeat at 𝄇 bar 23
Contributors:
- السيد أحمد (Mr. Ahmad)
- Σοφία (Sofia)
- 안녕하세요 (annyeonghaseyo)
Budget: €500 + £350 + ¥75,000
For details contact: Professor María at m.gutierrez@lab.edu
or Dr. Yamada at yamada@lab.jp
"""
    # Run with more NFE steps for better quality on complex text
    run_tts(complex_text, "complex_output.wav", extra_args=["--nfe_step", "32", "--cfg_strength", "2.5"])
    
    print("\nAll samples have been generated. You can find them in the './data/output' directory.")

if __name__ == "__main__":
    main() 