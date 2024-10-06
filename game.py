import pygame
import sys
from player import Player

pygame.init()
pygame.display.set_caption("FlappyBird") # titulo

# configurações gerais
SCREEN_W, SCREEN_H = 244, 512
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
FPS = 60
clock = pygame.time.Clock()

# loop principal do jogo
while True:
    screen.fill("black")
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()