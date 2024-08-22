from collections import deque
import pygame
import time
from combat import *
from pausemenu import *
from directory import *
from writing import *
from dungeonmapgenerator import *
from characterpopups import *

class Crawler():
    def __init__(self,game,dungeon):
        self.game = game
        self.dungeon = dungeon
        self.dungeonMap = self.dungeon.getFloor(1)
        self.dungeonPos = self.setEntryAt()
        self.inDungeon = True
        self.state = "main"
        self.width = self.game.width - 60
        self.height = self.game.height - 60
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.pausemenu = PauseMenu(self.game)
        self.combat = Combat(self.game)
        self.party = self.game.player.party
        self.enemyList = []
        self.message = ""
        self.messageTimer = 0
        self.wanderer = -1
        for loot in self.dungeonMap.loot:
            print(self.game.directory.getItemName(loot.loot))

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
            self.enemyHandler()
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
            if self.state == "lootSummary":
                self.state == "main"
        if self.game.RIGHT:
            if self.dungeonMap.map[self.dungeonPos[0]][self.dungeonPos[1]+1] != self.dungeonMap.wallChar:
                self.dungeonPos[1] += 1
                self.stepTo(self.dungeonPos[0],self.dungeonPos[1])
            self.drawScreen()
            if self.state == "lootSummary":
                self.state == "main"
        if self.game.DOWN:
            if self.dungeonMap.map[self.dungeonPos[0]+1][self.dungeonPos[1]] != self.dungeonMap.wallChar:
                self.dungeonPos[0] += 1
                self.stepTo(self.dungeonPos[0],self.dungeonPos[1])
            self.drawScreen()
            if self.state == "lootSummary":
                self.state == "main"
        if self.game.LEFT:
            if self.dungeonMap.map[self.dungeonPos[0]][self.dungeonPos[1]-1] != self.dungeonMap.wallChar:
                self.dungeonPos[1] -= 1
                self.stepTo(self.dungeonPos[0],self.dungeonPos[1])
            self.drawScreen()
            if self.state == "lootSummary":
                self.state == "main"
        if self.game.A:
            print("A")
            if self.state == "lootSummary":
                if self.game.player.party.add(self.lootLookup().loot,self.game.directory):
                    self.message = "You picked up the " + self.game.directory.getItemName(self.lootLookup().loot,True)
                    self.dungeonMap.removeLoot(self.lootLookup())
                    self.state = "main"
                else:
                    self.message = "Your inventory is full"
                self.messageTimer = 1000
            if self.state == "wandererSummary":
                lvl = difficultyToLevel(self.dungeonMap.dungeonLevel)
                if difficultyToLevel(self.dungeonMap.dungeonLevel) > self.game.player.party.getHighestLevel():
                    lvl = self.game.player.party.getHighestLevel()
                newChar = self.game.directory.buildCharacter(lvl,self.game.player.party.members,self.game.player.getNewCharID())
                if len(self.game.player.party.members) < 4:
                    self.game.player.party.members.append(newChar)
                    self.message = "You awaken " + newChar.name + ", the Level " + str(newChar.level) + " " + newChar.type.name
                else:
                    CharacterSwap(self.game,newChar)
                self.dungeonMap.map[self.dungeonPos[0]][self.dungeonPos[1]] = FLOOR_CHAR
                self.messageTimer = 1000
                self.state = "main"
        if self.game.B:
            print("B")
        if self.game.X:
            print("X")
            #self.inDungeon = False
            #self.game.inGame = False
        if self.game.START:
            self.pausemenu.pause(self.game.player.currentPos)

    def drawScreen(self):
        blockSize = 30 #Set the size of the grid block
        self.game.screen.fill((0,0,0))
        floorInfo = "Floor " + str(self.dungeonMap.floor) + "/" + str(self.dungeonMap.maxFloors)
        write(self.game,15,self.width-80,self.height+10,"ST) Pause")
        write(self.game,15,self.width-80,self.height+30,floorInfo)
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
                for enemy in self.enemyList:
                    if r == enemy.coords[0] and c == enemy.coords[1]:
                        mapChar = 'M'
                if mapChar == '_':
                    mapChar = self.dungeonMap.map[r][c]
                    color = self.setColor(mapChar)
                text = self.font.render(mapChar,True,color)
                textWidth, textHeight = self.font.size(mapChar)
                offset = (blockSize-textWidth)/2
                self.game.screen.blit(text,(x+offset,y+5))
        if self.state == "lootSummary":
            text = "Inside the chest is a " + self.game.directory.getItemName(self.lootLookup().loot,True)
            self.messageTimer = 0
            write(self.game, 20, 30,self.height+10,text)
        if self.state == "wandererSummary":
            text = "A wanderer lies on the ground, unconscious."
            self.messageTimer = 0
            write(self.game, 20, 30,self.height+10,text)
        if self.messageTimer > 0:
            write(self.game, 20, 30,self.height+10,self.message)
            self.messageTimer -= 1

    def nextFloor(self):
        nextFloor = self.dungeonMap.floor + 1
        self.dungeonMap = self.dungeon.getFloor(nextFloor)
        self.dungeonPos = list(self.setEntryAt("Entrance"))
        self.enemyList = []

    def previousFloor(self):
        prevFloor = self.dungeonMap.floor - 1
        self.dungeonMap = self.dungeon.getFloor(prevFloor)
        self.dungeonPos = list(self.setEntryAt("Downstairs"))
        self.enemyList = []

    def setEntryAt(self,entry="Entrance"):
        if entry == "Entrance":
            enterPoint = self.dungeonMap.entrance
        elif entry == "Downstairs":
            enterPoint = self.dungeonMap.downStairs
        return enterPoint
        #if self.dungeonMap.map[enterPoint[0]-1][enterPoint[1]] == FLOOR_CHAR:
        #    return ((enterPoint[0]-1,enterPoint[1]))
        #if self.dungeonMap.map[enterPoint[0]][enterPoint[1]+1] == FLOOR_CHAR:
        #    return ((enterPoint[0],enterPoint[1]+1))
        #if self.dungeonMap.map[enterPoint[0]+1][enterPoint[1]] == FLOOR_CHAR:
        #    return ((enterPoint[0]+1,enterPoint[1]))
        #if self.dungeonMap.map[enterPoint[0]][enterPoint[1]-1] == FLOOR_CHAR:
        #    return ((enterPoint[0],enterPoint[1]-1))
        
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
    
    def enemyHandler(self):
        defeatedEnemy = -1
        if len(self.enemyList) < math.ceil(len(self.dungeonMap.rooms)/4):
            newEnemy = Enemy(self.dungeonMap.getRandomEnemySpawnCoords(self.dungeonPos),self.dungeonMap)
            self.enemyList.append(newEnemy)
        for i, enemy in enumerate(self.enemyList):
            enemy.tickEnemy()
            if enemy.actReady:
                if self.getDistance(self.dungeonPos,enemy.coords) <= enemy.fov and (enemy.mode == "patrol" or enemy.mode == "return"):
                    enemy.mode = "hunt"
                elif self.getDistance(self.dungeonPos,enemy.coords) > enemy.huntFov and enemy.mode == "hunt":
                    enemy.mode = "return"
                enemy.act(self.dungeonPos)
                if enemy.coords == self.dungeonPos:
                    encounter = []
                    encounter = self.game.directory.buildEncounter(self.dungeonMap.dungeonLevel,Biome.Other)
                    self.combat.initialize(encounter)
                    defeatedEnemy = i
        if defeatedEnemy != -1:
            self.enemyList.pop(defeatedEnemy)
        if self.combat.defeat:
            self.inDungeon = False

    def stepTo(self,r,c):
        #print(f'({r}, {c})')
        if self.dungeonMap.map[r][c] == ENTRANCE_CHAR:
            self.inDungeon = False
        elif self.dungeonMap.map[r][c] == LOOT_CHAR:
            self.state = "lootSummary"
        elif self.dungeonMap.map[r][c] == WANDERER_CHAR:
            self.state = "wandererSummary"
        elif self.dungeonMap.map[r][c] == STAIRS_DOWN_CHAR:
            self.nextFloor()
        elif self.dungeonMap.map[r][c] == STAIRS_UP_CHAR:
            self.previousFloor()
        else:
            self.state = "main"

    def getDistance(self,start,target):
        return (abs(start[0]-target[0]) + abs(start[1]-target[1]))
    
    def lootLookup(self):
        for loot in self.dungeonMap.loot:
            if loot.coords[0] == self.dungeonPos[0] and loot.coords[1] == self.dungeonPos[1]:
                return loot
        print("Uh oh")
        return "Uh oh"


