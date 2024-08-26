import pygame
import random
import math
from directory import *

BUILDING_HEIGHT = 4
BUILDING_WIDTH = 7
PATH_FREQUENCY = 2

BUILDING_WALL = '='
BUILDING_DOOR = 'O'
PATH_CHAR = '%'

FOREST_CHAR = '#'
PLAINS_CHAR = ';'
DESERT_CHAR = '.'

directory = Directory()


class VillageDatabase():
    def __init__(self):
        self.villages = {}

    def addVillage(self,coords,village):
        self.villages[coords] = village

    def getVillage(self,coords,type,level,biome):
        if coords not in self.villages.keys():
            newVillage = VillageMap(coords,level,type,biome)
            newVillage.generate()
            self.addVillage(coords,newVillage)
        return self.villages[coords]
    
    def doesExist(self,coords):
        return coords in self.villages.keys()
    
    def printContents(self):
        for entry in self.villages:
            print(f'{entry}: {self.villages[entry].villageType.name}')


class VillageMap():
    def __init__(self,coords,level,type,biome):
        self.map = []
        self.coords = coords        # Coords         : Duple containing (row,col) of where the village is located in the world
        self.buildings = []         # Buildings      : List of VillageRooms
        self.entranceRoom = -1
        self.connectedRooms = {}    # ConnectedRooms : Dictionary of indexes in rooms, depicting how many connections each room has
        self.visited = []
        self.villageLevel = level
        self.villageType = type
        self.minBuildings = 0
        self.maxBuildings = 0
        if type is VillageType.Village:
            self.setBuildingNumberRange(4,6)
            self.maxRows = VILLAGE_DIM
            self.maxCols = VILLAGE_DIM
        elif type is VillageType.Town:
            self.setBuildingNumberRange(7,9)
            self.maxRows = TOWN_DIM
            self.maxCols = TOWN_DIM
        elif type is VillageType.City:
            self.setBuildingNumberRange(10,12)
            self.maxRows = CITY_DIM
            self.maxCols = CITY_DIM
        self.buildingBuffer = 3
        self.entranceSide = "None"
        self.entrance = (0,0)
        self.floorChar = self.getFloorChar(biome)
        self.pathFreq = PATH_FREQUENCY

    def initializeMap(self):
        for i in range(0,self.maxRows):
            row = []
            for j in range(0,self.maxCols):
                row.append(self.floorChar)
            self.map.append(row)

    def getFloorChar(self,biome):
        if biome is Biome.Forest:
            return FOREST_CHAR
        elif biome is Biome.Plains:
            return PLAINS_CHAR
        elif biome is Biome.Desert:
            return DESERT_CHAR

    def setBuildingNumberRange(self,min,max):
        self.minBuildings = min
        self.maxBuildings = max

    def generate(self):
        self.initializeMap()
        numBuildings = random.randint(self.minBuildings,self.maxBuildings)
        for i in range(numBuildings):
            self.fitBuilding(20)
        for room in self.buildings:
            print(room.toString())
        self.buildPathways(self.pathFreq)
        self.addEntrance()
        numLoot = math.ceil(numBuildings/3) + random.choice([-1,0,0,0,1,1])
        self.addLoot(numLoot)
        if random.randint(0,2) == 2:
            self.addWanderer()
        self.writeMap()

    def writeMap(self):
        filename = "villages/" + str(self.coords[0]) + "_" + str(self.coords[1]) + "_village.txt"
        with open(filename,"w") as file:
            for row in self.map:
                for element in row:
                    file.write(element)
                file.write("\n")

    def makeBuilding(self):
        rows = random.randint(self.minRoomRows,self.maxRoomRows)
        cols = random.randint(self.minRoomCols,self.maxRoomCols)
        return (rows,cols)
    
    def fitBuilding(self,attempts=100):
        success = False
        for i in range(attempts):
            testRow = random.randint(self.roomBuffer,self.maxRows-BUILDING_HEIGHT-self.roomBuffer)
            testCol = random.randint(self.roomBuffer,self.maxCols-BUILDING_WIDTH-self.roomBuffer)
            # print(f'Trying to make a room at {testRow}, {testCol}, with dimensions {size[0]}x{size[1]}')
            success = self.checkBuildingFit(testRow,testCol)
            if success:
                self.buildings.append(VillageBuilding(testRow,testCol))
                self.placeBuilding(testRow,testCol)
                break
            
    def checkBuildingFit(self,testR,testC):
        for i in range(testR-self.roomBuffer,(testR+BUILDING_HEIGHT)+self.roomBuffer):
            for j in range(testC-self.roomBuffer,(testC+BUILDING_WIDTH)+self.roomBuffer):
                if self.map[i][j] == BUILDING_WALL:
                    return False
        return True
    
    def placeBuilding(self,testR,testC):
        for i in range(testR,testR+BUILDING_HEIGHT):
            for j in range(testC,testC+BUILDING_WIDTH):
                self.map[i][j] = BUILDING_WALL

    def buildPathways(self,n):
        for i in range(len(self.buildings)):
            if i not in self.connectedRooms:
                #print(f'Connecting room {i}')
                closestRooms = self.findNClosestBuildings(i,n)
                for closeRoom in closestRooms:
                    self.connect(i,closeRoom)
        self.ensureAllBuildingsConnect()
        #print(self.connectedRooms)

    def findNClosestBuildings(self,roomIndex,n):
        lowestNDistances = []
        lowestNIndexes = []
        for i in range(len(self.buildings)):
            if i == roomIndex:
                continue
            distance = self.buildings[roomIndex].getDistanceFrom(self.buildings[i].getCoords())
            if len(lowestNDistances) < n:
                lowestNDistances.append(distance)
                lowestNIndexes.append(i)
            elif distance < max(lowestNDistances):
                lowestNDistances[lowestNDistances.index(max(lowestNDistances))] = distance
                lowestNIndexes[lowestNDistances.index(max(lowestNDistances))] = i
        #print(f'Closest rooms are {lowestNIndexes}')
        return lowestNIndexes

    def connect(self,indexA,indexB):
        #print(f'Connecting {indexA} to {indexB}')
        connA = self.buildings[indexA].getRandomPoint()
        connB = self.buildings[indexB].getRandomPoint()
        if random.randint(1,2) == 1:

            if connA[1] < connB[1]:
                for i in range(connA[1],connB[1]+1):
                    self.map[connA[0]][i] = PATH_CHAR
            else:
                for i in range(connB[1],connA[1]+1):
                    self.map[connA[0]][i] = PATH_CHAR
            if connA[0] < connB[0]:
                for i in range(connA[0],connB[0]+1):
                    self.map[i][connB[1]] = PATH_CHAR
            else:
                for i in range(connB[0],connA[0]+1):
                    self.map[i][connB[1]] = PATH_CHAR

        else:
            
            if connA[0] < connB[0]:
                for i in range(connA[0],connB[0]+1):
                    self.map[i][connB[1]] = PATH_CHAR
            else:
                for i in range(connB[0],connA[0]+1):
                    self.map[i][connB[1]] = PATH_CHAR
            if connA[1] < connB[1]:
                for i in range(connA[1],connB[1]+1):
                    self.map[connA[0]][i] = PATH_CHAR
            else:
                for i in range(connB[1],connA[1]+1):
                    self.map[connA[0]][i] = PATH_CHAR

        if indexA in self.connectedRooms:
            self.connectedRooms[indexA].append(indexB)
        else:
            self.connectedRooms[indexA] = [indexB]

        if indexB in self.connectedRooms:
            self.connectedRooms[indexB].append(indexA)
        else:
            self.connectedRooms[indexB] = [indexA]

    def ensureAllBuildingsConnect(self):
        repeat = True
        n = 1
        while repeat:
            print("Ensuring...")
            repeat = False
            for index in self.connectedRooms.keys():
                self.visited = [0]*len(self.buildings)
                self.dfs(index)
                if 0 in self.visited:
                    #print(f'Not all nodes reachable from {index}')
                    timeout = 0
                    while(timeout<10):
                        closest = self.findNClosestBuildings(index,n)
                        if closest not in self.connectedRooms[index]:
                            self.connect(closest[0],index)
                            timeout = 10
                        timeout += 1
                    repeat = True
                    n += 1

    def dfs(self,node):
        #print(node)
        self.visited[node] = 1
        for connection in self.connectedRooms[node]:
            if self.visited[connection] == 0:
                self.dfs(connection)


class VillageBuilding():
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.height = BUILDING_HEIGHT
        self.width = BUILDING_WIDTH
    
    def getDoorway(self):
        return (self.row+3,self.col)
    
    def toString(self):
        return "(" + str(self.row) + "," + str(self.col) + ") to (" + str(self.row+self.height) + "," + str(self.col+self.width) + ")"
    
    def getCoords(self):
        return ((self.row,self.col))
    
    def getDistanceFrom(self,coords):
        return abs(self.row-coords[0]) + abs(self.col-coords[1])
    
    def setEntrance(self,map):
        coords = self.getRandomPoint()
        map[coords[0]][coords[1]] = BUILDING_DOOR
        return coords
    

class VillageLoot():
    def __init__(self,coords,level,types):
        self.coords = coords
        self.level = level
        self.types = types
        self.rarity = LootRarity.Uncommon
        self.loot = self.rollItem(directory)

    def setLootRarity(self,rarity):
        self.rarity = rarity

    def rollItem(self,dir):
        return dir.rollForLoot(self.level,self.rarity,self.types)