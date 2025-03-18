FROM python:3.10-slim

USER root

ARG DEBIAN_FRONTEND=noninteractive

LABEL github_repo="https://github.com/SWivid/F5-TTS"

RUN set -x \
    && apt-get update \
    && apt-get -y install --no-install-recommends wget curl git build-essential \
    sox libsox-fmt-all libsox-fmt-mp3 libsndfile1-dev ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /workspace

# Install PyTorch (CPU version)
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install F5-TTS directly as a package
RUN pip install --no-cache-dir f5-tts

ENV SHELL=/bin/bash

WORKDIR /workspace

# Command to run the Gradio interface
CMD ["f5-tts_infer-gradio", "--host", "0.0.0.0", "--port", "8000"]
