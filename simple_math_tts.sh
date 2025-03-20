#!/bin/bash
# Simple script to convert math formulas to speech using F5-TTS
# This is a more direct approach with fewer layers

# Check if conda is available
if ! command -v conda &> /dev/null; then
  echo "Error: conda is not installed or not in PATH."
  exit 1
fi

# Make sure f5tts_env exists
if ! conda info --envs | grep -q "f5tts_env"; then
  echo "Error: f5tts_env not found. Please run ./setup_f5tts_env.sh first."
  exit 1
fi

# Check arguments
if [ $# -lt 1 ]; then
  echo "Usage: ./simple_math_tts.sh \"Your text with math formulas like E = mc²\""
  echo "       ./simple_math_tts.sh -f example_math.txt"
  exit 1
fi

# Get the absolute path to the current directory
CURRENT_DIR="$(pwd)"

# Create output directory
mkdir -p "${CURRENT_DIR}/output"

# Handle file input or direct text
if [ "$1" = "-f" ] && [ -n "$2" ]; then
  # Input is a file
  if [ ! -f "$2" ]; then
    echo "Error: File '$2' not found."
    exit 1
  fi
  
  INPUT_SOURCE="file $2"
  cat "$2" > /tmp/math_input.txt
  INPUT_FILE="/tmp/math_input.txt"
  OUTPUT_FILE="${CURRENT_DIR}/output/$(basename "$2" .txt)_tts.wav"
else
  # Input is direct text
  INPUT_SOURCE="command line"
  echo "$1" > /tmp/math_input.txt
  INPUT_FILE="/tmp/math_input.txt"
  OUTPUT_FILE="${CURRENT_DIR}/output/math_tts_output.wav"
fi

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate f5tts_env

# Step 1: Convert math to readable text using math_text_converter.py directly
echo "Converting math formulas from $INPUT_SOURCE to readable text..."

# Create a temporary Python script that uses the full path to math_text_converter.py
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << EOL
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, '${CURRENT_DIR}')

# Now we can import from math_text_converter.py
from math_text_converter import convert_math_to_speech_text

with open('${INPUT_FILE}', 'r', encoding='utf-8') as f:
    text = f.read().strip()
    
converted = convert_math_to_speech_text(text)
print(converted)
EOL

# Run the conversion script
CONVERTED_TEXT=$(python "$TEMP_SCRIPT")

# Read original text
ORIGINAL_TEXT=$(cat "$INPUT_FILE")
echo "Original text from $INPUT_SOURCE:"
echo "$ORIGINAL_TEXT"
echo ""
echo "Converted text:"
echo "$CONVERTED_TEXT"

# Save to file for reference
echo "$CONVERTED_TEXT" > "${CURRENT_DIR}/output/math_tts_converted.txt"
echo "Converted text saved to: ${CURRENT_DIR}/output/math_tts_converted.txt"

# Step 2: Run F5-TTS directly
echo "Generating speech using F5-TTS..."
echo "Output will be saved to: $OUTPUT_FILE"
f5-tts_infer-cli --model F5TTS_v1_Base --gen_text "$CONVERTED_TEXT" --output_file "$OUTPUT_FILE" --nfe_step 20 --cfg_strength 2.0

if [ $? -eq 0 ]; then
  echo "✅ Speech generated successfully! Output saved to: $OUTPUT_FILE"
else
  echo "❌ Error generating speech."
  echo "Make sure you have sufficient disk space and permissions to write to the output directory."
fi

# Clean up temporary files
rm -f "$TEMP_SCRIPT" "/tmp/math_input.txt"

# Deactivate environment
conda deactivate 