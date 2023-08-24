import pygame
import copy

class PauseMenu():
    def __init__(self,game):
        self.game = game
        self.paused = False
        self.state = "main"
        self.cursorPos = 0
        self.mapPos = (0,0)
        self.currentPos = (0,0)
        self.delay = 0
        self.left = 10
        self.top = 10
        self.right = self.game.width - 20
        self.bottom = self.game.height - 20
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.mapZoomSize = 20

    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0,0))
        pygame.display.update()
        self.game.buttonReset()

    def display(self):
        self.game.screen.fill(self.game.black)
        self.state = "main"
        self.drawScreen()
        while self.paused:
            self.game.eventHandler()
            self.getInput()
            self.drawScreen()
            self.blitScreen()
        self.game.screen.fill(self.game.black)
        self.blitScreen()

    def pause(self, mapPos):
        self.paused = True
        self.delay = 5
        self.mapPos = copy.deepcopy(mapPos)
        self.currentPos = copy.deepcopy(mapPos)
        self.display()

    def drawScreen(self):
        self.game.screen.fill(self.game.black)
        if self.state == "main" or self.state == "partySelect":
            screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
            pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
            self.write(40, 30, 40, "Paused")
            self.write(20, 60, 90, "Resume")
            self.write(20, 60, 115, "Party")
            self.write(20, 60, 140, "Inventory")
            self.write(20, 60, 165, "Map")
            self.write(20, 60, 190, "Quit")
            if self.state == "main":
                self.write(20, 30, 87 + (self.cursorPos*25), "->")
            if self.state == "partySelect":
                self.write(30, 210, 75 + (self.cursorPos*100), "->")
            for i in range(0,len(self.game.party.members)):
                self.drawMinStatBlock(250, 45 + (i*100), self.game.party.members[i])
        if self.state == "map":
            screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
            pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
            blockSize = self.mapZoomSize #Set the size of the grid block
            self.game.screen.fill((0,0,0))
            mapFont = pygame.font.Font('freesansbold.ttf',round(blockSize/1.5))
            for x in range(30, self.right, blockSize):
                for y in range(30, self.bottom, blockSize):
                    gridWidth = self.right / blockSize
                    gridHeight = self.bottom / blockSize
                    rect = pygame.Rect(x, y, blockSize, blockSize)
                    pygame.draw.rect(self.game.screen, (0,0,0), rect)
                    r = int(((y / blockSize)-(gridHeight/2))+self.mapPos[0])
                    c = int(((x / blockSize)-(gridWidth/2))+self.mapPos[1])
                    mapChar = '_'
                    if r < 0 or r >= self.game.WorldMap.sizeR:
                        mapChar = ' '
                    if c < 0 or c >= self.game.WorldMap.sizeC:
                        mapChar = ' '
                    if r == self.currentPos[0] and c == self.currentPos[1]:
                        mapChar = '@'
                    if mapChar == '_':
                        revMapList = list(self.game.WorldMap.revealedMap[r])
                        revMapList[c] = '1'
                        self.game.WorldMap.revealedMap[r] = ''.join(revMapList)
                        mapChar = self.game.WorldMap.map[r][c]

                    text = mapFont.render(mapChar,True,self.game.white)
                    textWidth, textHeight = mapFont.size(mapChar)
                    offset = (blockSize-textWidth)/2

                    self.game.screen.blit(text,(x+offset,y+(round(blockSize/6))))

    def getInput(self):
        if self.delay > 0:
            self.delay -=  1
            return
        if self.game.A:
            if self.state == "main":
                if self.cursorPos == 0:
                    print("RESUME")
                    self.paused = False
                if self.cursorPos == 1:
                    print("PARTY")
                    self.state = "partySelect"
                    self.cursorPos = 0
                    return
                if self.cursorPos == 2:
                    print("INVENTORY")
                if self.cursorPos == 3:
                    print("MAP")
                    self.state = "map"
                if self.cursorPos == 4:
                    print("QUIT")
                    self.paused = False
                    self.game.inGame = False
            if self.state == "partySelect":
                print(self.game.party.members[self.cursorPos].name)
            if self.state == "map":
                print("ZOOMIN")
                if self.mapZoomSize <= 40 and self.mapZoomSize >= 10:
                    self.mapZoomSize += 5
                elif self.mapZoomSize <= 50:
                    self.mapZoomSize += 2
        if self.game.B:
            if self.state == "partySelect":
                self.state = "main"
                self.cursorPos = 1
            if self.state == "map":
                print("ZOOMOUT")
                if self.mapZoomSize > 10:
                    self.mapZoomSize -= 5
                elif self.mapZoomSize > 4:
                    self.mapZoomSize -= 2
        if self.game.X:
            self.paused = False
        if self.game.Y:
            print('Y')
        if self.game.UP:
            if self.state == "main":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = 4
            if self.state == "partySelect":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = len(self.game.party.members)-1
            if self.state == "map":
                self.mapPos[0] -= self.panMap()
        if self.game.DOWN:
            if self.state == "main":
                self.cursorPos += 1
                if self.cursorPos > 4:
                    self.cursorPos = 0
            if self.state == "partySelect":
                self.cursorPos += 1
                if self.cursorPos > len(self.game.party.members)-1:
                    self.cursorPos = 0
            if self.state == "map":
                self.mapPos[0] += self.panMap()
        if self.game.LEFT:
            if self.state == "map":
                self.mapPos[1] -= self.panMap()
        if self.game.RIGHT:
            if self.state == "map":
                self.mapPos[1] += self.panMap()

    def write(self,size,x,y,text):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text, True, self.game.white)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.game.screen.blit(text_surface,text_rect)
        return font.size(text)
    
    def drawMinStatBlock(self,xPos,yPos,character):
        outlineRect = pygame.Rect(xPos,yPos,350,90)
        pygame.draw.rect(self.game.screen,self.game.white,outlineRect,2)
        self.write(14, xPos+10, yPos+10, character.name + ", Level " + str(character.level) + " " + character.type.name)
        self.write(14, xPos+10, yPos+30, "HP " + str(character.hp) + "/" + str(character.hpMax))
        self.write(14, xPos+10, yPos+50, "MP " + str(character.mp) + "/" + str(character.mpMax))
        self.write(14, xPos+218, yPos+10, "ATK " + str(character.getAttack()))
        self.write(14, xPos+283, yPos+10, "DEF " + str(character.getDefense()))
        self.write(14, xPos+218, yPos+28, "ACC " + str(character.getAccuracy()))
        self.write(14, xPos+283, yPos+28, "DDG " + str(character.getDodge()))
        self.write(14, xPos+218, yPos+46, "CRT " + str(character.getCritRate()))
        self.write(14, xPos+283, yPos+46, "LCK " + str(character.getLuck()))
        self.write(14, xPos+218, yPos+64, "AMP " + str(character.getAmplifier()))
        self.write(14, xPos+283, yPos+64, "MPG " + str(character.getManaRegen()))

    def panMap(self):
        if self.mapZoomSize == 40:
            return 2
        elif self.mapZoomSize == 35:
            return 3
        elif self.mapZoomSize == 30:
            return 4
        elif self.mapZoomSize == 25:
            return 5
        elif self.mapZoomSize == 20:
            return 6
        elif self.mapZoomSize == 15:
            return 7
        elif self.mapZoomSize == 10:
            return 8
        elif self.mapZoomSize == 8:
            return 9
        elif self.mapZoomSize == 6:
            return 10
        elif self.mapZoomSize == 4:
            return 10