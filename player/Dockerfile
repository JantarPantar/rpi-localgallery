FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalace základních závislostí
RUN apt-get update && apt-get install -y \
    # SDL2 základní balíčky
    libsdl2-dev libsdl2-image-dev libsdl2-ttf-2.0-0 \
    # Video knihovny
    libavcodec-dev libavformat-dev libswscale-dev \
    # Grafické knihovny
    libfreetype6-dev libjpeg-dev libpng-dev \
    # DRM pro hardware akceleraci
    libdrm2 libdrm-dev \
    # Systémové nástroje
    ffmpeg \
    # Fonty
    fonts-dejavu-core \
    # Debug nástroje
    strace \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Pokus o instalaci volitelných balíčků
RUN apt-get update && apt-get install -y \
    libsdl2-mixer-2.0-0 \
    python3-opencv \
    fbset \
    fonts-liberation \
    2>/dev/null || true \
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