#!/bin/bash
# Script to convert math formulas to speech using Google TTS
# This is a faster alternative to the F5-TTS version

# Check arguments
if [ $# -lt 1 ]; then
  echo "Usage: ./math_google_tts.sh \"Your text with math formulas like E = mc²\""
  echo "       ./math_google_tts.sh -f example_math.txt"
  echo "Options:"
  echo "  -l, --language    Specify language code (default: en-US)"
  echo "  -v, --voice       Specify voice name (default: en-US-Neural2-F)"
  echo "  -s, --speed       Specify speech speed (default: 1.0)"
  echo "  -p, --pitch       Specify speech pitch (default: 0.0)"
  exit 1
fi

# Get the absolute path to the current directory
CURRENT_DIR="$(pwd)"

# Create output directory
mkdir -p "${CURRENT_DIR}/output"

# Default Google TTS settings
LANGUAGE="en-US"
VOICE="en-US-Neural2-F"
SPEED="1.0"
PITCH="0.0"

# Parse options
FILE_INPUT=false
FILE_PATH=""
TEXT_INPUT=""

# Process positional and flag arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -f|--file)
      FILE_INPUT=true
      FILE_PATH="$2"
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
  OUTPUT_FILE="${CURRENT_DIR}/output/$(basename "$FILE_PATH" .txt)_tts.mp3"
else
  # Input is direct text
  if [ -z "$TEXT_INPUT" ]; then
    echo "Error: No input text provided."
    exit 1
  fi
  
  INPUT_SOURCE="command line"
  echo "$TEXT_INPUT" > /tmp/math_input.txt
  INPUT_FILE="/tmp/math_input.txt"
  OUTPUT_FILE="${CURRENT_DIR}/output/math_tts_output.mp3"
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

# Step 2: Use Google TTS API
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
  echo "✅ Speech generated successfully! Output saved to: $OUTPUT_FILE"
else
  echo "❌ Error generating speech."
  echo "Make sure you have internet connection and the gtts package is installed."
fi

# Clean up temporary files
rm -f "$TEMP_SCRIPT" "$GTTS_SCRIPT" "/tmp/math_input.txt" 