from game import *
from directory import *
from utility import *
from constants import *
from writing import *
from playerdata import *

BUILDING_HEIGHT = 4
BUILDING_WIDTH = 7

BUILDING_ROOF = '='
BUILDING_WALL = 'I'
BUILDING_DOOR = 'O'

class Building():
    def __init__(self,row,col,level):
        self.game = None
        self.row = row
        self.col = col
        self.height = BUILDING_HEIGHT
        self.width = BUILDING_WIDTH
        self.player = None
        self.level = level
        self.inBuilding = True
        self.cursorPos = 0
        self.left = 10
        self.top = 10
        self.right = -1
        self.bottom = -1
        self.state = "main"
        self.substate = "none"
        self.delay = 5
        self.color = (173, 84, 0) # Brown

    def enter(self,game,player):
        self.game = game
        self.player = player
        self.right = self.game.width - 20
        self.bottom = self.game.height - 20
        self.initializeOnEnter()
        self.display()

    def initializeOnEnter(self):
        self.cursorPos = 0
        self.state = "main"
        self.substate = "none"
        print("Enter!")
    
    def getDoorway(self):
        return (self.row+(BUILDING_HEIGHT-1),self.col+int((BUILDING_WIDTH-1)/2))
    
    def getOutsideDoorway(self):
        return (self.row+(BUILDING_HEIGHT),self.col+int((BUILDING_WIDTH-1)/2))

    def isInBuilding(self,r,c):
        if r >= self.row and r < self.row + BUILDING_HEIGHT:
            if c >= self.col and c < self.col + BUILDING_WIDTH:
                return True
        return False
    
    def toString(self):
        return "(" + str(self.getOutsideDoorway()[0]) + "," + str(self.getOutsideDoorway()[1]) + ")"

    def getCoords(self):
        return ((self.row,self.col))
    
    def getDistanceFrom(self,coords):
        return abs(self.getOutsideDoorway()[0]-coords[0]) + abs(self.getOutsideDoorway()[1]-coords[1])
    
    def setEntrance(self,map):
        coords = self.getDoorway()
        map[coords[0]][coords[1]] = BUILDING_DOOR
        return coords

    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0,0))
        pygame.display.update()
        self.game.buttonReset()

    def display(self):
        self.inMenu = True
        self.game.screen.fill(self.game.black)
        self.drawScreen()
        while self.inMenu and self.game.inGame:
            self.game.eventHandler()
            self.getInput()
            if not self.inMenu:
                break
            self.drawScreen()
            self.blitScreen()
        self.game.screen.fill(self.game.black)
        self.blitScreen()

    def getInput(self):
        if self.delay > 0:
            self.delay -= 1
            return
        if self.game.UP:
            print("UP")
        if self.game.DOWN:
            print("DOWN")
        if self.game.A:
            print("A")
        if self.game.B:
            print("B")
        if self.game.X:
            print("X")
        if self.game.Y:
            print("Y")

    def drawScreen(self):
        self.game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)

        if self.state == "main":
            write(self.game, 40, 30, 40, "Building")


