import pygame
import random

class Map():
    def __init__(self):
        self.map = []
        self.revealedMap = []
        self.sizeR = 200
        self.sizeC = 400
        self.startingPos = (0,0)
        self.finishPos = (0,0)

    def loadMap(self):
        with open("generated_map.txt","r") as file:
            for row in file:
                self.map.append(row)
        with open("revealed_map.txt","r") as file:
            for row in file:
                self.revealedMap.append(row.strip())
                
        #Setting starting position...
        r = random.randint(round(self.sizeR/3),round((self.sizeR/3)*2))
        c = random.randint(round(self.sizeC/3),round((self.sizeR/3)*2))
        while self.map[r][c] == ' ':
            r = random.randint(round(self.sizeR/3),round((self.sizeR/3)*2))
            c = random.randint(round(self.sizeC/3),round((self.sizeR/3)*2))
        self.startingPos = (r,c)

    def generateMap(self):
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
        self.grow(50)
        print("Smoothing corners...")
        self.smoothCorners()
        self.border()

        #Setting starting position...
        r = random.randint(round(self.sizeR/3),round((self.sizeR/3)*2))
        c = random.randint(round(self.sizeC/3),round((self.sizeR/3)*2))
        while self.map[r][c] == ' ':
            r = random.randint(round(self.sizeR/3),round((self.sizeR/3)*2))
            c = random.randint(round(self.sizeC/3),round((self.sizeR/3)*2))
        self.startingPos = (r,c)

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

        self.ensurePath(r,c)
        print("Generating landmarks...")
        self.placeLandmarks(1000)

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
        landmarks = num
        for i in range(0,landmarks):
            r = random.randint(1,self.sizeR-1)
            c = random.randint(1,self.sizeC-1)
            sel = random.randint(1,5)
            if self.map[r][c] == '.':
                if sel == 1:
                    self.map[r][c] = 'W' # Well
                elif sel == 2:
                    self.map[r][c] = 'P' # Pyramid
                elif sel == 3:
                    self.map[r][c] = 'H' # Sinkhole
                else:
                    self.map[r][c] = 'S' # Shack
            if self.map[r][c] == ';':
                if sel == 1:
                    self.map[r][c] = 'A' # Abandoned Cabin
                elif sel == 2:
                    self.map[r][c] = 'C' # Cave
                elif sel == 3:
                    self.map[r][c] = 'B' # Bandit Camp
                else:
                    self.map[r][c] = 'S' # Shack
            if self.map[r][c] == '#':
                if sel == 1:
                    self.map[r][c] = 'R' # Ruins
                elif sel == 2:
                    self.map[r][c] = 'T' # Treehouse
                elif sel == 3:
                    self.map[r][c] = 'G' # Shrine
                else:
                    self.map[r][c] = 'S' # Shack

    def saveRevealed(self):
        with open("revealed_map.txt","w") as file:
            for row in self.revealedMap:
                for element in row:
                    file.write(element)
                file.write("\n")