import pygame
from directory import *
from overworld import *

class PlayerData():
    def __init__(self,startPos,directory,hostel):
        self.currentPos = startPos
        self.party = Party()
        self.gold = 0
        self.charNum = 100
        self.party.initializeMembers(directory,self.getNewCharID())
        self.hostel = hostel
        self.lastCheckpoint = (0,0)
    def printContents(self):
        for member in self.party.members:
            print(member.name)
        for member in self.hostel:
            print(member.name)
    def getNewCharID(self):
        self.charNum += 1
        return self.charNum-1
    def awardGold(self,diff):
        gold = (diff * 5) + (round(diff/2) * random.randint(0,4))
        self.gold += gold
        return gold