class Forge(Building):
    def __init__(self,row,col,level):
        Building.__init__(self,row,col,level)
        self.color = (0,0,255) # Blue
        self.itemType = "none"
        self.targetItem = None
        self.currentRefineLevel = []
        self.tentativeRefineLevel = []
        self.refinementStatCurrentValues = []
        self.refinementStatTentativeValues = []
        self.pageModifer = 0

    def initializeOnEnter(self):
        self.itemType = "none"
        self.targetItem = None
        self.currentRefineLevel = []
        self.tentativeRefineLevel = []
        self.refinementStatCurrentValues = []
        self.refinementStatTentativeValues = []
        self.pageModifer = 0

    def getInput(self):
        if self.delay > 0:
            self.delay -= 1
            return
        if self.game.UP:
            print("UP")
            if self.state == "selectItem":
                if self.cursorPos == 1 and self.pageModifer > 0:
                    self.pageModifer -= 1
                elif self.cursorPos > 0:
                    self.cursorPos -= 1
            if self.state == "partySelect":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = len(self.game.player.party.members)-1
            if self.state == "weaponRefinement":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = 2
            if self.state == "armorRefinement":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = 1
        if self.game.DOWN:
            print("DOWN")
            if self.state == "selectItem":
                if self.cursorPos == 3 and (self.pageModifer+5 < len(self.player.party.equipment)):
                    self.pageModifer += 1
                elif self.cursorPos < 4 and self.cursorPos < len(self.player.party.equipment)-1:
                    self.cursorPos += 1
            if self.state == "partySelect":
                self.cursorPos += 1
                if self.cursorPos > len(self.game.player.party.members)-1:
                    self.cursorPos = 0
            if self.state == "weaponRefinement":
                self.cursorPos += 1
                if self.cursorPos > 2:
                    self.cursorPos = 0
            if self.state == "armorRefinement":
                self.cursorPos += 1
                if self.cursorPos > 1:
                    self.cursorPos = 0
        if self.game.LEFT:
            if self.state == "weaponRefinement" or self.state == "armorRefinement":
                if self.tentativeRefineLevel[self.cursorPos] > self.currentRefineLevel[self.cursorPos]:
                    self.tentativeRefineLevel[self.cursorPos] -= 1
        if self.game.RIGHT:
            if self.state == "weaponRefinement" or self.state == "armorRefinement":
                if self.tentativeRefineLevel[self.cursorPos] < MAX_REFINE_LEVEL:
                    self.tentativeRefineLevel[self.cursorPos] += 1
        if self.game.A:
            print("A")
            if self.state == "main":
                self.state = "chooseInventory"
                self.substate = "refine"
                self.cursorPos = 0
            elif self.state == "chooseInventory":
                self.state = "chooseItemType"
                self.cursorPos = 0
            elif self.state == "chooseItemType":
                self.state = "partySelect"
                self.itemType = "weapon"
                self.cursorPos = 0
            elif self.state == "selectItem":
                self.targetItem = self.game.player.party.equipment[self.cursorPos]
                if self.game.directory.getItemType(self.targetItem) == Type.Weapon:
                     self.itemType = "weapon"
                elif self.game.directory.getItemType(self.targetItem) == Type.Armor:
                     self.itemType = "armor"
                if self.substate == "refine" and self.itemType == "weapon":
                    self.currentRefineLevel = [self.targetItem.atkRefine,self.targetItem.accRefine,self.targetItem.crtRefine]
                    self.tentativeRefineLevel = [self.targetItem.atkRefine,self.targetItem.accRefine,self.targetItem.crtRefine]
                    self.state = "weaponRefinement"
                elif self.substate == "refine" and self.itemType == "armor":
                    self.currentRefineLevel = [self.targetItem.defRefine,self.targetItem.ddgRefine]
                    self.tentativeRefineLevel = [self.targetItem.defRefine,self.targetItem.ddgRefine]
                    self.state = "armorRefinement"
                self.substate = "selectItem"
            elif self.state == "partySelect":
                if self.substate == "refine" and self.itemType == "weapon":
                    self.targetItem = self.game.player.party.members[self.cursorPos].eqpWpn
                    self.currentRefineLevel = [self.targetItem.atkRefine,self.targetItem.accRefine,self.targetItem.crtRefine]
                    self.tentativeRefineLevel = [self.targetItem.atkRefine,self.targetItem.accRefine,self.targetItem.crtRefine]
                    self.state = "weaponRefinement"
                elif self.substate == "refine" and self.itemType == "armor":
                    self.targetItem = self.game.player.party.members[self.cursorPos].eqpAmr
                    self.currentRefineLevel = [self.targetItem.defRefine,self.targetItem.ddgRefine]
                    self.tentativeRefineLevel = [self.targetItem.defRefine,self.targetItem.ddgRefine]
                    self.state = "armorRefinement"
                self.substate = "partySelect"
            elif self.state == "weaponRefinement":
                self.state = "confirmWeaponRefine"
            elif self.state == "armorRefinement":
                self.state = "confirmArmorRefine"
            elif self.state == "confirmWeaponRefine" or self.state == "confirmArmorRefine":
                if self.player.gold >= self.calculateCost(self.targetItem.rarity,self.currentRefineLevel,self.tentativeRefineLevel):
                    self.cursorPos = 0
                    self.player.gold -= self.calculateCost(self.targetItem.rarity,self.currentRefineLevel,self.tentativeRefineLevel)
                    self.targetItem.refine(self.tentativeRefineLevel)
                    self.currentRefineLevel = self.tentativeRefineLevel[:]
                    self.state = self.substate
                    self.substate = "refine"
        if self.game.B:
            print("B")
            if self.state == "main":
                self.inMenu = False
            elif self.state == "chooseInventory":
                self.cursorPos = 0
                self.state = "main"
            elif self.state == "chooseItemType":
                self.cursorPos = 0
                self.state = "chooseInventory"
            elif self.state == "selectItem":
                self.cursorPos = 0
                self.state = "chooseInventory"
            elif self.state == "partySelect":
                self.cursorPos = 0
                self.state = "chooseItemType"
            elif self.state == "weaponRefinement" or self.state == "armorRefinement" or self.state == "confirmWeaponRefine" or self.state == "confirmArmorRefine":
                self.cursorPos = 0
                self.state = self.substate
                self.substate = "refine"
        if self.game.X:
            print("X")
            if self.state == "main":
                self.state = "chooseInventory"
                self.substate = "reforge"
                self.cursorPos = 0
            elif self.state == "chooseInventory":
                self.state = "selectItem"
                self.cursorPos = 0
            elif self.state == "chooseItemType":
                self.state = "partySelect"
                self.itemType = "armor"
                self.cursorPos = 0
        if self.game.Y:
            print("Y")
        if self.game.START:
            print("START")
            self.inMenu = False

    def drawScreen(self):
        self.game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.line(self.game.screen,self.game.white,(self.left,300),(self.right+9,300),2)
        pygame.draw.line(self.game.screen,self.game.white,(self.right-self.left-180,300),(self.right-self.left-180,self.bottom+8),2)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
        description = self.getDescription(self.state, self.substate)
        wrapWrite(self.game, 20, description, self.right-self.left-15)

        if self.state == "main":
            write(self.game, 30, self.left+10, self.top+305, "Forge")
            write(self.game, 25,self.right-150,self.top+310,"A) Refine")
            write(self.game, 25,self.right-150,self.top+360,"X) Reforge")
            write(self.game, 25,self.right-150,self.top+410,"B) Leave")

        elif self.state == "chooseInventory" or self.state == "selectItem":
            write(self.game, 25,self.right-150,self.top+310,"A) Equipped")
            write(self.game, 25,self.right-150,self.top+360,"X) Inventory")
            write(self.game, 25,self.right-150,self.top+410,"B) Back")
            if self.state == "selectItem":
                self.printEquipment()

        elif self.state == "chooseItemType":
            write(self.game, 25,self.right-150,self.top+310,"A) Weapon")
            write(self.game, 25,self.right-150,self.top+360,"X) Armor")
            write(self.game, 25,self.right-150,self.top+410,"B) Back")

        elif self.state == "chooseItemType" or self.state == "partySelect":
            write(self.game, 25,self.right-150,self.top+340,"A) Select")
            write(self.game, 25,self.right-150,self.top+390,"B) Back")
            write(self.game, 15, self.left+300, (self.top+310)+(25*self.cursorPos), "<-")
            for i, member in enumerate(self.player.party.members):
                write(self.game, 20, self.left+35, (self.top+310)+(25*i), str(i+1) + ") " + member.name)

        elif self.state == "weaponRefinement" or self.state == "armorRefinement" or self.state == "confirmWeaponRefine" or self.state == "confirmArmorRefine":
            write(self.game, 25, self.left+10, self.top+305, self.targetItem.name)
            refinementString = []
            refinementStat = []
            if self.state == "weaponRefinement" or self.state == "confirmWeaponRefine":
                refinementStat = ["Atk","Acc","Crt"]
                for tentativeLevel in self.tentativeRefineLevel:
                    workingString = ""
                    for level in range(0,MAX_REFINE_LEVEL):
                        if level < tentativeLevel:
                            workingString += "[X]"
                        else:
                            workingString += "[ ]"
                    refinementString.append(workingString)
                refinementStatCurrentValues = [self.targetItem.getAttack(), self.targetItem.getAccuracy(), self.targetItem.getCritrate()]
                refinementStatTentativeValues = [self.targetItem.attack + (self.tentativeRefineLevel[0] * ATK_REFINE_BOOST), self.targetItem.accuracy + (self.tentativeRefineLevel[1] * ACC_REFINE_BOOST), self.targetItem.critrate + (self.tentativeRefineLevel[2] * CRT_REFINE_BOOST)]
            if self.state == "armorRefinement" or self.state == "confirmArmorRefine":
                refinementStat = ["Def","Ddg"]
                for tentativeLevel in self.tentativeRefineLevel:
                    workingString = ""
                    for level in range(0,MAX_REFINE_LEVEL):
                        if level < tentativeLevel:
                            workingString += "[X]"
                        else:
                            workingString += "[ ]"
                    refinementString.append(workingString)
                refinementStatCurrentValues = [self.targetItem.getDefense(), self.targetItem.getDodge()]
                refinementStatTentativeValues = [self.targetItem.defense + (self.tentativeRefineLevel[0] * DEF_REFINE_BOOST), self.targetItem.dodge + (self.tentativeRefineLevel[1] * DDG_REFINE_BOOST)]
            cursorXVal = 0
            for i in range(len(refinementStat)):
                cursorXVal, _ = write(self.game, 20, self.left+35, (self.top+340) + (i*25), refinementStat[i] + ": " + refinementString[i] + " - " + str(refinementStatCurrentValues[i]) + " -> " + str(refinementStatTentativeValues[i]))
            write(self.game, 20, self.left+300, (self.top+340) + (self.cursorPos*25), "<-")
            if self.state == "weaponRefinement" or self.state == "armorRefinement":
                write(self.game, 20, self.left+35, 430, "Cost: " + str(self.calculateCost(self.targetItem.rarity,self.currentRefineLevel,self.tentativeRefineLevel)) + " (You have: " + str(self.player.gold) + ")")
                write(self.game, 25,self.right-150,self.top+340,"A) Refine")
                write(self.game, 25,self.right-150,self.top+390,"B) Back")
            elif self.state == "confirmWeaponRefine" or self.state == "confirmArmorRefine":
                write(self.game, 25,self.right-150,self.top+340,"A) Confirm")
                write(self.game, 25,self.right-150,self.top+390,"B) Cancel")

    def getDescription(self,state,substate):
        description = ""
        if state == "main":
            description = "'Ah, welcome!' A short, thin man smiles warmly from the back of the forge, setting a mallet down on an anvil. 'What can I do for you today?'"
        elif state == "chooseInventory" or state == "selectItem" or state == "chooseItemType" or state == "partySelect":
            description = "'Take your time. I can bend and refine metal at your command.'"
        elif state == "weaponRefinement" or state == "armorRefinement":
            description = "'People, we're stubborn. But metal... with a bit of convincing, can become anything.'"
        elif state == "confirmWeaponRefine" or state == "confirmArmorRefine":
            description = "'Alright, so you want me to refine your " + self.targetItem.name + " to "
            for entry in self.tentativeRefineLevel:
                description += "+" + str(entry) + "/"
            description += "? That'll just be " + str(self.calculateCost(self.targetItem.rarity,self.currentRefineLevel,self.tentativeRefineLevel)) + " gold, please.'"
        return description

    def calculateCost(self,rarity,currentLevel,tentativeLevel):
        totalCost = 0
        for i in range(len(currentLevel)):
            for j in range(currentLevel[i]+1,tentativeLevel[i]+1):
                totalCost += 20 * rarity * j
        return totalCost

    def drawEquipmentBlock(self,xPos,yPos,character):
        outlineRect = pygame.Rect(xPos,yPos,350,90)
        pygame.draw.rect(self.game.screen,self.game.white,outlineRect,2)
        write(self.game, 14, xPos+10, yPos+10, character.name + ", Level " + str(character.level) + " " + character.type.name)
        write(self.game, 14, xPos+10, yPos+30, "HP " + str(character.getHP()) + "/" + str(character.getMaxHP()))
        write(self.game, 14, xPos+10, yPos+50, "MP " + str(character.getMP()) + "/" + str(character.getMaxMP()))
        write(self.game, 14, xPos+10, yPos+70, "XP " + str(character.xp) + "/" + str(character.nextLevel))
        write(self.game, 12, xPos+120, yPos+30, "Weapon: " + str(character.eqpWpn.name))
        write(self.game, 12, xPos+120, yPos+50, "Armor: " + str(character.eqpAmr.name))
        if character.eqpAcc.name == "NULL":
            name = "None"
        else:
            name = character.eqpAcc.name
        write(self.game, 12, xPos+120, yPos+70, "Accessory: " + str(name))

    def printEquipment(self):
        list = self.game.player.party.equipment
        for i in range(5):
            if i < len(list):
                write(self.game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.pageModifer) + ") " + self.game.directory.getItemName(list[i]))
            else:
                write(self.game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.pageModifer) + ")")
        write(self.game, 15, self.left+300, (self.top+310)+(25*self.cursorPos), "<-")

    def drawCharacterNameBlock(self,xPos,yPos,character):
        outlineRect = pygame.Rect(xPos,yPos,250,33)
        pygame.draw.rect(self.game.screen,self.game.white,outlineRect,2)
        write(self.game, 14, xPos+10, yPos+10, character.name + ", Level " + str(character.level) + " " + character.type.name)


