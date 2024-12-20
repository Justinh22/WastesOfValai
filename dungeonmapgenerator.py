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
STAIRS_DOWN_CHAR = 'D'
STAIRS_UP_CHAR = 'U'

directory = Directory()


class DungeonDatabase():
    def __init__(self):
        self.dungeons = {}

    def addDungeon(self,coords,dungeon):
        self.dungeons[coords] = dungeon

    def getDungeon(self,coords,type,level=0,floors=-1):
        if coords not in self.dungeons.keys():
            if floors == -1:
                floors = random.randint(1,DUNGEON_MAX_FLOORS)
            print(f'{floors} floors in dungeon')
            newDungeon = Dungeon(coords,type,level,floors)
            self.addDungeon(coords,newDungeon)
        return self.dungeons[coords]
    
    def doesExist(self,coords):
        return coords in self.dungeons.keys()
    
    def printContents(self):
        for entry in self.dungeons:
            print(f'{entry}: {self.dungeons[entry].dungeonType.name}')


class Dungeon():
    def __init__(self,coords,type,level,floors):
        self.name = getRandomDungeonName(type)
        self.coords = coords
        self.dungeonType = type
        self.dungeonLevel = level
        self.floors = floors
        self.floorMaps = []
        self.generate()

    def generate(self):
        for i in range(self.floors):
            newDungeonMap = DungeonMap(self.coords,self.dungeonType,self.dungeonLevel,i+1,self.floors)
            newDungeonMap.generate()
            self.floorMaps.append(newDungeonMap)

    def getFloor(self,num):
        if num <= self.floors and num > 0:
            return self.floorMaps[num-1]
        else:
            return None


class DungeonMap():
    def __init__(self,coords,type,level,floor,maxFloors):
        self.map = []
        self.coords = coords        # Coords         : Duple containing (row,col) of where the dungeon is located in the world
        self.rooms = []             # Rooms          : List of DungeonRooms
        self.entranceRoom = -1
        self.downStairsRoom = -1
        self.connectedRooms = {}    # ConnectedRooms : Dictionary of indexes in rooms, depicting how many connections each room has
        self.floor = floor
        self.maxFloors = maxFloors
        self.visited = []
        self.dungeonLevel = level
        self.dungeonType = type
        self.hallwayFreq = 2
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
        self.downStairs = (0,0)
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
        print(f'GENERATING FLOOR {self.floor} MAP')
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
        if self.floor != self.maxFloors:
            self.addDownStairs()
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
                    if self.floor == 1:
                        self.entrance = self.rooms[i].setEntrance(self.map)
                    else:
                        self.entrance = self.rooms[i].setUpStairs(self.map)
                    self.entranceRoom = self.rooms[i].getCoords()
                    #print(f'Entrance in room at {self.entranceRoom}')
                    done = True
                    break
            connections += 1

    def addDownStairs(self):
        connections = 1
        done = False
        while done == False:
            for i in range(len(self.connectedRooms)):
                if len(self.connectedRooms[i]) == connections and self.rooms[i].getCoords() != self.entranceRoom:
                    self.downStairs = self.rooms[i].setDownStairs(self.map)
                    print(f'Downstairs: {self.downStairs}')
                    self.downStairsRoom = self.rooms[i].getCoords()
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
            self.loot.append(DungeonLoot(lootRooms[i].setLoot(self.map),self.dungeonLevel,types,self.floor,self.maxFloors))
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
        return [Type.Weapon, Type.Weapon, Type.Armor, Type.Armor, Type.Potion, Type.Consumable, Type.AtkSpell, Type.SptSpell]


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
    
    def setUpStairs(self,map):
        coords = self.getRandomPoint()
        map[coords[0]][coords[1]] = STAIRS_UP_CHAR
        return coords
    
    def setDownStairs(self,map):
        coords = self.getRandomPoint()
        map[coords[0]][coords[1]] = STAIRS_DOWN_CHAR
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
    def __init__(self,coords,level,types,floor,maxFloors):
        self.coords = coords
        self.level = level
        self.types = types
        self.maxFloors = maxFloors
        self.checkForAccessories(floor/maxFloors)
        self.rarity = self.getRarity(floor/maxFloors)
        if self.rarity == LootRarity.Rare and random.randint(1,5) == 5:
            self.loot = directory.getMagicWeapon(self.level)
        else:
            self.loot = self.rollItem(directory)

    def checkForAccessories(self,ratio):
        if ratio >= (1/2) and self.maxFloors >= 2:
            self.types.append(Type.Accessory)

    def getRarity(self,ratio):
        if self.maxFloors >= 3:
            if ratio <= (2/3):
                return LootRarity.Uncommon
            else:
                return LootRarity.Rare
        else:
            return LootRarity.Uncommon

    def setLootRarity(self,rarity):
        self.rarity = rarity

    def rollItem(self,dir):
        return dir.rollForLoot(self.level,self.rarity,self.types)
        
def getRandomDungeonName(type):
    #
    # D - Dungeon Word
    # o - of
    # A - Adjective
    # t - the
    # N - Noun
    #
    nameFormats = ["DotAN","AD","DoN","DotN","tDoN","tDoAN","tAD"]
    dungeonNameString = ""
    nameFormat = random.choice(nameFormats)
    for char in nameFormat:
        if dungeonNameString != "":
            dungeonNameString += " "
        if char == "D":
            dungeonword = []
            if type == DungeonType.Well:
                dungeonword += ["Tunnels",
                                "Well",
                                "Catacombs",
                                "City"]
            elif type == DungeonType.Pyramid:
                dungeonword += ["Tomb",
                                "Pyramid",
                                "Labyrinth"]
            elif type == DungeonType.BanditCamp:
                dungeonword += ["Camp",
                                "Stronghold",
                                "Hideout",
                                "Lair"]
            elif type == DungeonType.Cave:
                dungeonword += ["Tunnels",
                                "Cavern",
                                "Cave",
                                "Hive",
                                "Pit"]
            elif type == DungeonType.Ruins:
                dungeonword += ["Ruins",
                                "City",
                                "Wreckage",
                                "Fortress"]
            elif type == DungeonType.Treehouse:
                dungeonword += ["Treehouse",
                                "Canopy",
                                "Lair",
                                "Treetops"]
            dungeonNameString += random.choice(dungeonword)
        elif char == "o":
            dungeonNameString += "of"
        elif char == "A":
            adjective = ["Flaming",
                         "Lost",
                         "Arcane",
                         "Archmage's",
                         "Dead King's",
                         "Twisted",
                         "Frigid",
                         "Vacant",
                         "Old",
                         "Dead Queen's",
                         "Familiar",
                         "Overgrown",
                         "Crumbling"]
            dungeonNameString += random.choice(adjective)
        elif char == "t":
            if dungeonNameString == "":
                dungeonNameString += "The"
            else:
                dungeonNameString += "the"
        elif char == "N":
            noun = ["Souls",
                    "Bones",
                    "Skulls",
                    "Killers",
                    "Decayed",
                    "Fae",
                    "Kobolds",
                    "Dragon",
                    "Bandits",
                    "Mistakes",
                    "Curses"]
            dungeonNameString += random.choice(noun)
    return dungeonNameString