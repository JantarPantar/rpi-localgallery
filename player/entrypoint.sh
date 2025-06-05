#!/bin/bash
export DISPLAY=:0
export SDL_VIDEODRIVER=x11
export SDL_AUDIODRIVER=dummy

echo "Waiting for X11 socket..."
while [ ! -e /tmp/.X11-unix/X0 ]; do
  sleep 0.5
done

echo "Starting player..."
exec python main.py