class Shop(Building):
    def __init__(self,row,col,level):
        Building.__init__(self,row,col,level)
        self.shopInventory = []
        self.playerInventory = []
        self.shopPageModifier = 0
        self.targetItem = None

    def initializeOnEnter(self):
        if len(self.shopInventory) == 0:
            self.fillShopInventory()
        self.playerInventory = self.getTargetInventory()
        self.shopPageModifier = 0
        self.targetItem = None

    def getInput(self):
        if self.delay > 0:
            self.delay -= 1
            return
        if self.game.UP:
            print("UP")
            if self.state == "shopScreen":
                if self.cursorPos == 1 and self.shopPageModifier > 0:
                    self.shopPageModifier -= 1
                elif self.cursorPos > 0:
                    self.cursorPos -= 1
        if self.game.DOWN:
            print("DOWN")
            if self.state == "shopScreen":
                if self.cursorPos == 3 and (self.shopPageModifier+5 < len(self.shopInventory)):
                    self.shopPageModifier += 1
                elif self.cursorPos < 4 and self.cursorPos < len(self.shopInventory)-1:
                    self.cursorPos += 1
        if self.game.A:
            print("A")
            if self.state == "main":
                self.state = "shopScreen"
                self.substate = "none"
            elif self.state == "shopScreen":
                if self.player.gold > self.calculateCost(self.shopInventory[self.cursorPos+self.shopPageModifier]):
                    if self.canAddItem():
                        self.targetItem = self.shopInventory[self.cursorPos+self.shopPageModifier]
                        self.state = "confirmPurchase"
                    else:
                        self.substate = "inventoryFull"
                else:
                    self.substate = "tooExpensive"
            elif self.state == "confirmPurchase":
                self.player.gold -= self.calculateCost(self.targetItem)
                self.player.party.add(self.targetItem.id,self.game.directory)
                self.state = "shopScreen"
                self.substate = "purchased"
        if self.game.B:
            print("B")
            if self.state == "main":
                self.inMenu = False
            elif self.state == "shopScreen":
                self.state = "main"
                self.substate = "none"
            elif self.state == "confirmPurchase":
                self.state = "shopScreen"
                self.substate = "none"
        if self.game.X:
            print("X")
        if self.game.Y:
            print("Y")

    def drawScreen(self):
        self.game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.line(self.game.screen,self.game.white,(self.left,300),(self.right+9,300),2)
        pygame.draw.line(self.game.screen,self.game.white,(self.right-self.left-180,300),(self.right-self.left-180,self.bottom+8),2)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
        description = self.getShopDescription(self.state, self.substate)
        wrapWrite(self.game, 20, description, self.right-self.left-15)
        
        if self.state == "main":
            write(self.game, 30, self.left+10, self.top+305, self.getShopName())
            write(self.game, 25,self.right-150,self.top+340,"A) Shop")
            write(self.game, 25,self.right-150,self.top+390,"B) Leave")

        elif self.state == "shopScreen":
            self.printShopInventory()
            write(self.game, 25,self.right-150,self.top+340,"A) Buy")
            write(self.game, 25,self.right-150,self.top+390,"B) Back")

        elif self.state == "confirmPurchase":
            self.printStatBlock(self.targetItem)
            write(self.game, 25,self.right-150,self.top+340,"A) Confirm")
            write(self.game, 25,self.right-150,self.top+390,"B) Cancel")

    def printShopInventory(self):
        shopDisplay = []
        for i in range(5):
            if i + self.shopPageModifier >= len(self.shopInventory):
                shopDisplay.append("None")
            else:
                shopDisplay.append(self.shopInventory[i + self.shopPageModifier])
        for i in range(5):
            if shopDisplay[i] == "None":
                write(self.game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.shopPageModifier) + ")")
            else:
                write(self.game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.shopPageModifier) + ") " + self.game.directory.getItemName(shopDisplay[i]))
                writeOrientation(self.game, 20, self.right-self.left-200, (self.top+310)+(25*i), str(self.calculateCost(shopDisplay[i])) + "g", "R")
        write(self.game, 20,self.left+20,(self.top+310)+(25*self.cursorPos),">")

    def printStatBlock(self, item):
        if type(item) == int:
            item = self.game.directory.getItem(item)
        itemType = self.game.directory.getItemType(item)
        write(self.game, 20, self.left + 10, 315, item.name)
        wrapWrite(self.game, 15, item.description, self.right - self.left - 175, self.left + 10, 370)
        if itemType == Type.AtkSpell or itemType == Type.SptSpell:
            spelltype = "Attack" if item.type == SpellType.Attack or item.type == SpellType.Debuff else "Support"
            writeOrientation(self.game, 15, self.right - self.left - 185, 315, "Level "+str(item.rarity)+" "+spelltype+" Spell | "+str(item.manacost) + " MP", "R")
            if item.type == SpellType.Attack:
                write(self.game, 15, self.left + 10, 345, "Deals " + str(item.attack) + " damage.")
            elif item.type == SpellType.Buff:
                buffText = ""
                commaSeparator = ""
                if item.potency[0] > 0:
                    buffText += commaSeparator + "ATK +" + str(item.potency[0])
                    commaSeparator = ", "
                if item.potency[1] > 0:
                    buffText += commaSeparator + "ACC +" + str(item.potency[1])
                    commaSeparator = ", "
                if item.potency[2] > 0:
                    buffText += commaSeparator + "CRT +" + str(item.potency[2])
                    commaSeparator = ", "
                if item.potency[3] > 0:
                    buffText += commaSeparator + "DEF +" + str(item.potency[3])
                    commaSeparator = ", "
                if item.potency[4] > 0:
                    buffText += commaSeparator + "DDG +" + str(item.potency[4])
                    commaSeparator = ", "
                if item.potency[5] > 0:
                    buffText += commaSeparator + "LCK +" + str(item.potency[5])
                    commaSeparator = ", "
                if item.potency[6] > 0:
                    buffText += commaSeparator + "Regenerates " + str(item.potency[6]) + " HP each turn."
                write(self.game, 15, self.left + 10, 345, buffText)
            elif item.type == SpellType.Heal:
                write(self.game, 15, self.left + 10, 345, "Heals for " + str(item.potency[6]) + " HP.")
        elif itemType == Type.Weapon or itemType == Type.Armor or itemType == Accessory:
            statText = ""
            if itemType == Type.Weapon:
                writeOrientation(self.game, 15, self.right - self.left - 185, 315, "Level "+str(item.rarity)+" "+item.type.name, "R")
                if item.atkRefine > 0 or item.accRefine > 0 or item.crtRefine > 0:
                    writeOrientation(self.game, 15, self.right-40, 245, "+" + str(item.atkRefine) + "/+" + str(item.accRefine) + "/+" + str(item.crtRefine), "R")
                statText = "ATK " + str(item.getAttack()) + " | ACC " + str(item.getAccuracy()) + " | CRT " + str(item.getCritrate()) + " | AMP " + str(item.amplifier)
            elif itemType == Type.Armor:
                writeOrientation(self.game, 15, self.right - self.left - 185, 315, "Level "+str(item.rarity)+" "+item.type.name+" Armor", "R")
                if item.defRefine > 0 or item.ddgRefine > 0:
                    writeOrientation(self.game, 15, self.right - self.left - 185, 315, "+" + str(item.defRefine) + "/+" + str(item.ddgRefine))
                statText = "DEF " + str(item.getDefense()) + " | DDG " + str(item.getDodge()) + " | MPG " + str(item.manaregen)
            write(self.game, 15, self.left + 10, 345, statText)
        elif itemType == Type.Potion:
            statText = ""
            commaSeparator = ""
            if itemType == Type.Potion:
                if item.hpGain > 0:
                    statText += "+" + str(item.hpGain) + " HP"
                    commaSeparator = ", "
                if item.mpGain > 0:
                    statText += commaSeparator + "+" + str(item.mpGain) + " MP"
                write(self.game, 15, self.left + 10, 345, statText)
            if itemType == Type.AtkSpell or itemType == Type.SptSpell:
                spelltype = "Attack" if itemType == Type.AtkSpell else "Support"
                writeOrientation(self.game, 15, self.right - self.left - 185, 315, "Level "+str(item.rarity)+" "+spelltype+" Spell | "+str(item.manacost) + " MP", "R")
                writeOrientation(self.game, 15, self.right - self.left - 185, 315, "Use to learn spell.", "R")
                if item.type == SpellType.Attack:
                    write(self.game, 15, self.left + 10, 345, "Deals " + str(item.attack) + " damage.")
                elif item.type == SpellType.Buff:
                    buffText = ""
                    commaSeparator = ""
                    if item.potency[0] > 0:
                        buffText += commaSeparator + "ATK +" + str(item.potency[0])
                        commaSeparator = ", "
                    if item.potency[1] > 0:
                        buffText += commaSeparator + "ACC +" + str(item.potency[1])
                        commaSeparator = ", "
                    if item.potency[2] > 0:
                        buffText += commaSeparator + "CRT +" + str(item.potency[2])
                        commaSeparator = ", "
                    if item.potency[3] > 0:
                        buffText += commaSeparator + "DEF +" + str(item.potency[3])
                        commaSeparator = ", "
                    if item.potency[4] > 0:
                        buffText += commaSeparator + "DDG +" + str(item.potency[4])
                        commaSeparator = ", "
                    if item.potency[5] > 0:
                        buffText += commaSeparator + "LCK +" + str(item.potency[5])
                        commaSeparator = ", "
                    if item.potency[6] > 0:
                        buffText += commaSeparator + "Regenerates " + str(item.potency[6]) + " HP each turn."
                    write(self.game, 15, self.left + 10, 345, buffText)
                elif item.type == SpellType.Heal:
                    write(self.game, 15, self.left + 10, 345, "Heals for " + str(item.potency[6]) + " HP.")

    def getShopName(self):
        return "Shop"

    def getShopDescription(self,state,substate):
        return "Basic shop template!"

    def getTargetInventory(self):
        return self.player.party.equipment

    def fillShopInventory(self):
        for i in range(8):
            self.shopInventory.append(self.game.directory.getWeaponByRarity([WeaponType.Axe,WeaponType.Sword,WeaponType.Spear,WeaponType.Dagger,WeaponType.Staff],self.game.directory.getLootRarity(self.level,Type.Weapon)))
    
    def calculateCost(self, item):
        return 20
        
    def canAddItem(self):
        return len(self.playerInventory) < MAX_INVENTORY_SIZE


