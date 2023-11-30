import pygame
from combat import *
from pausemenu import *
from directory import *
from writing import *
from dungeonmapgenerator import *

ENEMY_VISION_KERNAL = []
ENEMY_VISION_KERNAL.append( [ 0 , 0 , 40, 0 , 0 ] )
ENEMY_VISION_KERNAL.append( [ 0 , 2 , 25, 2 , 0 ] )
ENEMY_VISION_KERNAL.append( [ 0 , 3 , 15, 3 , 0 ] )
ENEMY_VISION_KERNAL.append( [ 1 , 2 , 10, 2 , 1 ] )
ENEMY_VISION_KERNAL.append( [ 1 , 2 , 5 , 2 , 1 ] )

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
        self.enemyStepTick = 0
        self.enemyStepSpeed = 100
        self.enemyList = []

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
    
    def enemyHandler(self):
        if self.enemyStepTick < self.enemyStepSpeed:
            self.enemyStepTick += 1
        else:
            print("tick")
            self.enemyStepTick = 0
            if len(self.enemyList) < 2:
                newEnemy = Enemy(self.dungeonMap.getRandomEnemySpawnCoords(),self.dungeonMap)
                self.enemyList.append(newEnemy)
                return
            for enemy in self.enemyList:
                enemy.patrol()

    def stepTo(self,r,c):
        print(f'({r}, {c})')
        if self.dungeonMap.map[r][c] == 'O':
            self.inDungeon = False


