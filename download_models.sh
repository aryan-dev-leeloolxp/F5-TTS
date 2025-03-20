#!/bin/bash
# Download F5-TTS models
# This script helps download the model files required for F5-TTS

echo "Checking for F5-TTS model files..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH."
    echo "Please install Miniconda or Anaconda first."
    exit 1
fi

# Check if f5tts_env exists
if ! conda info --envs | grep -q "f5tts_env"; then
    echo "F5-TTS environment not found."
    echo "Please run ./setup_f5tts_env.sh first to set up the environment."
    exit 1
fi

# Activate the environment
eval "$(conda shell.bash hook)"
conda activate f5tts_env

# Try to generate a very short test to see if model files are already downloaded
echo "Testing if model files are already downloaded..."
TEMP_FILE=$(mktemp)
timeout 60 f5-tts_infer-cli --model F5TTS_v1_Base --gen_text "Test." --output_file "$TEMP_FILE" 2>&1 | grep -q "Downloading"

if [ $? -eq 0 ]; then
    echo "F5-TTS is downloading the model files. This may take a while..."
    echo "Please wait for the download to complete."
    
    # Wait for up to 5 minutes for the download to complete
    timeout 300 f5-tts_infer-cli --model F5TTS_v1_Base --gen_text "Test." --output_file "$TEMP_FILE"
    
    if [ $? -ne 0 ]; then
        echo "❌ Model download timed out. You may need to manually run:"
        echo "   conda activate f5tts_env"
        echo "   f5-tts_infer-cli --model F5TTS_v1_Base --gen_text \"Test.\" --output_file test.wav"
        exit 1
    fi
    
    echo "✅ Model files downloaded successfully!"
else
    echo "Model files appear to be already downloaded or the download is not working."
    echo "If you're having issues, try running:"
    echo "   conda activate f5tts_env"
    echo "   f5-tts_infer-cli --model F5TTS_v1_Base --gen_text \"Test.\" --output_file test.wav"
fi

# Clean up
rm -f "$TEMP_FILE"
conda deactivate

echo "You can now use the math_tts.sh script to convert math formulas to speech." 