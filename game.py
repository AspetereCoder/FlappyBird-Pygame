import pygame
import sys
from scripts.player import Player
from scripts.pipe import Pipe
from random import randint

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
        self.font = pygame.font.Font("assets/fonts/Vaticanus-G3yVG.ttf", 52)

        # carregando imagens
        self.background = pygame.image.load("assets/imgs/background.png").convert()
        self.ground = pygame.image.load("assets/imgs/ground.png").convert()
        # escalonando o background e o chão para se ajustar as dimensões da tela
        self.background = pygame.transform.scale(self.background, (self.SCREEN_W, self.SCREEN_H))
        self.ground = pygame.transform.scale(self.ground, (self.SCREEN_W, 100))
        self.ground_position = 0

        # todos os pipes ficarão armazenados aqui
        self.pipes = []
        self.pipe_gap = 100 # distância do vão entre um pipe e outro
        self.pipe_dist = 125 # distância entre um pipe_group e outro

    def run(self):
        # gerando os pipes iniciais
        self.generate_pipes()


        # loop principal do jogo
        while True:
            self.draw_background()
            self.draw_pipes()

            self.handle_pipes()

            self.event_handling()

            self.player.render(self.screen)

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

        # desenhando score do player 
        text_to_render = self.font.render(str(self.player.score), True, "white")
        self.screen.blit(text_to_render, ((self.SCREEN_W / 2) - 10, 100))

        self.ground_position -= 3 # velocidade do scroll do ground

    def event_handling(self):
        # tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.velocity = -5
                    
    def generate_pipes(self, amount=5):
        # essa função só é chamada uma vez
        # ela gera os pipes iniciais, que por padrão são 6
        
        for i in range(amount):

            upper_pipe_x = self.SCREEN_W + (self.pipe_dist * i)
            upper_pipe_y = 0
            upper_pipe_height = randint(100, 300)

            lower_pipe_x = upper_pipe_x
            lower_pipe_y = upper_pipe_y + upper_pipe_height + self.pipe_gap
            lower_pipe_height = 550 - lower_pipe_y

            upper_pipe = Pipe(upper_pipe_x, upper_pipe_y, upper_pipe_height, flipped=True)
            lower_pipe = Pipe(lower_pipe_x, lower_pipe_y, lower_pipe_height)

            self.pipes.append([upper_pipe, lower_pipe])


    def draw_pipes(self):
        for pipe_group in self.pipes:
            upper_pipe = pipe_group[0]
            lower_pipe = pipe_group[1]

            upper_pipe.render(self.screen)
            lower_pipe.render(self.screen)
    
    def handle_pipes(self):
        for pipe_group in self.pipes:
            upper_pipe = pipe_group[0]
            lower_pipe = pipe_group[1]

            if (upper_pipe.x + upper_pipe.img.get_width() <= 0):
                # apagando os pipes 
                self.pipes.pop(0)
                # gerando outro
                self.generate_pipes(1)
    
            # essa rect serve para registrar o score do player
            collision_rect = pygame.rect.Rect(upper_pipe.x + (upper_pipe.img.get_width() / 2), upper_pipe.y + upper_pipe.height, 1, self.pipe_gap)
            
            # caso a rect do player e a rect acima colidam, significa que o player
            # passou no meio do cano, portanto é registrado um ponto a+ em seu score
            if (self.player.rect.colliderect(collision_rect) and (self.player.rect.x + self.player.img.get_width() / 2) == collision_rect.x):
                # efeito sonoro de pontuação
                score_sfx = pygame.mixer.Sound("assets/sfx/score_sfx.mp3")
                score_sfx.play()

                self.player.score += 1
                del collision_rect

Game().run()