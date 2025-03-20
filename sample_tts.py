#!/usr/bin/env python3
"""
Sample script to demonstrate F5-TTS usage.
This can be run inside the Docker container.
"""

import os
import subprocess
from math_text_converter import convert_math_to_speech_text

# Output directory
OUTPUT_DIR = "/workspace/data/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_tts(text, output_filename, model="F5TTS_v1_Base", extra_args=None, convert_math=True):
    """Run F5-TTS with the given text and save to the given output file."""
    output_file = os.path.join(OUTPUT_DIR, output_filename)
    
    # Convert mathematical formulas to readable text if requested
    if convert_math:
        text = convert_math_to_speech_text(text)
        print("Math formulas converted to readable text")
    
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
    run_tts(simple_text, "simple_output.wav", convert_math=False)  # No math to convert here
    
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
    # Also convert math formulas to readable text
    run_tts(complex_text, "complex_output_with_math_conversion.wav", 
            extra_args=["--nfe_step", "32", "--cfg_strength", "2.5"],
            convert_math=True)
    
    # Generate the same text without math conversion for comparison
    run_tts(complex_text, "complex_output_without_math_conversion.wav", 
            extra_args=["--nfe_step", "32", "--cfg_strength", "2.5"],
            convert_math=False)
    
    # Example 3: Text with purely mathematical content for demonstration
    math_text = """
Here are some key equations in physics and mathematics:
1. Einstein's energy-mass equivalence: E = mc²
2. Newton's second law: F = ma
3. Pythagorean theorem: a² + b² = c²
4. Euler's identity: e^(iπ) + 1 = 0
5. Maxwell's equation: ∇ × B = μ₀J + μ₀ε₀∂E/∂t
6. Wave equation: ∂²u/∂t² = c²∇²u
7. Schrödinger equation: iℏ∂Ψ/∂t = ĤΨ
8. Fourier transform: F(ω) = ∫f(t)e^(-iωt)dt
"""
    # Run TTS on mathematical text with conversion
    run_tts(math_text, "math_equations_converted.wav", 
            extra_args=["--nfe_step", "32"], 
            convert_math=True)
    
    print("\nAll samples have been generated. You can find them in the './data/output' directory.")
    print("Files with '_with_math_conversion' in their names have mathematical formulas converted to readable text.")
    print("Files with '_without_math_conversion' contain the original mathematical notation.")

if __name__ == "__main__":
    main() 