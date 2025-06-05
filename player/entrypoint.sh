#!/bin/bash
export SDL_VIDEODRIVER=fbcon
export SDL_FBDEV=/dev/fb0
export SDL_AUDIODRIVER=dummy

echo "Starting player without X11..."
exec python main.py
