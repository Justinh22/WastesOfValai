import pygame
from directory import *
from overworld import *

class PlayerData():
    def __init__(self,startPos,directory,hostel):
        self.currentPos = startPos
        self.party = Party()
        self.party.initializeMembers(directory)
        self.hostel = hostel
    def printContents(self):
        for member in self.party.members:
            print(member.name)
        for member in self.hostel:
            print(member.name)