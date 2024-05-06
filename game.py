import pygame
import pickle
from mainmenu import *
from mapgenerator import *
from directory import *
from overworld import *
from writing import *
from room import *
from dungeonmapgenerator import *
from playerdata import *

class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.inGame = False

        self.A, self.B, self.X, self.Y, self.L, self.R = False, False, False, False, False, False
        self.UP, self.DOWN, self.LEFT, self.RIGHT = False, False, False, False
        self.SELECT, self.START = False, False
        self.white, self.gray, self.darkgrey, self.black = (255,255,255), (150,150,150), (85,85,85), (0,0,0)
        self.tan, self.lightgreen, self.green = (232, 235, 96), (181, 247, 94), (90, 176, 72)
        self.brown, self.maroon, self.yellow = (173, 84, 0), (173, 0, 0), (255, 255, 0)
        self.red, self.blue, self.lightblue = (255,0,0), (0,0,255), (0,255,255)

        self.width, self.height = 640, 480
        self.screen = pygame.Surface((self.width, self.height))
        self.screen = pygame.display.set_mode((self.width,self.height))

        self.FPS = 30
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

        self.directory = Directory()
        
        self.mainmenu = MainMenu(self)
        self.WorldMap = Map()
        self.player = PlayerData(list(self.WorldMap.startingPos),self.directory,[])
        self.overworld = Overworld(self)
        self.roomDB = RoomDatabase()
        self.dungeonDB = DungeonDatabase()

        self.steps = 0
        self.stepsThreshold = 100
        self.difficulty = 1

        self.debug_manualEncounters = False

    def run(self):
        while self.inGame:
            self.buttonReset()
            self.eventHandler()
            self.overworld.display()
            self.screen.blit(self.screen, [0,0])
            pygame.display.update()
        self.WorldMap.saveRevealed()

    def write(self,size,x,y,text):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text, True, self.white)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface,text_rect)

    def buttonReset(self):
        self.A, self.B, self.X, self.Y = False, False, False, False
        self.L, self.R = False, False
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
                if event.key==pygame.K_q:
                    self.L = True
                if event.key==pygame.K_e:
                    self.R = True
                if event.key==pygame.K_n:
                    self.START = True
                if event.key==pygame.K_m:
                    self.SELECT = True

    def stir(self):
        self.steps += 1
        if self.steps > self.stepsThreshold:
            if self.difficulty < MAX_DIFFICULTY:
                self.difficulty += 1
            self.steps = 0

    def save(self):
        roomdb = open('databases/roomDatabase.db','wb')
        dungeondb = open('databases/dungeonDatabase.db','wb')
        playerdb = open('databases/playerDatabase.db','wb')
        pickle.dump(self.roomDB, roomdb)
        pickle.dump(self.dungeonDB, dungeondb)
        pickle.dump(self.player,playerdb)
        roomdb.close()
        dungeondb.close()
        playerdb.close()

    def load(self):
        roomdb = open('databases/roomDatabase.db','rb')
        dungeondb = open('databases/dungeonDatabase.db','rb')
        playerdb = open('databases/playerDatabase.db','rb')
        self.roomDB = pickle.load(roomdb)
        self.dungeonDB = pickle.load(dungeondb)
        self.player = pickle.load(playerdb)
        self.roomDB.printContents()
        self.dungeonDB.printContents()
        self.player.party.printContents()
        roomdb.close()
        dungeondb.close()
        playerdb.close()