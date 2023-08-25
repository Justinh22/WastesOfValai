import pygame;
import random;

class RoomDatabase():
    def __init__(self):
        self.rooms = {}
    def addRoom(self,coords,room):
        self.rooms[coords] = room
#   def save(self):
#       pickle it!

class Room():
    def __init__(self,coords,desc="",feat=[],loot=[]):
        self.coords = coords
        self.description = desc
        self.features = feat
        self.loot = loot