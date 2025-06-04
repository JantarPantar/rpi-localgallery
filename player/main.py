import os
import time
import pygame
import cv2

MEDIA_FOLDER = "/media/usb"
IMAGE_DISPLAY_TIME = 5  # seconds

def get_files():
    supported_images = ('.jpg', '.jpeg', '.png', '.bmp')
    supported_videos = ('.mp4', '.mov', '.avi', '.mkv')
    files = [os.path.join(MEDIA_FOLDER, f) for f in os.listdir(MEDIA_FOLDER)]
    files.sort(key=lambda x: os.path.getctime(x), reverse=True)
    return [f for f in files if f.lower().endswith(supported_images + supported_videos)]

def display_image(screen, path):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, screen.get_size())
    for alpha in range(0, 255, 5):
        image.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(image, (0, 0))
        pygame.display.flip()
        time.sleep(0.01)
    time.sleep(IMAGE_DISPLAY_TIME)

def play_video(path):
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.resize(frame, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
        pygame.display.get_surface().blit(surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(1000 / cap.get(cv2.CAP_PROP_FPS)))
    cap.release()

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    while True:
        for path in get_files():
            if path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                display_image(screen, path)
            elif path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                play_video(path)

if __name__ == '__main__':
    main()
