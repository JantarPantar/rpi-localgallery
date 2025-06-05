import os
import time
import pygame
import cv2
import sys
import qrcode
import subprocess
from io import BytesIO

# Použít nastavení z proměnných prostředí nebo výchozí hodnoty pro CLI režim
os.environ["SDL_VIDEODRIVER"] = os.environ.get("SDL_VIDEODRIVER", "fbcon")
os.environ["SDL_AUDIODRIVER"] = os.environ.get("SDL_AUDIODRIVER", "dummy")

MEDIA_FOLDER = "/media/usb"
IMAGE_DISPLAY_TIME = 5  # sekund
QR_SSID = "WIFI:T:nopass;S:bros.photo;"
WATERMARK_PATH = "/app/logo.png"


def generate_qr_code(url):
    qr = qrcode.QRCode(box_size=2, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return pygame.image.load(buffer, "qr.png")


def get_fb_resolution():
    try:
        out = subprocess.check_output("fbset -s", shell=True).decode()
        for line in out.splitlines():
            if line.strip().startswith('mode'):
                res = line.strip().split('"')[1]
                width, height = map(int, res.split('x'))
                print(f"Framebuffer resolution detected: {width}x{height}")
                return width, height
    except Exception as e:
        print(f"Nelze zjistit rozlišení framebufferu: {e}")
    return 1280, 720  # fallback


def get_files():
    supported_images = ('.jpg', '.jpeg', '.png', '.bmp')
    supported_videos = ('.mp4', '.mov', '.avi', '.mkv')
    try:
        files = [os.path.join(MEDIA_FOLDER, f) for f in os.listdir(MEDIA_FOLDER)]
        files = [f for f in files if f.lower().endswith(supported_images + supported_videos) and os.path.isfile(f)]
        files.sort(key=lambda x: os.path.getctime(x), reverse=True)
        return files
    except Exception as e:
        print(f"Chyba při načítání složky: {e}")
        return []


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()


def draw_sidebar(screen, qr_img, font):
    screen_width, screen_height = screen.get_size()
    sidebar_width = screen_width // 5
    sidebar_rect = pygame.Rect(screen_width - sidebar_width, 0, sidebar_width, screen_height)

    pygame.draw.rect(screen, (240, 240, 240), sidebar_rect)

    qr_resized = pygame.transform.scale(qr_img, (sidebar_width - 40, sidebar_width - 40))
    screen.blit(qr_resized, (screen_width - sidebar_width + 20, 20))

    instructions = [
        "📶 Wi-Fi: bros.photo",
        "🖥️ Otevři v prohlížeči:",
        "  http://bros.photo",
        "",
        "📤 Přidej fotky kliknutím",
        "na + nebo je přetáhni.",
        "",
        "📸 Prezentace se",
        "sama aktualizuje."
    ]

    y = sidebar_width + 30
    for line in instructions:
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (screen_width - sidebar_width + 20, y))
        y += font.get_linesize() + 2


def draw_watermark(surface, logo_img):
    logo = pygame.transform.scale(logo_img, (100, 100))
    logo.set_alpha(128)
    surface.blit(logo, (10, 10))


def display_image(screen, path, qr_img, logo_img, font):
    print(f"Zobrazuji obrázek: {path}")
    try:
        screen_width, screen_height = screen.get_size()
        sidebar_width = screen_width // 5
        main_width = screen_width - sidebar_width

        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (main_width, screen_height))

        for alpha in range(0, 256, 25):
            handle_events()
            image.set_alpha(alpha)
            screen.fill((0, 0, 0))
            screen.blit(image, (0, 0))
            draw_watermark(screen, logo_img)
            draw_sidebar(screen, qr_img, font)
            pygame.display.flip()
            pygame.time.wait(10)

        start_time = time.time()
        while time.time() - start_time < IMAGE_DISPLAY_TIME:
            handle_events()
            screen.fill((0, 0, 0))
            screen.blit(image, (0, 0))
            draw_watermark(screen, logo_img)
            draw_sidebar(screen, qr_img, font)
            pygame.display.flip()
            pygame.time.wait(100)
    except Exception as e:
        print(f"Chyba při zobrazení obrázku: {e}")


def play_video(path, qr_img, logo_img, font):
    print(f"Přehrávám video: {path}")
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"Nelze otevřít video {path}")
        return

    screen = pygame.display.get_surface()
    screen_width, screen_height = screen.get_size()
    sidebar_width = screen_width // 5
    main_width = screen_width - sidebar_width

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or fps > 120:
        fps = 25
    delay = int(1000 / fps)

    while cap.isOpened():
        handle_events()
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (main_width, screen_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        screen.fill((0, 0, 0))
        screen.blit(surface, (0, 0))
        draw_watermark(screen, logo_img)
        draw_sidebar(screen, qr_img, font)
        pygame.display.flip()
        pygame.time.delay(delay)
    cap.release()


def main():
    pygame.init()
    pygame.display.set_caption("Galerie")

    width, height = get_fb_resolution()
    try:
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    except pygame.error as e:
        print(f"Chyba při inicializaci display: {e}")
        sys.exit(1)

    font = pygame.font.SysFont("Arial", 20)

    qr_img = generate_qr_code(QR_SSID)
    logo_img = pygame.image.load(WATERMARK_PATH).convert_alpha()

    while True:
        files = get_files()
        if not files:
            print("Žádné soubory, čekám...")
            time.sleep(5)
            continue
        for path in files:
            if path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                display_image(screen, path, qr_img, logo_img, font)
            elif path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                play_video(path, qr_img, logo_img, font)


if __name__ == '__main__':
    main()
