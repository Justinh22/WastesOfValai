import pygame
import pickle
from mainmenu import *
from mapgenerator import *
from directory import *
from overworld import *
from writing import *
from room import *
from dungeonmapgenerator import *
from villagemapgenerator import *
from playerdata import *

class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.inGame = False

        self.keys = {"A": False, "B": False, "X": False, "Y": False, "L": False, "R": False,
                     "UP": False, "DOWN": False, "LEFT": False, "RIGHT": False, "SELECT": False, "START": False}
        self.heldKeys = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False}
        self.keydownDelay = KEYDOWN_START_DELAY
        self.white, self.gray, self.darkgrey, self.black = (255,255,255), (150,150,150), (85,85,85), (0,0,0)
        self.tan, self.lightgreen, self.green, self.orange = (232, 235, 96), (181, 247, 94), (90, 176, 72), (179,114,2)
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
        self.villageDB = VillageDatabase()

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

    def write(self,size,x,y,text):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text, True, self.white)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface,text_rect)

    def buttonReset(self):
        self.keys["A"], self.keys["B"], self.keys["X"], self.keys["Y"] = False, False, False, False
        self.keys["L"], self.keys["R"] = False, False
        self.keys["UP"], self.keys["DOWN"], self.keys["LEFT"], self.keys["RIGHT"] = False, False, False, False
        self.keys["SELECT"], self.keys["START"] = False, False

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running, self.inGame = False, False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w:
                    self.setKey("UP",True)
                if event.key==pygame.K_d:
                    self.setKey("RIGHT",True)
                if event.key==pygame.K_s:
                    self.setKey("DOWN",True)
                if event.key==pygame.K_a:
                    self.setKey("LEFT",True)
                if event.key==pygame.K_j:
                    self.setKey("A",True)
                if event.key==pygame.K_k:
                    self.setKey("B",True)
                if event.key==pygame.K_l:
                    self.setKey("X",True)
                if event.key==pygame.K_SEMICOLON:
                    self.setKey("Y",True)
                if event.key==pygame.K_q:
                    self.setKey("L",True)
                if event.key==pygame.K_e:
                    self.setKey("R",True)
                if event.key==pygame.K_n:
                    self.setKey("START",True)
                if event.key==pygame.K_m:
                    self.setKey("SELECT",True)
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_w:
                    self.setKey("UP",False)
                if event.key==pygame.K_d:
                    self.setKey("RIGHT",False)
                if event.key==pygame.K_s:
                    self.setKey("DOWN",False)
                if event.key==pygame.K_a:
                    self.setKey("LEFT",False)
                if event.key==pygame.K_j:
                    self.setKey("A",False)
                if event.key==pygame.K_k:
                    self.setKey("B",False)
                if event.key==pygame.K_l:
                    self.setKey("X",False)
                if event.key==pygame.K_SEMICOLON:
                    self.setKey("Y",False)
                if event.key==pygame.K_q:
                    self.setKey("L",False)
                if event.key==pygame.K_e:
                    self.setKey("R",False)
                if event.key==pygame.K_n:
                    self.setKey("START",False)
                if event.key==pygame.K_m:
                    self.setKey("SELECT",False)
            self.heldKeyHandler()


    def heldKeyHandler(self):
        keyheld = False
        trigger = False
        for key in self.heldKeys.keys():
            if self.heldKeys[key]:
                keyheld = True
        if keyheld:
            self.keydownDelay -= 1
            if self.keydownDelay <= 0:
                trigger = True
            for key in self.heldKeys.keys():
                if self.heldKeys[key] and trigger:
                    self.keys[key] = True
                    self.keydownDelay = KEYDOWN_DELAY
        else:
            self.keydownDelay = KEYDOWN_START_DELAY


    def setKey(self,key,val):
        self.keys[key] = val
        if key in self.heldKeys:
            self.heldKeys[key] = val


    def save(self):
        roomdb = open('databases/roomDatabase.db','wb')
        dungeondb = open('databases/dungeonDatabase.db','wb')
        villagedb = open('databases/villageDatabase.db','wb')
        playerdb = open('databases/playerDatabase.db','wb')
        pickle.dump(self.roomDB, roomdb)
        pickle.dump(self.dungeonDB, dungeondb)
        pickle.dump(self.villageDB, villagedb)
        pickle.dump(self.player,playerdb)
        roomdb.close()
        dungeondb.close()
        villagedb.close()
        playerdb.close()
        self.WorldMap.saveRevealed()
        self.WorldMap.saveWorld()

    def load(self):
        roomdb = open('databases/roomDatabase.db','rb')
        dungeondb = open('databases/dungeonDatabase.db','rb')
        villagedb = open('databases/villageDatabase.db','rb')
        playerdb = open('databases/playerDatabase.db','rb')
        self.roomDB = pickle.load(roomdb)
        self.dungeonDB = pickle.load(dungeondb)
        self.villageDB = pickle.load(villagedb)
        self.player = pickle.load(playerdb)
        self.roomDB.printContents()
        self.dungeonDB.printContents()
        self.villageDB.printContents()
        self.player.party.printContents()
        roomdb.close()
        dungeondb.close()
        villagedb.close()
        playerdb.close()