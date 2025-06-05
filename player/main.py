import pygame
import sys

pygame.init()
pygame.display.set_mode((800, 480))  # nebo rozlišení fbset
pygame.display.set_caption("Framebuffer test")

screen = pygame.display.get_surface()
screen.fill((255, 0, 0))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()