#!/bin/bash
set -e

echo "Zkouším SDL ovladače..."

for drv in kmsdrm fbcon; do
    echo "Zkouším ovladač: $drv"
    export SDL_VIDEODRIVER=$drv
    export SDL_FBDEV=/dev/fb0
    if python3 main.py; then
        echo "✅ Ovladač $drv úspěšně funguje."
        exit 0
    else
        echo "❌ Ovladač $drv selhal."
    fi
done

echo "❗ Fallback na dummy ovladač."
export SDL_VIDEODRIVER=dummy
python3 main.py
