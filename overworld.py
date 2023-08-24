import pygame
from combat import *
from pausemenu import *
from directory import *

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
            self.drawScreen()
        if self.game.RIGHT:
            if self.game.WorldMap.map[self.game.currentPos[0]][self.game.currentPos[1]+1] != ' ' and self.game.WorldMap.map[self.game.currentPos[0]][self.game.currentPos[1]+1] != 'X':
                self.game.currentPos[1] += 1
            self.drawScreen()
        if self.game.DOWN:
            if self.game.WorldMap.map[self.game.currentPos[0]+1][self.game.currentPos[1]] != ' ' and self.game.WorldMap.map[self.game.currentPos[0]+1][self.game.currentPos[1]] != 'X':
                self.game.currentPos[0] += 1
            self.drawScreen()
        if self.game.LEFT:
            if self.game.WorldMap.map[self.game.currentPos[0]][self.game.currentPos[1]-1] != ' ' and self.game.WorldMap.map[self.game.currentPos[0]][self.game.currentPos[1]-1] != 'X':
                self.game.currentPos[1] -= 1
            self.drawScreen()
        if self.game.A:
            self.pausemenu.pause(self.game.currentPos)
        if self.game.B:
            encounter = []
            encounter = self.game.directory.buildEncounter(self.party.power,self.getBiome(self.game.currentPos[0],self.game.currentPos[1]))
            self.party.debug_RandomInventory(self.game.directory)
            self.combat.initialize(self.party,encounter)
        if self.game.X:
            print("X")
            #self.inWorld = False
            #self.game.inGame = False

    def drawScreen(self):
        blockSize = 30 #Set the size of the grid block
        self.game.screen.fill((0,0,0))
        for x in range(30, self.width, blockSize):
            for y in range(30, self.height, blockSize):
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

                text = self.font.render(mapChar,True,self.game.white)
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
