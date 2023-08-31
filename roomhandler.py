import pygame
from room import * # Includes feature.py, directory.py, and constants.py

class RoomHandler():
    def __init__(self,game,room):
        self.room = room
        self.game = game
        self.inRoom = False
        self.left = 10
        self.top = 10
        self.right = self.game.width - 20
        self.bottom = self.game.height - 20
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.state = "main"
        self.delay = 5

    def enter(self):
        self.inRoom = True
        self.display()

    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0,0))
        pygame.display.update()
        self.game.buttonReset()

    def display(self):
        self.game.screen.fill(self.game.black)
        self.state = "main"
        self.drawScreen()
        while self.inRoom:
            self.game.eventHandler()
            self.getInput()
            if self.inRoom == False:
                break
            self.drawScreen()
            self.blitScreen()
        self.game.screen.fill(self.game.black)
        self.blitScreen()

    def getInput(self):
        if self.delay > 0:
            self.delay -= 1
            return
        if self.game.A:
            print("A")
        if self.game.B:
            print("B")
        if self.game.X:
            print("X")
            self.inRoom = False
        if self.game.Y:
            print("Y")
        if self.game.UP:
            print("UP")
        if self.game.DOWN:
            print("DOWN")
        if self.game.LEFT:
            print("LEFT")
        if self.game.RIGHT:
            print("RIGHT")

    def drawScreen(self):
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
        pygame.draw.line(self.game.screen,self.game.white,(self.left,300),(self.right+9,300),2)
        self.roomWrite(20,self.room.description)

    def write(self,size,x,y,text):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text, True, self.game.white)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.game.screen.blit(text_surface,text_rect)
        return font.size(text)

    def roomWrite(self,size,text,y=20):
        font = pygame.font.Font('freesansbold.ttf',size)
        textList = self.wrap(font,text)
        for i in range(0,len(textList)):
            text_surface = font.render(textList[i], True, self.game.white)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.left+10,y+((size+5)*i))
            self.game.screen.blit(text_surface,text_rect)
        return font.size(text)
    
    def wrap(self,font,text):
        windowsize = self.right - self.left - 10
        fullText = [text]
        if font.size(text)[0] > windowsize:
            fullText.clear()
            listText = text.split()
            lineList = []
            for word in listText:
                lineList.append(word)
                line = ' '.join(lineList)
                if font.size(line)[0] > windowsize:
                    lastWord = lineList[-1]
                    lineList.pop(-1)
                    line = ' '.join(lineList)
                    fullText.append(line)
                    lineList.clear()
                    lineList.append(lastWord)
        fullText.append(line)
        return fullText