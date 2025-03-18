# F5-TTS Docker Setup for macOS M3

This is a simplified Docker configuration for running F5-TTS on macOS M3 with ARM architecture (Apple Silicon).

## Quick Start

1. Make sure Docker Desktop is installed and running

2. Run the start script:
   ```bash
   ./start.sh
   ```
3. Open the web interface at:
   ```
   http://localhost:8000
   ```

## Manual Start

If you prefer to run commands manually:

```bash
# Build and start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

## Data Directory

The `./data` directory is mounted to `/workspace/data` in the container for persistent storage.

## Notes

- This setup uses a CPU-based PyTorch image since Docker doesn't currently support Metal Performance Shaders (MPS) for GPU acceleration on Mac.
- F5-TTS is installed directly from PyPI for simplicity.
- For more information on F5-TTS usage, see the [official documentation](https://github.com/SWivid/F5-TTS).
