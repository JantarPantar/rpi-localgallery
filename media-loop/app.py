# media-loop/app.py
import os, time, subprocess
import pygame
from glob import glob

USB_PATH = "/mnt/usb"

def get_media_files():
    exts = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.mp4', '*.mov', '*.avi', '*.mkv']
    files = []
    for ext in exts:
        files.extend(glob(os.path.join(USB_PATH, ext)))
    return sorted(files, key=os.path.getmtime)

def display_image(screen, path):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, screen.get_size())
    screen.blit(img, (0, 0))
    pygame.display.flip()
    time.sleep(5)

def play_video(path):
    subprocess.run(["ffplay", "-autoexit", "-fs", "-loglevel", "quiet", path])

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    while True:
        files = get_media_files()
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
                display_image(screen, f)
            else:
                play_video(f)

if __name__ == "__main__":
    main()
