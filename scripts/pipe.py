import pygame
from random import randint

class Pipe:
    def __init__(self):
        self.x = 350
        self.y = 0
        self.img = pygame.image.load("assets/imgs/pipe.png").convert()
        self.rect = self.img.get_rect()

    def render(self, surface):
        surface.blit(self.img, (self.x, self.y))

        self.update()

    def update(self):
        ...
        