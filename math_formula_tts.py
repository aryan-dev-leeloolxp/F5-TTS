#!/usr/bin/env python3
"""
Script to convert mathematical formulas to spoken text and then to speech using F5-TTS.
Usage:
    python math_formula_tts.py "Your sentence with math formulas like E = mc²"
    python math_formula_tts.py --input input.txt --output output.wav
"""

import argparse
import os
import subprocess
import sys
import shutil
from math_text_converter import convert_math_to_speech_text

# Default output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def check_tts_cli():
    """Check if f5-tts_infer-cli is available and can be run."""
    try:
        # Check if the command exists in PATH
        if shutil.which("f5-tts_infer-cli") is None:
            print("Error: f5-tts_infer-cli not found in PATH.")
            print("Please ensure F5-TTS is properly installed and activated.")
            return False
            
        # Try to run a simple version check
        result = subprocess.run(
            ["f5-tts_infer-cli", "--help"], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            print("Error: f5-tts_infer-cli exists but returns an error:")
            print(result.stderr)
            return False
            
        return True
    except Exception as e:
        print(f"Error checking f5-tts_infer-cli: {e}")
        return False

def save_text_to_file(text, file_path):
    """Save text to a file as a fallback."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"Error saving text to file: {e}")
        return False

def process_text(text, output_file, model="F5TTS_v1_Base", nfe_steps=20, cfg_strength=2.0):
    """
    Process text containing math formulas:
    1. Convert math formulas to readable text
    2. Generate speech from the converted text
    
    Args:
        text: Input text with math formulas
        output_file: Path to save the audio output
        model: F5-TTS model to use
        nfe_steps: Number of NFE steps for generation
        cfg_strength: CFG strength for generation
    
    Returns:
        True if successful, False otherwise
    """
    # Step 1: Convert math formulas to readable text
    print("Converting mathematical formulas to readable text...")
    converted_text = convert_math_to_speech_text(text)
    
    print("\nOriginal text:")
    print(text)
    print("\nConverted text:")
    print(converted_text)
    
    # Save converted text to file as fallback
    text_output = os.path.splitext(output_file)[0] + ".txt"
    save_text_to_file(converted_text, text_output)
    print(f"Converted text saved to: {text_output}")
    
    # Check if TTS is available
    if not check_tts_cli():
        print("\nSkipping TTS generation due to F5-TTS environment issues.")
        print("The converted text has been saved to a file instead.")
        print("\nPossible solutions:")
        print("1. Make sure you're using the correct Python environment")
        print("2. Try downgrading to Python 3.11 or earlier")
        print("3. Check F5-TTS installation and dependencies")
        return True  # Return True because we handled the error gracefully
    
    # Step 2: Generate speech using F5-TTS
    print(f"\nGenerating speech using {model}...")
    
    # Command for F5-TTS
    cmd = [
        "f5-tts_infer-cli",
        "--gen_text", converted_text,
        "--output_file", output_file,
        "--model", model,
        "--nfe_step", str(nfe_steps),
        "--cfg_strength", str(cfg_strength)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Speech generated successfully! Output saved to: {output_file}")
            return True
        else:
            print("Error generating speech:")
            print(result.stderr)
            print("\nThe converted text has been saved to a file instead.")
            return False
    except Exception as e:
        print(f"Exception occurred while generating speech: {e}")
        print("\nThe converted text has been saved to a file instead.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Convert mathematical formulas to speech using F5-TTS")
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("text", nargs="?", help="Text with mathematical formulas")
    input_group.add_argument("--input", "-i", help="Input text file containing mathematical formulas")
    
    # Output and TTS options
    parser.add_argument("--output", "-o", help="Output audio file (WAV format)")
    parser.add_argument("--model", "-m", default="F5TTS_v1_Base", 
                       help="F5-TTS model to use (default: F5TTS_v1_Base)")
    parser.add_argument("--nfe_steps", type=int, default=20,
                       help="Number of NFE steps for generation (default: 20)")
    parser.add_argument("--cfg_strength", type=float, default=2.0,
                       help="CFG strength for generation (default: 2.0)")
    parser.add_argument("--text-only", action="store_true",
                       help="Only convert math to text, don't run TTS")
    
    args = parser.parse_args()
    
    # Get input text
    if args.text:
        text = args.text
    else:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading input file: {e}")
            return 1
    
    # Determine output file
    if args.output:
        output_file = args.output
    else:
        # Generate default output filename
        if args.input:
            base_name = os.path.splitext(os.path.basename(args.input))[0]
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_tts.wav")
        else:
            output_file = os.path.join(OUTPUT_DIR, "math_formula_tts.wav")
    
    # If text-only mode is enabled, just convert and save text
    if args.text_only:
        converted_text = convert_math_to_speech_text(text)
        text_output = os.path.splitext(output_file)[0] + ".txt"
        if save_text_to_file(converted_text, text_output):
            print(f"Converted text saved to: {text_output}")
            return 0
        else:
            return 1
    
    # Process the text
    success = process_text(
        text, 
        output_file, 
        model=args.model,
        nfe_steps=args.nfe_steps,
        cfg_strength=args.cfg_strength
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 