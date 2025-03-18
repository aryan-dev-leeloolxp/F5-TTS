#!/bin/bash

# Make sure the container is running
if ! docker ps | grep -q f5-tts; then
  echo "F5-TTS container is not running. Starting it now..."
  ./start.sh
  sleep 5  # Give the container a moment to start
fi

# Create output directory
mkdir -p data/output

# Copy the sample script to the data directory so it's accessible from the container
cp sample_tts.py data/

# Run the sample script inside the container
echo "Running the sample TTS script inside the container..."
echo "This will generate two outputs:"
echo "1. Simple text sample"
echo "2. Complex multilingual text with mathematical notation"
echo ""
echo "Note: The complex text may take longer to process due to higher quality settings."

docker exec f5-tts-f5-tts-1 python /workspace/data/sample_tts.py

echo ""
echo "Process complete! Check the data/output directory for the generated audio files:"
echo "- simple_output.wav - Basic text sample"
echo "- complex_output.wav - Complex multilingual text with mathematical notation"
echo ""
echo "You can also access the web interface at http://localhost:8000 to try more examples." 