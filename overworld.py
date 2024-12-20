import pygame
from combat import *
from pausemenu import *
from directory import *
from roomhandler import *
from writing import *
from dungeoncrawler import *
from villageexplorer import *
from utility import *

class Overworld():
    def __init__(self,game):
        self.game = game
        self.inWorld = True
        self.inDungeon = False
        self.inVillage = False
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
            if self.inVillage:
                self.game.screen.fill(self.game.black)
                self.currentVillage.display()
                if self.currentVillage.inVillage == False:
                    self.inVillage = False
            self.drawScreen()
            self.blitScreen()
        self.game.screen.fill(self.game.black)
        self.blitScreen()

    def getInput(self):
        if self.game.keys["UP"]:
            if self.game.WorldMap.map[self.game.player.currentPos[0]-1][self.game.player.currentPos[1]] != OCEAN_CHAR and self.game.WorldMap.map[self.game.player.currentPos[0]-1][self.game.player.currentPos[1]] != 'X':
                self.game.player.currentPos[0] -= 1
                self.stepTo(self.game.player.currentPos[0],self.game.player.currentPos[1])
            self.drawScreen()
        if self.game.keys["RIGHT"]:
            if self.game.WorldMap.map[self.game.player.currentPos[0]][self.game.player.currentPos[1]+1] != OCEAN_CHAR and self.game.WorldMap.map[self.game.player.currentPos[0]][self.game.player.currentPos[1]+1] != 'X':
                self.game.player.currentPos[1] += 1
                self.stepTo(self.game.player.currentPos[0],self.game.player.currentPos[1])
            self.drawScreen()
        if self.game.keys["DOWN"]:
            if self.game.WorldMap.map[self.game.player.currentPos[0]+1][self.game.player.currentPos[1]] != OCEAN_CHAR and self.game.WorldMap.map[self.game.player.currentPos[0]+1][self.game.player.currentPos[1]] != 'X':
                self.game.player.currentPos[0] += 1
                self.stepTo(self.game.player.currentPos[0],self.game.player.currentPos[1])
            self.drawScreen()
        if self.game.keys["LEFT"]:
            if self.game.WorldMap.map[self.game.player.currentPos[0]][self.game.player.currentPos[1]-1] != OCEAN_CHAR and self.game.WorldMap.map[self.game.player.currentPos[0]][self.game.player.currentPos[1]-1] != 'X':
                self.game.player.currentPos[1] -= 1
                self.stepTo(self.game.player.currentPos[0],self.game.player.currentPos[1])
            self.drawScreen()
        if self.game.keys["A"]:
            print("A")
        if self.game.keys["B"]:
            if self.game.debug_manualEncounters:
                encounter = []
                encounter = self.game.directory.buildEncounter(self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[self.game.player.currentPos[0]][self.game.player.currentPos[1]]),self.getBiome(self.game.player.currentPos[0],self.game.player.currentPos[1]))
                self.combat.initialize(encounter)
        if self.game.keys["X"]:
            print("X")
        if self.game.keys["Y"]:
            print("Y")
        if self.game.keys["START"]:
            self.pausemenu.pause(self.game.player.currentPos)
            if self.game.player.party.callaretsCompact:
                self.game.player.currentPos = list(self.game.player.lastCheckpoint)

    def drawScreen(self):
        blockSize = 30 #Set the size of the grid block
        self.game.screen.fill((0,0,0))
        power = math.ceil(self.game.player.party.getPower()/2)
        diffText = self.getBiome(self.game.player.currentPos[0],self.game.player.currentPos[1]).name + ": Difficulty " + str(self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[self.game.player.currentPos[0]][self.game.player.currentPos[1]]))
        areaDifficulty = self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[self.game.player.currentPos[0]][self.game.player.currentPos[1]])
        difficultyDiff = abs(areaDifficulty-power)
        if difficultyDiff > 3:
            difficultyDiff = 3
        
        if areaDifficulty > power:
            color = (255, 255 - (difficultyDiff * 85), 255 - (difficultyDiff * 85))
            text = self.font.render(diffText,True,color)
        elif areaDifficulty < power:
            color = (255 - (difficultyDiff * 85), 255, 255 - (difficultyDiff * 85))
            text = self.font.render(diffText,True,color)
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
                    mapChar = OCEAN_CHAR
                    color = self.game.blue
                if c < 0 or c >= self.game.WorldMap.sizeC:
                    mapChar = OCEAN_CHAR
                    color = self.game.blue
                if r == self.game.player.currentPos[0] and c == self.game.player.currentPos[1]:
                    mapChar = '@'
                if mapChar == '_':
                    revMapList = list(self.game.WorldMap.revealedMap[r])
                    revMapList[c] = '1'
                    self.game.WorldMap.revealedMap[r] = ''.join(revMapList)
                    mapChar = self.game.WorldMap.map[r][c]
                    if mapChar == FOREST_CHAR: # Forest
                        color = self.game.green
                    elif mapChar == PLAINS_CHAR: # Plains
                        color = self.game.lightgreen
                    elif mapChar == DESERT_CHAR: # Desert
                        color = self.game.tan
                    elif mapChar == PATH_CHAR: # Path
                        color = self.game.orange
                    elif mapChar == OCEAN_CHAR: # Path
                        color = self.game.blue
                    elif self.game.roomDB.doesExist((r,c)) or self.game.dungeonDB.doesExist((r,c)) or self.game.villageDB.doesExist((r,c)):
                        color = self.game.gray
                text = self.font.render(mapChar,True,color)
                textWidth, textHeight = self.font.size(mapChar)
                offset = (blockSize-textWidth)/2

                self.game.screen.blit(text,(x+offset,y+5))

    def getBiome(self,r,c):
        if self.game.WorldMap.map[r][c] == FOREST_CHAR:
            return Biome.Forest
        elif self.game.WorldMap.map[r][c] == PLAINS_CHAR:
            return Biome.Plains
        elif self.game.WorldMap.map[r][c] == DESERT_CHAR:
            return Biome.Desert
        elif self.game.WorldMap.map[r][c] == PATH_CHAR:
            return Biome.Path
        else:
            return Biome.Other
        
    def getDungeonType(self,r,c):
        if self.game.WorldMap.map[r][c] == WELL_CHAR:
            return DungeonType.Well
        elif self.game.WorldMap.map[r][c] == PYRAMID_CHAR:
            return DungeonType.Pyramid
        elif self.game.WorldMap.map[r][c] == BANDITCAMP_CHAR:
            return DungeonType.BanditCamp
        elif self.game.WorldMap.map[r][c] == CAVE_CHAR:
            return DungeonType.Cave
        elif self.game.WorldMap.map[r][c] == RUINS_CHAR:
            return DungeonType.Ruins
        elif self.game.WorldMap.map[r][c] == TREEHOUSE_CHAR:
            return DungeonType.Treehouse

    def stepTo(self,r,c): # Simplified; any non-terrain space is treated as a Shack
        # self.game.stir()
        if self.game.WorldMap.map[r][c] != FOREST_CHAR and self.game.WorldMap.map[r][c] != PLAINS_CHAR and self.game.WorldMap.map[r][c] != DESERT_CHAR and self.game.WorldMap.map[r][c] != PATH_CHAR:
            self.steps += 1
            if self.game.WorldMap.map[r][c] == HAVEN_CHAR or self.game.WorldMap.map[r][c] == VILLAGE_CHAR:
                if (not (self.game.roomDB.doesExist((r,c))) and self.game.WorldMap.map[r][c] == HAVEN_CHAR) or (not (self.game.villageDB.doesExist((r,c))) and self.game.WorldMap.map[r][c] == VILLAGE_CHAR):
                    if self.game.player.lastCheckpoint != (0,0):
                        pathfinder = Pathfinder(self.game.player.lastCheckpoint,(r,c),self.game.WorldMap.map)
                        path = pathfinder.calculatePath()
                        for step in path:
                            if self.game.WorldMap.map[step[0]][step[1]] == FOREST_CHAR or self.game.WorldMap.map[step[0]][step[1]] == PLAINS_CHAR or self.game.WorldMap.map[step[0]][step[1]] == DESERT_CHAR:
                                tempList = list(self.game.WorldMap.map[step[0]])
                                print(f'Writing a {type(self.game.WorldMap.map[step[0]][step[1]])} at ({step[0]},{step[1]})')
                                tempList[step[1]] = PATH_CHAR
                                self.game.WorldMap.map[step[0]] = ""
                                for char in tempList:
                                    self.game.WorldMap.map[step[0]] += char
                self.game.player.lastCheckpoint = (r,c)
            if self.game.WorldMap.map[r][c] == ABANDONED_VILLAGE_CHAR or self.game.WorldMap.map[r][c] == HAVEN_CHAR or self.game.WorldMap.map[r][c] == SHACK_CHAR:
                if self.game.WorldMap.map[r][c] == HAVEN_CHAR:
                    typ = "haven"
                elif self.game.WorldMap.map[r][c] == SHACK_CHAR or self.game.WorldMap.map[r][c] == ABANDONED_VILLAGE_CHAR:
                    typ = "room"
                print(f'Type: {typ}')
                newRoom = RoomHandler(self.game, self.game.roomDB.getRoom((r,c),self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c]),typ))
                newRoom.enter()
            elif self.game.WorldMap.map[r][c] == VILLAGE_CHAR:
                print("Das a village bay-be!")
                self.currentVillage = Explorer(self.game,self.game.villageDB.getVillage((r,c),self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c]), self.approximateBiome(r,c)))
                self.currentVillage.inVillage = True
                self.inVillage = True
            else:
                self.currentDungeon = Crawler(self.game,self.game.dungeonDB.getDungeon((r,c),self.getDungeonType(r,c),self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c])))
                self.currentDungeon.inDungeon = True
                self.inDungeon = True
        elif self.game.debug_manualEncounters is False and self.game.WorldMap.map[r][c] != PATH_CHAR: # Roll for random encounter
            difficultyDiffBias = self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c]) - math.ceil(self.game.player.party.getPower()/2)
            if difficultyDiffBias > 3:
                difficultyDiffBias = 3
            elif difficultyDiffBias <= -3:
                difficultyDiffBias = -3
            difficultyDiffBias *= 4

            if self.steps < 5:
                odds = 15
            elif self.steps < 10:
                odds = 18
            else:
                odds = 20

            odds += difficultyDiffBias
            rollA = random.randint(1,100)
            rollB = random.randint(1,100)

            if (rollA+rollB) <= (odds*2) and self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c]) == self.lastDiff:
                self.steps = 0
                encounter = []
                encounter = self.game.directory.buildEncounter(self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c]),self.getBiome(self.game.player.currentPos[0],self.game.player.currentPos[1]))
                self.combat.initialize(encounter)
        self.lastDiff = self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c])


    def approximateBiome(self,r,c):
        checklist = [(-1,0),(0,1),(1,0),(0,-1)]
        biomeRankings = {Biome.Forest: 0, Biome.Plains: 0, Biome.Desert: 0}
        for mod in checklist:
            biome = self.getBiome(r+mod[0],c+mod[1])
            if biome is not Biome.Other and biome is not Biome.Path:
                biomeRankings[biome] += 1
        return max(biomeRankings, key=biomeRankings.get)


class Pathfinder():
    def __init__(self,start,end,map):
        self.startPoint = start
        self.endPoint = end
        self.map = map
        self.path = []
        self.obstacles = [OCEAN_CHAR,BORDER_CHAR]
        self.workingPath = set()

    def calculatePath(self):
        path = self.bfs(self.startPoint)
        return path
    
    def isValid(self,row,col):
        return self.map[row][col] not in self.obstacles

    def bfs(self,start):
        queue = deque([(start, [])])
        visited = set()

        while queue:
            current, path = queue.popleft()
            row, col = current

            if current == self.endPoint:
                return path + [current]
            
            if current in visited:
                continue

            visited.add(current)

            for r, c in [(0,1), (1,0), (0,-1), (-1,0)]:
                newR, newC = row + r, col + c
                nextPos = (newR, newC)

                if self.isValid(newR, newC):
                    queue.append((nextPos, path + [current]))

        return None