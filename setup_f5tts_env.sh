#!/bin/bash
# Setup script for F5-TTS environment
# This script creates a Python 3.11 conda environment and installs F5-TTS

echo "Setting up F5-TTS environment..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH."
    echo "Please install Miniconda or Anaconda first."
    exit 1
fi

# Check if f5tts_env already exists
if conda info --envs | grep -q "f5tts_env"; then
    echo "F5-TTS environment already exists."
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Exiting without changes."
        exit 0
    fi
    
    # Remove existing environment
    conda remove -n f5tts_env --all -y
    echo "Removed existing f5tts_env environment."
fi

# Create new environment with Python 3.11
echo "Creating new conda environment with Python 3.11..."
conda create -n f5tts_env python=3.11 -y

# Activate the environment
echo "Activating environment..."
eval "$(conda shell.bash hook)"
conda activate f5tts_env

# Install F5-TTS
echo "Installing F5-TTS and dependencies..."
pip install f5-tts

# Verify installation
echo "Verifying installation..."
if command -v f5-tts_infer-cli &> /dev/null; then
    echo "✅ F5-TTS installed successfully!"
    echo
    echo "To use F5-TTS, activate the environment with:"
    echo "  conda activate f5tts_env"
    echo
    echo "Then you can run the math formula conversion script:"
    echo "  ./math_tts.sh \"Your text with math formulas\""
else
    echo "❌ F5-TTS installation failed or command not found in PATH."
    echo "Please check for error messages above."
fi

# Deactivate environment
conda deactivate 