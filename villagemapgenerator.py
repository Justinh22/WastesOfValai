import pygame
import random
import math
from directory import *
from pathfinder import Pathfinder
from constants import *
from buildings import *

PATH_FREQUENCY = 2

VILLAGE_PATH_BRANCHES = 4
TOWN_PATH_BRANCHES = 7
CITY_PATH_BRANCHES = 10

directory = Directory()


class VillageDatabase():
    def __init__(self):
        self.villages = {}

    def addVillage(self,coords,village):
        self.villages[coords] = village
        print(f'Villages: {self.villages}')

    def getVillage(self,coords,level,biome):
        if coords not in self.villages.keys():
            typ = self.getVillageType()
            newVillage = VillageMap(coords,level,typ,biome)
            newVillage.generate()
            self.addVillage(coords,newVillage)
        return self.villages[coords]
    
    def doesExist(self,coords):
        return coords in self.villages.keys()
    
    def printContents(self):
        for entry in self.villages:
            print(f'{entry}: {self.villages[entry].villageType.name}')

    def getVillageType(self):
        randomNum = random.randint(1,6)
        if randomNum <= 3:
            return VillageType.Village
        elif randomNum <= 5:
            return VillageType.Town
        elif randomNum == 6:
            return VillageType.City


class VillageMap():
    def __init__(self,coords,level,typ,biome):
        self.map = []
        self.name = getRandomVillageName(typ)
        self.coords = coords        # Coords         : Duple containing (row,col) of where the village is located in the world
        self.buildings = []         # Buildings      : List of Buildings
        self.visited = []
        self.villageLevel = level
        self.villageType = typ
        self.groundChar = self.getGroundChar(biome)
        self.minBuildings = 0
        self.maxBuildings = 0
        self.firstPriorityBuildings = [VillageBuildings.Inn, VillageBuildings.BlackMarket, VillageBuildings.Forge, VillageBuildings.RuneCarver]
        self.shopBuildings = [VillageBuildings.Weaponsmith, VillageBuildings.Armory, VillageBuildings.GeneralStore, VillageBuildings.Library, VillageBuildings.Temple]
        if self.villageType is VillageType.Village:
            self.setBuildingNumberRange(3,4)
            self.maxRows = VILLAGE_DIM
            self.maxCols = VILLAGE_DIM
        elif self.villageType is VillageType.Town:
            self.setBuildingNumberRange(5,6)
            self.maxRows = TOWN_DIM
            self.maxCols = TOWN_DIM
        else:
            self.setBuildingNumberRange(7,9)
            self.maxRows = CITY_DIM
            self.maxCols = CITY_DIM
        self.buildingBuffer = 3
        self.entranceSide = "None"
        self.entrance = (round(self.maxRows/2),3)
        self.pathFreq = PATH_FREQUENCY
        self.branches = self.getPathBranches()

    def initializeMap(self):
        for i in range(0,self.maxRows):
            row = []
            for j in range(0,self.maxCols):
                row.append(self.groundChar)
            self.map.append(row)

    def getGroundChar(self,biome):
        if biome is Biome.Forest:
            return FOREST_CHAR
        elif biome is Biome.Plains:
            return PLAINS_CHAR
        elif biome is Biome.Desert:
            return DESERT_CHAR
        return None
        
    def getPathBranches(self):
        print(self.villageType)
        if self.villageType == VillageType.Village.value:
            return VILLAGE_PATH_BRANCHES
        elif self.villageType == VillageType.Town.value:
            return TOWN_PATH_BRANCHES
        elif self.villageType == VillageType.City.value:
            return CITY_PATH_BRANCHES
        return None

    def setBuildingNumberRange(self,min,max):
        self.minBuildings = min
        self.maxBuildings = max

    def generate(self):
        self.initializeMap()
        numBuildings = random.randint(self.minBuildings,self.maxBuildings)
        self.buildPathways()
        for i in range(numBuildings):
            self.fitBuilding(20)
        random.shuffle(self.buildings)
        for building in self.buildings:
            building.setEntrance(self.map)
        self.connectBuildingsToPath()
        self.addEntrance()
        self.writeMap()

    def writeMap(self):
        filename = "villages/" + str(self.coords[0]) + "_" + str(self.coords[1]) + "_village.txt"
        with open(filename,"w") as file:
            for row in self.map:
                for element in row:
                    file.write(element)
                file.write("\n")
    
    def fitBuilding(self,attempts=20):
        success = False
        for i in range(attempts):
            testRow = random.randint(self.buildingBuffer,self.maxRows-BUILDING_HEIGHT-self.buildingBuffer)
            testCol = random.randint(self.buildingBuffer,self.maxCols-BUILDING_WIDTH-self.buildingBuffer)
            success = self.checkBuildingFit(testRow,testCol)
            if success:
                if len(self.firstPriorityBuildings) > 0:
                    chance = self.firstPriorityBuildings.pop(random.randint(0,len(self.firstPriorityBuildings)-1))
                else:
                    if len(self.shopBuildings) > 0:
                        chance = self.shopBuildings.pop(random.randint(0,len(self.shopBuildings)-1))
                    else:
                        self.shopBuildings = [VillageBuildings.Weaponsmith, VillageBuildings.Armory, VillageBuildings.GeneralStore, VillageBuildings.Library, VillageBuildings.Temple]
                        chance = self.shopBuildings.pop(random.randint(0,len(self.shopBuildings)-1))
                if chance == VillageBuildings.Forge:
                    self.buildings.append(Forge(testRow,testCol,self.villageLevel))
                elif chance == VillageBuildings.Weaponsmith:
                    self.buildings.append(Weaponsmith(testRow,testCol,self.villageLevel))
                elif chance == VillageBuildings.Armory:
                    self.buildings.append(Armory(testRow,testCol,self.villageLevel))
                elif chance == VillageBuildings.GeneralStore:
                    self.buildings.append(GeneralStore(testRow,testCol,self.villageLevel))
                elif chance == VillageBuildings.Library:
                    self.buildings.append(Library(testRow,testCol,self.villageLevel))
                elif chance == VillageBuildings.Temple:
                    self.buildings.append(Temple(testRow,testCol,self.villageLevel))
                elif chance == VillageBuildings.BlackMarket:
                    self.buildings.append(BlackMarket(testRow,testCol,self.villageLevel))
                elif chance == VillageBuildings.Inn:
                    self.buildings.append(Inn(testRow,testCol,self.villageLevel))
                elif chance == VillageBuildings.RuneCarver:
                    self.buildings.append(RuneCarver(testRow,testCol,self.villageLevel))
                self.placeBuilding(testRow,testCol)
                break
            
    def checkBuildingFit(self,testR,testC):
        for i in range(testR-self.buildingBuffer,(testR+BUILDING_HEIGHT)+self.buildingBuffer):
            for j in range(testC-self.buildingBuffer,(testC+BUILDING_WIDTH)+self.buildingBuffer):
                if self.map[i][j] == BUILDING_WALL or self.map[i][j] == BUILDING_ROOF or self.map[i][j] == PATH_CHAR:
                    return False
        return True
    
    def placeBuilding(self,testR,testC):
        for i in range(testR,testR+BUILDING_HEIGHT):
            for j in range(testC,testC+BUILDING_WIDTH):
                if i < (testR+BUILDING_HEIGHT/2):
                    self.map[i][j] = BUILDING_ROOF
                else:
                    self.map[i][j] = BUILDING_WALL

    def buildPathways(self):
        burnout = 0
        currentR = self.entrance[0]
        currentC = self.entrance[1]
        for i in range(round(self.maxCols/2)):
            self.map[currentR][currentC] = PATH_CHAR
            currentC += 1

    def connectBuildingsToPath(self):
        for building in self.buildings:
            closestPath = self.findClosestValidPath(building)
            self.connect(building,closestPath)

    def findClosestValidPath(self,building):
        minDistance = 100
        pathCoords = (0,0)
        for rowIndex, row in enumerate(self.map):
            for colIndex, element in enumerate(row):
                if minDistance > building.getDistanceFrom((rowIndex,colIndex)) and element == PATH_CHAR:
                    found = True
                    minDistance = building.getDistanceFrom((rowIndex,colIndex))
                    pathCoords = (rowIndex,colIndex)
        return pathCoords

    def connect(self,building,pathCoords):
        pathfinder = Pathfinder(building.getOutsideDoorway(),pathCoords,self.map)
        pathfinder.setObstacle(BUILDING_WALL)
        pathfinder.setObstacle(BUILDING_ROOF)
        path = pathfinder.calculatePath()
        if path is not None:
            for step in path:
                self.map[step[0]][step[1]] = PATH_CHAR

    def addEntrance(self):
        return (random.randint(0,self.maxRows),0)
    
def getRandomVillageName(type):
    villageNameString = ""
    villageNames = [
        "Coalfell",
        "Windemire",
        "Brightflower",
        "Axton",
        "Plonerro",
        "Waxon",
        "Flestigo",
        "Rhythagon",
        "Barkstead",
        "Wirecross",
        "Fhestinom",
        "Khilrow",
        "Refuge",
        "Mayrest",
        "Buerathey",
        "Chapelside",
        "Khantegos",
        "Road's End",
        "Callarnock",
        "Arton",
        "Greyhand",
        "Wommiwool",
        "Tallirite",
        "Ulvo",
        "Zyxic"
    ]
    villageNameString += random.choice(villageNames) + " " + type.name
    return villageNameString