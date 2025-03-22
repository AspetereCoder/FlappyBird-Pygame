import pygame
import sys
from scripts.player import Player
from scripts.pipe import Pipe

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("FlappyBird") # nome da tela

        # configurações gerais
        self.SCREEN_W, self.SCREEN_H = 600, 650
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.player = Player()

        # carregando imagens
        self.background = pygame.image.load("assets/imgs/background.png").convert()
        self.ground = pygame.image.load("assets/imgs/ground.png").convert()
        # escalonando o background e o chão para se ajustar as dimensões da tela
        self.background = pygame.transform.scale(self.background, (self.SCREEN_W, self.SCREEN_H))
        self.ground = pygame.transform.scale(self.ground, (self.SCREEN_W, 100))
        self.ground_position = 0

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
        # desenhando plano de fundo
        self.screen.blit(self.background, (0, 0))

        # desenhando chão
        self.screen.blit(self.ground, (self.ground_position, self.SCREEN_H - 100))
        self.screen.blit(self.ground, (self.ground_position + self.SCREEN_W, self.SCREEN_H - 100))

        # efeito de scroll
        if (self.ground_position < -self.SCREEN_W):
            self.ground_position = 0

        self.ground_position -= 3 # velocidade do scroll do ground

    def event_handling(self):
        # tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

Game().run()