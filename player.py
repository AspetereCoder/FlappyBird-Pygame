import pygame

class Player:
    def __init__(self, x_pos, y_pos):
        self.x = 0
        self.y = 0
        self.sprites = None
    
    def show(self, surface):
        pygame.draw.rect(surface, "green", (self.x, self.y, 40, 40))

    def update(self):
        ...