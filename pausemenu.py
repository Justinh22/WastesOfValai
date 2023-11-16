import pygame
import copy
import math
import constants

class PauseMenu():
    def __init__(self,game):
        self.game = game
        self.paused = False
        self.state = "main"
        self.mapMode = "biome"
        self.cursorPos = 0
        self.mapPos = (0,0)
        self.currentPos = (0,0)
        self.targetPartyMember = 0
        self.menuSelection = 0
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
        if self.state == "partyMember" or self.state == "equipment" or self.state == "inventory" or self.state == "spellbook":
            screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
            pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
            self.write(40, 30, 40, self.game.party.members[self.targetPartyMember].name)
            self.write(20, 60, 90, "Return")
            self.write(20, 60, 115, "Equipment")
            self.write(20, 60, 140, "Inventory")
            self.write(20, 60, 165, "Spells")
            self.drawMinStatBlock(250, 45, self.game.party.members[self.targetPartyMember])
            weapon = self.game.party.members[self.targetPartyMember].eqpWpn
            self.write(12, 250, 150, "Weapon: " + weapon.name + " (" + str(weapon.attack) + " ATK, " + str(weapon.accuracy) + " ACC, " + str(weapon.critrate) + " CRT, " + str(weapon.amplifier) + " AMP)")
            armor = self.game.party.members[self.targetPartyMember].eqpAmr
            self.write(12, 250, 170, "Armor: " + armor.name + " (" + str(armor.defense) + " DEF, " + str(armor.dodge) + " DDG, " + str(armor.manaregen) + " MPG)")
        if self.state == "partyMember":
            self.write(20, 30, 87 + (self.cursorPos*25), "->")
        if self.state == "equipment":
            self.write(20, 270, 230, "Equipment")
            self.printInventory("equipment")
        if self.state == "inventory":
            self.write(20, 270, 230, "Inventory")
            self.printInventory("inventory")
        if self.state == "spellbook":
            self.write(20, 270, 230, "Spellbook")
            self.printInventory("spellbook")
        if self.state == "map":
            screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
            pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
            blockSize = self.mapZoomSize #Set the size of the grid block
            self.game.screen.fill((0,0,0))
            mapFont = pygame.font.Font('freesansbold.ttf',round(blockSize/1.5))
            for x in range(30, self.right, blockSize):
                for y in range(30, self.bottom, blockSize):
                    color = self.game.white
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
                        if self.game.WorldMap.revealedMap[r][c] == '1':
                            mapChar = self.game.WorldMap.map[r][c]
                            if self.mapMode == "biome":
                                if mapChar == '#': # Forest
                                    color = self.game.green
                                elif mapChar == ';': # Plains
                                    color = self.game.lightgreen
                                elif mapChar == '.': # Desert
                                    color = self.game.tan
                            elif self.mapMode == "difficulty" and mapChar != ' ' and mapChar != 'X':
                                diff = self.game.WorldMap.letterToVal(self.game.WorldMap.difficultyMap[r][c])
                                color = (255,225-(9*diff),225-(9*diff))
                        else:
                            if self.game.WorldMap.map[r][c] == 'X':
                                mapChar = self.game.WorldMap.map[r][c]
                            else:
                                mapChar = ' '

                    text = mapFont.render(mapChar,True,color)
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
                    self.game.running = False
            elif self.state == "partySelect":
                print(self.game.party.members[self.cursorPos].name)
                self.state = "partyMember"
                self.targetPartyMember = self.cursorPos
                self.cursorPos = 0
            elif self.state == "map":
                print("ZOOMIN")
                if self.mapZoomSize < 40 and self.mapZoomSize >= 10:
                    self.mapZoomSize += 5
                elif self.mapZoomSize < 40 and self.mapZoomSize >= 4:
                    self.mapZoomSize += 2
            elif self.state == "partyMember":
                if self.cursorPos == 0:
                    self.state = "main"
                elif self.cursorPos == 1:
                    self.state = "equipment"
                    self.menuSelection = self.cursorPos
                    self.cursorPos = 0
                elif self.cursorPos == 2:
                    self.state = "inventory"
                    self.menuSelection = self.cursorPos
                    self.cursorPos = 0
                elif self.cursorPos ==  3:
                    self.state = "spellbook"
                    self.menuSelection = self.cursorPos
                    self.cursorPos = 0
            elif self.state == "equipment" or self.state == "inventory" or self.state == "spellbook":
                self.state = "itemSummary"
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
            if self.state == "partyMember":
                self.state = "partySelect"
                self.cursorPos = self.targetPartyMember
            if self.state == "equipment" or self.state == "inventory" or self.state == "spellbook":
                self.state = "partyMember"
                self.cursorPos = self.menuSelection
        if self.game.X:
            if self.state == "map":
                self.state = "main"
            else:
                self.paused = False
        if self.game.Y:
            if self.state == "map":
                if self.mapMode == "biome":
                    self.mapMode = "difficulty"
                else:
                    self.mapMode = "biome"
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
            if self.state == "partyMember":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = 3
            elif self.state == "equipment" or self.state == "inventory" or self.state == "spellbook":
                if self.cursorPos <= 1:
                    self.cursorPos += 8
                else:
                    self.cursorPos -= 2
        if self.game.DOWN:
            if self.state == "main":
                self.cursorPos += 1
                if self.cursorPos > 4:
                    self.cursorPos = 0
            elif self.state == "partySelect":
                self.cursorPos += 1
                if self.cursorPos > len(self.game.party.members)-1:
                    self.cursorPos = 0
            elif self.state == "map":
                self.mapPos[0] += self.panMap()
            elif self.state == "partyMember":
                self.cursorPos += 1
                if self.cursorPos > 3:
                    self.cursorPos = 0
            elif self.state == "equipment" or self.state == "inventory" or self.state == "spellbook":
                if self.cursorPos >= 8:
                    self.cursorPos -= 8
                else:
                    self.cursorPos += 2
        if self.game.LEFT:
            if self.state == "map":
                self.mapPos[1] -= self.panMap()
            elif self.state == "equipment" or self.state == "inventory" or self.state == "spellbook":
                if self.cursorPos % 2 == 0:
                    self.cursorPos += 1
                else:
                    self.cursorPos -= 1
        if self.game.RIGHT:
            if self.state == "map":
                self.mapPos[1] += self.panMap()
            elif self.state == "equipment" or self.state == "inventory" or self.state == "spellbook":
                if self.cursorPos % 2 == 0:
                    self.cursorPos += 1
                else:
                    self.cursorPos -= 1

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
        self.write(14, xPos+10, yPos+70, "XP " + str(character.xp) + "/" + str(character.nextLevel))
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
        
    def printInventory(self, type):
        scroll = False
        if type == "equipment":
            list = self.game.party.equipment
        elif type == "inventory":
            list = self.game.party.inventory
            scroll = True
        elif type == "spellbook":
            list = self.game.party.spellbook

        for i in range(math.ceil(constants.MAX_INVENTORY_SIZE/2)):
            if i*2 < len(list):
                self.write(15, 100, 275 + (25*i), str((i*2)+1) + ") " + self.game.directory.getItemName(list[i*2],scroll))
            else:
                self.write(15, 100, 275 + (25*i), str((i*2)+1) + ") ")
            if (i*2)+1 < len(list):
                self.write(15, 350, 275 + (25*i), str((i*2)+2) + ") " + self.game.directory.getItemName(list[(i*2)+1],scroll))
            else:
                self.write(15, 350, 275 + (25*i), str((i*2)+2) + ") ")
        self.write(15, 85 + ((self.cursorPos%2)*250), 272 + (25*(math.floor(self.cursorPos/2))), ">")
