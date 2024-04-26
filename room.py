import pygame
import random
from feature import *

class RoomDatabase():
    def __init__(self):
        self.rooms = {}                 # Dictionary of {(int, int): Room} : Complete list of all implemented Rooms in the world, organized by coords

    def addRoom(self,coords,room):
        self.rooms[coords] = room

    def getRoom(self,coords,difficulty,type="room"):
        if coords not in self.rooms.keys(): # If the requested room has not yet been implemented, implement it and store in dictionary
            newRoom = Room(coords,difficulty,type)
            self.addRoom(coords,newRoom)
        return self.rooms[coords]
    
    def doesExist(self,coords):
        return (coords in self.rooms.keys())
        
    def printContents(self):
        for entry in self.rooms:
            print(f'{entry}: {self.rooms[entry].type}')


class Room():
    def __init__(self,coords,difficulty,type="room",id=-1):
        self.coords = coords            # (int, int) : Contains row and column coordinates of this room
        self.id = id                    # int : Numeric id of this room
        self.description = ""           # String : Contains written description of the room
        self.difficulty = difficulty    # int : Difficulty of the biome this room is in
        self.features = []              # List of Feature : Contains all Features in the room
        self.type = type
        if self.type == "room":
            self.implementRoomTemplate(self.id,difficulty)
        elif self.type == "haven":
            self.implementHaven(self.id,difficulty)

    def implementRoomTemplate(self,id,difficulty):
        if id == -1:
            id = templateList.randomId()
        template = templateList.getRoomTemplate(id)
        templateList.markAsSeen(id)
        self.description = template.description
        for featID in template.features:
            feat = featureList.getFeature(featID)
            feat.rollForLoot(difficulty)
            self.features.append(feat)

    def implementHaven(self,id,difficulty):
        if id == -1:
            id = templateList.randomHavenId()
        template = templateList.getHavenTemplate(id)
        self.description = template.description
        for featID in template.features:
            feat = featureList.getFeature(featID)
            feat.rollForLoot(difficulty)
            self.features.append(feat)


class RoomTemplate():
    def __init__(self,id,desc="",feats=[]):
        self.id = id
        self.description = desc         # String : Contains written description of the room
        self.features = feats           # List of int : Contains ids of features to be contained in the implementation of this room

class RoomTemplateList():
    def __init__(self):
        self.roomTemplateList = []      # List of RoomTemplate : Complete directory of all RoomTemplates
        self.havenTemplateList = []
        self.initRoomTemplateList()
        self.initHavenTemplateList()
        self.roomSeenList = [False for i in range(len(self.roomTemplateList))]

    def getRoomTemplate(self,id):
        return self.roomTemplateList[id] # This will only work as long as the ids in the roomTemplateList align with their index.
    
    def getHavenTemplate(self,id):
        return self.havenTemplateList[id]
    
    def randomId(self):
        good = False
        bruteForceCount = 10
        for bruteForceVal in range(0,bruteForceCount): # Attempt brute force room guess up to bruteForceCount times
            id = random.randint(0,len(self.roomTemplateList)-1)
            if self.roomSeenList[id] == False:
                good = True
                break
        if good == False: # If brute force failed, gather all possible rooms and choose one at random
            roomOptions = []
            for idOption in range(0,len(self.roomTemplateList)):
                if self.roomSeenList[idOption] == False:
                    roomOptions.append(idOption)
            id = roomOptions[random.randint(0,len(roomOptions)-1)]
        return id
    
    def randomHavenId(self):
        return random.randint(0,len(self.havenTemplateList)-1)
    
    def markAsSeen(self,id):
        self.roomSeenList[id] = True # This will only work as long as the ids in the roomTemplateList align with their index.
        if False not in self.roomSeenList:
            self.roomSeenList = [False for i in range(len(self.roomTemplateList))] # Reset roomSeenList

    def initRoomTemplateList(self):
######################################################################## ROOM LIST #########################################################################################
        R0 = RoomTemplate(0,"You enter a quaint wooden cabin. An old wooden table stands atop a tattered rug, just before a roaring hearth at the back of the room. A chest sits in the corner of the room.",[0,2,3,14])
        self.roomTemplateList.append(R0)

        R1 = RoomTemplate(1,"You enter a room with walls and floors of stone. A desk sits at its center, with an open spellbook atop it. Shimmering runes adorn the walls.",[1,9,10,17])
        self.roomTemplateList.append(R1)

        R2 = RoomTemplate(2,"You enter an old hunting cabin. A hearth is lit at the back of the cabin with a painting hanging above it. A suit of armor stands against the opposite wall, next to a weapon rack. The floorboards creak under your feet.",[4,7,14,random.randint(15,16),18])
        self.roomTemplateList.append(R2)

        R3 = RoomTemplate(3,"You enter a metal chamber with a cold atmostphere. A few metal shelves climb the walls, and in the middle of the floor you see a lockbox sitting on a table, with black slime creeping up its legs. You hear a faint whispering...",[8,11,12,19,20])
        self.roomTemplateList.append(R3)

        R4 = RoomTemplate(4,"You enter an empty room with a stone altar at its center. The walls are impossibly smooth, contrasting the cobblestone floor. An ancient scroll sits atop the altar.",[5,13,21,22])
        self.roomTemplateList.append(R4)
############################################################################################################################################################################

    def initHavenTemplateList(self):
        R0 = RoomTemplate(0,"You enter a cozy wooden shack. The roaring fire in the hearth warms your bones, and beds along the wall offer you a quiet place to rest.",[23,14])
        self.havenTemplateList.append(R0)

        R1 = RoomTemplate(1,"You enter a cozy wooden shack. The roaring fire in the hearth warms your bones, and beds along the wall offer you a quiet place to rest. A wanderer sits by the fire.",[23,14,24])
        self.havenTemplateList.append(R1)

featureList = FeatureList()
templateList = RoomTemplateList()