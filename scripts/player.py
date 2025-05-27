import pygame

class Player:
    def __init__(self):
        self.x = 200
        self.y = 325
        self.sprites = [pygame.image.load("assets/imgs/player-down.png"), pygame.image.load("assets/imgs/player-idle.png"), pygame.image.load("assets/imgs/player-up.png")]
        self.sprite_index = 0
        self.img = self.sprites[self.sprite_index]
        self.score = 0
        self.velocity = 1
        self.rect = pygame.rect.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        self.is_alive = True

    def render(self, surface):
        surface.blit(self.img, (self.x, self.y))

        self.update()
    def update(self):
        self.img = self.sprites[int(self.sprite_index)]

        # lógica da animação do sprite
        self.sprite_index += 0.2
        
        if self.sprite_index >= 3:
            self.sprite_index = 0
        
        # sistema de gravidade
        self.y += self.velocity
        self.velocity += 0.2

        self.rect = pygame.rect.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())