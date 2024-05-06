import pygame
import random
import math
from directory import *

WELL_WALL = '='
PYRAMID_WALL = '+'
BANDIT_WALL = 'X'
CAVE_WALL = '&'
RUINS_WALL = '%'
TREEHOUSE_WALL = '~'
FLOOR_CHAR = ' '
ENTRANCE_CHAR = 'O'
LOOT_CHAR = 'L'
WANDERER_CHAR = 'W'

directory = Directory()


class DungeonDatabase():
    def __init__(self):
        self.dungeons = {}

    def addDungeon(self,coords,dungeon):
        self.dungeons[coords] = dungeon

    def getDungeon(self,coords,type,level=0,hallFreq=2):
        if coords not in self.dungeons.keys():
            newDungeon = DungeonMap(coords,type,level,hallFreq)
            newDungeon.generate()
            self.addDungeon(coords,newDungeon)
        return self.dungeons[coords]
    
    def doesExist(self,coords):
        return coords in self.dungeons.keys()
    
    def printContents(self):
        for entry in self.dungeons:
            print(f'{entry}: {self.dungeons[entry].dungeonType.name}')


class DungeonMap():
    def __init__(self,coords,type=DungeonType.Well,level=0,hallFreq=2):
        self.map = []
        self.coords = coords        # Coords         : Duple containing (row,col) of where the dungeon is located in the world
        self.rooms = []             # Rooms          : List of DungeonRooms
        self.entranceRoom = -1
        self.connectedRooms = {}    # ConnectedRooms : Dictionary of indexes in rooms, depicting how many connections each room has
        self.visited = []
        self.dungeonLevel = level
        self.dungeonType = type
        self.hallwayFreq = hallFreq
        self.maxRows = DUNGEON_DIM
        self.maxCols = DUNGEON_DIM
        self.minRooms = 6
        self.maxRooms = 12
        self.minRoomCols = 4
        self.maxRoomCols = 8
        self.minRoomRows = 4
        self.maxRoomRows = 8
        self.roomBuffer = 1
        self.entrance = (0,0)
        self.loot = []
        self.wallChar = self.getWallChar(type)

    def getWallChar(self,type):
        if type == DungeonType.Well:
            return WELL_WALL
        elif type == DungeonType.Pyramid:
            return PYRAMID_WALL
        elif type == DungeonType.BanditCamp:
            return BANDIT_WALL
        elif type == DungeonType.Cave:
            return CAVE_WALL
        elif type == DungeonType.Ruins:
            return RUINS_WALL
        elif type == DungeonType.Treehouse:
            return TREEHOUSE_WALL

    def initializeMap(self):
        for i in range(0,self.maxRows):
            row = []
            for j in range(0,self.maxCols):
                row.append(self.wallChar)
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
        numRooms = random.randint(self.minRooms,self.maxRooms)
        for i in range(numRooms):
            coords = self.makeRoom()
            self.fitRoom(coords,20)
        for room in self.rooms:
            print(room.toString())
        self.buildHallways(self.hallwayFreq)
        self.addEntrance()
        numLoot = math.ceil(numRooms/3) + random.choice([-1,0,0,0,1,1])
        self.addLoot(numLoot)
        if random.randint(0,2) == 2:
            self.addWanderer()
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
                #print(f'Connecting room {i}')
                closestRooms = self.findNClosestRooms(i,n)
                for closeRoom in closestRooms:
                    self.connect(i,closeRoom)
        self.ensureAllRoomsConnect()
        #print(self.connectedRooms)

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
        #print(f'Closest rooms are {lowestNIndexes}')
        return lowestNIndexes

    def connect(self,indexA,indexB):
        #print(f'Connecting {indexA} to {indexB}')
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
        repeat = True
        n = 1
        while repeat:
            print("Ensuring...")
            repeat = False
            for index in self.connectedRooms.keys():
                self.visited = [0]*len(self.rooms)
                self.dfs(index)
                if 0 in self.visited:
                    #print(f'Not all nodes reachable from {index}')
                    timeout = 0
                    while(timeout<10):
                        closest = self.findNClosestRooms(index,n)
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

    def addEntrance(self):
        connections = 1
        done = False
        while done == False:
            for i in range(len(self.connectedRooms)):
                if len(self.connectedRooms[i]) == connections:
                    self.entrance = self.rooms[i].setEntrance(self.map)
                    self.entranceRoom = self.rooms[i].getCoords()
                    #print(f'Entrance in room at {self.entranceRoom}')
                    done = True
                    break
            connections += 1

    def addLoot(self,lootCount):
        lootRooms = self.rooms
        random.shuffle(lootRooms)
        for i in range(lootCount):
            if lootRooms[i].getCoords() == self.entranceRoom:
                continue
            types = self.getLootTypesFromDungeonType()
            self.loot.append(DungeonLoot(lootRooms[i].setLoot(self.map),self.dungeonLevel,types))
            #print(f'Loot in room {i}')

    def addWanderer(self):
        possRooms = self.rooms
        random.shuffle(possRooms)
        for i in range(len(possRooms)):
            if possRooms[i].getCoords() == self.entranceRoom:
                continue
            possRooms[i].setWanderer(self.map)
            break
            #print(f'Loot in room {i}')

    def removeLoot(self,loot):
        for i in range(len(self.loot)):
            if loot.coords == self.loot[i].coords:
                self.loot.pop(i)
                self.map[loot.coords[0]][loot.coords[1]] = ' '
                self.writeMap()
                break

    def getRandomEnemySpawnCoords(self,pos):
        possRooms = self.rooms
        random.shuffle(possRooms)
        patrolPoints = []
        while len(patrolPoints) <= 3:
            room = random.randint(0,len(possRooms)-1)
            if possRooms[room].getCoords() == self.entranceRoom:
                continue
            if possRooms[room] != self.entranceRoom:
                point = possRooms[room].getRandomPoint()
                if abs(pos[0]-point[0])+abs(pos[1]-point[1]) < 12:
                    continue
                patrolPoints.append(possRooms[room].getRandomPoint())
        return patrolPoints

    def getLootTypesFromDungeonType(self):
        # As of now, all dungeons are capable of containing the same loot
        return [Type.Weapon, Type.Weapon, Type.Armor, Type.Armor, Type.Potion, Type.AtkSpell, Type.SptSpell]


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
    
    def setEntrance(self,map):
        coords = self.getRandomPoint()
        map[coords[0]][coords[1]] = ENTRANCE_CHAR
        return coords

    def setLoot(self,map):
        coords = self.getRandomPoint()
        map[coords[0]][coords[1]] = LOOT_CHAR
        return coords
    
    def setWanderer(self,map):
        coords = self.getRandomPoint()
        map[coords[0]][coords[1]] = WANDERER_CHAR
        return coords
    

class DungeonLoot():
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