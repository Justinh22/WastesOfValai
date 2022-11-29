import pygame
from combat import *
from directory import *

class Overworld():
    def __init__(self,game):
        self.game = game
        self.currentPos = list(self.game.WorldMap.startingPos)
        self.inWorld = True
        self.width = self.game.width - 60
        self.height = self.game.height - 60
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.combat = Combat(self.game)
        self.party = []
        self.lvlTot = 0
        for i in range(0,random.randint(3,4)):
            lvl = random.randint(1,8)
            self.party.append(Character(getCharacterName(),lvl,self.game.directory.classDirectory[random.randint(0,11)],random.randint(0,5))) #random.randint(0,11)
            self.party[i].eqpWpn = game.directory.getWeapon(game.directory.getItemByRarities("Weapon",lvl-1,lvl))
            self.party[i].eqpAmr = game.directory.getArmor(game.directory.getItemByRarities("Armor",lvl-1,lvl))
            self.lvlTot += lvl

    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0,0))
        pygame.display.update()
        self.game.buttonReset()

    def display(self):
        self.inWorld = True
        self.game.screen.fill((0,0,0))
        self.currentPos = list(self.game.WorldMap.startingPos)
        self.drawScreen()
        while self.inWorld:
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
            if self.game.WorldMap.map[self.currentPos[0]-1][self.currentPos[1]] != ' ' and self.game.WorldMap.map[self.currentPos[0]-1][self.currentPos[1]] != 'X':
                self.currentPos[0] -= 1
            self.drawScreen()
        if self.game.RIGHT:
            if self.game.WorldMap.map[self.currentPos[0]][self.currentPos[1]+1] != ' ' and self.game.WorldMap.map[self.currentPos[0]][self.currentPos[1]+1] != 'X':
                self.currentPos[1] += 1
            self.drawScreen()
        if self.game.DOWN:
            if self.game.WorldMap.map[self.currentPos[0]+1][self.currentPos[1]] != ' ' and self.game.WorldMap.map[self.currentPos[0]+1][self.currentPos[1]] != 'X':
                self.currentPos[0] += 1
            self.drawScreen()
        if self.game.LEFT:
            if self.game.WorldMap.map[self.currentPos[0]][self.currentPos[1]-1] != ' ' and self.game.WorldMap.map[self.currentPos[0]][self.currentPos[1]-1] != 'X':
                self.currentPos[1] -= 1
            self.drawScreen()
        if self.game.B:
            encounter = []
            encounter = self.game.directory.buildEncounter(self.lvlTot,self.getBiome(self.currentPos[0],self.currentPos[1]))
            self.combat.initialize(self.party,encounter)
        if self.game.X:
            self.inWorld = False
            pygame.quit()

    def drawScreen(self):
        blockSize = 30 #Set the size of the grid block
        self.game.screen.fill((0,0,0))
        for x in range(30, self.width, blockSize):
            for y in range(30, self.height, blockSize):
                gridWidth = self.width / blockSize
                gridHeight = self.height / blockSize
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.game.screen, (255,255,255), rect, 1)
                r = int(((y / blockSize)-(gridHeight/2))+self.currentPos[0])
                c = int(((x / blockSize)-(gridWidth/2))+self.currentPos[1])
                mapChar = '_'
                if r < 0 or r >= self.game.WorldMap.sizeR:
                    mapChar = ' '
                if c < 0 or c >= self.game.WorldMap.sizeC:
                    mapChar = ' '
                if r == self.currentPos[0] and c == self.currentPos[1]:
                    mapChar = '@'
                if mapChar == '_':
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
