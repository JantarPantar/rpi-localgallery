FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libsdl2-dev libsdl2-image-dev libsmpeg-dev libavcodec-dev \
    libavformat-dev libswscale-dev libfreetype6-dev libjpeg-dev \
    libpng-dev libx11-dev libgl1-mesa-glx libopencv-dev \
    && pip install pygame opencv-python

COPY main.py /app/main.py
WORKDIR /app

CMD ["python", "main.py"]
