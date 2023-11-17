import sys
import pygame
from writing import *

class MainMenu():
    def __init__(self,game):
        self.game = game
        self.displayRunning = True
        self.cursor = pygame.Rect(0,0,20,20)
        self.cursorState = "Start"
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
                self.game.WorldMap.generateMap()
                print("Start!")
                print(self.game.WorldMap.startingPos)
            if self.cursorState == "Load":
                self.game.inGame = True
                self.displayRunning = False
                self.game.screen.fill(self.game.black)
                self.game.write(20, self.startPos[0], self.startPos[1], "Loading...")
                self.blitScreen()
                self.game.WorldMap.loadMap()
                print("Load!")
            if self.cursorState == "Quit":
                print("Quit!")
                pygame.quit()
                sys.exit()

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
