import pygame
from mainmenu import *
from mapgenerator import *
from directory import *
from overworld import *

class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.inGame = False

        self.A, self.B, self.X, self.Y = False, False, False, False
        self.UP, self.DOWN, self.LEFT, self.RIGHT = False, False, False, False
        self.SELECT, self.START = False, False
        self.white, self.black = (255,255,255), (0,0,0)
        self.red, self.blue = (255,0,0), (0,0,255)

        self.width, self.height = 640, 480
        self.screen = pygame.Surface((self.width, self.height))
        self.screen = pygame.display.set_mode((self.width,self.height))

        self.FPS = 30
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

        self.directory = Directory()
        
        self.mainmenu = MainMenu(self)
        self.WorldMap = Map()
        self.overworld = Overworld(self)

    def run(self):
        while self.inGame:
            self.buttonReset()
            self.eventHandler()
            self.overworld.display()
            self.screen.blit(self.screen, [0,0])
            pygame.display.update()

    def write(self,size,x,y,text):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text, True, self.white)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface,text_rect)

    def buttonReset(self):
        self.A, self.B, self.X, self.Y = False, False, False, False
        self.UP, self.DOWN, self.LEFT, self.RIGHT = False, False, False, False
        self.SELECT, self.START = False, False

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running, self.inGame = False, False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w:
                    self.UP = True
                if event.key==pygame.K_d:
                    self.RIGHT = True
                if event.key==pygame.K_s:
                    self.DOWN = True
                if event.key==pygame.K_a:
                    self.LEFT = True
                if event.key==pygame.K_j:
                    self.A = True
                if event.key==pygame.K_k:
                    self.B = True
                if event.key==pygame.K_l:
                    self.X = True
                if event.key==pygame.K_SEMICOLON:
                    self.Y = True
                if event.key==pygame.K_n:
                    self.START = True
                if event.key==pygame.K_m:
                    self.SELECT = True
