#!/bin/bash
# Unified script to convert math formulas to speech using either F5-TTS or Google TTS
# This script provides flexibility between quality (F5-TTS) and speed (Google TTS)

# Get the absolute path to the current directory
CURRENT_DIR="$(pwd)"

# Default settings
TTS_ENGINE="google"  # Options: "f5" or "google"
LANGUAGE="en-US"
VOICE="en-US-Neural2-F"
SPEED="1.0"
PITCH="0.0"
NFE_STEPS="20"
CFG_STRENGTH="2.0"

# Display help
show_help() {
  echo "Usage: ./math_tts_unified.sh [OPTIONS] \"Your text with math formulas like E = mc²\""
  echo "       ./math_tts_unified.sh [OPTIONS] -f example_math.txt"
  echo ""
  echo "Options:"
  echo "  -e, --engine ENGINE    Specify TTS engine (default: google, options: f5, google)"
  echo "  -f, --file FILE        Use a file as input instead of command line text"
  echo "  -o, --output FILE      Specify output file path"
  echo "  -l, --language LANG    Specify language code for Google TTS (default: en-US)"
  echo "  -v, --voice VOICE      Specify voice name for Google TTS (default: en-US-Neural2-F)"
  echo "  -s, --speed SPEED      Specify speech speed (default: 1.0)"
  echo "  -p, --pitch PITCH      Specify speech pitch for Google TTS (default: 0.0)"
  echo "  -n, --nfe STEPS        Specify NFE steps for F5-TTS (default: 20)"
  echo "  -c, --cfg VALUE        Specify CFG strength for F5-TTS (default: 2.0)"
  echo "  -h, --help             Show this help message"
  echo ""
  echo "Examples:"
  echo "  ./math_tts_unified.sh \"E = mc²\"                    # Use Google TTS (default)"
  echo "  ./math_tts_unified.sh -e f5 \"E = mc²\"              # Use F5-TTS"
  echo "  ./math_tts_unified.sh -f example_math.txt           # Use file input with Google TTS"
  echo "  ./math_tts_unified.sh -e f5 -f example_math.txt     # Use file input with F5-TTS"
  exit 0
}

# Parse options
FILE_INPUT=false
FILE_PATH=""
TEXT_INPUT=""
OUTPUT_FILE=""

# Process positional and flag arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      show_help
      ;;
    -e|--engine)
      TTS_ENGINE="$2"
      if [[ ! "$TTS_ENGINE" =~ ^(f5|google)$ ]]; then
        echo "Error: Engine must be either 'f5' or 'google'"
        exit 1
      fi
      shift 2
      ;;
    -f|--file)
      FILE_INPUT=true
      FILE_PATH="$2"
      shift 2
      ;;
    -o|--output)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    -l|--language)
      LANGUAGE="$2"
      shift 2
      ;;
    -v|--voice)
      VOICE="$2"
      shift 2
      ;;
    -s|--speed)
      SPEED="$2"
      shift 2
      ;;
    -p|--pitch)
      PITCH="$2"
      shift 2
      ;;
    -n|--nfe)
      NFE_STEPS="$2"
      shift 2
      ;;
    -c|--cfg)
      CFG_STRENGTH="$2"
      shift 2
      ;;
    *)
      # If this is the first positional arg and FILE_PATH is empty, assume it's text input
      if [ "$FILE_INPUT" = false ]; then
        TEXT_INPUT="$1"
        shift
      else
        echo "Unknown option: $1"
        exit 1
      fi
      ;;
  esac
done

# Create output directory
mkdir -p "${CURRENT_DIR}/output"

