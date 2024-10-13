import pygame

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sprites = [pygame.image.load("assets/imgs/player-down.png"), pygame.image.load("assets/imgs/player-idle.png"), pygame.image.load("assets/imgs/player-up.png")]
        self.image = self.sprites[0]

    def render(self, surface):
        surface.blit(self.image, (20, 20))

        self.update()
    def update(self):
        ...