class Weaponsmith(Shop):
    def __init__(self,row,col,level):
        Shop.__init__(self,row,col,level)
        self.color = (90,176,72) # Green

    def getShopName(self):
        return "Weaponsmith"

    def getShopDescription(self,state,substate):
        description = ""
        if state == "main":
            description = "The inside of the shack is rather cluttered, with shelves and racks being full of weaponry. A burly-looking man stands behind a wooden counter. \
                'Ah, nice to see an out-of-towner for once. So? You gonna buy somethin', or just stand there? I've got the finest weapons gold can buy.'"
        elif state == "shopScreen" and substate == "none":
            description = "'Take a look, kid. I'm sure you'll find somethin' that'll pique your interest.'"
        elif state == "shopScreen" and substate == "purchased":
            description = "'You won't regret it, kid. Got your eye on anything else?'"
        elif state == "shopScreen" and substate == "inventoryFull":
            description = "'You, uh, might want to make some room in your backpack there first, kid...'"
        elif state == "shopScreen" and substate == "tooExpensive":
            description = "'Hey, you tryna hustle me or somethin'? Come back when you can afford it.'"
        elif state == "confirmPurchase":
            description = "'You want the " + self.game.directory.getItemName(self.targetItem) + "? That's gonna cost you 'bout " + str(self.calculateCost(self.targetItem)) + " gold.'"
        return description

    def getTargetInventory(self):
        return self.player.party.equipment

    def fillShopInventory(self):
        weaponTypes = [WeaponType.Axe,WeaponType.Sword,WeaponType.Spear,WeaponType.Dagger,WeaponType.Staff]
        random.shuffle(weaponTypes)
        shopWeaponTypes = weaponTypes[0:2]
        for weapon in self.game.directory.weaponDirectory:
            if weapon.rarity <= self.game.directory.getLootRarity(self.level, Type.Weapon)+1 and (weapon.type in shopWeaponTypes):
                self.shopInventory.append(weapon)

    def calculateCost(self, item):
        return 20 * round(item.rarity ** 1.5)
        
    def canAddItem(self):
        return len(self.playerInventory) < MAX_INVENTORY_SIZE


