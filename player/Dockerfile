FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalace potřebných balíčků
RUN apt-get update && apt-get install -y \
    # SDL2 a jeho komponenty
    libsdl2-dev libsdl2-image-dev libsdl2-ttf-2.0-0 libsdl2-mixer-2.0-0 \
    # Video knihovny
    libavcodec-dev libavformat-dev libswscale-dev \
    # Grafika a písmo
    libfreetype6-dev libjpeg-dev libpng-dev fonts-dejavu-core fonts-liberation \
    # DRM / framebuffer
    libdrm2 libdrm-dev libts-0.0-0 fbset fbi \
    # Debug nástroje
    strace \
    # Ostatní
    ffmpeg python3-opencv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalace Python balíčků
RUN pip install --no-cache-dir pygame opencv-python qrcode[pil]

# Kopírování souborů
COPY main.py /app/main.py
COPY entrypoint.sh /app/entrypoint.sh
COPY logo.png /app/logo.png

WORKDIR /app

# Nastavení oprávnění
RUN chmod +x entrypoint.sh
RUN useradd -m -s /bin/bash gallery && chown -R gallery:gallery /app

# Přednastavení SDL (možno přepsat v entrypointu)
ENV SDL_VIDEODRIVER=fbcon
ENV SDL_FBDEV=/dev/fb0
ENV SDL_AUDIODRIVER=dummy

USER gallery

# Spouštíme aplikaci
ENTRYPOINT ["./entrypoint.sh"]
