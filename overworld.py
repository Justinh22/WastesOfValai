import pygame
from combat import *
from pausemenu import *
from directory import *
from roomhandler import *

class Overworld():
    def __init__(self,game):
        self.game = game
        self.inWorld = True
        self.width = self.game.width - 60
        self.height = self.game.height - 60
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.pausemenu = PauseMenu(self.game)
        self.combat = Combat(self.game)
        self.party = self.game.party
        self.steps = 0

    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0,0))
        pygame.display.update()
        self.game.buttonReset()

    def display(self):
        self.inWorld = True
        self.game.screen.fill((0,0,0))
        self.game.currentPos = list(self.game.WorldMap.startingPos)
        self.drawScreen()
        while self.inWorld and self.game.inGame:
            self.game.eventHandler()
            self.getInput()
            if self.combat.inCombat:
                self.game.screen.fill(self.game.black)
                self.combat.display()
            self.drawScreen()
            self.blitScreen()
        self.game.screen.fill(self.game.black)
        self.blitScreen()

    def getInput(self):
        if self.game.UP:
            if self.game.WorldMap.map[self.game.currentPos[0]-1][self.game.currentPos[1]] != ' ' and self.game.WorldMap.map[self.game.currentPos[0]-1][self.game.currentPos[1]] != 'X':
                self.game.currentPos[0] -= 1
                self.stepTo(self.game.currentPos[0],self.game.currentPos[1])
            self.drawScreen()
        if self.game.RIGHT:
            if self.game.WorldMap.map[self.game.currentPos[0]][self.game.currentPos[1]+1] != ' ' and self.game.WorldMap.map[self.game.currentPos[0]][self.game.currentPos[1]+1] != 'X':
                self.game.currentPos[1] += 1
                self.stepTo(self.game.currentPos[0],self.game.currentPos[1])
            self.drawScreen()
        if self.game.DOWN:
            if self.game.WorldMap.map[self.game.currentPos[0]+1][self.game.currentPos[1]] != ' ' and self.game.WorldMap.map[self.game.currentPos[0]+1][self.game.currentPos[1]] != 'X':
                self.game.currentPos[0] += 1
                self.stepTo(self.game.currentPos[0],self.game.currentPos[1])
            self.drawScreen()
        if self.game.LEFT:
            if self.game.WorldMap.map[self.game.currentPos[0]][self.game.currentPos[1]-1] != ' ' and self.game.WorldMap.map[self.game.currentPos[0]][self.game.currentPos[1]-1] != 'X':
                self.game.currentPos[1] -= 1
                self.stepTo(self.game.currentPos[0],self.game.currentPos[1])
            self.drawScreen()
        if self.game.A:
            self.pausemenu.pause(self.game.currentPos)
        if self.game.B:
            encounter = []
            encounter = self.game.directory.buildEncounter(self.party.getPower(),self.getBiome(self.game.currentPos[0],self.game.currentPos[1]))
            self.combat.initialize(self.party,encounter)
        if self.game.X:
            print("X")
            #self.inWorld = False
            #self.game.inGame = False

    def drawScreen(self):
        blockSize = 30 #Set the size of the grid block
        self.game.screen.fill((0,0,0))
        diffText = self.getBiome(self.game.currentPos[0],self.game.currentPos[1]) + ": Difficulty " + str(self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[self.game.currentPos[0]][self.game.currentPos[1]]))
        self.write(20,30,self.height+10,diffText)
        self.write(20,self.width-75,self.height+10,"A) Pause")
        for x in range(30, self.width, blockSize):
            for y in range(30, self.height, blockSize):
                color = self.game.white
                gridWidth = self.width / blockSize
                gridHeight = self.height / blockSize
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.game.screen, (255,255,255), rect, 1)
                r = int(((y / blockSize)-(gridHeight/2))+self.game.currentPos[0])
                c = int(((x / blockSize)-(gridWidth/2))+self.game.currentPos[1])
                mapChar = '_'
                if r < 0 or r >= self.game.WorldMap.sizeR:
                    mapChar = ' '
                if c < 0 or c >= self.game.WorldMap.sizeC:
                    mapChar = ' '
                if r == self.game.currentPos[0] and c == self.game.currentPos[1]:
                    mapChar = '@'
                if mapChar == '_':
                    revMapList = list(self.game.WorldMap.revealedMap[r])
                    revMapList[c] = '1'
                    self.game.WorldMap.revealedMap[r] = ''.join(revMapList)
                    mapChar = self.game.WorldMap.map[r][c]
                    if mapChar == '#': # Forest
                        color = self.game.green
                    elif mapChar == ';': # Plains
                        color = self.game.lightgreen
                    elif mapChar == '.': # Desert
                        color = self.game.tan
                text = self.font.render(mapChar,True,color)
                textWidth, textHeight = self.font.size(mapChar)
                offset = (blockSize-textWidth)/2

                self.game.screen.blit(text,(x+offset,y+5))

    def getBiome(self,r,c):
        if self.game.WorldMap.map[r][c] == '#':
            return "Forest"
        elif self.game.WorldMap.map[r][c] == ';':
            return "Plains"
        elif self.game.WorldMap.map[r][c] == '.':
            return "Desert"
        else:
            return "Dungeon"

    def stepTo(self,r,c): # Simplified; any non-terrain space is treated as a Shack
        # self.game.stir()
        self.steps += 1
        if self.game.WorldMap.map[r][c] != '#' and self.game.WorldMap.map[r][c] != ';' and self.game.WorldMap.map[r][c] != '.':
            newRoom = RoomHandler(self.game, self.game.roomDB.getRoom((r,c),self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c])))
            newRoom.enter()
        else: # Roll for random encounter
            if self.steps < 5:
                odds = 15
            elif self.steps < 10:
                odds = 1
            elif self.steps < 15:
                odds = 2
            else:
                odds = 3
            if random.randint(odds,15) == 14:
                self.steps = 0
                encounter = []
                encounter = self.game.directory.buildEncounter(self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c]),self.getBiome(self.game.currentPos[0],self.game.currentPos[1]))
                self.party.debug_RandomInventory(self.game.directory)
                self.combat.initialize(self.party,encounter)

    def write(self,size,x,y,text):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text, True, self.game.white)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.game.screen.blit(text_surface,text_rect)
        return font.size(text)