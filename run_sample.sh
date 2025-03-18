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
docker exec f5-tts-f5-tts-1 python /workspace/data/sample_tts.py

echo ""
echo "Process complete! Check the data/output directory for the generated audio file."
echo "You can also access the web interface at http://localhost:8000 to try more examples." 