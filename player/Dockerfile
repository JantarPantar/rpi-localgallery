FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalace všech potřebných balíčků
RUN apt-get update && apt-get install -y \
    # SDL2 a závislosti
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 \
    # Video a audio
    libavcodec-dev libavformat-dev libswscale-dev \
    libfreetype6-dev libjpeg-dev libpng-dev \
    # Pro framebuffer a DRM
    libdrm2 libdrm-dev \
    # OpenCV
    python3-opencv \
    # Systémové nástroje
    ffmpeg fbset \
    # Fonty
    fonts-dejavu-core fonts-liberation \
    # Debug nástroje
    strace ltrace \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python balíčky
RUN pip install --no-cache-dir pygame opencv-python qrcode[pil]

# Kopírování souborů
COPY main.py /app/main.py
COPY entrypoint.sh /app/entrypoint.sh
COPY logo.png /app/logo.png

WORKDIR /app

# Oprávnění
RUN chmod +x entrypoint.sh

# Vytvoření uživatele pro bezpečnost (volitelné)
RUN useradd -m -s /bin/bash gallery
RUN chown -R gallery:gallery /app

# Spuštění
ENTRYPOINT ["./entrypoint.sh"]