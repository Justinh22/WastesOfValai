import pygame
from directory import *
from overworld import *

class PlayerData():
    def __init__(self,startPos,directory):
        self.currentPos = startPos
        self.party = Party()
        self.party.initializeMembers(directory)