import pygame
import sys
from scripts.player import Player
from scripts.pipe import Pipe

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("FlappyBird") # nome da tela

        # configurações gerais
        self.SCREEN_W, self.SCREEN_H = 400, 650
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.player = Player()

        self.background = pygame.image.load("assets/imgs/background.png").convert()
        # escalonando o background para se ajustar as dimensões da tela
        self.background = pygame.transform.scale(self.background, (self.SCREEN_W, self.SCREEN_H))

        self.test_pipe = Pipe()

    def run(self):
        # loop principal do jogo
        while True:
            self.draw_background()

            self.event_handling()

            self.player.render(self.screen)
            self.test_pipe.render(self.screen)

            pygame.display.update()
            self.clock.tick(self.FPS)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def event_handling(self):
        # tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

Game().run()