import pygame
import random
import math
from directory import *

WALL_CHAR = '='
FLOOR_CHAR = ' '
ENTRANCE_CHAR = 'O'
LOOT_CHAR = 'L'


class DungeonMap():
    def __init__(self,dir,coords,level=0,type=0,hallFreq=2):
        self.dir = dir
        self.map = []
        self.coords = coords        # Coords         : Duple containing (row,col)
        self.rooms = []             # Rooms          : List of DungeonRooms
        self.connectedRooms = {}    # ConnectedRooms : Dictionary of indexes in rooms, depicting how many connections each room has
        self.visited = []
        self.dungeonLevel = level
        self.dungeonType = type
        self.hallwayFreq = hallFreq
        self.maxRows = 40
        self.maxCols = 40
        self.minRooms = 6
        self.maxRooms = 12
        self.minRoomCols = 4
        self.maxRoomCols = 8
        self.minRoomRows = 4
        self.maxRoomRows = 8
        self.roomBuffer = 1
        self.entrance = (0,0)
        self.loot = []
        self.monsters = []

    def initializeMap(self):
        for i in range(0,self.maxRows):
            row = []
            for j in range(0,self.maxCols):
                row.append(WALL_CHAR)
            self.map.append(row)

    def setRoomSizeRange(self,minR,maxR,minC,maxC):
        self.minRoomCols = minC
        self.maxRoomCols = maxC
        self.minRoomRows = minR
        self.maxRoomRows = maxR

    def setRoomNumberRange(self,min,max):
        self.minRooms = min
        self.maxRooms = max

    def generate(self):
        self.initializeMap()
        for i in range(random.randint(self.minRooms,self.maxRooms)):
            coords = self.makeRoom()
            self.fitRoom(coords,20)
        for room in self.rooms:
            print(room.toString())
        self.buildHallways(self.hallwayFreq)
        self.writeMap()

    def writeMap(self):
        filename = "dungeons/" + str(self.coords[0]) + "_" + str(self.coords[1]) + "_dungeon.txt"
        with open(filename,"w") as file:
            for row in self.map:
                for element in row:
                    file.write(element)
                file.write("\n")

    def makeRoom(self):
        rows = random.randint(self.minRoomRows,self.maxRoomRows)
        cols = random.randint(self.minRoomCols,self.maxRoomCols)
        return (rows,cols)
    
    def fitRoom(self,size,attempts=100):
        success = False
        for i in range(attempts):
            testRow = random.randint(self.roomBuffer,self.maxRows-size[0]-self.roomBuffer)
            testCol = random.randint(self.roomBuffer,self.maxCols-size[1]-self.roomBuffer)
            # print(f'Trying to make a room at {testRow}, {testCol}, with dimensions {size[0]}x{size[1]}')
            success = self.checkRoomFit(testRow,testCol,size[0],size[1])
            if success:
                self.rooms.append(DungeonRoom(testRow,testCol,size[0],size[1]))
                self.placeRoom(testRow,testCol,size[0],size[1])
                break
            
    def checkRoomFit(self,testR,testC,sizeR,sizeC):
        for i in range(testR-self.roomBuffer,(testR+sizeR)+self.roomBuffer):
            for j in range(testC-self.roomBuffer,(testC+sizeC)+self.roomBuffer):
                if self.map[i][j] == FLOOR_CHAR:
                    return False
        return True
    
    def placeRoom(self,testR,testC,sizeR,sizeC):
        for i in range(testR,testR+sizeR):
            for j in range(testC,testC+sizeC):
                self.map[i][j] = FLOOR_CHAR

    def buildHallways(self,n):
        for i in range(len(self.rooms)):
            if i not in self.connectedRooms:
                print(f'Connecting room {i}')
                closestRooms = self.findNClosestRooms(i,n)
                for closeRoom in closestRooms:
                    self.connect(i,closeRoom)
        self.ensureAllRoomsConnect()
        print(self.connectedRooms)

    def findNClosestRooms(self,roomIndex,n):
        lowestNDistances = []
        lowestNIndexes = []
        for i in range(len(self.rooms)):
            if i == roomIndex:
                continue
            distance = self.rooms[roomIndex].getDistanceFrom(self.rooms[i].getCoords())
            if len(lowestNDistances) < n:
                lowestNDistances.append(distance)
                lowestNIndexes.append(i)
            elif distance < max(lowestNDistances):
                lowestNDistances[lowestNDistances.index(max(lowestNDistances))] = distance
                lowestNIndexes[lowestNDistances.index(max(lowestNDistances))] = i
        print(f'Closest rooms are {lowestNIndexes}')
        return lowestNIndexes

    def connect(self,indexA,indexB):
        print(f'Connecting {indexA} to {indexB}')
        connA = self.rooms[indexA].getRandomPoint()
        connB = self.rooms[indexB].getRandomPoint()
        if random.randint(1,2) == 1:

            if connA[1] < connB[1]:
                for i in range(connA[1],connB[1]+1):
                    self.map[connA[0]][i] = FLOOR_CHAR
            else:
                for i in range(connB[1],connA[1]+1):
                    self.map[connA[0]][i] = FLOOR_CHAR
            if connA[0] < connB[0]:
                for i in range(connA[0],connB[0]+1):
                    self.map[i][connB[1]] = FLOOR_CHAR
            else:
                for i in range(connB[0],connA[0]+1):
                    self.map[i][connB[1]] = FLOOR_CHAR

        else:
            
            if connA[0] < connB[0]:
                for i in range(connA[0],connB[0]+1):
                    self.map[i][connB[1]] = FLOOR_CHAR
            else:
                for i in range(connB[0],connA[0]+1):
                    self.map[i][connB[1]] = FLOOR_CHAR
            if connA[1] < connB[1]:
                for i in range(connA[1],connB[1]+1):
                    self.map[connA[0]][i] = FLOOR_CHAR
            else:
                for i in range(connB[1],connA[1]+1):
                    self.map[connA[0]][i] = FLOOR_CHAR

        if indexA in self.connectedRooms:
            self.connectedRooms[indexA].append(indexB)
        else:
            self.connectedRooms[indexA] = [indexB]

        if indexB in self.connectedRooms:
            self.connectedRooms[indexB].append(indexA)
        else:
            self.connectedRooms[indexB] = [indexA]

    def ensureAllRoomsConnect(self):
        for index in self.connectedRooms.keys():
            self.visited = [0]*len(self.rooms)
            self.dfs(index)
            if 0 in self.visited:
                print(f'Not all nodes reachable from {index}')
                timeout = 0
                while(timeout<10):
                    closest = self.findNClosestRooms(index,1)
                    if closest not in self.connectedRooms[index]:
                        self.connect(closest[0],index)
                        timeout = 10
                    timeout += 1
            else:
                print(f'All nodes reachable from {index}')

    def dfs(self,node):
        print(node)
        self.visited[node] = 1
        for connection in self.connectedRooms[node]:
            if self.visited[connection] == 0:
                self.dfs(connection)

    def addEntrance(self):
        for roomIndex in self.connectedRooms:
            if len(roomIndex) == 1:
                self.entrance = roomIndex.setEntrance()
                break
        self.entrance = self.connectedRooms[0].setEntrance()


