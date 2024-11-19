import pygame
import time
from combat import *
from pausemenu import *
from directory import *
from writing import *
from villagemapgenerator import *
from characterpopups import *
from pathfinder import *

class Explorer():
    def __init__(self,game,village):
        self.game = game
        self.village = village
        self.villagePos = self.village.entrance
        self.inVillage = True
        self.state = "main"
        self.width = self.game.width - 60
        self.height = self.game.height - 60
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.pausemenu = PauseMenu(self.game)
        self.party = self.game.player.party
        self.message = ""
        self.messageTimer = 0

    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0,0))
        pygame.display.update()
        self.game.buttonReset()

    def display(self):
        self.inVillage = True
        self.game.screen.fill((0,0,0))
        self.villagePos = list(self.village.entrance)
        self.drawScreen()
        while self.inVillage and self.game.inGame:
            self.game.eventHandler()
            self.getInput()
            self.drawScreen()
            self.blitScreen()
        self.game.screen.fill(self.game.black)
        self.blitScreen()

    def getInput(self):
        if self.game.UP:
            self.stepTo(-1,0)
            self.drawScreen()
        if self.game.RIGHT:
            self.stepTo(0,+1)
            self.drawScreen()
        if self.game.DOWN:
            self.stepTo(+1,0)
            self.drawScreen()
        if self.game.LEFT:
            self.stepTo(0,-1)
            self.drawScreen()
        if self.game.A:
            print("A")
        if self.game.B:
            print("B")
        if self.game.X:
            print("X")
        if self.game.START:
            self.pausemenu.pause(self.game.player.currentPos)

    def drawScreen(self):
        blockSize = 30 #Set the size of the grid block
        self.game.screen.fill((0,0,0))
        write(self.game,15,self.width-80,self.height+10,"ST) Pause")
        for x in range(30, self.width, blockSize):
            for y in range(30, self.height, blockSize):
                color = self.game.white
                gridWidth = self.width / blockSize
                gridHeight = self.height / blockSize
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.game.screen, (255,255,255), rect, 1)
                r = int(((y / blockSize)-(gridHeight/2))+self.villagePos[0])
                c = int(((x / blockSize)-(gridWidth/2))+self.villagePos[1])
                mapChar = '_'
                if r < 0 or r >= self.village.maxRows:
                    mapChar = self.village.groundChar
                    color = self.setColor(mapChar,r,c)
                if c < 0 or c >= self.village.maxCols:
                    mapChar = self.village.groundChar
                    color = self.setColor(mapChar,r,c)
                if r == self.villagePos[0] and c == self.villagePos[1]:
                    mapChar = '@'
                if mapChar == '_':
                    mapChar = self.village.map[r][c]
                    color = self.setColor(mapChar,r,c)
                text = self.font.render(mapChar,True,color)
                textWidth, textHeight = self.font.size(mapChar)
                offset = (blockSize-textWidth)/2
                self.game.screen.blit(text,(x+offset,y+5))
        
    def setColor(self,mapChar,r,c):
        if mapChar == FOREST_CHAR: # Forest
            color = self.game.green
        elif mapChar == PLAINS_CHAR: # Plains
            color = self.game.lightgreen
        elif mapChar == DESERT_CHAR: # Desert
            color = self.game.tan
        elif mapChar == PATH_CHAR: # Path
            color = self.game.orange
        elif mapChar == BUILDING_WALL: # Building Wall
            color = self.game.brown
        elif mapChar == BUILDING_ROOF: # Building Roof
            color = self.game.brown
            for building in self.village.buildings:
                if building.isInBuilding(r,c):
                    color = building.color
        elif mapChar == BUILDING_DOOR: # Building Door
            color = self.game.gray
        return color

    def stepTo(self,rMod,cMod):
        #print(f'({r}, {c})')
        self.villagePos[0] += rMod
        self.villagePos[1] += cMod
        if self.villagePos[0]+rMod < 0 or self.villagePos[0]+rMod > self.village.maxRows-1 or self.villagePos[1]+cMod < 0 or self.villagePos[1]+cMod > self.village.maxCols-1:
            self.inVillage = False
            return
        if self.village.map[self.villagePos[0]][self.villagePos[1]] == BUILDING_WALL or self.village.map[self.villagePos[0]][self.villagePos[1]] == BUILDING_ROOF:
            self.villagePos[0] -= rMod
            self.villagePos[1] -= cMod
        if self.village.map[self.villagePos[0]][self.villagePos[1]] == BUILDING_DOOR:
            building = self.buildingLookup(self.villagePos[0],self.villagePos[1])
            building.enter(self.game,self.game.player)

    def buildingLookup(self,r,c):
        for building in self.village.buildings:
            if (r,c) == building.getDoorway():
                return building

    def getDistance(self,start,target):
        return (abs(start[0]-target[0]) + abs(start[1]-target[1]))