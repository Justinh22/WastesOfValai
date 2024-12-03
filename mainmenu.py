import sys
import pygame
from writing import *
from debug import *
from constants import *
import os
import glob

class MainMenu():
    def __init__(self,game):
        self.game = game
        self.displayRunning = True
        self.cursor = pygame.Rect(0,0,20,20)
        self.cursorState = "Start"
        self.debug_lv = 1
        self.debug_cls = -1
        self.debug_startingItems = []
        self.debug_startingGold = []
        self.startingZone = 1
        self.debugOps = []
        self.startPos = (self.game.width/2,self.game.height/2+30)
        self.loadPos = (self.game.width/2,self.game.height/2+50)
        self.quitPos = (self.game.width/2,self.game.height/2+70)
        self.cursor.midtop = (self.startPos[0]-100,self.startPos[1])

    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0,0))
        pygame.display.update()
        self.game.buttonReset()

    def display(self):
        self.displayRunning = True
        while self.displayRunning:
            self.game.eventHandler()
            self.getInput()
            self.game.screen.fill(self.game.black)
            self.game.write(50, self.game.width / 2, self.game.height / 2 - 50, "Wastes of Valai")
            self.game.write(20, self.startPos[0], self.startPos[1], "Venture Out")
            self.game.write(20, self.loadPos[0], self.loadPos[1], "Load Game")
            self.game.write(20, self.quitPos[0], self.quitPos[1], "Quit")
            self.game.write(20, self.cursor.x, self.cursor.y, "->")
            self.blitScreen()
        self.game.screen.fill(self.game.black)
        self.blitScreen()

    def getInput(self):
        self.cursorHandler()
        if self.game.keys["A"]:
            if self.cursorState == "Start":
                self.game.inGame = True
                self.displayRunning = False
                self.game.screen.fill(self.game.black)
                self.game.write(20, self.startPos[0], self.startPos[1], "Loading...")
                self.blitScreen()
                self.wipeDungeonDir()
                self.wipeVillageDir()
                for op in self.debugOps:
                    self.setDebug(op)
                self.executeDebug()
                self.game.WorldMap.generateMap(self.startingZone)
                print("Start!")
                print(self.game.WorldMap.startingPos)
            if self.cursorState == "Load":
                self.game.inGame = True
                self.displayRunning = False
                self.game.screen.fill(self.game.black)
                self.game.load()
                self.game.write(20, self.startPos[0], self.startPos[1], "Loading...")
                self.blitScreen()
                self.game.WorldMap.loadMap(self.game.player.currentPos[0],self.game.player.currentPos[1])
                print("Load!")
            if self.cursorState == "Quit":
                print("Quit!")
                pygame.quit()
                sys.exit()
        if self.game.keys["X"]:
            if "StartClass" not in self.debugOps:
                print("StartClass")
                self.debugOps.append("StartClass")
        if self.game.keys["Y"]:
            if "StartLevel" not in self.debugOps:
                print("StartLevel")
                self.debugOps.append("StartLevel")
        if self.game.keys["L"]:
            if "ManualEncounters" not in self.debugOps:
                print("ManualEncounters")
                self.debugOps.append("ManualEncounters")
        if self.game.keys["R"]:
            if "ManualLevelUp" not in self.debugOps:
                print("ManualLevelUp")
                self.debugOps.append("ManualLevelUp")
        if self.game.keys["START"]:
            if "StartingItems" not in self.debugOps:
                print("StartingItems")
                self.debugOps.append("StartingItems")
        if self.game.keys["SELECT"]:
            if "StartingZone" not in self.debugOps:
                print("StartingZone")
                self.debugOps.append("StartingZone")
        if self.game.keys["B"]:
            if "StartingGold" not in self.debugOps:
                print("StartingGold")
                self.debugOps.append("StartingGold")


    def cursorHandler(self):
        if self.game.keys["DOWN"]:
            if self.cursorState == "Start":
                self.cursor.midtop = (self.loadPos[0]-100, self.loadPos[1])
                self.cursorState = "Load"
            elif self.cursorState == "Load":
                self.cursor.midtop = (self.quitPos[0]-100, self.quitPos[1])
                self.cursorState = "Quit"
            elif self.cursorState == "Quit":
                self.cursor.midtop = (self.startPos[0]-100, self.startPos[1])
                self.cursorState = "Start"
        elif self.game.keys["UP"]:
            if self.cursorState == "Start":
                self.cursor.midtop = (self.quitPos[0]-100, self.quitPos[1])
                self.cursorState = "Quit"
            elif self.cursorState == "Load":
                self.cursor.midtop = (self.startPos[0]-100, self.startPos[1])
                self.cursorState = "Start"
            elif self.cursorState == "Quit":
                self.cursor.midtop = (self.loadPos[0]-100, self.loadPos[1])
                self.cursorState = "Load"

    def wipeDungeonDir(self):
        folder = 'dungeons/'
        for filename in os.listdir(folder):
            if filename.endswith('.txt'):
                os.remove(os.path.join(folder,filename))

    def wipeVillageDir(self):
        folder = 'villages/'
        for filename in os.listdir(folder):
            if filename.endswith('.txt'):
                os.remove(os.path.join(folder,filename))

    def setDebug(self,typ):
        if typ == "StartLevel":
            self.debug_lv = getDebug(0)
        if typ == "StartClass":
            self.debug_cls = getDebug(1)
        if typ == "ManualEncounters":
            self.game.debug_manualEncounters = True
        if typ == "ManualLevelUp":
            self.game.debug_manualLevelUp = True
        if typ == "StartingItems":
            self.debug_startingItems = getDebug(4)
        if typ == "StartingZone":
            self.debug_startingZone = getDebug(5)
        if typ == "StartingGold":
            self.debug_startingGold = getDebug(6)
    
    def executeDebug(self):
        print(self.debugOps)
        if "StartLevel" in self.debugOps or "StartClass" in self.debugOps:
            self.game.player.party.debug_setToLevel(self.game.directory,self.debug_lv,self.debug_cls,self.game.player.getNewCharID())
            self.game.player.getNewCharID()
            self.game.player.getNewCharID()
            self.game.player.getNewCharID()
            # Accounting for all characters made in ID...
        if "ManualEncounters" not in self.debugOps:
            self.game.debug_manualEncounters = bool(getDebug(2))
        if "ManualLevelUp" not in self.debugOps:
            self.game.debug_manualLevelUp = bool(getDebug(3))
        if "StartingItems" in self.debugOps:
            for i, item in enumerate(self.debug_startingItems):
                self.game.player.party.add(item,self.game.directory)
        if "StartingZone" in self.debugOps:
            self.startingZone = self.debug_startingZone
        if "StartingGold" in self.debugOps:
            self.game.player.gold += self.debug_startingGold