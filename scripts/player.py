import pygame

class Player:
    def __init__(self):
        self.x = 200
        self.y = 325
        self.sprites = [pygame.image.load("assets/imgs/player-down.png"), pygame.image.load("assets/imgs/player-idle.png"), pygame.image.load("assets/imgs/player-up.png")]
        self.sprite_index = 0
        self.image = self.sprites[self.sprite_index]

    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))

        self.update()
    def update(self):
        self.image = self.sprites[int(self.sprite_index)]

        # lógica da animação do sprite
        self.sprite_index += 0.2
        
        if self.sprite_index >= 3:
            self.sprite_index = 0
        