import pygame
import copy
import math
from constants import *
from writing import *
from dungeonmapgenerator import *

class PauseMenu():
    def __init__(self,game):
        self.game = game
        self.paused = False
        self.state = "main"
        self.substate = "none"
        self.action = "none"
        self.itemName = "none"
        self.mapMode = "biome"
        self.cursorPos = 0
        self.mapPos = (0,0)
        self.currentPos = (0,0)
        self.targetPartyMember = 0
        self.spellTarget = -1
        self.targetElement = 0
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
        self.cursorPos = 0
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
         # DEBUG: print(f'State: {self.state}, Substate: {self.substate}')

        if self.state == "main" or self.state == "partySelect":
            screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
            pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
            write(self.game, 40, 30, 40, "Paused")
            write(self.game, 20, 60, 90, "Resume")
            write(self.game, 20, 60, 115, "Party")
            write(self.game, 20, 60, 140, "Inventory")
            write(self.game, 20, 60, 165, "Map")
            write(self.game, 20, 60, 190, "Quit")
            if self.state == "main":
                write(self.game, 20, 30, 87 + (self.cursorPos*25), "->")
            if self.state == "partySelect":
                write(self.game, 30, 210, 75 + (self.cursorPos*100), "->")
            for i in range(0,len(self.game.party.members)):
                self.drawMinStatBlock(250, 45 + (i*100), self.game.party.members[i])

        if self.state == "targetSelect":
            screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
            pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
            write(self.game, 40, 30, 40, self.game.party.members[self.targetPartyMember].name)
            write(self.game, 20, 60, 90, "Return")
            write(self.game, 20, 60, 115, "Equipment")
            write(self.game, 20, 60, 140, "Inventory")
            write(self.game, 20, 60, 165, "Spells")
            write(self.game, 30, 210, 75 + (self.cursorPos*100), "->")
            for i in range(0,len(self.game.party.members)):
                self.drawMinStatBlock(250, 45 + (i*100), self.game.party.members[i])

        if self.state == "partyMember" or self.state == "equipment" or self.state == "inventory" or self.state == "spellbook" or self.state == "itemSummary" or self.state == "confirmAction":
            screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
            pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
            write(self.game, 40, 30, 40, self.game.party.members[self.targetPartyMember].name)
            write(self.game, 20, 60, 90, "Return")
            write(self.game, 20, 60, 115, "Equipment")
            write(self.game, 20, 60, 140, "Inventory")
            write(self.game, 20, 60, 165, "Spells")
            self.drawMinStatBlock(250, 45, self.game.party.members[self.targetPartyMember])
            weapon = self.game.party.members[self.targetPartyMember].eqpWpn
            write(self.game, 12, 250, 150, "Weapon: " + weapon.name + " (" + str(weapon.attack) + " ATK, " + str(weapon.accuracy) + " ACC, " + str(weapon.critrate) + " CRT, " + str(weapon.amplifier) + " AMP)")
            armor = self.game.party.members[self.targetPartyMember].eqpAmr
            write(self.game, 12, 250, 170, "Armor: " + armor.name + " (" + str(armor.defense) + " DEF, " + str(armor.dodge) + " DDG, " + str(armor.manaregen) + " MPG)")

            if self.state == "partyMember":
                classOutline = pygame.Rect(250,200,350,240)
                pygame.draw.rect(self.game.screen,self.game.white,classOutline,2)
                write(self.game, 20, 260, 215, self.game.party.members[self.targetPartyMember].type.name)
                write(self.game, 12, 260, 242, "Weapon Prf: "+self.game.party.members[self.targetPartyMember].type.wpnProfToString())
                write(self.game, 12, 260, 262, "Armor Prf: "+self.game.party.members[self.targetPartyMember].type.amrProfToString())
                write(self.game, 12, 300, 295, "POWER: ")
                write(self.game, 12, 390, 293, self.intToRating(self.game.party.members[self.targetPartyMember].type.rating[0]))
                write(self.game, 12, 300, 310, "STURDINESS: ")
                write(self.game, 12, 390, 308, self.intToRating(self.game.party.members[self.targetPartyMember].type.rating[1]))
                write(self.game, 12, 300, 325, "NIMBLENESS: ")
                write(self.game, 12, 390, 323, self.intToRating(self.game.party.members[self.targetPartyMember].type.rating[2]))
                write(self.game, 12, 450, 295, "ARCANA: ")
                write(self.game, 12, 514, 293, self.intToRating(self.game.party.members[self.targetPartyMember].type.rating[3]))
                write(self.game, 12, 450, 310, "FAITH: ")
                write(self.game, 12, 514, 308, self.intToRating(self.game.party.members[self.targetPartyMember].type.rating[4]))
                write(self.game, 12, 450, 325, "LUCK: ")
                write(self.game, 12, 514, 323, self.intToRating(self.game.party.members[self.targetPartyMember].type.rating[5]))
                wrapWrite(self.game, 12, self.game.party.members[self.targetPartyMember].type.description, 340, 260, 355)


        if self.state == "partyMember":
            write(self.game, 20, 30, 87 + (self.cursorPos*25), "->")

        if self.state == "equipment":
            write(self.game, 20, 270, 230, "Equipment")
            self.printInventory("equipment")

        if self.state == "inventory":
            write(self.game, 20, 270, 230, "Inventory")
            self.printInventory("inventory")

        if self.state == "spellbook":
            write(self.game, 20, 270, 230, "Spellbook")
            self.printInventory("spellbook")

        if self.state == "itemSummary" or self.state == "confirmAction":
            summaryOutline = pygame.Rect(40,200,self.right-60,self.bottom-310)
            pygame.draw.rect(self.game.screen,self.game.white,summaryOutline,2)
            if self.substate == "spellbook":
                tgt = self.game.directory.getItem(self.game.party.members[self.targetPartyMember].spells[self.targetElement])
                self.itemName = self.game.directory.getItemName(tgt.id)
                write(self.game, 20, 60, 220, self.itemName)
                writeOrientation(self.game, 20, self.right-90, 220, str(tgt.manacost) + " MP", "L")
                if tgt.type == SpellType.Attack:
                    write(self.game, 15, 60, 245, "Deals " + str(tgt.attack) + " damage.")
                elif tgt.type == SpellType.Buff:
                    buffText = ""
                    commaSeparator = ""
                    if tgt.potency[0] > 0:
                        buffText += commaSeparator + "ATK +" + str(tgt.potency[0])
                        commaSeparator = ", "
                    if tgt.potency[1] > 0:
                        buffText += commaSeparator + "ACC +" + str(tgt.potency[1])
                        commaSeparator = ", "
                    if tgt.potency[2] > 0:
                        buffText += commaSeparator + "CRT +" + str(tgt.potency[2])
                        commaSeparator = ", "
                    if tgt.potency[3] > 0:
                        buffText += commaSeparator + "DEF +" + str(tgt.potency[3])
                        commaSeparator = ", "
                    if tgt.potency[4] > 0:
                        buffText += commaSeparator + "DDG +" + str(tgt.potency[4])
                        commaSeparator = ", "
                    if tgt.potency[5] > 0:
                        buffText += commaSeparator + "LCK +" + str(tgt.potency[5])
                        commaSeparator = ", "
                    if tgt.potency[6] > 0:
                        buffText += commaSeparator + "Regenerates " + str(tgt.potency[6]) + " HP each turn."
                    write(self.game, 15, 60, 245, buffText)
                elif tgt.type == SpellType.Heal:
                    write(self.game, 15, 60, 245, "Heals for " + str(tgt.potency[6]) + " HP.")
                if self.state == "itemSummary" and self.game.directory.getItem(self.game.party.members[self.targetPartyMember].spells[self.targetElement]).type == SpellType.Heal: # Cast:
                    write(self.game, 22, 540, 420, "Cast")
                    write(self.game, 22, 510 + (self.cursorPos*100), 417, "->")
            elif self.substate == "equipment":
                tgt = self.game.directory.getItem(self.game.party.equipment[self.targetElement])
                statText = ""
                itemType = self.game.directory.getItemType(tgt.id)
                self.itemName = self.game.directory.getItemName(tgt.id,True)
                write(self.game, 20, 60, 220, self.itemName)
                if itemType == Type.Weapon:
                    statText = "ATK " + str(tgt.attack) + " | ACC " + str(tgt.accuracy) + " | CRT " + str(tgt.critrate) + " | AMP " + str(tgt.amplifier)
                elif itemType == Type.Armor:
                    statText = "DEF " + str(tgt.defense) + " | DDG " + str(tgt.dodge) + " | MPG " + str(tgt.manaregen)
                write(self.game, 15, 60, 245, statText)
                if self.state == "itemSummary":
                    write(self.game, 22, 440, 420, "Equip")
                    write(self.game, 22, 540, 420, "Drop")
                    write(self.game, 22, 410 + (self.cursorPos*100), 417, "->")
            elif self.substate == "inventory":
                tgt = self.game.directory.getItem(self.game.party.inventory[self.targetElement])
                statText = ""
                commaSeparator = ""
                itemType = self.game.directory.getItemType(tgt.id)
                self.itemName = self.game.directory.getItemName(tgt.id,True)
                write(self.game, 20, 60, 220, self.itemName)
                if itemType == Type.Potion:
                    if tgt.hpGain > 0:
                        statText += "+" + str(tgt.hpGain) + " HP"
                        commaSeparator = ", "
                    if tgt.mpGain > 0:
                        statText += commaSeparator + "+" + str(tgt.mpGain) + " MP"
                    write(self.game, 15, 60, 245, statText)
                if itemType == Type.AtkSpell or itemType == Type.SptSpell:
                    writeOrientation(self.game, 20, self.right-40, 220, str(tgt.manacost) + " MP", "R")
                    writeOrientation(self.game, 15, self.right-40, 245, "Use to learn spell.", "R")
                    if tgt.type == SpellType.Attack:
                        write(self.game, 15, 60, 245, "Deals " + str(tgt.attack) + " damage.")
                    elif tgt.type == SpellType.Buff:
                        buffText = ""
                        commaSeparator = ""
                        if tgt.potency[0] > 0:
                            buffText += commaSeparator + "ATK +" + str(tgt.potency[0])
                            commaSeparator = ", "
                        if tgt.potency[1] > 0:
                            buffText += commaSeparator + "ACC +" + str(tgt.potency[1])
                            commaSeparator = ", "
                        if tgt.potency[2] > 0:
                            buffText += commaSeparator + "CRT +" + str(tgt.potency[2])
                            commaSeparator = ", "
                        if tgt.potency[3] > 0:
                            buffText += commaSeparator + "DEF +" + str(tgt.potency[3])
                            commaSeparator = ", "
                        if tgt.potency[4] > 0:
                            buffText += commaSeparator + "DDG +" + str(tgt.potency[4])
                            commaSeparator = ", "
                        if tgt.potency[5] > 0:
                            buffText += commaSeparator + "LCK +" + str(tgt.potency[5])
                            commaSeparator = ", "
                        if tgt.potency[6] > 0:
                            buffText += commaSeparator + "Regenerates " + str(tgt.potency[6]) + " HP each turn."
                        write(self.game, 15, 60, 245, buffText)
                    elif tgt.type == SpellType.Heal:
                        write(self.game, 15, 60, 245, "Heals for " + str(tgt.potency[6]) + " HP.")
                if self.state == "itemSummary":
                    write(self.game, 22, 440, 420, "Use")
                    write(self.game, 22, 540, 420, "Drop")
                    write(self.game, 22, 410 + (self.cursorPos*100), 417, "->")
            pygame.draw.line(self.game.screen,self.game.white,(85,275),(self.right-60,275),1)
            wrapWrite(self.game, 15, tgt.description, self.right-85, 60, 290)
        
        if self.state == "confirmAction":
            write(self.game, 15, 35, 360, "Are you sure you want to "+self.action+" the "+self.itemName+"? (Press A to Confirm)")

        if self.state == "map":
            screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
            pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
            blockSize = self.mapZoomSize # Set the size of the grid block
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
                if (self.state == "equipment" and self.cursorPos < len(self.game.party.equipment)) or \
                    (self.state == "inventory" and self.cursorPos < len(self.game.party.inventory)) or \
                    (self.state == "spellbook" and self.cursorPos < len(self.game.party.members[self.targetPartyMember].spells)):
                    self.targetElement = self.cursorPos
                    self.cursorPos = 0
                    self.substate = self.state
                    self.state = "itemSummary"
            elif self.state == "itemSummary":
                if self.substate == "equipment" and self.cursorPos == 0: # Equip
                    self.action = "equip"
                    self.state = "confirmAction"
                if (self.substate == "equipment" or self.substate == "inventory") and self.cursorPos == 1: # Drop
                    self.action = "drop"
                    self.state = "confirmAction"
                if self.substate == "inventory" and self.cursorPos == 0: # Use
                    self.action = "use"
                    self.state = "confirmAction"
                if self.substate == "spellbook" and self.cursorPos == 0 and self.game.directory.getItem(self.game.party.members[self.targetPartyMember].spells[self.targetElement]).type == SpellType.Heal: # Cast
                    self.action = "cast"
                    self.state = "targetSelect"
                    self.cursorPos = 0
            elif self.state == "confirmAction":
                self.actionHandler(self.substate, self.action, self.targetPartyMember, self.targetElement, self.spellTarget)
                if self.substate == "equipment":
                    self.state = "equipment"
                elif self.substate == "inventory":
                    self.state = "inventory"
                elif self.substate == "spellbook":
                    self.state = "spellbook"
                self.substate = "none"
                self.spellTarget = -1
                print(f'STATE HERE IS {self.state}')
            elif self.state == "targetSelect":
                self.spellTarget = self.cursorPos
                self.state = "confirmAction"
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
            if self.state == "itemSummary":
                self.cursorPos = 0
                self.state = self.substate
                self.substate = "none"
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
            elif self.state == "main":
                newDgn = DungeonMap(self.game.directory,(0,0),DungeonType.Ruins)
                newDgn.generate()
        if self.game.UP:
            if self.state == "main":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = 4
            if self.state == "partySelect" or self.state == "targetSelect":
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
            elif self.state == "partySelect" or self.state == "targetSelect":
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
            elif self.state == "itemSummary":
                self.cursorPos -= 1
                if self.substate == "equipment" or self.substate == "inventory":
                    if self.cursorPos < 0:
                        self.cursorPos = 1
        if self.game.RIGHT:
            if self.state == "map":
                self.mapPos[1] += self.panMap()
            elif self.state == "equipment" or self.state == "inventory" or self.state == "spellbook":
                if self.cursorPos % 2 == 0:
                    self.cursorPos += 1
                else:
                    self.cursorPos -= 1
            elif self.state == "itemSummary":
                self.cursorPos += 1
                if self.substate == "equipment" or self.substate == "inventory":
                    if self.cursorPos > 1:
                        self.cursorPos = 0
                elif self.substate == "spellbook":
                    self.cursorPos = 0
        if self.game.START:
            self.paused = False
    
    def drawMinStatBlock(self,xPos,yPos,character):
        outlineRect = pygame.Rect(xPos,yPos,350,90)
        pygame.draw.rect(self.game.screen,self.game.white,outlineRect,2)
        write(self.game, 14, xPos+10, yPos+10, character.name + ", Level " + str(character.level) + " " + character.type.name)
        write(self.game, 14, xPos+10, yPos+30, "HP " + str(character.hp) + "/" + str(character.hpMax))
        write(self.game, 14, xPos+10, yPos+50, "MP " + str(character.mp) + "/" + str(character.mpMax))
        write(self.game, 14, xPos+10, yPos+70, "XP " + str(character.xp) + "/" + str(character.nextLevel))
        write(self.game, 14, xPos+218, yPos+10, "ATK " + str(character.getAttack()))
        write(self.game, 14, xPos+283, yPos+10, "DEF " + str(character.getDefense()))
        write(self.game, 14, xPos+218, yPos+28, "ACC " + str(character.getAccuracy()))
        write(self.game, 14, xPos+283, yPos+28, "DDG " + str(character.getDodge()))
        write(self.game, 14, xPos+218, yPos+46, "CRT " + str(character.getCritRate()))
        write(self.game, 14, xPos+283, yPos+46, "LCK " + str(character.getLuck()))
        write(self.game, 14, xPos+218, yPos+64, "AMP " + str(character.getAmplifier()))
        write(self.game, 14, xPos+283, yPos+64, "MPG " + str(character.getManaRegen()))

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
            return 10
        elif self.mapZoomSize == 6:
            return 12
        elif self.mapZoomSize == 4:
            return 20
        
    def printInventory(self, type):
        scroll = False
        if type == "equipment":
            list = self.game.party.equipment
        elif type == "inventory":
            list = self.game.party.inventory
            scroll = True
        elif type == "spellbook":
            list = self.game.party.members[self.targetPartyMember].spells

        for i in range(math.ceil(MAX_INVENTORY_SIZE/2)): # FIX: Allow for no capacity on spellbook
            if i*2 < len(list):
                write(self.game, 15, 100, 275 + (25*i), str((i*2)+1) + ") " + self.game.directory.getItemName(list[i*2],scroll))
            else:
                write(self.game, 15, 100, 275 + (25*i), str((i*2)+1) + ") ")
            if (i*2)+1 < len(list):
                write(self.game, 15, 350, 275 + (25*i), str((i*2)+2) + ") " + self.game.directory.getItemName(list[(i*2)+1],scroll))
            else:
                write(self.game, 15, 350, 275 + (25*i), str((i*2)+2) + ") ")
        write(self.game, 15, 85 + ((self.cursorPos%2)*250), 272 + (25*(math.floor(self.cursorPos/2))), ">")

    def actionHandler(self,tgtList,action,targetPartyMember,targetElement,spellTarget=-1):
        if action == "equip":
            if self.game.party.members[targetPartyMember].checkProficiency(self.game.party.equipment[targetElement],self.game.directory):
                self.game.party.equipment[targetElement] = self.game.party.members[targetPartyMember].equip(self.game.party.equipment[targetElement],self.game.directory)
        elif action == "drop":
            if tgtList == "inventory":
                self.game.party.dropItem(targetElement)
            elif tgtList == "equipment":
                self.game.party.dropEquipment(targetElement)
        elif action == "use":
            if self.game.directory.getItemType(self.game.party.inventory[targetElement]) == Type.Potion:
                self.game.party.usePotion(targetPartyMember,targetElement,self.game.directory)
            elif self.game.directory.getItemType(self.game.party.inventory[targetElement]) == Type.AtkSpell or self.game.directory.getItemType(self.game.party.inventory[targetElement]) == Type.SptSpell:
                if self.game.party.members[targetPartyMember].checkProficiency(self.game.party.inventory[targetElement],self.game.directory):
                    self.game.party.learnSpell(targetPartyMember, targetElement)
        elif action == "cast":
            if self.game.party.members[targetPartyMember].canCast(targetElement,self.game.directory):
                self.game.party.members[targetPartyMember].expendMana(targetElement,self.game.directory)
                self.game.party.members[spellTarget].gainHP(self.game.directory.getItem(self.game.party.members[targetPartyMember].spells[targetElement]).getHeal())

    def intToRating(self,val):
        ret = ""
        for i in range(val):
            ret += "+"
        return ret