class Enemy():
    def __init__(self,coords,dungeonMap):
        self.coords = list(coords)
        self.mode = "patrol"
        self.confidence = 0
        self.submode = "walk"
        self.fov = 10
        self.patrolDir = "north"
        self.map = dungeonMap

    def patrol(self):
        self.confidence -= 1
        if self.confidence <= 0:
            decision = random.randint(1,2)
            if decision == 1:
                self.submode == "walk"
            elif decision == 2:
                self.submode == "turn"
            self.confidence = 5

        if self.submode == "turn":
            self.patrolDir = self.checkForTurnChoice()
        if self.isFeasible(self.patrolDir):
            self.coords = self.nextSpace()
            self.patrolDir = self.checkForTurnChoice()
        else:
            feas = []
            feas.append(self.scanInDir("north"))
            feas.append(self.scanInDir("east"))
            feas.append(self.scanInDir("south"))
            feas.append(self.scanInDir("west"))
            self.turnBias(feas)
            best = feas.index(min(feas))
            if best == 0:
                self.patrolDir = "north"
            elif best == 1:
                self.patrolDir = "east"
            elif best == 2:
                self.patrolDir = "south"
            elif best == 3:
                self.patrolDir = "west"

    def turnBias(self,feas):
        if self.patrolDir == "north":
            feas[1] -= 10
            feas[3] -= 10
        elif self.patrolDir == "east":
            feas[0] -= 10
            feas[2] -= 10
        elif self.patrolDir == "south":
            feas[1] -= 10
            feas[3] -= 10
        elif self.patrolDir == "west":
            feas[0] -= 10
            feas[2] -= 10

    def checkForTurnChoice(self):
        valid = True
        direction = "none"
        straightStepper = 1
        leftStepper = 1
        rightStepper = 1
        if self.patrolDir == "north":
            while valid:
                if self.map.map[self.coords[0]][self.coords[1]-leftStepper] != ' ':
                    valid = False
                leftStepper += 1
            valid = True
            while valid:
                if self.map.map[self.coords[0]][self.coords[1]+rightStepper] != ' ':
                    valid = False
                rightStepper += 1
            valid = True
            while valid:
                if self.map.map[self.coords[0]-straightStepper][self.coords[1]] != ' ':
                    valid = False
                straightStepper += 1
        elif self.patrolDir == "east":
            while valid:
                if self.map.map[self.coords[0]-leftStepper][self.coords[1]] != ' ':
                    valid = False
                leftStepper += 1
            valid = True
            while valid:
                if self.map.map[self.coords[0]+rightStepper][self.coords[1]] != ' ':
                    valid = False
                rightStepper += 1
            valid = True
            while valid:
                if self.map.map[self.coords[0]][self.coords[1]+straightStepper] != ' ':
                    valid = False
                straightStepper += 1
        elif self.patrolDir == "south":
            while valid:
                if self.map.map[self.coords[0]][self.coords[1]+leftStepper] != ' ':
                    valid = False
                leftStepper += 1
            valid = True
            while valid:
                if self.map.map[self.coords[0]][self.coords[1]-rightStepper] != ' ':
                    valid = False
                rightStepper += 1
            valid = True
            while valid:
                if self.map.map[self.coords[0]+straightStepper][self.coords[1]] != ' ':
                    valid = False
                straightStepper += 1
        elif self.patrolDir == "west":
            while valid:
                if self.map.map[self.coords[0]+leftStepper][self.coords[1]] != ' ':
                    valid = False
                leftStepper += 1
            valid = True
            while valid:
                if self.map.map[self.coords[0]-rightStepper][self.coords[1]] != ' ':
                    valid = False
                rightStepper += 1
            valid = True
            while valid:
                if self.map.map[self.coords[0]][self.coords[1]-straightStepper] != ' ':
                    valid = False
                straightStepper += 1
        threshold = 4 + random.randint(0,2)
        if leftStepper > rightStepper and leftStepper >= threshold and leftStepper > straightStepper:
            direction = "left"
            print("Turning left")
        elif rightStepper >= leftStepper and rightStepper >= threshold and rightStepper > straightStepper:
            direction = "right"
            print("Turning right")
        if direction == "none":
            print("Staying straight")
        return self.getTurn(self.patrolDir,direction)

    #def hunt(self):

    def getTurn(self,dir,turn):
        if dir == "north":
            if turn == "left":
                return "west"
            elif turn == "right":
                return "east"
            else:
                return "north"
        if dir == "east":
            if turn == "left":
                return "north"
            elif turn == "right":
                return "south"
            else:
                return "east"
        if dir == "south":
            if turn == "left":
                return "east"
            elif turn == "right":
                return "west"
            else:
                return "south"
        if dir == "west":
            if turn == "left":
                return "south"
            elif turn == "right":
                return "north"
            else:
                return "west"

    def nextSpace(self):
        if self.patrolDir == "north":
            return ((self.coords[0]-1,self.coords[1]))
        elif self.patrolDir == "east":
            return ((self.coords[0],self.coords[1]+1))
        elif self.patrolDir == "south":
            return ((self.coords[0]+1,self.coords[1]))
        elif self.patrolDir == "west":
            return ((self.coords[0],self.coords[1]-1))
        
    def isFeasible(self,dir):
        return self.scanInDir(dir) < 40
        
    def scanInDir(self,dir):
        feasibility = 0
        for i in range(5):
            for j in range(5):
                if dir == "north":
                    feasibility += self.checkKernal((self.coords[0]-i-1,self.coords[1]-j-2),(i,j))
                elif dir == "east":
                    feasibility += self.checkKernal((self.coords[0]-i-2,self.coords[1]+j+1),(i,j))
                elif dir == "south":
                    feasibility += self.checkKernal((self.coords[0]+i+1,self.coords[1]-j-2),(i,j))
                elif dir == "west":
                    feasibility += self.checkKernal((self.coords[0]-i-2,self.coords[1]-j-1),(i,j))
        print(f'Feasibility: {feasibility}')
        return feasibility
                    
    def checkKernal(self,mapCoords,kernalCoords):
        if mapCoords[0] > len(self.map.map)-1 or mapCoords[0] < 0 or mapCoords[1] > len(self.map.map[0])-1 or mapCoords[1] < 0:
            return 0
        if self.map.map[mapCoords[0]][mapCoords[1]] == self.map.wallChar:
            return ENEMY_VISION_KERNAL[kernalCoords[0]][kernalCoords[1]]
        else:
            return 0