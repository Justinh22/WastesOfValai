import pygame
from combat import *
from pausemenu import *
from directory import *
from writing import *
from dungeonmapgenerator import *

class Crawler():
    def __init__(self,game,dungeonMap):
        self.game = game
        self.dungeonMap = dungeonMap
        self.dungeonPos = self.setEntry()
        self.inDungeon = True
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
        self.inDungeon = True
        self.game.screen.fill((0,0,0))
        self.dungeonPos = list(self.dungeonMap.entrance)
        self.drawScreen()
        while self.inDungeon and self.game.inGame:
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
            if self.dungeonMap.map[self.dungeonPos[0]-1][self.dungeonPos[1]] != self.dungeonMap.wallChar:
                self.dungeonPos[0] -= 1
                self.stepTo(self.dungeonPos[0],self.dungeonPos[1])
            self.drawScreen()
        if self.game.RIGHT:
            if self.dungeonMap.map[self.dungeonPos[0]][self.dungeonPos[1]+1] != self.dungeonMap.wallChar:
                self.dungeonPos[1] += 1
                self.stepTo(self.dungeonPos[0],self.dungeonPos[1])
            self.drawScreen()
        if self.game.DOWN:
            if self.dungeonMap.map[self.dungeonPos[0]+1][self.dungeonPos[1]] != self.dungeonMap.wallChar:
                self.dungeonPos[0] += 1
                self.stepTo(self.dungeonPos[0],self.dungeonPos[1])
            self.drawScreen()
        if self.game.LEFT:
            if self.dungeonMap.map[self.dungeonPos[0]][self.dungeonPos[1]-1] != self.dungeonMap.wallChar:
                self.dungeonPos[1] -= 1
                self.stepTo(self.dungeonPos[0],self.dungeonPos[1])
            self.drawScreen()
        if self.game.A:
            self.pausemenu.pause(self.game.currentPos)
        if self.game.B:
            print("B")
        if self.game.X:
            print("X")
            #self.inDungeon = False
            #self.game.inGame = False

    def drawScreen(self):
        blockSize = 30 #Set the size of the grid block
        self.game.screen.fill((0,0,0))
        write(self.game, 20,self.width-75,self.height+10,"A) Pause")
        for x in range(30, self.width, blockSize):
            for y in range(30, self.height, blockSize):
                color = self.game.white
                gridWidth = self.width / blockSize
                gridHeight = self.height / blockSize
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.game.screen, (255,255,255), rect, 1)
                r = int(((y / blockSize)-(gridHeight/2))+self.dungeonPos[0])
                c = int(((x / blockSize)-(gridWidth/2))+self.dungeonPos[1])
                mapChar = '_'
                if r < 0 or r >= DUNGEON_DIM:
                    mapChar = self.dungeonMap.wallChar
                    color = self.setColor(mapChar)
                if c < 0 or c >= DUNGEON_DIM:
                    mapChar = self.dungeonMap.wallChar
                    color = self.setColor(mapChar)
                if r == self.dungeonPos[0] and c == self.dungeonPos[1]:
                    mapChar = '@'
                if mapChar == '_':
                    mapChar = self.dungeonMap.map[r][c]
                    color = self.setColor(mapChar)
                text = self.font.render(mapChar,True,color)
                textWidth, textHeight = self.font.size(mapChar)
                offset = (blockSize-textWidth)/2

                self.game.screen.blit(text,(x+offset,y+5))

    def setEntry(self):
        if self.dungeonMap.map[self.dungeonMap.entrance[0]-1][self.dungeonMap.entrance[1]] == ' ':
            return ((self.dungeonMap.entrance[0]-1,self.dungeonMap.entrance[1]))
        if self.dungeonMap.map[self.dungeonMap.entrance[0]][self.dungeonMap.entrance[1]+1] == ' ':
            return ((self.dungeonMap.entrance[0],self.dungeonMap.entrance[1]+1))
        if self.dungeonMap.map[self.dungeonMap.entrance[0]+1][self.dungeonMap.entrance[1]] == ' ':
            return ((self.dungeonMap.entrance[0]+1,self.dungeonMap.entrance[1]))
        if self.dungeonMap.map[self.dungeonMap.entrance[0]][self.dungeonMap.entrance[1]-1] == ' ':
            return ((self.dungeonMap.entrance[0],self.dungeonMap.entrance[1]-1))
        
    def setColor(self,mapChar):
        if mapChar == WELL_WALL:
            color = self.game.gray
        elif mapChar == PYRAMID_WALL:
            color = self.game.tan
        elif mapChar == BANDIT_WALL:
            color = self.game.maroon
        elif mapChar == CAVE_WALL:
            color = self.game.brown
        elif mapChar == RUINS_WALL:
            color = self.game.lightgreen
        elif mapChar == TREEHOUSE_WALL:
            color = self.game.green
        else:
            color = self.game.white
        return color

    def stepTo(self,r,c):
        print(f'({r}, {c})')
        if self.dungeonMap.map[r][c] == 'O':
            self.inDungeon = False