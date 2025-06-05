#!/bin/bash

# Kontrola dostupných zařízení
echo "=== Diagnostika SDL ==="
echo "Dostupné video ovladače:"
python3 -c "import pygame; pygame.init(); print(pygame.display.get_driver())" 2>/dev/null || echo "Pygame inicializace selhala"

echo "Framebuffer zařízení:"
ls -la /dev/fb* 2>/dev/null || echo "Žádné framebuffer zařízení"

echo "DRM zařízení:"
ls -la /dev/dri/* 2>/dev/null || echo "Žádné DRM zařízení"

echo "Aktuální TTY:"
tty

# Nastavení oprávnění
echo "Nastavuji oprávnění..."
sudo chmod 666 /dev/fb0 2>/dev/null || echo "Nelze nastavit oprávnění pro /dev/fb0"
sudo chmod 666 /dev/dri/card0 2>/dev/null || echo "Nelze nastavit oprávnění pro /dev/dri/card0"

# Export proměnných prostředí
export SDL_AUDIODRIVER=dummy
export SDL_NOMOUSE=1

# Pokus o různé konfigurace
echo "=== Spouštím aplikaci ==="

# Nejprve zkusíme kmsdrm
export SDL_VIDEODRIVER=kmsdrm
export KMSDRM_DEVICE=/dev/dri/card0
echo "Zkouším SDL_VIDEODRIVER=kmsdrm..."
timeout 10s python3 main.py && exit 0

# Pak framebuffer
export SDL_VIDEODRIVER=fbcon  
export SDL_FBDEV=/dev/fb0
echo "Zkouším SDL_VIDEODRIVER=fbcon..."
timeout 10s python3 main.py && exit 0

# Nakonec dummy
export SDL_VIDEODRIVER=dummy
echo "Zkouším SDL_VIDEODRIVER=dummy..."
python3 main.py