class Enemy():
    def __init__(self,coords,dungeonMap):
        self.patrolPoints = coords
        self.coords = list(self.patrolPoints[0])
        self.tick = 0
        self.speed = DUNGEON_ENEMY_SPEED
        self.mode = "patrol"
        self.fov = 6
        self.huntFov = 10
        self.map = dungeonMap
        self.path = []
        self.huntPath = []
        self.pathIndex = 0
        self.huntIndex = []
        self.actReady = False
        self.returnPathSet = False
        self.pathfind(self.patrolPoints[0],self.patrolPoints[1],self.path)
        self.pathfind(self.patrolPoints[1],self.patrolPoints[2],self.path)
        self.pathfind(self.patrolPoints[2],self.patrolPoints[0],self.path)

    def tickEnemy(self):
        self.setSpeed()
        self.tick += 1
        if self.tick >= self.speed:
            self.actReady = True
            self.tick = 0

    def setSpeed(self):
        if self.mode == "patrol" or self.mode == "return":
            self.speed = DUNGEON_ENEMY_SPEED
        elif self.mode == "hunt":
            self.speed = DUNGEON_ENEMY_SPEED/2

    def act(self,coords):
        self.actReady = False
        if self.mode == "patrol":
            self.patrol()
        if self.mode == "hunt":
            self.hunt(coords)
        if self.mode == "return":
            self.returnToPath()

    def patrol(self):
        self.pathIndex += 1
        if self.pathIndex >= len(self.path):
            self.pathIndex = 0
        self.coords = list(self.path[self.pathIndex])

    def hunt(self,target):
        self.huntPath = []
        self.pathfind(tuple(self.coords),tuple(target),self.huntPath)
        if len(self.huntPath) > 1:
            self.coords = list(self.huntPath[1])

    def returnToPath(self):
        if self.returnPathSet == False:
            self.huntPath = []
            self.huntIndex = 0
            self.pathfind(tuple(self.coords),tuple(self.path[self.pathIndex]),self.huntPath)
        self.huntIndex += 1
        if self.huntIndex >= len(self.huntPath):
            self.huntIndex = 0
            self.mode = "patrol"
        self.coords = list(self.huntPath[self.huntIndex])
        
    def pathfind(self,start,target,path):
        pathfinder = Pathfinder(start,target,self.map)
        path += pathfinder.calculatePath()

class Pathfinder():
    def __init__(self,start,end,map):
        self.startPoint = start
        self.endPoint = end
        self.map = map
        self.path = []
        self.workingPath = set()

    def calculatePath(self):
        path = self.bfs(self.startPoint)
        return path
    
    def isValid(self,row,col):
        return self.map.map[row][col] != self.map.wallChar

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
