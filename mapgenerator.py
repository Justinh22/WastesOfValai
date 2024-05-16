import pygame
import random
import math
from constants import *
from writing import *

class Map():
    def __init__(self):
        self.map = []
        self.revealedMap = []
        self.difficultyMap = []
        self.sizeR = MAP_HEIGHT
        self.sizeC = MAP_WIDTH
        self.startingPos = (0,0)
        self.finishPos = (0,0)
        self.startingZone = 2


    def loadMap(self,startR=-1,startC=-1):
        with open("generated_map.txt","r") as file:
            for row in file:
                self.map.append(row)
        with open("revealed_map.txt","r") as file:
            for row in file:
                self.revealedMap.append(row.strip())
        with open("difficulty_map.txt","r") as file:
            for row in file:
                self.difficultyMap.append(row)
                
        if startR == -1 and startC == -1:
            self.startingPos = (round(self.sizeR/2),round(self.sizeC/2))
            while self.map[self.startingPos[0]][self.startingPos[1]] == ' ':
                if self.startingPos[0] > round(self.sizeR/3):
                    self.startingPos = (self.startingPos[0]-1, self.startingPos[1])
                else:
                    self.startingPos = (self.startingPos[0], self.startingPos[1]+1)
        else:
            self.startingPos = (startR,startC)


    def generateMap(self,startingZone=1):
        row = []
        revealedRow = []
        for i in range(0,self.sizeR):
            for j in range(0,self.sizeC):
                randomChar = random.randint(1,4)
                if randomChar == 1:
                    row.append('#')
                elif randomChar == 2:
                    row.append(';')
                elif randomChar == 3:
                    row.append('.')
                else:
                    row.append(' ')
                revealedRow.append('0')
            self.map.append(row)
            self.revealedMap.append(revealedRow)
            row = []
            revealedRow = []
        print("Building map...")
        self.grow(MAP_GROWTH_CYCLES)
        print("Smoothing corners...")
        self.smoothCorners()
        print("Generate difficulty map...")
        self.genDifficultyMapBiomes()
        self.border()

        # Setting starting point...
        potentialStartPoints = []
        while potentialStartPoints == []:
            startingZoneChar = self.valToLetter(startingZone)
            for r in range(1,self.sizeR-1):
                for c in range(1,self.sizeC-1):
                    if self.difficultyMap[r][c] != startingZoneChar:
                        continue
                    for coords in [(-1,0), (0,-1), (1,0), (0,1)]:
                        if self.map[r+coords[0]][c+coords[1]] == ' ' or self.difficultyMap[r+coords[0]][c+coords[1]] != startingZoneChar:
                            continue
                    potentialStartPoints.append((r,c))
            if potentialStartPoints == []:
                startingZone += 1

        self.startingPos = random.choice(potentialStartPoints)

        endSet = random.randint(1,8)
        if endSet == 1:
            randRA = 5
            randRB = round(self.sizeR/3)
            randCA = 5
            randCB = round(self.sizeC/3)
        elif endSet == 2:
            randRA = 5
            randRB = round(self.sizeR/3)
            randCA = round(self.sizeC/3)
            randCB = round((self.sizeC/3)*2)
        elif endSet == 3:
            randRA = 5
            randRB = round(self.sizeR/3)
            randCA = round((self.sizeC/3)*2)
            randCB = round(self.sizeC-5)
        elif endSet == 4:
            randRA = round(self.sizeR/3)
            randRB = round((self.sizeR/3)*2)
            randCA = 5
            randCB = round(self.sizeC/3)
        elif endSet == 5:
            randRA = round(self.sizeR/3)
            randRB = round((self.sizeR/3)*2)
            randCA = round((self.sizeC/3)*2)
            randCB = round(self.sizeC-5)
        elif endSet == 6:
            randRA = round((self.sizeR/3)*2)
            randRB = round(self.sizeR-5)
            randCA = 5
            randCB = round(self.sizeC/3)
        elif endSet == 7:
            randRA = round((self.sizeR/3)*2)
            randRB = round(self.sizeR-5)
            randCA = round(self.sizeC/3)
            randCB = round((self.sizeC/3)*2)
        else:
            randRA = round((self.sizeR/3)*2)
            randRB = round(self.sizeR-5)
            randCA = round((self.sizeC/3)*2)
            randCB = round(self.sizeC-5)

        #Setting tower position...
        rEnd = random.randint(randRA,randRB)
        cEnd = random.randint(randCA,randCB)
        while self.map[rEnd][cEnd] == ' ':
            rEnd = random.randint(randRA,randRB)
            cEnd = random.randint(randCA,randCB)
        self.map[rEnd][cEnd] = 'O'
        self.finishPos = (rEnd,cEnd)

        #Setting temple position...
        rEnd = random.randint(randRA,randRB)
        cEnd = random.randint(randCA,randCB)
        while self.map[-rEnd][-cEnd] == ' ':
            rEnd = random.randint(randRA,randRB)
            cEnd = random.randint(randCA,randCB)
        self.map[-rEnd][-cEnd] = 'V'

        print("Generating landmarks...")
        self.placeLandmarks(LANDMARK_COUNT)
        self.setFirstHaven()

        with open("generated_map.txt","w") as file:
            for row in self.map:
                for element in row:
                    file.write(element)
                file.write("\n")

        with open("revealed_map.txt","w") as file:
            for row in self.revealedMap:
                for element in row:
                    file.write(element)
                file.write("\n")

        with open("difficulty_map.txt","w") as file:
            for row in self.difficultyMap:
                for element in row:
                    file.write(element)
                file.write("\n")


    def grow(self,cycles):
        r_first = 1
        r_last = self.sizeR-1
        c_first = 1
        c_last = self.sizeC-1
        vert = 0
        for cycle in range(0,cycles):
            print(f'{round((cycle/cycles)*100)}%')
            if vert < cycles/2:
                for r in range(r_first,r_last):
                    for c in range(c_first,c_last):
                        neighbors = self.getNeighbors(r,c)
                        self.map[r][c] = max(neighbors, key=neighbors.get)
            else:
                for c in range(c_first,c_last):
                    for r in range(r_first,r_last):
                        neighbors = self.getNeighbors(r,c)
                        self.map[r][c] = max(neighbors, key=neighbors.get)
            vert += 1


    def getNeighbors(self,r,c):
        neighbors = {}
        order = list(range(1,5))
        random.shuffle(order)
        for i in order:
            if i == 1:
                if self.map[r-1][c] not in neighbors:
                    neighbors[self.map[r-1][c]] = 1
                else:
                    neighbors[self.map[r-1][c]] += 1
            elif i == 2:
                if self.map[r][c+1] not in neighbors:
                    neighbors[self.map[r][c+1]] = 1
                else:
                    neighbors[self.map[r][c+1]] += 1
            elif i == 3:
                if self.map[r+1][c] not in neighbors:
                    neighbors[self.map[r+1][c]] = 1
                else:
                    neighbors[self.map[r+1][c]] += 1
            else:
                if self.map[r][c-1] not in neighbors:
                    neighbors[self.map[r][c-1]] = 1
                else:
                    neighbors[self.map[r][c-1]] += 1
        return neighbors


    def smoothCorners(self):
        for r in range(1,self.sizeR-1):
            for c in range(1,self.sizeC-1):
                if (self.map[r][c]==self.map[r-1][c] and self.map[r][c]==self.map[r-1][c+1] and self.map[r][c]==self.map[r][c+1] and self.map[r][c]!=self.map[r+1][c] and self.map[r][c]!=self.map[r][c-1]):
                    self.map[r][c] = self.map[r+1][c]
                elif (self.map[r][c]==self.map[r][c+1] and self.map[r][c]==self.map[r+1][c+1] and self.map[r][c]==self.map[r+1][c] and self.map[r][c]!=self.map[r-1][c] and self.map[r][c]!=self.map[r][c-1]):
                    self.map[r][c] = self.map[r][c-1]
                elif (self.map[r][c]==self.map[r+1][c] and self.map[r][c]==self.map[r+1][c-1] and self.map[r][c]==self.map[r][c-1] and self.map[r][c]!=self.map[r-1][c] and self.map[r][c]!=self.map[r][c+1]):
                    self.map[r][c] = self.map[r-1][c]
                elif (self.map[r][c]==self.map[r][c-1] and self.map[r][c]==self.map[r-1][c-1] and self.map[r][c]==self.map[r-1][c] and self.map[r][c]!=self.map[r+1][c] and self.map[r][c]!=self.map[r][c+1]):
                    self.map[r][c] = self.map[r][c+1]


    def border(self):
        for i in range(0,self.sizeR):
            self.map[i][0] = 'X'
            self.map[i][self.sizeC-1] = 'X'
        for i in range(0,self.sizeC):
            self.map[self.sizeR-1][i] = 'X'
            self.map[0][i] = 'X'


    def ensurePath(self,r,c): #Try looking from ocean tiles at top and following them down
        return True


    def placeLandmarks(self,num):
        rooms = math.ceil(num * (.5))
        dungeons = math.ceil(num * (.2))
        havens = math.ceil(num * (.3))
        
        roomList = self.pseudoRandomPlacement(rooms)
        for room in roomList:
            randomVal = random.randint(1,3)
            if randomVal == 1:
                self.map[room[0]][room[1]] = 'A' # Abandoned Camp
            else:
                self.map[room[0]][room[1]] = 'S' # Shack

        dungeonList = self.pseudoRandomPlacement(dungeons)
        for dungeon in dungeonList:
            randomVal = random.randint(1,2)
            if self.map[dungeon[0]][dungeon[1]] == '.':
                if randomVal == 1:
                    self.map[dungeon[0]][dungeon[1]] = 'W' # Well
                elif randomVal == 2:
                    self.map[dungeon[0]][dungeon[1]] = 'P' # Pyramid
            elif self.map[dungeon[0]][dungeon[1]] == ';':
                if randomVal == 1:
                    self.map[dungeon[0]][dungeon[1]] = 'B' # Bandit Camp
                elif randomVal == 2:
                    self.map[dungeon[0]][dungeon[1]] = 'C' # Cave
            elif self.map[dungeon[0]][dungeon[1]] == '#':
                if randomVal == 1:
                    self.map[dungeon[0]][dungeon[1]] = 'R' # Ruins
                elif randomVal == 2:
                    self.map[dungeon[0]][dungeon[1]] = 'T' # Treehouse

        havenList = self.pseudoRandomPlacement(havens)
        for haven in havenList:
            self.map[haven[0]][haven[1]] = 'H' # Haven


    def pseudoRandomPlacement(self,num):
        rows = cols = math.floor(math.sqrt(num))
        quadrantSizeR = math.ceil(MAP_HEIGHT / math.ceil(math.sqrt(num)))
        quadrantSizeC = math.ceil(MAP_WIDTH / math.ceil(math.sqrt(num)))
        r = 0
        c = 0
        count = 0
        coordsList = []
        randomQuadOn = False
        burnout = 50
        while count < num or burnout <= 0:
            upperBoundR = quadrantSizeR*(r+1)
            if upperBoundR >= MAP_HEIGHT:
                upperBoundR = MAP_HEIGHT-1
            upperBoundC = quadrantSizeC*(c+1)
            if upperBoundC >= MAP_WIDTH:
                upperBoundC = MAP_WIDTH-1

            targetR = random.randint(quadrantSizeR*r, upperBoundR)
            targetC = random.randint(quadrantSizeC*c, upperBoundC)
            if self.map[targetR][targetC] == ' ' or self.map[targetR][targetC] == 'X':
                burnout -= 1
                continue
            burnout = 50
            coordsList.append((targetR,targetC))

            if not randomQuadOn:
                c += 1
                if c >= cols:
                    c = 0
                    r += 1
                    if r >= rows:
                        randomQuadOn = True
            else:
                r = random.randint(0,rows-1)
                c = random.randint(0,cols-1)
            count += 1
        
        return coordsList


    def saveRevealed(self):
        with open("revealed_map.txt","w") as file:
            for row in self.revealedMap:
                for element in row:
                    file.write(element)
                file.write("\n")


    def saveWorld(self):
        with open("generated_map.txt","w") as file:
            print("Saving...")
            for i, row in enumerate(self.map):
                #print(f'Writing row {i}: Length {len(row)}. Last element: {row[-1]}')
                for element in row:
                    if element != '\n':
                        file.write(element)
                file.write("\n")

    
    def setFirstHaven(self):
        good = False
        while not good:
            rowMod = random.choice([-2,-1,1,2])
            colMod = random.choice([-2,-1,1,2])
            if self.map[self.startingPos[0]+rowMod][self.startingPos[1]+colMod] != ' ':
                self.map[self.startingPos[0]+rowMod][self.startingPos[1]+colMod] = 'H'
                good = True


    def genDifficultyMapBiomes(self):
        radius = 1
        diff = 1
        biomeList = []
        self.difficultyMap = [ [0]*self.sizeC for i in range(self.sizeR)]
        startingPoint = (round(self.sizeR/2),round(self.sizeC/2))
        currentBiome = self.map[startingPoint[0]][startingPoint[1]]
        while (startingPoint[0] + radius < self.sizeR) or (startingPoint[0] - radius >= self.sizeR) or (startingPoint[1] + radius < self.sizeC) or (startingPoint[1] - radius >= self.sizeC):
            r, c = (startingPoint[0] - radius), (startingPoint[1] - radius)
            currentBiome = self.map[r][c]
            biomeList.clear()
            biomeList.append(currentBiome)
            self.difficultyMap[r][c] = diff
            #self.printCoords(r,c)
            while r < startingPoint[0] + radius:
                if r < self.sizeR-1:
                    r += 1
                else:
                    break
                #self.printCoords(r,c)
                currentBiome = self.map[r][c]
                if currentBiome != biomeList[-1] and self.difficultyMap[r][c] == 0:
                    diff = self.checkDiffAtCoords((r,c))
                    self.spread(self.sizeR, self.sizeC, r, c, currentBiome, diff)
                diff = self.difficultyMap[r][c]
            while c < startingPoint[1] + radius:
                if c < self.sizeC-1:
                    c += 1
                else:
                    break
                #self.printCoords(r,c)
                currentBiome = self.map[r][c]
                if currentBiome != biomeList[-1] and self.difficultyMap[r][c] == 0:
                    diff = self.checkDiffAtCoords((r,c))
                    self.spread(self.sizeR, self.sizeC, r, c, currentBiome, diff)
                diff = self.difficultyMap[r][c]
            while r >= startingPoint[0] - radius:
                if r > 0:
                    r -= 1
                else:
                    break
                #self.printCoords(r,c)
                currentBiome = self.map[r][c]
                if currentBiome != biomeList[-1] and self.difficultyMap[r][c] == 0:
                    diff = self.checkDiffAtCoords((r,c))
                    self.spread(self.sizeR, self.sizeC, r, c, currentBiome, diff)
                diff = self.difficultyMap[r][c]
            while c > startingPoint[1] - radius:
                if c > 0:
                    c -= 1
                else:
                    break
                #self.printCoords(r,c)
                currentBiome = self.map[r][c]
                if currentBiome != biomeList[-1] and self.difficultyMap[r][c] == 0:
                    diff = self.checkDiffAtCoords((r,c))
                    self.spread(self.sizeR, self.sizeC, r, c, currentBiome, diff)
                diff = self.difficultyMap[r][c]
            radius += 1

        for r in range(len(self.difficultyMap)):
            for c in range(len(self.difficultyMap[0])):
                if self.difficultyMap[r][c] < 1 or self.difficultyMap[r][c] > MAX_DIFFICULTY:
                    diff = self.checkDiffAtCoords((r,c))
                    self.spread(self.sizeR, self.sizeC, r, c, self.difficultyMap[r][c], diff)

        valMap = self.difficultyMap
        self.difficultyMap = []

        for r in range(len(valMap)):
            line = ""
            for c in range(len(valMap[0])):
                letter = self.valToLetter(valMap[r][c])
                if self.map[r][c] == ' ':
                    letter = ' '
                line += letter
            self.difficultyMap.append(line)


    def printCoords(self,r,c):
        print(f'({r},{c})')


    def genDifficultyMapUniform(self):
        for r in range(0,self.sizeR):
            row = []
            for c in range(0,self.sizeC):
                row.append(self.checkDiffAtCoords((r,c)))
            self.difficultyMap.append(row)


    def checkDiffAtCoords(self,coords):
        r, c = coords[0], coords[1]
        scaledR, scaledC = abs(r-(round(self.sizeR/2))), abs(c-(round(self.sizeC/2)))
        divisionValR, divisionValC = (round(self.sizeR/2)) / MAX_DIFFICULTY, (round(self.sizeC/2)) / MAX_DIFFICULTY
        difficultyValR = math.ceil(scaledR / divisionValR)
        difficultyValC = math.ceil(scaledC / divisionValC)
        return max(difficultyValR,difficultyValC)
    

    def isInMap(self,r,c):
        if r >= 0 and r < self.sizeR and c >= 0 and c < self.sizeC:
            return True
        return False


    def isValid(self, m, n, r, c, biome, diff):
        if r<0 or r>= m or c<0 or c>= n or self.map[r][c] != biome or self.difficultyMap[r][c] == diff:
            return False
        return True
 

    def spread(self, m, n, r, c, biome, diff):
        queue = []
        queue.append([r, c])
        self.difficultyMap[r][c] = diff

        while queue:
            currPixel = queue.pop()
            posX = currPixel[0]
            posY = currPixel[1]
            
            if self.isValid(m, n, posX + 1, posY, biome, diff):
                self.difficultyMap[posX+1][posY] = diff
                queue.append([posX+1, posY])
            
            if self.isValid(m, n, posX-1, posY, biome, diff):
                self.difficultyMap[posX-1][posY]= diff
                queue.append([posX-1, posY])
            
            if self.isValid(m, n, posX, posY + 1, biome, diff):
                self.difficultyMap[posX][posY+1]= diff
                queue.append([posX, posY+1])
            
            if self.isValid(m, n, posX, posY-1, biome, diff):
                self.difficultyMap[posX][posY-1]= diff
                queue.append([posX, posY-1])


    def valToLetter(self,val):
        return chr(val+64)
    

    def letterToVal(self,letter):
        return ord(letter)-64