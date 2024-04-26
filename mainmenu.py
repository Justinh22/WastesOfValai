import sys
import pygame
from writing import *
from debug import *
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
        if self.game.A:
            if self.cursorState == "Start":
                self.game.inGame = True
                self.displayRunning = False
                self.game.screen.fill(self.game.black)
                self.game.write(20, self.startPos[0], self.startPos[1], "Loading...")
                self.blitScreen()
                self.wipeDungeonDir()
                self.game.WorldMap.generateMap()
                for op in self.debugOps:
                    self.setDebug(op)
                self.executeDebug()
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
        if self.game.X:
            if "StartClass" not in self.debugOps:
                print("StartClass")
                self.debugOps.append("StartClass")
        if self.game.Y:
            if "StartLevel" not in self.debugOps:
                print("StartLevel")
                self.debugOps.append("StartLevel")

    def cursorHandler(self):
        if self.game.DOWN:
            if self.cursorState == "Start":
                self.cursor.midtop = (self.loadPos[0]-100, self.loadPos[1])
                self.cursorState = "Load"
            elif self.cursorState == "Load":
                self.cursor.midtop = (self.quitPos[0]-100, self.quitPos[1])
                self.cursorState = "Quit"
            elif self.cursorState == "Quit":
                self.cursor.midtop = (self.startPos[0]-100, self.startPos[1])
                self.cursorState = "Start"
        elif self.game.UP:
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

    def setDebug(self,typ):
        if typ == "StartLevel":
            self.debug_lv = getDebug(0)
        if typ == "StartClass":
            self.debug_cls = getDebug(1)
        if typ == "StartClass" or "StartLevel":
            self.game.player.party.debug_setToLevel(self.game.directory,self.debug_lv,self.debug_cls)
    
    def executeDebug(self):
        if "StartLevel" in self.debugOps or "StartClass" in self.debugOps:
            self.game.player.party.debug_setToLevel(self.game.directory,self.debug_lv,self.debug_cls)