class Armory(Shop):
    def __init__(self,row,col,level):
        Shop.__init__(self,row,col,level)
        self.color = (255, 255, 0) # Yellow

    def getShopName(self):
        return "Armory"

    def getShopDescription(self,state,substate):
        description = ""
        if state == "main":
            description = "The armory is filled with racks with full suits of armor of different shapes and sizes. From a back room, you hear the clanging of metal. A young boy stands behind a small counter. \
                'Ah, hello! We've got lots of armor! You want some?'"
        elif state == "shopScreen" and substate == "none":
            description = "'Great! Take a look at what we have. My mom makes all of it by hand at the forge, so it's top quality.'"
        elif state == "shopScreen" and substate == "purchased":
            description = "'Really!? Thanks! You won't regret it!'"
        elif state == "shopScreen" and substate == "inventoryFull":
            description = "'Hey, uh, your bag looks pretty full there...'"
        elif state == "shopScreen" and substate == "tooExpensive":
            description = "'My mom says I shouldn't barter with this stuff... you sure you don't have any more gold on you?'"
        elif state == "confirmPurchase":
            description = "'Okay, so you want the " + self.game.directory.getItemName(self.targetItem) + "? Cool, that'll be... " + str(self.calculateCost(self.targetItem)) + " gold!'"
        return description

    def getTargetInventory(self):
        return self.player.party.equipment

    def fillShopInventory(self):
        armorTypes = [ArmorType.Light,ArmorType.Medium,ArmorType.Heavy,ArmorType.Robe]
        random.shuffle(armorTypes)
        shopArmorTypes = armorTypes[0:2]
        if ArmorType.Robe in shopArmorTypes:
            shopArmorTypes.append(ArmorType.Arcanist)
        for armor in self.game.directory.armorDirectory:
            if armor.rarity <= self.game.directory.getLootRarity(self.level, Type.Armor)+1 and (armor.type in shopArmorTypes):
                self.shopInventory.append(armor)

    def calculateCost(self, item):
        return 20 * round(item.rarity ** 1.5)
        
    def canAddItem(self):
        return len(self.playerInventory) < MAX_INVENTORY_SIZE


