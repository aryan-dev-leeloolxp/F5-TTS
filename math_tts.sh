#!/bin/bash
# Simple wrapper for math_formula_tts.py
# This script provides an easy way to convert mathematical formulas to speech

# Make sure the script is executable
chmod +x math_formula_tts.py
chmod +x setup_f5tts_env.sh
chmod +x download_models.sh

# Check if there are arguments
if [ $# -eq 0 ]; then
  echo "Usage:"
  echo "  ./math_tts.sh \"Your text with math formulas like E = mc²\""
  echo "  ./math_tts.sh -i input.txt -o output.wav"
  echo "  ./math_tts.sh --text-only \"Your text with math formulas\" # Only converts math to text, no TTS"
  echo "  ./math_tts.sh --help (for all options)"
  exit 1
fi

# Check if conda is available
if ! command -v conda &> /dev/null; then
  echo "Error: conda is not installed or not in PATH."
  echo "Please install Miniconda or Anaconda first."
  exit 1
fi

# Check if text-only mode is requested
TEXT_ONLY=false
for arg in "$@"; do
  if [ "$arg" == "--text-only" ]; then
    TEXT_ONLY=true
    break
  fi
done

# If not in text-only mode, ensure everything is set up
if [ "$TEXT_ONLY" == "false" ]; then
  # Check if f5tts_env exists
  if ! conda info --envs | grep -q "f5tts_env"; then
    echo "F5-TTS environment not found. Setting it up now..."
    ./setup_f5tts_env.sh
    if [ $? -ne 0 ]; then
      echo "❌ Failed to set up F5-TTS environment."
      echo "Switching to text-only mode."
      TEXT_ONLY_ARGS="--text-only"
    fi
  fi

  # Check if model files are downloaded (only if we're in full TTS mode)
  if [ "$TEXT_ONLY" == "false" ] && [ -z "$TEXT_ONLY_ARGS" ]; then
    echo "Checking F5-TTS model files..."
    ./download_models.sh
    if [ $? -ne 0 ]; then
      echo "❌ Issues with F5-TTS model files."
      echo "Switching to text-only mode."
      TEXT_ONLY_ARGS="--text-only"
    fi
  fi
fi

# Always run the command through conda to ensure we use the right environment
# Add text-only flag if needed
if [ -n "$TEXT_ONLY_ARGS" ]; then
  ARGS=("$TEXT_ONLY_ARGS" "$@")
else
  ARGS=("$@")
fi

echo "Running with f5tts_env conda environment..."
conda run -n f5tts_env python math_formula_tts.py "${ARGS[@]}"
exit_code=$?

# Check exit status
if [ $exit_code -eq 0 ]; then
  echo "✅ Math formula conversion completed successfully!"
else
  echo "❌ Math formula conversion failed with exit code $exit_code."
  echo ""
  echo "If you're having issues with the TTS part, try:"
  echo "  1. Using the --text-only option: ./math_tts.sh --text-only \"Your text with math formulas\""
  echo "  2. Check model files by running: ./download_models.sh"
fi 