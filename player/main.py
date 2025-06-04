import os
import time
import pygame
import cv2

MEDIA_FOLDER = "/media/usb"
IMAGE_DISPLAY_TIME = 5  # seconds

def get_files():
    supported_images = ('.jpg', '.jpeg', '.png', '.bmp')
    supported_videos = ('.mp4', '.mov', '.avi', '.mkv')
    try:
        files = [os.path.join(MEDIA_FOLDER, f) for f in os.listdir(MEDIA_FOLDER)]
        files = [f for f in files if f.lower().endswith(supported_images + supported_videos) and os.path.isfile(f)]
        files.sort(key=lambda x: os.path.getctime(x), reverse=True)
        return files
    except Exception as e:
        print(f"Error reading media folder: {e}")
        return []

def display_image(screen, path):
    print(f"Displaying image: {path}")
    try:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, screen.get_size())
        for alpha in range(0, 255, 15):
            image.set_alpha(alpha)
            screen.fill((0, 0, 0))
            screen.blit(image, (0, 0))
            pygame.display.flip()
            time.sleep(0.01)
        start_time = time.time()
        while time.time() - start_time < IMAGE_DISPLAY_TIME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.time.wait(100)
    except Exception as e:
        print(f"Failed to display image {path}: {e}")

def play_video(path):
    print(f"Playing video: {path}")
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"Cannot open video {path}")
        return
    screen = pygame.display.get_surface()
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 25  # fallback FPS
    delay = int(1000 / fps)

    while cap.isOpened():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()

        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (screen.get_width(), screen.get_height()))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(delay)
    cap.release()

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Media Player")

    while True:
        files = get_files()
        if not files:
            print("No media files found, waiting...")
            time.sleep(5)
            continue
        for path in files:
            if path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                display_image(screen, path)
            elif path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                play_video(path)

if __name__ == '__main__':
    main()
