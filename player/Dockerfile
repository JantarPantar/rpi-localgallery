FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    libsdl2-dev libsdl2-image-dev libavcodec-dev libavformat-dev libswscale-dev \
    libfreetype6-dev libjpeg-dev libpng-dev libx11-dev libgl1-mesa-glx ffmpeg \
    python3-opencv x11-xserver-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install pygame opencv-python

COPY main.py /app/main.py
COPY entrypoint.sh /app/entrypoint.sh
WORKDIR /app

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]