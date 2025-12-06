FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    build-essential \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    torch==2.6.0 \
    torchaudio==2.6.0 \
    --index-url https://download.pytorch.org/whl/cu124

RUN pip install --no-cache-dir \
    "chatterbox-tts @ git+https://github.com/travisvn/chatterbox-multilingual.git@exp"

RUN pip install --no-cache-dir \
    runpod \
    requests \
    soundfile \
    huggingface_hub \
    safetensors

COPY handler.py /app/handler.py

# Create cache directories with proper permissions
RUN mkdir -p /tmp/numba_cache /tmp/librosa_cache && chmod -R 777 /tmp/numba_cache /tmp/librosa_cache

# Fix librosa caching issue - give write permission to site-packages
RUN chmod -R 777 /usr/local/lib/python3.11/site-packages/librosa/

ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/app/cache
ENV NUMBA_CACHE_DIR=/tmp/numba_cache
ENV MPLCONFIGDIR=/tmp/mpl

CMD ["python", "-u", "/app/handler.py"]
