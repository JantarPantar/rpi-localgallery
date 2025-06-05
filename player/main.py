import os
import time
import pygame
import cv2
import sys
import qrcode
import subprocess
from io import BytesIO

# Zkuste různé SDL ovladače
def setup_sdl_driver():
    # Pokus o různé ovladače v pořadí podle priority
    drivers = ["kmsdrm", "fbcon", "dummy"]
    
    for driver in drivers:
        try:
            os.environ["SDL_VIDEODRIVER"] = driver
            print(f"Zkouším SDL ovladač: {driver}")
            
            # Test inicializace
            pygame.init()
            pygame.display.set_mode((100, 100), pygame.NOFRAME)
            pygame.quit()
            
            print(f"Úspěšně nastaven ovladač: {driver}")
            return driver
        except Exception as e:
            print(f"Ovladač {driver} selhal: {e}")
            continue
    
    raise Exception("Žádný SDL ovladač nefunguje")

# Nastavení audio ovladače
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Pro kmsdrm ovladač
os.environ["KMSDRM_DEVICE"] = "/dev/dri/card0"

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


def get_display_resolution():
    """Získej rozlišení displeje různými způsoby"""
    try:
        # Pokus o získání rozlišení z DRM
        result = subprocess.run(['cat', '/sys/class/drm/card0-HDMI-A-1/modes'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            mode = result.stdout.strip().split('\n')[0]
            width, height = map(int, mode.split('x'))
            print(f"DRM rozlišení: {width}x{height}")
            return width, height
    except:
        pass
    
    try:
        # Pokus o framebuffer
        out = subprocess.check_output("fbset -s", shell=True).decode()
        for line in out.splitlines():
            if line.strip().startswith('mode'):
                res = line.strip().split('"')[1]
                width, height = map(int, res.split('x'))
                print(f"Framebuffer rozlišení: {width}x{height}")
                return width, height
    except:
        pass
    
    print("Použito výchozí rozlišení: 1920x1080")
    return 1920, 1080  # fallback


def get_files():
    supported_images = ('.jpg', '.jpeg', '.png', '.bmp')
    supported_videos = ('.mp4', '.mov', '.avi', '.mkv')
    try:
        if not os.path.exists(MEDIA_FOLDER):
            print(f"Složka {MEDIA_FOLDER} neexistuje")
            return []
            
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
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
        "Wi-Fi: bros.photo",
        "Otevri v prohlizeci:",
        "  http://bros.photo",
        "",
        "Pridej fotky kliknuti",
        "na + nebo je pretahni.",
        "",
        "Prezentace se",
        "sama aktualizuje."
    ]

    y = sidebar_width + 30
    for line in instructions:
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (screen_width - sidebar_width + 20, y))
        y += font.get_linesize() + 2


def draw_watermark(surface, logo_img):
    try:
        logo = pygame.transform.scale(logo_img, (100, 100))
        logo.set_alpha(128)
        surface.blit(logo, (10, 10))
    except Exception as e:
        print(f"Chyba při kreslení watermarku: {e}")


def display_image(screen, path, qr_img, logo_img, font):
    print(f"Zobrazuji obrázek: {path}")
    try:
        screen_width, screen_height = screen.get_size()
        sidebar_width = screen_width // 5
        main_width = screen_width - sidebar_width

        image = pygame.image.load(path)
        # Zachování poměru stran
        img_width, img_height = image.get_size()
        aspect_ratio = img_width / img_height
        
        if aspect_ratio > main_width / screen_height:
            new_width = main_width
            new_height = int(main_width / aspect_ratio)
        else:
            new_height = screen_height
            new_width = int(screen_height * aspect_ratio)
        
        image = pygame.transform.scale(image, (new_width, new_height))
        
        # Vycentrování obrázku
        x_offset = (main_width - new_width) // 2
        y_offset = (screen_height - new_height) // 2

        # Fade in efekt
        for alpha in range(0, 256, 25):
            handle_events()
            image.set_alpha(alpha)
            screen.fill((0, 0, 0))
            screen.blit(image, (x_offset, y_offset))
            draw_watermark(screen, logo_img)
            draw_sidebar(screen, qr_img, font)
            pygame.display.flip()
            pygame.time.wait(10)

        # Zobrazení na plný čas
        start_time = time.time()
        while time.time() - start_time < IMAGE_DISPLAY_TIME:
            handle_events()
            screen.fill((0, 0, 0))
            screen.blit(image, (x_offset, y_offset))
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
    try:
        # Nastavení SDL ovladače
        active_driver = setup_sdl_driver()
        print(f"Používám SDL ovladač: {active_driver}")
        
        pygame.init()
        pygame.display.set_caption("Galerie")

        width, height = get_display_resolution()
        
        # Pokus o fullscreen, pokud selže, použij windowed
        try:
            screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
            print(f"Fullscreen mode: {width}x{height}")
        except pygame.error as e:
            print(f"Fullscreen selhal: {e}, zkouším windowed")
            screen = pygame.display.set_mode((width, height))

        # Pokus o načtení fontu
        try:
            font = pygame.font.Font(None, 24)
        except:
            font = pygame.font.SysFont("Arial", 20)

        qr_img = generate_qr_code(QR_SSID)
        
        # Pokus o načtení loga
        try:
            logo_img = pygame.image.load(WATERMARK_PATH).convert_alpha()
        except Exception as e:
            print(f"Nelze načíst logo: {e}")
            # Vytvoření dummy loga
            logo_img = pygame.Surface((100, 100))
            logo_img.fill((255, 255, 255))

        print("Aplikace spuštěna, začínám prezentaci...")

        while True:
            files = get_files()
            if not files:
                print("Žádné soubory, čekám...")
                # Zobrazení prázdné obrazovky s pokyny
                screen.fill((0, 0, 0))
                draw_sidebar(screen, qr_img, font)
                text = font.render("Cekam na soubory...", True, (255, 255, 255))
                screen.blit(text, (50, height//2))
                pygame.display.flip()
                time.sleep(5)
                continue
                
            for path in files:
                if path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    display_image(screen, path, qr_img, logo_img, font)
                elif path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                    play_video(path, qr_img, logo_img, font)
                    
    except Exception as e:
        print(f"Kritická chyba: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()