class GeneralStore(Shop):
    def __init__(self,row,col,level):
        Shop.__init__(self,row,col,level)
        self.color = (179,114,2) # Orange

    def getShopName(self):
        return "General Store + Bakery"

    def getShopDescription(self,state,substate):
        description = ""
        if state == "main":
            description = "A mystifying aroma hits you as you enter the store. A short, slender woman walks out from a back room, hastily taking off an apron and oven mitts. 'Sorry, sorry! It's a busy day \
                today, let me tell you... Anyway, what do you want? I've got a fresh batch of muffins ready to go!'"
        elif state == "shopScreen" and substate == "none":
            description = "'Here's our general exploring items menu. Aaaand over here we have our baked goods menu! What looks good to you?'"
        elif state == "shopScreen" and substate == "purchased":
            description = "'You know, a long day of shopping always works up my appetite, I dunno about you!'"
        elif state == "shopScreen" and substate == "inventoryFull":
            description = "'Hey, looks like your pockets are pretty full there!'"
        elif state == "shopScreen" and substate == "tooExpensive":
            description = "'Hey, my prices aren't that high! You can cough up a bit more gold to support your local bakery- I mean general store!'"
        elif state == "confirmPurchase":
            description = "'Ah, so you want the " + self.game.directory.getItemName(self.targetItem) + "... That'll be " + str(self.calculateCost(self.targetItem)) + " gold then. (you know, those go great with cookies...)'"
        return description

    def getTargetInventory(self):
        return self.player.party.inventory

    def fillShopInventory(self):
        for item in self.game.directory.potionDirectory:
            if item.rarity <= self.game.directory.getLootRarity(self.level, Type.Potion)+1:
                self.shopInventory.append(item)

    def calculateCost(self, item):
        return 20 * item.rarity
        
    def canAddItem(self):
        return len(self.playerInventory) < MAX_INVENTORY_SIZE


class Library(Shop):
    def __init__(self,row,col,level):
        Shop.__init__(self,row,col,level)
        self.color = (0,255,255) # Light Blue

    def getShopName(self):
        return "Library"

    def getShopDescription(self,state,substate):
        description = ""
        if state == "main":
            description = "The library is completely silent, with the only sound being the door gently closing behind you as you step inside. A tall man leans from around a tall bookshelf and shushes you. \
                He whispers toward you; '*excuse me, would you please peruse a little more quietly? You are disrupting the others.*' There is no one else here."
        elif state == "shopScreen" and substate == "none":
            description = "'*Spells, you say? Very well, we have a variety of scrolls here. Just don't rummage around so brutishly.*'"
        elif state == "shopScreen" and substate == "purchased":
            description = "'*Pleasure doing business with you. Will there be anything else for you this evening?*'"
        elif state == "shopScreen" and substate == "inventoryFull":
            description = "'*Excuse me, I think we both know quite well that you cannot carry this.*'"
        elif state == "shopScreen" and substate == "tooExpensive":
            description = "'*Ahem... You seem to lack the finances for that particular scroll.*'"
        elif state == "confirmPurchase":
            description = "'*Ah, the " + self.game.directory.getItemName(self.targetItem, True) + "? Excellent choice, that will be " + str(self.calculateCost(self.targetItem)) + " gold.*'"
        return description

    def getTargetInventory(self):
        return self.player.party.inventory

    def fillShopInventory(self):
        elements = [Element.Lightning, Element.Fire, Element.Ice]
        element = random.choice(elements)
        for spell in self.game.directory.atkSpellDirectory:
            if spell.rarity <= self.game.directory.getLootRarity(self.level, Type.AtkSpell)+1 and (spell.element == element):
                self.shopInventory.append(spell)

    def calculateCost(self, item):
        return 20 * round(item.rarity ** 1.5)
        
    def canAddItem(self):
        return len(self.playerInventory) < MAX_INVENTORY_SIZE


class Temple(Shop):
    def __init__(self,row,col,level):
        Shop.__init__(self,row,col,level)
        self.color = (255,255,255) # White

    def getShopName(self):
        return "Temple"

    def getShopDescription(self,state,substate):
        description = ""
        if state == "main":
            description = "The temple is serene, and a large stained glass window bathes the room in colored light, depicting a large golden bird soaring over a figure wielding a warhammer. 'Hi! You aren't \
                from around here, are you?' a soft voice says, as a tall, robed woman stands from a pew. 'Would you like to pray, or look over our scroll collection?'"
        elif state == "shopScreen" and substate == "none":
            description = "'Spells to help others, or yourself. Whatever Rendai wills.'"
        elif state == "shopScreen" and substate == "purchased":
            description = "'You made a great choice. I thank you.'"
        elif state == "shopScreen" and substate == "inventoryFull":
            description = "'I apologize, but I don't think you'll be able to fit that in your pack...'"
        elif state == "shopScreen" and substate == "tooExpensive":
            description = "'I'm sorry... but our temple needs to fund itself somehow.'"
        elif state == "confirmPurchase":
            description = "'Ah, the " + self.game.directory.getItemName(self.targetItem, True) + "! That'll just be " + str(self.calculateCost(self.targetItem)) + " gold, if you wouldn't mind.'"
        return description

    def getTargetInventory(self):
        return self.player.party.inventory

    def fillShopInventory(self):
        spellTypesA = [SpellType.Heal, SpellType.Buff]
        spellTypesB = [SpellType.Raise, SpellType.Cleanse]
        spellTypes = [random.choice(spellTypesA), random.choice(spellTypesB)]
        for spell in self.game.directory.sptSpellDirectory:
            if spell.rarity <= self.game.directory.getLootRarity(self.level, Type.SptSpell)+1 and (spell.type in spellTypes):
                self.shopInventory.append(spell)

    def calculateCost(self, item):
        return 20 * round(item.rarity ** 1.5)
        
    def canAddItem(self):
        return len(self.playerInventory) < MAX_INVENTORY_SIZE


