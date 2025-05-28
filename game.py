import pygame
import sys
from scripts.player import Player
from scripts.pipe import Pipe
from random import randint

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("FlappyBird") # nome da tela
        pygame.display.set_icon(pygame.image.load("assets/imgs/game_icon.png")) # icone da tela

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
        self.ground_rect = pygame.rect.Rect(0, self.SCREEN_H - 100, self.ground.get_width(), self.ground.get_height())

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
            self.draw_score()

            self.handle_pipes()

            self.event_handling()

            self.check_player_collision()

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

        if self.player.is_alive: # o chão só se mexe se o player estiver vivo
            self.ground_position -= 3 # velocidade do scroll do ground

    def draw_score(self):
        # desenhando score do player 
        text_to_render = self.font.render(str(self.player.score), True, "white")
        self.screen.blit(text_to_render, ((self.SCREEN_W / 2) - 10, 100))

    def event_handling(self):
        # tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.is_alive:
                    self.player.velocity = -5
                    wing_flap_sfx = pygame.mixer.Sound("assets/sfx/wingflap_sfx.mp3")
                    wing_flap_sfx.play()
                    
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

            # caso o player esteja morto, os pipes não devem se mover
            if not self.player.is_alive:
                upper_pipe.speed = 0
                lower_pipe.speed = 0    

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

    def check_player_collision(self):
        # colisão com os pipes
        rect_lists = []
        for rect_team in self.pipes:
            rect_lists.append(rect_team[0].rect)
            rect_lists.append(rect_team[1].rect)

        if self.player.rect.collidelistall(rect_lists) and self.player.is_alive:
            # o sfx só toca uma vez e o estado do player fica como morto
            self.player.is_alive = False
            collision_sfx = pygame.mixer.Sound("assets/sfx/collision_sfx.mp3").play()
        # colisão com o chão
        elif self.player.rect.colliderect(self.ground_rect) and self.player.is_alive:
            self.player.is_alive = False
            collision_sfx = pygame.mixer.Sound("assets/sfx/collision_sfx.mp3").play()
    
Game().run()