#!/bin/bash
# build-and-run.sh - spustí Docker kontejner s galerií na RPi

set -e

# Cesta k USB disku
USB_MOUNT="/media/usb"
 
# Kontrola připojení USB disku
if [ ! -d "$USB_MOUNT" ]; then
  echo "❌ USB disk není připojen do $USB_MOUNT"
  echo "📌 Připoj USB flashku a ujisti se, že je připojená na $USB_MOUNT"
  exit 1
fi

# Build a spuštění
echo "🔨 Stavím a spouštím Docker kontejner..."
docker compose up --build -d

echo "✅ Aplikace běží na http://localhost nebo http://<IP-raspberry-pi>"
