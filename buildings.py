from game import *
from directory import *
from utility import *
from constants import *
from writing import *
from playerdata import *

BUILDING_HEIGHT = 4
BUILDING_WIDTH = 7

BUILDING_WALL = '='
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

    def initializeOnEnter(self):
        self.itemType = "none"
        self.targetItem = None
        self.currentRefineLevel = []
        self.tentativeRefineLevel = []
        self.refinementStatCurrentValues = []
        self.refinementStatTentativeValues = []

    def getInput(self):
        if self.delay > 0:
            self.delay -= 1
            return
        if self.game.UP:
            print("UP")
            if self.state == "main":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = 2
            if self.state == "chooseInventory":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = 2
            if self.state == "selectItem":
                if self.cursorPos <= 1:
                    self.cursorPos += 8
                else:
                    self.cursorPos -= 2
            if self.state == "chooseItemType":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = 2
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
            if self.state == "main":
                self.cursorPos += 1
                if self.cursorPos > 2:
                    self.cursorPos = 0
            if self.state == "chooseInventory":
                self.cursorPos += 1
                if self.cursorPos > 2:
                    self.cursorPos = 0
            if self.state == "selectItem":
                if self.cursorPos >= 8:
                    self.cursorPos -= 8
                else:
                    self.cursorPos += 2
            if self.state == "chooseItemType":
                self.cursorPos += 1
                if self.cursorPos > 2:
                    self.cursorPos = 0
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
            if self.state == "selectItem":
                if self.cursorPos % 2 == 0:
                    self.cursorPos += 1
                else:
                    self.cursorPos -= 1
            if self.state == "weaponRefinement" or self.state == "armorRefinement":
                if self.tentativeRefineLevel[self.cursorPos] > self.currentRefineLevel[self.cursorPos]:
                    self.tentativeRefineLevel[self.cursorPos] -= 1
        if self.game.RIGHT:
            if self.state == "selectItem":
                if self.cursorPos % 2 == 0:
                    self.cursorPos += 1
                else:
                    self.cursorPos -= 1
            if self.state == "weaponRefinement" or self.state == "armorRefinement":
                if self.tentativeRefineLevel[self.cursorPos] < MAX_REFINE_LEVEL:
                    self.tentativeRefineLevel[self.cursorPos] += 1
        if self.game.A:
            print("A")
            if self.state == "main":
                if self.cursorPos == 0:
                    self.state = "chooseInventory"
                    self.substate = "refine"
                    self.cursorPos = 0
                elif self.cursorPos == 1:
                    self.state = "chooseInventory"
                    self.substate = "reforge"
                    self.cursorPos = 0
                elif self.cursorPos == 2:
                    self.inMenu = False
            elif self.state == "chooseInventory":
                if self.cursorPos == 0:
                    self.state = "chooseItemType"
                    self.cursorPos = 0
                elif self.cursorPos == 1:
                    self.state = "selectItem"
                    self.cursorPos = 0
                elif self.cursorPos == 2:
                    self.state = "main"
                    self.cursorPos = 0
            elif self.state == "chooseItemType":
                if self.cursorPos == 0:
                    self.state = "partySelect"
                    self.itemType = "weapon"
                    self.cursorPos = 0
                elif self.cursorPos == 1:
                    self.state = "partySelect"
                    self.itemType = "armor"
                    self.cursorPos = 0
                elif self.cursorPos == 2:
                    self.state = "chooseInventory"
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
        if self.game.Y:
            print("Y")
        if self.game.START:
            print("START")
            self.inMenu = False

    def drawScreen(self):
        self.game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)

        if self.state == "main":
            write(self.game, 40, 30, 40, "Forge")
            write(self.game, 20, 60, 90, "Refine")
            write(self.game, 20, 60, 115, "Reforge")
            write(self.game, 20, 60, 140, "Exit")
            write(self.game, 20, 30, 87 + (self.cursorPos*25), "->")
            for i in range(0,len(self.game.player.party.members)):
                self.drawEquipmentBlock(250, 45 + (i*100), self.game.player.party.members[i])

        elif self.state == "chooseInventory" or self.state == "selectItem":
            write(self.game, 40, 30, 40, "Forge")
            write(self.game, 20, 60, 90, "Equipped")
            write(self.game, 20, 60, 115, "Inventory")
            write(self.game, 20, 60, 140, "Back")
            if self.state == "chooseInventory":
                write(self.game, 20, 30, 87 + (self.cursorPos*25), "->")
                for i in range(0,len(self.game.player.party.members)):
                    self.drawEquipmentBlock(250, 45 + (i*100), self.game.player.party.members[i])
            elif self.state == "selectItem":
                self.printEquipment()

        elif self.state == "chooseItemType" or self.state == "partySelect":
            write(self.game, 40, 30, 40, "Forge")
            write(self.game, 20, 60, 90, "Weapon")
            write(self.game, 20, 60, 115, "Armor")
            write(self.game, 20, 60, 140, "Back")
            if self.state == "chooseItemType":
                write(self.game, 20, 30, 87 + (self.cursorPos*25), "->")
            elif self.state == "partySelect":
                write(self.game, 30, 210, 75 + (self.cursorPos*100), "->")
            for i in range(0,len(self.game.player.party.members)):
                self.drawEquipmentBlock(250, 45 + (i*100), self.game.player.party.members[i])

        elif self.state == "weaponRefinement" or self.state == "armorRefinement" or self.state == "confirmWeaponRefine" or self.state == "confirmArmorRefine":
            write(self.game, 40, 30, 40, "Refining")
            write(self.game, 35, 30, 145, self.targetItem.name)
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
                cursorXVal, _ = write(self.game, 25, 30, 200 + (i*40), refinementStat[i] + ": " + refinementString[i] + " - " + str(refinementStatCurrentValues[i]) + " -> " + str(refinementStatTentativeValues[i]))
            if self.state == "weaponRefinement" or self.state == "armorRefinement":
                write(self.game, 20, 120 + cursorXVal, 202 + (self.cursorPos*40), "<-")
                write(self.game, 20, 30, 350, "Cost: " + str(self.calculateCost(self.targetItem.rarity,self.currentRefineLevel,self.tentativeRefineLevel)) + " (You have: " + str(self.player.gold) + ")")
                write(self.game, 20, 30, 380, "A) Refine")
                write(self.game, 20, 130, 380, "B) Back")
            elif self.state == "confirmWeaponRefine" or self.state == "confirmArmorRefine":
                write(self.game, 15, 30, 350, "Refine your " + self.targetItem.name + " for " +  str(self.calculateCost(self.targetItem.rarity,self.currentRefineLevel,self.tentativeRefineLevel)) + " gold?")
                write(self.game, 20, 30, 380, "A) Confirm")
                write(self.game, 20, 180, 380, "B) Cancel")

    def calculateCost(self,rarity,currentLevel,tentativeLevel):
        totalCost = 0
        for i in range(len(currentLevel)):
            for j in range(currentLevel[i]+1,tentativeLevel[i]+1):
                print(f'{i}: {j}')
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
            if i*2 < len(list):
                write(self.game, 15, 100, 275 + (25*i), str((i*2)+1) + ") " + self.game.directory.getItemName(list[i*2],False))
            else:
                write(self.game, 15, 100, 275 + (25*i), str((i*2)+1) + ") ")
            if (i*2)+1 < len(list):
                write(self.game, 15, 350, 275 + (25*i), str((i*2)+2) + ") " + self.game.directory.getItemName(list[(i*2)+1],False))
            else:
                write(self.game, 15, 350, 275 + (25*i), str((i*2)+2) + ") ")
        write(self.game, 15, 85 + ((self.cursorPos%2)*250), 272 + (25*(math.floor(self.cursorPos/2))), ">")

    def drawCharacterNameBlock(self,xPos,yPos,character):
        outlineRect = pygame.Rect(xPos,yPos,250,33)
        pygame.draw.rect(self.game.screen,self.game.white,outlineRect,2)
        write(self.game, 14, xPos+10, yPos+10, character.name + ", Level " + str(character.level) + " " + character.type.name)


