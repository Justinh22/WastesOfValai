import pygame
from combat import *
from pausemenu import *
from directory import *
from roomhandler import *
from writing import *
from dungeoncrawler import *
from utility import *

class Overworld():
    def __init__(self,game):
        self.game = game
        self.inWorld = True
        self.inDungeon = False
        self.currentDungeon = 0
        self.width = self.game.width - 60
        self.height = self.game.height - 60
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.pausemenu = PauseMenu(self.game)
        self.combat = Combat(self.game)
        self.steps = 0
        self.lastDiff = 0

    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0,0))
        pygame.display.update()
        self.game.buttonReset()

    def display(self):
        self.inWorld = True
        self.game.screen.fill((0,0,0))
        self.game.player.currentPos = list(self.game.WorldMap.startingPos)
        self.drawScreen()
        while self.inWorld and self.game.inGame:
            self.game.eventHandler()
            self.getInput()
            if self.combat.inCombat:
                self.game.screen.fill(self.game.black)
                self.combat.display()
            if self.inDungeon:
                self.game.screen.fill(self.game.black)
                self.currentDungeon.display()
                if self.currentDungeon.inDungeon == False:
                    self.inDungeon = False
            self.drawScreen()
            self.blitScreen()
        self.game.screen.fill(self.game.black)
        self.blitScreen()

    def getInput(self):
        if self.game.UP:
            if self.game.WorldMap.map[self.game.player.currentPos[0]-1][self.game.player.currentPos[1]] != ' ' and self.game.WorldMap.map[self.game.player.currentPos[0]-1][self.game.player.currentPos[1]] != 'X':
                self.game.player.currentPos[0] -= 1
                self.stepTo(self.game.player.currentPos[0],self.game.player.currentPos[1])
            self.drawScreen()
        if self.game.RIGHT:
            if self.game.WorldMap.map[self.game.player.currentPos[0]][self.game.player.currentPos[1]+1] != ' ' and self.game.WorldMap.map[self.game.player.currentPos[0]][self.game.player.currentPos[1]+1] != 'X':
                self.game.player.currentPos[1] += 1
                self.stepTo(self.game.player.currentPos[0],self.game.player.currentPos[1])
            self.drawScreen()
        if self.game.DOWN:
            if self.game.WorldMap.map[self.game.player.currentPos[0]+1][self.game.player.currentPos[1]] != ' ' and self.game.WorldMap.map[self.game.player.currentPos[0]+1][self.game.player.currentPos[1]] != 'X':
                self.game.player.currentPos[0] += 1
                self.stepTo(self.game.player.currentPos[0],self.game.player.currentPos[1])
            self.drawScreen()
        if self.game.LEFT:
            if self.game.WorldMap.map[self.game.player.currentPos[0]][self.game.player.currentPos[1]-1] != ' ' and self.game.WorldMap.map[self.game.player.currentPos[0]][self.game.player.currentPos[1]-1] != 'X':
                self.game.player.currentPos[1] -= 1
                self.stepTo(self.game.player.currentPos[0],self.game.player.currentPos[1])
            self.drawScreen()
        if self.game.A:
            print("A")
        if self.game.B:
            encounter = []
            encounter = self.game.directory.buildEncounter(self.game.player.party.getPower(),self.getBiome(self.game.player.currentPos[0],self.game.player.currentPos[1]))
            self.combat.initialize(encounter)
        if self.game.X:
            print("X")
        if self.game.Y:
            if len(self.game.player.party.members) < 4:
                self.game.player.party.members.append(self.game.directory.buildCharacter(difficultyToLevel(self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[self.game.player.currentPos[0]][self.game.player.currentPos[1]])),self.game.player.party.members))
            else:
                CharacterSwap(self.game,self.game.directory.buildCharacter(difficultyToLevel(self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[self.game.player.currentPos[0]][self.game.player.currentPos[1]])),self.game.player.party.members))
        if self.game.START:
            self.pausemenu.pause(self.game.player.currentPos)

    def drawScreen(self):
        blockSize = 30 #Set the size of the grid block
        self.game.screen.fill((0,0,0))
        diffText = self.getBiome(self.game.player.currentPos[0],self.game.player.currentPos[1]).name + ": Difficulty " + str(self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[self.game.player.currentPos[0]][self.game.player.currentPos[1]]))
        if self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[self.game.player.currentPos[0]][self.game.player.currentPos[1]]) > self.game.player.party.getPower()+1:
            text = self.font.render(diffText,True,self.game.red)
        elif self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[self.game.player.currentPos[0]][self.game.player.currentPos[1]]) < self.game.player.party.getPower()-10:
            text = self.font.render(diffText,True,self.game.green)
        else:
            text = self.font.render(diffText,True,self.game.white)
        self.game.screen.blit(text,(30,self.height+10))
        #write(self.game, 20,30,self.height+10,diffText)
        write(self.game, 20,self.width-80,self.height+10,"ST) Pause")
        for x in range(30, self.width, blockSize):
            for y in range(30, self.height, blockSize):
                color = self.game.white
                gridWidth = self.width / blockSize
                gridHeight = self.height / blockSize
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.game.screen, (255,255,255), rect, 1)
                r = int(((y / blockSize)-(gridHeight/2))+self.game.player.currentPos[0])
                c = int(((x / blockSize)-(gridWidth/2))+self.game.player.currentPos[1])
                mapChar = '_'
                if r < 0 or r >= self.game.WorldMap.sizeR:
                    mapChar = ' '
                if c < 0 or c >= self.game.WorldMap.sizeC:
                    mapChar = ' '
                if r == self.game.player.currentPos[0] and c == self.game.player.currentPos[1]:
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
            return Biome.Forest
        elif self.game.WorldMap.map[r][c] == ';':
            return Biome.Plains
        elif self.game.WorldMap.map[r][c] == '.':
            return Biome.Desert
        else:
            return Biome.Dungeon
        
    def getDungeonType(self,r,c):
        if self.game.WorldMap.map[r][c] == 'W':
            return DungeonType.Well
        elif self.game.WorldMap.map[r][c] == 'P':
            return DungeonType.Pyramid
        elif self.game.WorldMap.map[r][c] == 'B':
            return DungeonType.BanditCamp
        elif self.game.WorldMap.map[r][c] == 'C':
            return DungeonType.Cave
        elif self.game.WorldMap.map[r][c] == 'R':
            return DungeonType.Ruins
        elif self.game.WorldMap.map[r][c] == 'T':
            return DungeonType.Treehouse

    def stepTo(self,r,c): # Simplified; any non-terrain space is treated as a Shack
        # self.game.stir()
        self.steps += 1
        if self.game.WorldMap.map[r][c] != '#' and self.game.WorldMap.map[r][c] != ';' and self.game.WorldMap.map[r][c] != '.':
            if self.game.WorldMap.map[r][c] == 'A' or self.game.WorldMap.map[r][c] == 'H' or self.game.WorldMap.map[r][c] == 'S':
                if self.game.WorldMap.map[r][c] == 'H':
                    typ = "haven"
                else:
                    typ = "room"
                print(f'Type: {typ}')
                newRoom = RoomHandler(self.game, self.game.roomDB.getRoom((r,c),self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c]),typ))
                newRoom.enter()
            else:
                self.currentDungeon = Crawler(self.game,self.game.dungeonDB.getDungeon((r,c),self.getDungeonType(r,c),self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c])))
                self.currentDungeon.inDungeon = True
                self.inDungeon = True
        else: # Roll for random encounter
            if self.steps < 5:
                odds = 50
            elif self.steps < 10:
                odds = 1
            elif self.steps < 15:
                odds = 10
            else:
                odds = 25
            if random.randint(odds,50) == 49 and self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c]) == self.lastDiff and not (self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c]) < self.game.player.party.getPower()-10):
                self.steps = 0
                encounter = []
                encounter = self.game.directory.buildEncounter(self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c]),self.getBiome(self.game.player.currentPos[0],self.game.player.currentPos[1]))
                self.combat.initialize(encounter)
        self.lastDiff = self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c])