# Handle file input or direct text
if [ "$FILE_INPUT" = true ]; then
  # Input is a file
  if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File '$FILE_PATH' not found."
    exit 1
  fi
  
  INPUT_SOURCE="file $FILE_PATH"
  cat "$FILE_PATH" > /tmp/math_input.txt
  INPUT_FILE="/tmp/math_input.txt"
  
  if [ -z "$OUTPUT_FILE" ]; then
    if [ "$TTS_ENGINE" = "google" ]; then
      OUTPUT_FILE="${CURRENT_DIR}/output/$(basename "$FILE_PATH" .txt)_tts.mp3"
    else
      OUTPUT_FILE="${CURRENT_DIR}/output/$(basename "$FILE_PATH" .txt)_tts.wav"
    fi
  fi
else
  # Input is direct text
  if [ -z "$TEXT_INPUT" ]; then
    echo "Error: No input text provided."
    show_help
    exit 1
  fi
  
  INPUT_SOURCE="command line"
  echo "$TEXT_INPUT" > /tmp/math_input.txt
  INPUT_FILE="/tmp/math_input.txt"
  
  if [ -z "$OUTPUT_FILE" ]; then
    if [ "$TTS_ENGINE" = "google" ]; then
      OUTPUT_FILE="${CURRENT_DIR}/output/math_tts_output.mp3"
    else
      OUTPUT_FILE="${CURRENT_DIR}/output/math_tts_output.wav"
    fi
  fi
fi

# Step 1: Convert math to readable text using math_text_converter.py
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

# Step 2: Generate speech using the selected TTS engine
if [ "$TTS_ENGINE" = "google" ]; then
  # Use Google TTS API
  echo "Generating speech using Google TTS..."
  echo "Output will be saved to: $OUTPUT_FILE"
  
  # Create a temporary Python script that uses Google Text-to-Speech
  GTTS_SCRIPT=$(mktemp)
  cat > "$GTTS_SCRIPT" << EOL
from gtts import gTTS
import sys

text = """${CONVERTED_TEXT}"""
language = '${LANGUAGE}'

try:
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save('${OUTPUT_FILE}')
    print("✅ Speech generated successfully!")
except Exception as e:
    print(f"❌ Error generating speech: {e}")
    sys.exit(1)
EOL

  # Check if gtts is installed, if not install it
  if ! pip list | grep -q gtts; then
      echo "Installing Google Text-to-Speech (gtts) library..."
      pip install gtts
  fi

  # Run the Google TTS script
  python "$GTTS_SCRIPT"
  TTS_STATUS=$?

  if [ $TTS_STATUS -eq 0 ]; then
    echo "✅ Speech generated successfully using Google TTS! Output saved to: $OUTPUT_FILE"
  else
    echo "❌ Error generating speech with Google TTS."
    echo "Make sure you have internet connection and the gtts package is installed."
  fi
  
  # Clean up Google TTS script
  rm -f "$GTTS_SCRIPT"
  
else
  # Use F5-TTS
  echo "Generating speech using F5-TTS..."
  echo "Output will be saved to: $OUTPUT_FILE"
  
  # Check if conda is available
  if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH. Required for F5-TTS."
    exit 1
  fi

  # Make sure f5tts_env exists
  if ! conda info --envs | grep -q "f5tts_env"; then
    echo "Error: f5tts_env not found. Please run ./setup_f5tts_env.sh first."
    exit 1
  fi
  
  # Activate conda environment
  eval "$(conda shell.bash hook)"
  conda activate f5tts_env
  
  # Run F5-TTS
  f5-tts_infer-cli --model F5TTS_v1_Base --gen_text "$CONVERTED_TEXT" --output_file "$OUTPUT_FILE" --nfe_step "$NFE_STEPS" --cfg_strength "$CFG_STRENGTH"
  TTS_STATUS=$?
  
  if [ $TTS_STATUS -eq 0 ]; then
    echo "✅ Speech generated successfully using F5-TTS! Output saved to: $OUTPUT_FILE"
  else
    echo "❌ Error generating speech with F5-TTS."
    echo "Make sure you have sufficient disk space and permissions to write to the output directory."
  fi
  
  # Deactivate environment
  conda deactivate
fi

# Clean up temporary files
rm -f "$TEMP_SCRIPT" "/tmp/math_input.txt"

echo "Done!" 