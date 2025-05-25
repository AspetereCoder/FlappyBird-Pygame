import pygame
from random import randint

class Pipe:
    def __init__(self, x, y, height, flipped=False):
        self.x = x
        self.y = y
        self.img = pygame.image.load("assets/imgs/pipe.png").convert()
        self.flipped = flipped
        if flipped:
            # inverte a imagem verticalmente
            self.img = pygame.transform.flip(self.img, False, True)
        self.height = height
        self.img = pygame.transform.scale(self.img, (self.img.get_width(), self.height))
        self.rect = pygame.rect.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def render(self, surface):
        surface.blit(self.img, (self.x, self.y))

        self.update()

    def update(self):
        self.x -= 1
        
        # atualizando a rect
        self.rect = pygame.rect.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())