class BlackMarket(Shop):
    def __init__(self,row,col,level):
        Shop.__init__(self,row,col,level)
        self.color = (85,85,85) # Dark Gray

    def getInput(self):
        if self.delay > 0:
            self.delay -= 1
            return
        if self.game.UP:
            print("UP")
            if self.state == "shopScreen" or self.state == "sellEquipmentScreen" or self.state == "sellInventoryScreen":
                if self.cursorPos == 1 and self.shopPageModifier > 0:
                    self.shopPageModifier -= 1
                elif self.cursorPos > 0:
                    self.cursorPos -= 1
        if self.game.DOWN:
            print("DOWN")
            if self.state == "shopScreen" or self.state == "sellEquipmentScreen" or self.state == "sellInventoryScreen":
                if self.cursorPos == 3 and (self.shopPageModifier+5 < len(self.shopInventory)):
                    self.shopPageModifier += 1
                elif self.cursorPos < 4 and self.cursorPos < len(self.shopInventory)-1:
                    self.cursorPos += 1
        if self.game.A:
            print("A")
            if self.state == "main":
                self.state = "shopScreen"
                self.substate = "none"
            elif self.state == "shopScreen":
                if self.player.gold > self.calculateCost(self.shopInventory[self.cursorPos+self.shopPageModifier]):
                    if self.canAddItem(self.shopInventory[self.cursorPos+self.shopPageModifier]):
                        self.targetItem = self.shopInventory[self.cursorPos+self.shopPageModifier]
                        self.state = "confirmPurchase"
                    else:
                        self.substate = "inventoryFull"
                else:
                    self.substate = "tooExpensive"
            elif self.state == "confirmPurchase":
                self.player.gold -= self.calculateCost(self.targetItem)
                if type(self.targetItem) == int:
                    itemID = self.targetItem
                else:
                    itemID = self.targetItem.id
                self.player.party.add(itemID,self.game.directory)
                self.state = "shopScreen"
                self.substate = "purchased"
            elif self.state == "sellInventorySelect":
                self.state = "sellEquipmentScreen"
                self.substate = "none"
                self.cursorPos = 0
                self.shopPageModifier = 0
            elif self.state == "sellInventoryScreen" or self.state == "sellEquipmentScreen": # NOTE: For the sell process, targetItem represents the index of the proper inventory where the target item is found
                if self.state == "sellEquipmentScreen":
                    if self.cursorPos < len(self.player.party.equipment):
                        self.targetItem = self.cursorPos+self.shopPageModifier
                        self.substate = "equipment"
                        self.state = "confirmSale"
                        self.cursorPos = 0
                        self.shopPageModifier = 0
                else:
                    if self.cursorPos < len(self.player.party.inventory):
                        self.targetItem = self.cursorPos+self.shopPageModifier
                        self.substate = "inventory"
                        self.state = "confirmSale"
                        self.cursorPos = 0
                        self.shopPageModifier = 0
            elif self.state == "confirmSale":
                if self.substate == "equipment":
                    self.state = "sellEquipmentScreen"
                    item = self.player.party.equipment[self.targetItem]
                    self.player.gold += self.calculateSellValue(item)
                    self.player.party.equipment.pop(self.targetItem)
                elif self.substate == "inventory":
                    self.state = "sellInventoryScreen"
                    item = self.player.party.inventory[self.targetItem]
                    self.player.gold += self.calculateSellValue(item)
                    self.player.party.inventory.pop(self.targetItem)
                self.substate = "purchased"
        if self.game.B:
            print("B")
            if self.state == "main":
                self.inMenu = False
            elif self.state == "shopScreen":
                self.state = "main"
                self.substate = "none"
            elif self.state == "sellInventorySelect":
                self.state = "main"
                self.substate = "none"
            elif self.state == "sellEquipmentScreen" or self.state == "sellInventoryScreen":
                self.state = "sellInventorySelect"
                self.substate = "none"
            elif self.state == "confirmPurchase":
                self.state = "shopScreen"
                self.substate = "none"
            elif self.state == "confirmSale":
                if self.substate == "equipment":
                    self.state = "sellEquipmentScreen"
                elif self.substate == "inventory":
                    self.state = "sellInventoryScreen"
                self.substate = "none"
        if self.game.X:
            print("X")
            if self.state == "main":
                self.state = "sellInventorySelect"
                self.substate = "none"
            elif self.state == "sellInventorySelect":
                self.state = "sellInventoryScreen"
                self.substate = "none"
                self.cursorPos = 0
                self.shopPageModifier = 0
        if self.game.Y:
            print("Y")

    def drawScreen(self):
        self.game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.line(self.game.screen,self.game.white,(self.left,300),(self.right+9,300),2)
        pygame.draw.line(self.game.screen,self.game.white,(self.right-self.left-180,300),(self.right-self.left-180,self.bottom+8),2)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
        description = self.getShopDescription(self.state, self.substate)
        wrapWrite(self.game, 20, description, self.right-self.left-15)
        
        if self.state == "main":
            write(self.game, 30, self.left+10, self.top+305, self.getShopName())
            write(self.game, 25,self.right-150,self.top+310,"A) Shop")
            write(self.game, 25,self.right-150,self.top+360,"X) Sell")
            write(self.game, 25,self.right-150,self.top+410,"B) Leave")

        elif self.state == "shopScreen":
            self.printShopInventory()
            write(self.game, 25,self.right-150,self.top+340,"A) Buy")
            write(self.game, 25,self.right-150,self.top+390,"B) Back")

        elif self.state == "confirmPurchase":
            self.printStatBlock(self.targetItem)
            write(self.game, 25,self.right-150,self.top+340,"A) Confirm")
            write(self.game, 25,self.right-150,self.top+390,"B) Cancel")

        elif self.state == "sellInventorySelect":
            write(self.game, 25,self.right-150,self.top+310,"A) Eqmnt")
            write(self.game, 25,self.right-150,self.top+360,"X) Items")
            write(self.game, 25,self.right-150,self.top+410,"B) Back")

        elif self.state == "sellEquipmentScreen" or self.state == "sellInventoryScreen":
            stock = []
            if self.state == "sellEquipmentScreen":
                stock = self.player.party.equipment
            elif self.state == "sellInventoryScreen":
                stock = self.player.party.inventory
            self.printSellInventory(stock)
            write(self.game, 25,self.right-150,self.top+340,"A) Sell")
            write(self.game, 25,self.right-150,self.top+390,"B) Back")

        elif self.state == "confirmSale":
            if self.substate == "equipment":
                self.printStatBlock(self.player.party.equipment[self.targetItem])
            elif self.substate == "inventory":
                self.printStatBlock(self.player.party.inventory[self.targetItem])
            write(self.game, 25,self.right-150,self.top+340,"A) Confirm")
            write(self.game, 25,self.right-150,self.top+390,"B) Cancel")

    def printSellInventory(self, stock):
        sellDisplay = []
        for i in range(5):
            if i + self.shopPageModifier >= len(stock):
                sellDisplay.append("None")
            else:
                sellDisplay.append(stock[i + self.shopPageModifier])
        for i in range(5):
            if sellDisplay[i] == "None":
                write(self.game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.shopPageModifier) + ")")
            else:
                write(self.game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.shopPageModifier) + ") " + self.game.directory.getItemName(sellDisplay[i]))
                writeOrientation(self.game, 20, self.right-self.left-200, (self.top+310)+(25*i), str(self.calculateSellValue(sellDisplay[i])) + "g", "R")
        write(self.game, 20,self.left+20,(self.top+310)+(25*self.cursorPos),">")

    def getShopName(self):
        return "Black Market"

    def getShopDescription(self,state,substate):
        description = ""
        if state == "main":
            description = "The shack is fairly dim, aside from a few lanterns sitting on tables around the room, shedding dim light onto a wide assortment of valuable-looking items. A gaunt woman with an \
                eyepatch steps back from examining a long blade with a magnifying glass, and toward a rickety wooden desk in the middle of the room. 'Ah, looking for the best of the best are we? Well you've come \
                to the right place. I can also take some of that extra junk off your hands too if you'd like.'"
        elif state == "shopScreen" and substate == "none":
            description = "'Only the finest, so long as you don't care about where they came from, if you catch my drift.'"
        elif state == "shopScreen" and substate == "purchased":
            description = "'No refunds.'"
        elif state == "shopScreen" and substate == "inventoryFull":
            description = "'You've got a lot of shit on you, mate.'"
        elif state == "shopScreen" and substate == "tooExpensive":
            description = "The woman flashes a dagger from her hip; 'Listen, you'd best have the gold if you're gonna be looking, you got it?'"
        elif state == "confirmPurchase":
            description = "Got your eye on the " + self.game.directory.getItemName(self.targetItem, True) + ", eh? " + str(self.calculateCost(self.targetItem)) + " gold, final offer."
        elif state == "sellEquipmentScreen" or state == "sellInventoryScreen" or state == "sellInventorySelect" and substate == "none":
            description = "Let me take a look at what you've got there. Maybe we can strike a deal."
        elif state == "sellEquipmentScreen" or state == "sellInventoryScreen" and substate == "purchased":
            description = "Pleasure doing business with you, mate."
        elif state == "confirmSale":
            if self.substate == "equipment":
                item = self.player.party.equipment[self.targetItem]
            if self.substate == "inventory":
                item = self.player.party.inventory[self.targetItem]
            description = "Hmm... I'll give ya " + str(self.calculateSellValue(item)) + " for the " + self.game.directory.getItemName(item) + ", how's that?"
        return description

    def getTargetInventory(self):
        return self.player.party.equipment

    def fillShopInventory(self):
        burnout = 0
        for i in range(5):
            item = self.game.directory.rollForLoot(self.level,LootRarity.Rare,[Type.Weapon,Type.Armor,Type.Accessory,Type.AtkSpell,Type.SptSpell])
            if item not in self.shopInventory:
                self.shopInventory.append(item)
            else:
                i -= 1
                burnout += 1
            if burnout > 50:
                return
    
    def calculateCost(self, item):
        return round(20 * (self.game.directory.getItemRarity(item) ** 1.8))

    def calculateSellValue(self, item):
        return round(15 * (self.game.directory.getItemRarity(item) ** .8))
        
    def canAddItem(self,item):
        if type(item) != int:
            item = item.id
        itemType = self.game.directory.getItemType(item)
        if itemType == Type.Weapon or itemType == Type.Armor or itemType == Type.Accessory:
            return len(self.player.party.equipment) < MAX_INVENTORY_SIZE
        elif itemType == Type.Potion:
            return len(self.player.party.inventory) < MAX_INVENTORY_SIZE
        return True


class Bazaar(Building):
    def __init__(self,row,col,level):
        Building.__init__(self,row,col,level)

    def getInput(self):
        if self.delay > 0:
            self.delay -= 1
            return
        if self.game.UP:
            print("UP")
        if self.game.DOWN:
            print("DOWN")
        if self.game.A:
            print("A")
        if self.game.B:
            print("B")
        if self.game.X:
            print("X")
        if self.game.Y:
            print("Y")

    def drawScreen(self):
        self.game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)


class Inn(Building):
    def __init__(self,row,col,level):
        Building.__init__(self,row,col,level)

    def getInput(self):
        if self.delay > 0:
            self.delay -= 1
            return
        if self.game.UP:
            print("UP")
        if self.game.DOWN:
            print("DOWN")
        if self.game.A:
            print("A")
        if self.game.B:
            print("B")
        if self.game.X:
            print("X")
        if self.game.Y:
            print("Y")

    def drawScreen(self):
        self.game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)