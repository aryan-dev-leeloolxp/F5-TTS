#!/bin/bash

# Build and start the F5-TTS container
echo "Building and starting F5-TTS container..."
docker-compose up -d

echo "Container started! The web interface should be available at:"
echo "http://localhost:8000"

# Optional: Show logs
echo ""
echo "To view logs, run: docker-compose logs -f"
echo "To stop the container, run: docker-compose down" 