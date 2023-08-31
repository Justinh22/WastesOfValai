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
        self.cursorPos = 0
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
            if self.state == "main":
                self.state = "lookList"
                self.delay = 5
            elif self.state == "lookList":
                self.delay = 5
                self.state = "featureCheck"
            print("A")
        if self.game.B:
            if self.state == "main":
                self.inRoom = False
            elif self.state == "lookList":
                self.delay = 5
                self.state = "main"
            elif self.state == "featureCheck":
                self.delay = 5
                self.state = "lookList"
            print("B")
        if self.game.X:
            print("X")
        if self.game.Y:
            print("Y")
        if self.game.UP:
            if self.state == "lookList":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = len(self.room.features)-1
            print("UP")
        if self.game.DOWN:
            if self.state == "lookList":
                self.cursorPos += 1
                if self.cursorPos > len(self.room.features)-1:
                       self.cursorPos = 0
            print("DOWN")
        if self.game.LEFT:
            print("LEFT")
        if self.game.RIGHT:
            print("RIGHT")

    def drawScreen(self):
        self.game.screen.fill(self.game.black)
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
        pygame.draw.line(self.game.screen,self.game.white,(self.left,300),(self.right+9,300),2)
        pygame.draw.line(self.game.screen,self.game.white,(self.right-self.left-180,300),(self.right-self.left-180,self.bottom+8),2)
        self.roomWrite(20,self.room.description,self.right-self.left-15)
        if self.state == "main":
            self.write(25,self.right-150,self.top+340,"A) Look")
            self.write(25,self.right-150,self.top+390,"B) Leave")
        if self.state == "lookList":
            self.write(25,self.right-150,self.top+340,"A) Check")
            self.write(25,self.right-150,self.top+390,"B) Back")
            self.write(20,self.left+20,(self.top+310)+(25*self.cursorPos),">")
            for i in range(len(self.room.features)):
                self.write(20,self.left+35,(self.top+310)+(25*i),str(i+1)+") "+self.room.features[i].name)
        if self.state == "featureCheck":
            text = self.room.features[self.cursorPos].description
            if self.room.features[self.cursorPos].loot != -1:
                self.write(25,self.right-150,self.top+340,"A) Take")
                text += " You see a " + self.game.directory.getItemName(self.room.features[self.cursorPos].loot) + "."
            self.write(25,self.right-150,self.top+390,"B) Back")
            self.roomWrite(15,text,self.right-self.left-200,self.left+10,self.top+310)


    def write(self,size,x,y,text):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text, True, self.game.white)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.game.screen.blit(text_surface,text_rect)
        return font.size(text)

    def roomWrite(self,size,text,xBound,x=20,y=25):
        font = pygame.font.Font('freesansbold.ttf',size)
        textList = self.wrap(font,text,xBound)
        for i in range(0,len(textList)):
            text_surface = font.render(textList[i], True, self.game.white)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x,y+((size+5)*i))
            self.game.screen.blit(text_surface,text_rect)
        return font.size(text)
    
    def wrap(self,font,text,windowsize):
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
                    line = ' '.join(lineList)
            fullText.append(line)
        return fullText