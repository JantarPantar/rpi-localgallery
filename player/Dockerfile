FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev libsdl2-mixer-dev \
    libavcodec-dev libavformat-dev libswscale-dev \
    libfreetype6-dev libjpeg-dev libpng-dev libx11-dev libgl1-mesa-glx \
    libdrm-dev libgbm-dev fbset ffmpeg \
    && pip install pygame-ce opencv-python \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY main.py /app/main.py
WORKDIR /app

CMD ["python", "main.py"]