class Shop(Building):
    def __init__(self,row,col,level):
        Building.__init__(self,row,col,level)
        self.color = (90,176,72) # Green
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
                elif self.cursorPos < 4:
                    self.cursorPos += 1
        if self.game.A:
            print("A")
            if self.state == "main":
                self.state = "shopScreen"
                self.substate = "none"
            elif self.state == "shopScreen":
                if self.player.gold > self.calculateCost(self.shopInventory[self.cursorPos+self.shopPageModifier]):
                    if len(self.playerInventory) < MAX_INVENTORY_SIZE:
                        self.targetItem = self.shopInventory[self.cursorPos+self.shopPageModifier]
                        self.state = "confirmPurchase"
                    else:
                        self.substate = "inventoryFull"
                else:
                    self.substate = "tooExpensive"
            elif self.state == "confirmPurchase":
                self.player.gold -= self.calculateCost(self.targetItem)
                self.player.party.add(self.game.directory.copy(self.targetItem),self.game.directory)
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
        
        if self.state == "main":
            description = self.getShopDescription(self.state)
            wrapWrite(self.game, 20, description, self.right-self.left-15)
            write(self.game, 25,self.right-150,self.top+340,"A) Shop")
            write(self.game, 25,self.right-150,self.top+390,"B) Leave")

        elif self.state == "shopScreen":
            description = self.getShopDescription(self.state)
            self.printShopInventory()
            write(self.game, 25,self.right-150,self.top+340,"A) Buy")
            write(self.game, 25,self.right-150,self.top+390,"B) Back")

        elif self.state == "confirmPurchase":
            description = self.getShopDescription(self.state)
            self.printShopInventory()
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

    def getShopName(self):
        return "Shop"

    def getShopDescription(self,state):
        return "Basic shop template!"

    def getTargetInventory(self):
        return self.player.party.equipment

    def fillShopInventory(self):
        for i in range(8):
            self.shopInventory.append(self.game.directory.getWeaponByRarity([WeaponType.Axe,WeaponType.Sword,WeaponType.Spear,WeaponType.Dagger,WeaponType.Staff],self.game.directory.getLootRarity(self.level,Type.Weapon)))

    def calculateCost(self, item):
        return 20


class Weaponsmith(Shop):
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


class Armory(Shop):
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


class TradingPost(Shop):
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


class Library(Shop):
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


class Temple(Shop):
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