class DungeonRoom():
    def __init__(self,row,col,height,width):
        self.row = row
        self.col = col
        self.height = height
        self.width = width
    
    def getRandomPoint(self):
        return ((random.randint(self.row+1,self.row+self.height-1), random.randint(self.col+1,self.col+self.width-1)))
    
    def toString(self):
        return "(" + str(self.row) + "," + str(self.col) + ") to (" + str(self.row+self.height) + "," + str(self.col+self.width) + ")"
    
    def getCoords(self):
        return ((self.row,self.col))
    
    def getDistanceFrom(self,coords):
        return abs(self.row-coords[0]) + abs(self.col-coords[1])
    
    def setEntrance(self):
        coords = self.getRandomPoint()
        self.map[coords[0]][coords[1]] = ENTRANCE_CHAR
        return coords

    def setLoot(self):
        coords = self.getRandomPoint()
        self.map[coords[0]][coords[1]] = LOOT_CHAR
        return coords
    

class DungeonLoot():
    def __init__(self,coords,level,types):
        self.coords = coords
        self.level = level
        self.types = types
        self.rarity = LootRarity.Uncommon
        self.loot = self.rollItem()

    def setLootRarity(self,rarity):
        self.rarity = rarity

    def rollItem(self):
        return self.dir.rollForLoot(self.level,self.rarity,self.types)