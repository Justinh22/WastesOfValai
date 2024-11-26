from game import *
from directory import *
from utility import *
from constants import *
from writing import *
from playerdata import *
from characterpopups import Hostel

BUILDING_HEIGHT = 4
BUILDING_WIDTH = 7

BUILDING_ROOF = '='
BUILDING_WALL = 'I'
BUILDING_DOOR = 'O'

class Building():
    def __init__(self,row,col,level):
        self.directory = None
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
        self.directory = game.directory
        self.player = player
        self.right = game.width - 20
        self.bottom = game.height - 20
        self.initializeOnEnter(game)
        self.display(game)

    def initializeOnEnter(self, game):
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

    def blitScreen(self,game):
        game.screen.blit(game.screen, (0,0))
        pygame.display.update()
        game.buttonReset()

    def display(self,game):
        self.inMenu = True
        game.screen.fill(game.black)
        self.drawScreen(game)
        while self.inMenu and game.inGame:
            game.eventHandler()
            self.getInput(game)
            if not self.inMenu:
                break
            self.drawScreen(game)
            self.blitScreen(game)
        game.screen.fill(game.black)
        self.blitScreen(game)

    def getInput(self,game):
        if self.delay > 0:
            self.delay -= 1
            return
        if game.UP:
            print("UP")
        if game.DOWN:
            print("DOWN")
        if game.A:
            print("A")
        if game.B:
            print("B")
        if game.X:
            print("X")
        if game.Y:
            print("Y")

    def drawScreen(self,game):
        game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(game.screen,game.white,screenOutline,2)

        if self.state == "main":
            write(game, 40, 30, 40, "Building")


class Forge(Building):
    def __init__(self,row,col,level):
        Building.__init__(self,row,col,level)
        self.color = (0,0,255) # Blue
        self.itemType = "none"
        self.targetItem = None
        self.reforgeTarget = None
        self.currentRefineLevel = []
        self.tentativeRefineLevel = []
        self.refinementStatCurrentValues = []
        self.refinementStatTentativeValues = []
        self.pageModifier = 0

    def initializeOnEnter(self, game):
        self.itemType = "none"
        self.targetItem = None
        self.currentRefineLevel = []
        self.tentativeRefineLevel = []
        self.refinementStatCurrentValues = []
        self.refinementStatTentativeValues = []
        self.reforgeableItems = []
        self.pageModifier = 0

    def getInput(self,game):
        if self.delay > 0:
            self.delay -= 1
            return
        if game.UP:
            print("UP")
            if self.state == "selectItem":
                if self.cursorPos == 1 and self.pageModifier > 0:
                    self.pageModifier -= 1
                elif self.cursorPos > 0:
                    self.cursorPos -= 1
            if self.state == "partySelect":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = len(game.player.party.members)-1
            if self.state == "weaponRefinement":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = 2
            if self.state == "armorRefinement":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = 1
            if self.state == "reforge":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = len(self.reforgeableItems)-1
        if game.DOWN:
            print("DOWN")
            if self.state == "selectItem":
                if self.cursorPos == 3 and (self.pageModifier+5 < len(self.player.party.equipment)):
                    self.pageModifier += 1
                elif self.cursorPos < 4 and self.cursorPos < len(self.player.party.equipment)-1:
                    self.cursorPos += 1
            if self.state == "partySelect":
                self.cursorPos += 1
                if self.cursorPos > len(game.player.party.members)-1:
                    self.cursorPos = 0
            if self.state == "weaponRefinement":
                self.cursorPos += 1
                if self.cursorPos > 2:
                    self.cursorPos = 0
            if self.state == "armorRefinement":
                self.cursorPos += 1
                if self.cursorPos > 1:
                    self.cursorPos = 0
            if self.state == "reforge":
                self.cursorPos += 1
                if self.cursorPos > len(self.reforgeableItems)-1:
                    self.cursorPos = 0
        if game.LEFT:
            if self.state == "weaponRefinement" or self.state == "armorRefinement":
                if self.tentativeRefineLevel[self.cursorPos] > self.currentRefineLevel[self.cursorPos]:
                    self.tentativeRefineLevel[self.cursorPos] -= 1
        if game.RIGHT:
            if self.state == "weaponRefinement" or self.state == "armorRefinement":
                if self.tentativeRefineLevel[self.cursorPos] < MAX_REFINE_LEVEL:
                    self.tentativeRefineLevel[self.cursorPos] += 1
        if game.A:
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
                self.targetItem = game.player.party.equipment[self.cursorPos]
                if self.directory.getItemType(self.targetItem) == Type.Weapon:
                     self.itemType = "weapon"
                elif self.directory.getItemType(self.targetItem) == Type.Armor:
                     self.itemType = "armor"
                if self.substate == "refine" and self.itemType == "weapon":
                    self.currentRefineLevel = [self.targetItem.atkRefine,self.targetItem.accRefine,self.targetItem.crtRefine]
                    self.tentativeRefineLevel = [self.targetItem.atkRefine,self.targetItem.accRefine,self.targetItem.crtRefine]
                    self.state = "weaponRefinement"
                elif self.substate == "refine" and self.itemType == "armor":
                    self.currentRefineLevel = [self.targetItem.defRefine,self.targetItem.ddgRefine]
                    self.tentativeRefineLevel = [self.targetItem.defRefine,self.targetItem.ddgRefine]
                    self.state = "armorRefinement"
                elif self.substate == "reforge":
                    if self.itemType == "weapon":
                        self.itemType = Type.Weapon
                    elif self.itemType == "armor":
                        self.itemType = Type.Armor
                    print(self.itemType)
                    self.fillReforgeList()
                    self.state = "reforge"
                    self.cursorPos = 0
                self.substate = "selectItem"
            elif self.state == "partySelect":
                if self.substate == "refine" and self.itemType == "weapon":
                    self.targetItem = game.player.party.members[self.cursorPos].eqpWpn
                    self.cursorPos = 0
                    self.currentRefineLevel = [self.targetItem.atkRefine,self.targetItem.accRefine,self.targetItem.crtRefine]
                    self.tentativeRefineLevel = [self.targetItem.atkRefine,self.targetItem.accRefine,self.targetItem.crtRefine]
                    self.state = "weaponRefinement"
                elif self.substate == "refine" and self.itemType == "armor":
                    self.targetItem = game.player.party.members[self.cursorPos].eqpAmr
                    self.cursorPos = 0
                    self.currentRefineLevel = [self.targetItem.defRefine,self.targetItem.ddgRefine]
                    self.tentativeRefineLevel = [self.targetItem.defRefine,self.targetItem.ddgRefine]
                    self.state = "armorRefinement"
                elif self.substate == "reforge":
                    if self.itemType == "weapon":
                        self.itemType = Type.Weapon
                        self.targetItem = game.player.party.members[self.cursorPos].eqpWpn
                    elif self.itemType == "armor":
                        self.itemType = Type.Armor
                        self.targetItem = game.player.party.members[self.cursorPos].eqpAmr
                    self.fillReforgeList()
                    self.state = "reforge"
                    self.cursorPos = 0
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
            elif self.state == "reforge":
                if self.player.gold >= self.calculateReforgePrice(self.targetItem):
                    self.reforgeTarget = self.reforgeableItems[self.cursorPos]
                    self.state = "confirmReforge"
            elif self.state == "confirmReforge":
                self.player.gold -= self.calculateReforgePrice(self.targetItem)
                self.targetItem.reforge(self.reforgeTarget)
                self.state = self.substate
                self.substate = "reforge"
                self.cursorPos = 0
        if game.B:
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
            elif self.state == "reforge":
                self.cursorPos = 0
                self.state = self.substate
                self.substate = "reforge"
            elif self.state == "confirmReforge":
                self.state = "reforge"
        if game.X:
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
        if game.Y:
            print("Y")
        if game.START:
            print("START")
            self.inMenu = False

    def drawScreen(self,game):
        game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.line(game.screen,game.white,(self.left,300),(self.right+9,300),2)
        pygame.draw.line(game.screen,game.white,(self.right-self.left-180,300),(self.right-self.left-180,self.bottom+8),2)
        pygame.draw.rect(game.screen,game.white,screenOutline,2)
        description = self.getDescription(self.state, self.substate)
        wrapWrite(game, 20, description, self.right-self.left-15)

        if self.state == "main":
            write(game, 30, self.left+10, self.top+305, "Forge")
            write(game, 25,self.right-150,self.top+310,"A) Refine")
            write(game, 25,self.right-150,self.top+360,"X) Reforge")
            write(game, 25,self.right-150,self.top+410,"B) Leave")

        elif self.state == "chooseInventory":
            write(game, 25,self.right-150,self.top+310,"A) Equipped")
            write(game, 25,self.right-150,self.top+360,"X) Inventory")
            write(game, 25,self.right-150,self.top+410,"B) Back")

        elif self.state == "selectItem":
            write(game, 25,self.right-150,self.top+340,"A) Select")
            write(game, 25,self.right-150,self.top+390,"B) Back")
            self.printEquipment(game)

        elif self.state == "chooseItemType":
            write(game, 25,self.right-150,self.top+310,"A) Weapon")
            write(game, 25,self.right-150,self.top+360,"X) Armor")
            write(game, 25,self.right-150,self.top+410,"B) Back")

        elif self.state == "chooseItemType" or self.state == "partySelect":
            write(game, 25,self.right-150,self.top+340,"A) Select")
            write(game, 25,self.right-150,self.top+390,"B) Back")
            write(game, 15, self.left+300, (self.top+310)+(25*self.cursorPos), "<-")
            for i, member in enumerate(self.player.party.members):
                write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1) + ") " + member.name)

        elif self.state == "weaponRefinement" or self.state == "armorRefinement" or self.state == "confirmWeaponRefine" or self.state == "confirmArmorRefine":
            write(game, 25, self.left+10, self.top+305, self.targetItem.name)
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
                cursorXVal, _ = write(game, 20, self.left+35, (self.top+340) + (i*25), refinementStat[i] + ": " + refinementString[i] + " - " + str(refinementStatCurrentValues[i]) + " -> " + str(refinementStatTentativeValues[i]))
            write(game, 20, self.left+320, (self.top+340) + (self.cursorPos*25), "<-")
            if self.state == "weaponRefinement" or self.state == "armorRefinement":
                write(game, 20, self.left+35, 430, "Cost: " + str(self.calculateCost(self.targetItem.rarity,self.currentRefineLevel,self.tentativeRefineLevel)) + " (You have: " + str(self.player.gold) + ")")
                write(game, 25,self.right-150,self.top+340,"A) Refine")
                write(game, 25,self.right-150,self.top+390,"B) Back")
            elif self.state == "confirmWeaponRefine" or self.state == "confirmArmorRefine":
                write(game, 25,self.right-150,self.top+340,"A) Confirm")
                write(game, 25,self.right-150,self.top+390,"B) Cancel")

        elif self.state == "reforge" or self.state == "confirmReforge":
            write(game, 25,self.right-150,self.top+340,"A) Confirm")
            write(game, 25,self.right-150,self.top+390,"B) Cancel")
            for i in range(len(self.reforgeableItems)):
                if self.reforgeableItems[i] == "None":
                    write(game, 20, self.left+35, (self.top+320)+(25*i), str(i+1) + ")")
                else:
                    write(game, 20, self.left+35, (self.top+320)+(25*i), str(i+1) + ") " + self.directory.getItemName(self.reforgeableItems[i]))
                    writeOrientation(game, 20, self.right-self.left-200, (self.top+320)+(25*i), str(self.calculateReforgePrice(self.targetItem)) + "g", "R")
            write(game, 20, self.left+300, (self.top+323) + (self.cursorPos*25), "<-")

    def getDescription(self,state,substate):
        description = ""
        if state == "main":
            description = "'Ah, welcome!' A short, thin man smiles warmly from the back of the forge, setting a mallet down on an anvil. 'What can I do for you today?'"
        elif state == "chooseInventory" or state == "selectItem" or state == "chooseItemType" or state == "partySelect":
            description = "'Take your time. I can bend and refine metal at your command.'"
        elif state == "weaponRefinement" or state == "armorRefinement":
            description = "'Show me a blade, and I can show you its true potential. For the right price, of course.'"
        elif state == "confirmWeaponRefine" or state == "confirmArmorRefine":
            description = "'Alright, so you want me to refine your " + self.targetItem.name + " to "
            divider = ""
            for entry in self.tentativeRefineLevel:
                description += divider + "+" + str(entry)
                if divider == "":
                    divider += "/"
            description += "? That'll just be " + str(self.calculateCost(self.targetItem.rarity,self.currentRefineLevel,self.tentativeRefineLevel)) + " gold, please.'"
        elif state == "reforge":
            description = "'People, we're stubborn. But metal... with a bit of convincing, it can become anything.'"
        elif state == "confirmReforge":
            description = "'So you'd like to turn your " + self.targetItem.name + " into a " + self.reforgeTarget.name + "? That'll cost you " + str(self.calculateReforgePrice(self.targetItem)) + " gold.'"
        return description

    def calculateCost(self,rarity,currentLevel,tentativeLevel):
        totalCost = 0
        for i in range(len(currentLevel)):
            for j in range(currentLevel[i]+1,tentativeLevel[i]+1):
                totalCost += 20 * rarity * j
        return totalCost
    
    def calculateReforgePrice(self,item):
        return 10 * round(item.rarity ** 1.5)

    def printEquipment(self,game):
        list = game.player.party.equipment
        for i in range(5):
            if i < len(list):
                write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.pageModifier) + ") " + self.directory.getItemName(list[i]))
            else:
                write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.pageModifier) + ")")
        write(game, 15, self.left+300, (self.top+310)+(25*self.cursorPos), "<-")

    def fillReforgeList(self):
        self.reforgeableItems = []
        rarity = self.targetItem.rarity
        if self.itemType == Type.Weapon:
            print(len(self.directory.weaponDirectory))
            for item in self.directory.weaponDirectory:
                print(self.directory.getItemName(item))
                if item.rarity == rarity and item.id != self.targetItem.id:
                    self.reforgeableItems.append(self.directory.getWeapon(item.id))
        elif self.itemType == Type.Armor:
            print(len(self.directory.armorDirectory))
            for item in self.directory.armorDirectory:
                print(self.directory.getItemName(item))
                if item.rarity == rarity and item.id != self.targetItem.id:
                    self.reforgeableItems.append(self.directory.getArmor(item.id))
        print("The reforge list is: ")
        for item in self.reforgeableItems:
            print(self.directory.getItemName(item))


class Shop(Building):
    def __init__(self,row,col,level):
        Building.__init__(self,row,col,level)
        self.shopInventory = []
        self.playerInventory = []
        self.shopPageModifier = 0
        self.targetItem = None

    def initializeOnEnter(self, game):
        if len(self.shopInventory) == 0:
            self.fillShopInventory()
        self.playerInventory = self.getTargetInventory()
        self.shopPageModifier = 0
        self.targetItem = None

    def getInput(self,game):
        if self.delay > 0:
            self.delay -= 1
            return
        if game.UP:
            print("UP")
            if self.state == "shopScreen":
                if self.cursorPos == 1 and self.shopPageModifier > 0:
                    self.shopPageModifier -= 1
                elif self.cursorPos > 0:
                    self.cursorPos -= 1
        if game.DOWN:
            print("DOWN")
            if self.state == "shopScreen":
                if self.cursorPos == 3 and (self.shopPageModifier+5 < len(self.shopInventory)):
                    self.shopPageModifier += 1
                elif self.cursorPos < 4 and self.cursorPos < len(self.shopInventory)-1:
                    self.cursorPos += 1
        if game.A:
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
                self.player.party.add(self.targetItem.id,self.directory)
                self.state = "shopScreen"
                self.substate = "purchased"
        if game.B:
            print("B")
            if self.state == "main":
                self.inMenu = False
            elif self.state == "shopScreen":
                self.state = "main"
                self.substate = "none"
            elif self.state == "confirmPurchase":
                self.state = "shopScreen"
                self.substate = "none"
        if game.X:
            print("X")
        if game.Y:
            print("Y")

    def drawScreen(self,game):
        game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.line(game.screen,game.white,(self.left,300),(self.right+9,300),2)
        pygame.draw.line(game.screen,game.white,(self.right-self.left-180,300),(self.right-self.left-180,self.bottom+8),2)
        pygame.draw.rect(game.screen,game.white,screenOutline,2)
        description = self.getShopDescription(self.state, self.substate)
        wrapWrite(game, 20, description, self.right-self.left-15)
        
        if self.state == "main":
            write(game, 30, self.left+10, self.top+305, self.getShopName())
            write(game, 25,self.right-150,self.top+340,"A) Shop")
            write(game, 25,self.right-150,self.top+390,"B) Leave")

        elif self.state == "shopScreen":
            self.printShopInventory(game)
            write(game, 25,self.right-150,self.top+340,"A) Buy")
            write(game, 25,self.right-150,self.top+390,"B) Back")

        elif self.state == "confirmPurchase":
            self.printStatBlock(self.targetItem,game)
            write(game, 25,self.right-150,self.top+340,"A) Confirm")
            write(game, 25,self.right-150,self.top+390,"B) Cancel")

    def printShopInventory(self,game):
        shopDisplay = []
        for i in range(5):
            if i + self.shopPageModifier >= len(self.shopInventory):
                shopDisplay.append("None")
            else:
                shopDisplay.append(self.shopInventory[i + self.shopPageModifier])
        for i in range(5):
            if shopDisplay[i] == "None":
                write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.shopPageModifier) + ")")
            else:
                write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.shopPageModifier) + ") " + self.directory.getItemName(shopDisplay[i]))
                writeOrientation(game, 20, self.right-self.left-200, (self.top+310)+(25*i), str(self.calculateCost(shopDisplay[i])) + "g", "R")
        write(game, 20,self.left+20,(self.top+310)+(25*self.cursorPos),">")

    def printStatBlock(self, item, game):
        if type(item) == int:
            item = self.directory.getItem(item)
        itemType = self.directory.getItemType(item)
        write(game, 15, self.left + 10, 315, item.name)
        wrapWrite(game, 15, item.description, self.right - self.left - 200, self.left + 10, 370)
        if itemType == Type.AtkSpell or itemType == Type.SptSpell:
            spelltype = "Attack" if item.type == SpellType.Attack or item.type == SpellType.Debuff else "Support"
            writeOrientation(game, 15, self.right - self.left - 185, 315, "Level "+str(item.rarity)+" "+spelltype+" Spell | "+str(item.manacost) + " MP", "R")
            if item.type == SpellType.Attack:
                write(game, 15, self.left + 10, 345, "Deals " + str(item.attack) + " damage.")
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
                write(game, 15, self.left + 10, 345, buffText)
            elif item.type == SpellType.Heal:
                write(game, 15, self.left + 10, 345, "Heals for " + str(item.potency[6]) + " HP.")
        elif itemType == Type.Weapon or itemType == Type.Armor or itemType == Accessory:
            statText = ""
            if itemType == Type.Weapon:
                writeOrientation(game, 15, self.right - self.left - 185, 315, "Level "+str(item.rarity)+" "+item.type.name, "R")
                if item.atkRefine > 0 or item.accRefine > 0 or item.crtRefine > 0:
                    writeOrientation(game, 15, self.right-40, 245, "+" + str(item.atkRefine) + "/+" + str(item.accRefine) + "/+" + str(item.crtRefine), "R")
                statText = "ATK " + str(item.getAttack()) + " | ACC " + str(item.getAccuracy()) + " | CRT " + str(item.getCritrate()) + " | AMP " + str(item.amplifier)
            elif itemType == Type.Armor:
                writeOrientation(game, 15, self.right - self.left - 185, 315, "Level "+str(item.rarity)+" "+item.type.name+" Armor", "R")
                if item.defRefine > 0 or item.ddgRefine > 0:
                    writeOrientation(game, 15, self.right - self.left - 185, 315, "+" + str(item.defRefine) + "/+" + str(item.ddgRefine))
                statText = "DEF " + str(item.getDefense()) + " | DDG " + str(item.getDodge()) + " | MPG " + str(item.manaregen)
            write(game, 15, self.left + 10, 345, statText)
        elif itemType == Type.Potion:
            statText = ""
            commaSeparator = ""
            if itemType == Type.Potion:
                if item.hpGain > 0:
                    statText += "+" + str(item.hpGain) + " HP"
                    commaSeparator = ", "
                if item.mpGain > 0:
                    statText += commaSeparator + "+" + str(item.mpGain) + " MP"
                write(game, 15, self.left + 10, 345, statText)
            if itemType == Type.AtkSpell or itemType == Type.SptSpell:
                spelltype = "Attack" if itemType == Type.AtkSpell else "Support"
                writeOrientation(game, 15, self.right - self.left - 185, 315, "Level "+str(item.rarity)+" "+spelltype+" Spell | "+str(item.manacost) + " MP", "R")
                writeOrientation(game, 15, self.right - self.left - 185, 315, "Use to learn spell.", "R")
                if item.type == SpellType.Attack:
                    write(game, 15, self.left + 10, 345, "Deals " + str(item.attack) + " damage.")
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
                    write(game, 15, self.left + 10, 345, buffText)
                elif item.type == SpellType.Heal:
                    write(game, 15, self.left + 10, 345, "Heals for " + str(item.potency[6]) + " HP.")

    def getShopName(self):
        return "Shop"

    def getShopDescription(self,state,substate):
        return "Basic shop template!"

    def getTargetInventory(self):
        return self.player.party.equipment

    def fillShopInventory(self):
        for i in range(8):
            self.shopInventory.append(self.directory.getWeaponByRarity([WeaponType.Axe,WeaponType.Sword,WeaponType.Spear,WeaponType.Dagger,WeaponType.Staff],self.directory.getLootRarity(self.level,Type.Weapon)))
    
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
            description = "'You want the " + self.directory.getItemName(self.targetItem) + "? That's gonna cost you 'bout " + str(self.calculateCost(self.targetItem)) + " gold.'"
        return description

    def getTargetInventory(self):
        return self.player.party.equipment

    def fillShopInventory(self):
        weaponTypes = [WeaponType.Axe,WeaponType.Sword,WeaponType.Spear,WeaponType.Dagger,WeaponType.Staff]
        random.shuffle(weaponTypes)
        shopWeaponTypes = weaponTypes[0:2]
        for weapon in self.directory.weaponDirectory:
            if weapon.rarity <= self.directory.getLootRarity(self.level, Type.Weapon)+1 and (weapon.type in shopWeaponTypes):
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
            description = "'Okay, so you want the " + self.directory.getItemName(self.targetItem) + "? Cool, that'll be... " + str(self.calculateCost(self.targetItem)) + " gold!'"
        return description

    def getTargetInventory(self):
        return self.player.party.equipment

    def fillShopInventory(self):
        armorTypes = [ArmorType.Light,ArmorType.Medium,ArmorType.Heavy,ArmorType.Robe]
        random.shuffle(armorTypes)
        shopArmorTypes = armorTypes[0:2]
        if ArmorType.Robe in shopArmorTypes:
            shopArmorTypes.append(ArmorType.Arcanist)
        for armor in self.directory.armorDirectory:
            if armor.rarity <= self.directory.getLootRarity(self.level, Type.Armor)+1 and (armor.type in shopArmorTypes):
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
            description = "'Ah, so you want the " + self.directory.getItemName(self.targetItem) + "... That'll be " + str(self.calculateCost(self.targetItem)) + " gold then. (you know, those go great with cookies...)'"
        return description

    def getTargetInventory(self):
        return self.player.party.inventory

    def fillShopInventory(self):
        for item in self.directory.potionDirectory:
            if item.rarity <= self.directory.getLootRarity(self.level, Type.Potion)+1:
                self.shopInventory.append(item)
        for item in self.directory.consumableDirectory:
            if item.rarity <= self.directory.getLootRarity(self.level, Type.Consumable)+1:
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
            description = "'*Ah, the " + self.directory.getItemName(self.targetItem, True) + "? Excellent choice, that will be " + str(self.calculateCost(self.targetItem)) + " gold.*'"
        return description

    def getTargetInventory(self):
        return self.player.party.inventory

    def fillShopInventory(self):
        elements = [Element.Lightning, Element.Fire, Element.Ice]
        element = random.choice(elements)
        for spell in self.directory.atkSpellDirectory:
            if spell.rarity <= self.directory.getLootRarity(self.level, Type.AtkSpell)+1 and (spell.element == element):
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
            description = "'Ah, the " + self.directory.getItemName(self.targetItem, True) + "! That'll just be " + str(self.calculateCost(self.targetItem)) + " gold, if you wouldn't mind.'"
        return description

    def getTargetInventory(self):
        return self.player.party.inventory

    def fillShopInventory(self):
        spellTypesA = [SpellType.Heal, SpellType.Buff]
        spellTypesB = [SpellType.Raise, SpellType.Cleanse]
        spellTypes = [random.choice(spellTypesA), random.choice(spellTypesB)]
        for spell in self.directory.sptSpellDirectory:
            if spell.rarity <= self.directory.getLootRarity(self.level, Type.SptSpell)+1 and (spell.type in spellTypes):
                self.shopInventory.append(spell)

    def calculateCost(self, item):
        return 20 * round(item.rarity ** 1.5)
        
    def canAddItem(self):
        return len(self.playerInventory) < MAX_INVENTORY_SIZE


class BlackMarket(Shop):
    def __init__(self,row,col,level):
        Shop.__init__(self,row,col,level)
        self.color = (85,85,85) # Dark Gray

    def getInput(self,game):
        if self.delay > 0:
            self.delay -= 1
            return
        if game.UP:
            print("UP")
            if self.state == "shopScreen" or self.state == "sellEquipmentScreen" or self.state == "sellInventoryScreen":
                if self.cursorPos == 1 and self.shopPageModifier > 0:
                    self.shopPageModifier -= 1
                elif self.cursorPos > 0:
                    self.cursorPos -= 1
        if game.DOWN:
            print("DOWN")
            if self.state == "shopScreen" or self.state == "sellEquipmentScreen" or self.state == "sellInventoryScreen":
                if self.cursorPos == 3 and (self.shopPageModifier+5 < len(self.shopInventory)):
                    self.shopPageModifier += 1
                elif self.cursorPos < 4 and self.cursorPos < len(self.shopInventory)-1:
                    self.cursorPos += 1
        if game.A:
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
                self.player.party.add(itemID,self.directory)
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
        if game.B:
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
        if game.X:
            print("X")
            if self.state == "main":
                self.state = "sellInventorySelect"
                self.substate = "none"
            elif self.state == "sellInventorySelect":
                self.state = "sellInventoryScreen"
                self.substate = "none"
                self.cursorPos = 0
                self.shopPageModifier = 0
        if game.Y:
            print("Y")

    def drawScreen(self,game):
        game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.line(game.screen,game.white,(self.left,300),(self.right+9,300),2)
        pygame.draw.line(game.screen,game.white,(self.right-self.left-180,300),(self.right-self.left-180,self.bottom+8),2)
        pygame.draw.rect(game.screen,game.white,screenOutline,2)
        description = self.getShopDescription(self.state, self.substate)
        wrapWrite(game, 20, description, self.right-self.left-15)
        
        if self.state == "main":
            write(game, 30, self.left+10, self.top+305, self.getShopName())
            write(game, 25,self.right-150,self.top+310,"A) Shop")
            write(game, 25,self.right-150,self.top+360,"X) Sell")
            write(game, 25,self.right-150,self.top+410,"B) Leave")

        elif self.state == "shopScreen":
            self.printShopInventory(game)
            write(game, 25,self.right-150,self.top+340,"A) Buy")
            write(game, 25,self.right-150,self.top+390,"B) Back")

        elif self.state == "confirmPurchase":
            self.printStatBlock(self.targetItem,game)
            write(game, 25,self.right-150,self.top+340,"A) Confirm")
            write(game, 25,self.right-150,self.top+390,"B) Cancel")

        elif self.state == "sellInventorySelect":
            write(game, 25,self.right-150,self.top+310,"A) Eqmnt")
            write(game, 25,self.right-150,self.top+360,"X) Items")
            write(game, 25,self.right-150,self.top+410,"B) Back")

        elif self.state == "sellEquipmentScreen" or self.state == "sellInventoryScreen":
            stock = []
            if self.state == "sellEquipmentScreen":
                stock = self.player.party.equipment
            elif self.state == "sellInventoryScreen":
                stock = self.player.party.inventory
            self.printSellInventory(stock,game)
            write(game, 25,self.right-150,self.top+340,"A) Sell")
            write(game, 25,self.right-150,self.top+390,"B) Back")

        elif self.state == "confirmSale":
            if self.substate == "equipment":
                self.printStatBlock(self.player.party.equipment[self.targetItem],game)
            elif self.substate == "inventory":
                self.printStatBlock(self.player.party.inventory[self.targetItem],game)
            write(game, 25,self.right-150,self.top+340,"A) Confirm")
            write(game, 25,self.right-150,self.top+390,"B) Cancel")

    def printSellInventory(self, stock, game):
        sellDisplay = []
        for i in range(5):
            if i + self.shopPageModifier >= len(stock):
                sellDisplay.append("None")
            else:
                sellDisplay.append(stock[i + self.shopPageModifier])
        for i in range(5):
            if sellDisplay[i] == "None":
                write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.shopPageModifier) + ")")
            else:
                write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.shopPageModifier) + ") " + self.directory.getItemName(sellDisplay[i]))
                writeOrientation(game, 20, self.right-self.left-200, (self.top+310)+(25*i), str(self.calculateSellValue(sellDisplay[i])) + "g", "R")
        write(game, 20,self.left+20,(self.top+310)+(25*self.cursorPos),">")

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
            description = "Got your eye on the " + self.directory.getItemName(self.targetItem, True) + ", eh? " + str(self.calculateCost(self.targetItem)) + " gold, final offer."
        elif state == "sellEquipmentScreen" or state == "sellInventoryScreen" or state == "sellInventorySelect" and substate == "none":
            description = "Let me take a look at what you've got there. Maybe we can strike a deal."
        elif state == "sellEquipmentScreen" or state == "sellInventoryScreen" and substate == "purchased":
            description = "Pleasure doing business with you, mate."
        elif state == "confirmSale":
            if self.substate == "equipment":
                item = self.player.party.equipment[self.targetItem]
            if self.substate == "inventory":
                item = self.player.party.inventory[self.targetItem]
            description = "Hmm... I'll give ya " + str(self.calculateSellValue(item)) + " for the " + self.directory.getItemName(item) + ", how's that?"
        return description

    def getTargetInventory(self):
        return self.player.party.equipment

    def fillShopInventory(self):
        burnout = 0
        for i in range(8):
            item = self.directory.rollForLoot(self.level,LootRarity.Rare,[Type.Weapon,Type.Armor,Type.Accessory,Type.AtkSpell,Type.SptSpell])
            if item not in self.shopInventory:
                self.shopInventory.append(item)
            else:
                i -= 1
                burnout += 1
            if burnout > 50:
                return
    
    def calculateCost(self, item):
        return round(20 * (self.directory.getItemRarity(item) ** 1.8))

    def calculateSellValue(self, item):
        return round(15 * (self.directory.getItemRarity(item) ** .8))
        
    def canAddItem(self,item):
        if type(item) != int:
            item = item.id
        itemType = self.directory.getItemType(item)
        if itemType == Type.Weapon or itemType == Type.Armor or itemType == Type.Accessory:
            return len(self.player.party.equipment) < MAX_INVENTORY_SIZE
        elif itemType == Type.Potion:
            return len(self.player.party.inventory) < MAX_INVENTORY_SIZE
        return True


class Bazaar(Building):
    def __init__(self,row,col,level):
        Building.__init__(self,row,col,level)

    def getInput(self,game):
        if self.delay > 0:
            self.delay -= 1
            return
        if game.UP:
            print("UP")
        if game.DOWN:
            print("DOWN")
        if game.A:
            print("A")
        if game.B:
            print("B")
        if game.X:
            print("X")
        if game.Y:
            print("Y")

    def drawScreen(self,game):
        game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(game.screen,game.white,screenOutline,2)


class Inn(Building):
    def __init__(self,row,col,level):
        Building.__init__(self,row,col,level)
        self.color = (255,0,0) # Red
        self.foodList = []
        self.pageModifier = 0

    def initializeOnEnter(self, game):
        if len(self.foodList) == 0:
            self.fillMenu()
        self.state = "main"
        self.substate = "none"

    def getInput(self,game):
        if self.delay > 0:
            self.delay -= 1
            return
        if game.UP:
            print("UP")
            if self.state == "menu":
                if self.cursorPos == 1 and self.pageModifier > 0:
                    self.pageModifier -= 1
                elif self.cursorPos > 0:
                    self.cursorPos -= 1
        if game.DOWN:
            print("DOWN")
            if self.state == "menu":
                if self.cursorPos == 3 and (self.pageModifier+5 < len(self.foodList)):
                    self.pageModifier += 1
                elif self.cursorPos < 4 and self.cursorPos < len(self.foodList)-1:
                    self.cursorPos += 1
        if game.A:
            print("A")
            if self.state == "main":
                self.player.party.removeFoodEffect(self.directory)
                self.player.party.fullRestore()
                game.save()
                self.substate = "rested"
            elif self.state == "menu":
                if self.player.gold > self.calculateCost(self.foodList[self.cursorPos+self.pageModifier]):
                    self.targetItem = self.foodList[self.cursorPos+self.pageModifier]
                    self.state = "confirmFood"
                else:
                    self.substate = "tooExpensive"
            elif self.state == "confirmFood":
                self.player.gold -= self.calculateCost(self.targetItem)
                print(self.targetItem.name)
                self.player.party.addFoodEffect(self.targetItem,self.directory)
                self.state = "menu"
                self.substate = "purchased"
        if game.B:
            print("B")
            if self.state == "main":
                self.inMenu = False
            elif self.state == "menu":
                self.state = "main"
                self.substate = "none"
            elif self.state == "confirmFood":
                self.state = "menu"
                self.substate = "none"
        if game.X:
            print("X")
            if self.state == "main":
                Hostel(game)
        if game.Y:
            print("Y")
            if self.state == "main":
                self.state = "menu"
                self.substate = "none"

    def drawScreen(self,game):
        game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.line(game.screen,game.white,(self.left,300),(self.right+9,300),2)
        pygame.draw.line(game.screen,game.white,(self.right-self.left-180,300),(self.right-self.left-180,self.bottom+8),2)
        pygame.draw.rect(game.screen,game.white,screenOutline,2)
        description = self.getDescription(self.state, self.substate)
        wrapWrite(game, 20, description, self.right-self.left-15)

        if self.state == "main":
            write(game, 20,self.right-155,self.top+310,"A) Rest")
            write(game, 20,self.right-155,self.top+340,"X) Hostel")
            write(game, 20,self.right-155,self.top+370,"Y) Eat")
            write(game, 20,self.right-155,self.top+400,"B) Leave")

        elif self.state == "menu":
            write(game, 25,self.right-150,self.top+340,"A) Buy")
            write(game, 25,self.right-150,self.top+390,"B) Back")
            shopDisplay = []
            for i in range(5):
                if i + self.pageModifier >= len(self.foodList):
                    shopDisplay.append("None")
                else:
                    shopDisplay.append(self.foodList[i + self.pageModifier])
            for i in range(5):
                if shopDisplay[i] == "None":
                    write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.pageModifier) + ")")
                else:
                    write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.pageModifier) + ") " + self.directory.getItemName(shopDisplay[i]))
                    writeOrientation(game, 20, self.right-self.left-200, (self.top+310)+(25*i), "40g", "R")
            write(game, 20,self.left+20,(self.top+310)+(25*self.cursorPos),">")

        elif self.state == "confirmFood":
            write(game, 25,self.right-150,self.top+340,"A) Confirm")
            write(game, 25,self.right-150,self.top+390,"B) Cancel")
            self.printStatBlock(self.targetItem,game)

    def getDescription(self,state,substate):
        description = ""
        if state == "main" and substate == "none":
            description = "You enter a cozy log cabin, with a roaring fire in the hearth. An old man sitting by the fire looks up as you enter; \
                'Ah, a visitor! Stay as long as you like, friend. The rooms are free of charge, it's rough out there. If you'd like anything to eat, \
                just let me know.'"
        elif state == "main" and substate == "rested":
            description = "'Mornin'! Hope you slept well.'"
        elif state == "menu" and substate == "none":
            description = "'Lots of good food here, take a look!'"
        elif state == "menu" and substate == "purchased":
            description = "'Enjoy!'"
        elif state == "menu" and substate == "tooExpensive":
            description = "'Sorry, friend. I've gotta keep my family fed somehow.'"
        elif state == "confirmFood":
            description = "'Ah, the " + self.targetItem.name + "? Great choice, that'll be 40 gold.'"
        return description
    
    def printStatBlock(self,item,game):
        write(game, 15, self.left + 10, 315, item.name)
        wrapWrite(game, 15, item.description, self.right - self.left - 190, self.left + 10, 370)
        writeOrientation(game, 15, self.right - self.left - 185, 315, "Rarity " + str(item.rarity) + " Food", "R")
        buffString = ""
        commaString = ""
        if item.buff[0] > 0:
            buffString += commaString + "MHP +" + str(item.buff[0])
            commaString = ", "
        elif item.buff[1] > 0:
            buffString += commaString + "MMP +" + str(item.buff[1])
            commaString = ", "
        elif item.buff[2] > 0:
            buffString += commaString + "ACC +" + str(item.buff[2])
            commaString = ", "
        elif item.buff[3] > 0:
            buffString += commaString + "CRT +" + str(item.buff[3])
            commaString = ", "
        elif item.buff[4] > 0:
            buffString += commaString + "DEF +" + str(item.buff[4])
            commaString = ", "
        elif item.buff[5] > 0:
            buffString += commaString + "ATK +" + str(item.buff[5])
            commaString = ", "
        elif item.buff[6] > 0:
            buffString += commaString + "LCK +" + str(item.buff[6])
            commaString = ", "
        elif item.buff[7] > 0:
            buffString += commaString + "MPG +" + str(item.buff[7])
            commaString = ", "
        elif item.buff[8] > 0:
            buffString += commaString + "AMP +" + str(item.buff[8])
            commaString = ", "
        elif item.buff[9] > 0:
            buffString += commaString + "DDG +" + str(item.buff[9])
            commaString = ", "
        elif item.buff[10] > 0:
            buffString += commaString + "SPD +" + str(item.buff[10])
            commaString = ", "
        elif item.buff[11] > 0:
            buffString += commaString + "HPG +" + str(item.buff[11])
            commaString = ", "
        write(game, 15, self.left + 10, 345, "Provides " + buffString + " to entire party.")
    
    def fillMenu(self):
        self.foodList = self.directory.getRandomFood(8)

    def calculateCost(self,item):
        return 40


class RuneCarver(Building):
    def __init__(self,row,col,level):
        Building.__init__(self,row,col,level)
        self.color = (173, 0, 0) # Maroon
        self.usage = "none"
        self.targetItem = None
        self.targetRune = None
        self.pageModifier = 0
        self.runeList = []

    def initializeOnEnter(self, game):
        self.runeList = []
        self.fillRuneList()
        self.usage = "none"
        self.targetItem = None
        self.targetRune = None
        self.pageModifier = 0

    def getInput(self,game):
        if self.delay > 0:
            self.delay -= 1
            return
        if game.UP:
            print("UP")
            if self.state == "selectItem":
                if self.cursorPos == 1 and self.pageModifier > 0:
                    self.pageModifier -= 1
                elif self.cursorPos > 0:
                    self.cursorPos -= 1
            if self.state == "partySelect":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = len(game.player.party.members)-1
            if self.state == "runeEtching":
                if self.cursorPos == 1 and self.pageModifier > 0:
                    self.pageModifier -= 1
                elif self.cursorPos > 0:
                    self.cursorPos -= 1
        if game.DOWN:
            print("DOWN")
            if self.state == "selectItem":
                if self.cursorPos == 3 and (self.pageModifier+5 < len(self.player.party.equipment)):
                    self.pageModifier += 1
                elif self.cursorPos < 4 and self.cursorPos < len(self.player.party.equipment)-1:
                    self.cursorPos += 1
            if self.state == "partySelect":
                self.cursorPos += 1
                if self.cursorPos > len(game.player.party.members)-1:
                    self.cursorPos = 0
            if self.state == "runeEtching":
                if self.cursorPos == 3 and (self.pageModifier+5 < len(self.runeList)):
                    self.pageModifier += 1
                elif self.cursorPos < 4 and self.cursorPos < len(self.runeList)-1:
                    self.cursorPos += 1
        if game.A:
            print("A")
            if self.state == "main":
                self.usage = "etch"
                self.state = "chooseInventory"
                self.cursorPos = 0
            elif self.state == "chooseInventory":
                self.state = "partySelect"
                self.cursorPos = 0
            elif self.state == "selectItem":
                self.cursorPos = 0
                self.targetItem = game.player.party.equipment[self.cursorPos]
                if self.usage == "etch":
                    self.state = "runeEtching"
                elif self.usage == "enhance" and self.targetItem.rune != None:
                    self.state = "runeEnhancement"
                self.substate = "selectItem"
            elif self.state == "partySelect":
                self.targetItem = game.player.party.members[self.cursorPos].eqpWpn
                if self.usage == "etch":
                    self.state = "runeEtching"
                elif self.usage == "enhance" and self.targetItem.rune != None:
                    self.state = "runeEnhancement"
                self.substate = "partySelect"
                self.cursorPos = 0
            elif self.state == "runeEtching":
                if self.player.gold >= self.calculateEtchPrice(self.targetItem):
                    self.targetRune = self.runeList[self.cursorPos+self.pageModifier]
                    self.state = "confirmEtch"
                else:
                    self.substate = "tooExpensive"
            elif self.state == "confirmEtch":
                self.player.gold -= self.calculateEtchPrice(self.targetItem)
                self.targetItem.etchRune(self.targetRune)
                self.state = self.substate
                self.substate = "none"
                self.cursorPos = 0
            elif self.state == "runeEnhancement":
                if self.targetItem.rune.level < 3:
                    if self.player.gold >= self.calculateEnhancePrice(self.targetItem) :
                        self.state = "confirmEnhancement"
                    else:
                        self.substate = "tooExpensive"
            elif self.state == "confirmEnhancement":
                self.player.gold -= self.calculateEnhancePrice(self.targetItem)
                self.targetItem.rune.level += 1
                self.state = self.substate
                self.substate = "none"
                self.cursorPos = 0
        if game.B:
            print("B")
            if self.state == "main":
                self.inMenu = False
            elif self.state == "chooseInventory":
                self.cursorPos = 0
                self.state = "main"
            elif self.state == "selectItem":
                self.cursorPos = 0
                self.state = "chooseInventory"
            elif self.state == "partySelect":
                self.cursorPos = 0
                self.state = "chooseInventory"
            elif self.state == "runeEtching":
                self.cursorPos = 0
                self.state = self.substate
                self.substate = None
            elif self.state == "confirmEtch":
                self.state = "runeEtching"
            elif self.state == "runeEnhancement":
                self.cursorPos = 0
                self.state = self.substate
                self.substate = None
            elif self.state == "confirmEnhancement":
                self.state = "runeEnhancement"
        if game.X:
            print("X")
            if self.state == "main":
                self.usage = "enhance"
                self.state = "chooseInventory"
                self.cursorPos = 0
            elif self.state == "chooseInventory":
                self.state = "selectItem"
                self.cursorPos = 0
        if game.Y:
            print("Y")
        if game.START:
            print("START")
            self.inMenu = False

    def drawScreen(self,game):
        game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.line(game.screen,game.white,(self.left,300),(self.right+9,300),2)
        pygame.draw.line(game.screen,game.white,(self.right-self.left-180,300),(self.right-self.left-180,self.bottom+8),2)
        pygame.draw.rect(game.screen,game.white,screenOutline,2)
        description = self.getDescription(self.state, self.substate)
        wrapWrite(game, 20, description, self.right-self.left-25)

        if self.state == "main":
            write(game, 30, self.left+10, self.top+305,"Rune Carver")
            write(game, 25,self.right-150,self.top+310,"A) Etch")
            write(game, 25,self.right-150,self.top+360,"X) Enhance")
            write(game, 25,self.right-150,self.top+410,"B) Back")

        elif self.state == "chooseInventory":
            write(game, 25,self.right-150,self.top+310,"A) Equipped")
            write(game, 25,self.right-150,self.top+360,"X) Inventory")
            write(game, 25,self.right-150,self.top+410,"B) Back")

        elif self.state == "selectItem":
            write(game, 25,self.right-150,self.top+340,"A) Select")
            write(game, 25,self.right-150,self.top+390,"B) Back")
            self.printEquipment(game)

        elif self.state == "partySelect":
            write(game, 25,self.right-150,self.top+340,"A) Select")
            write(game, 25,self.right-150,self.top+390,"B) Back")
            write(game, 15, self.left+300, (self.top+310)+(25*self.cursorPos), "<-")
            for i, member in enumerate(self.player.party.members):
                write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1) + ") " + member.name)

        elif self.state == "runeEtching":
            write(game, 25,self.right-150,self.top+340,"A) Select")
            write(game, 25,self.right-150,self.top+390,"B) Cancel")
            for i in range(len(self.runeList)):
                if self.runeList[i] == "None":
                    write(game, 20, self.left+35, (self.top+320)+(25*i), str(i+1) + ")")
                else:
                    write(game, 20, self.left+35, (self.top+320)+(25*i), str(i+1) + ") " + self.directory.getItemName(self.runeList[i]))
                    writeOrientation(game, 20, self.right-self.left-200, (self.top+320)+(25*i), str(self.calculateEtchPrice(self.targetItem)) + "g", "R")
            write(game, 20, self.left+300, (self.top+323) + (self.cursorPos*25), "<-")

        elif self.state == "confirmEtch":
            write(game, 25,self.right-150,self.top+340,"A) Confirm")
            write(game, 25,self.right-150,self.top+390,"B) Cancel")
            self.printStatBlock(self.targetRune, game)

        elif self.state == "runeEnhancement" or self.state == "confirmEnhancement":
            write(game, 25,self.right-150,self.top+340,"A) Select")
            write(game, 25,self.right-150,self.top+390,"B) Cancel")
            write(game, 20, self.left+35, self.top+320, self.targetItem.rune.name + " " + self.targetItem.rune.getRuneLevelString() + " -> " + self.targetItem.rune.getRuneLevelString(self.targetItem.rune.level+1))
            write(game, 20, self.left+35, self.top+345, "Enchancement cost: " + str(self.calculateEnhancePrice(self.targetItem)) + "g")

    def getDescription(self,state,substate):
        description = ""
        if state == "main":
            description = "The building is cold, all of the walls being made of solid stone. Small slips of paper with ancient text on them hand from the ceiling. \
                A massive, burly man sits cross-legged on the floor in front of a small stone table. 'I study runes. With right price, I carve runes. Hold out your weapon.'"
        elif state == "chooseInventory" or state == "selectItem" or state == "partySelect":
            description = "'Hold out your weapon.'"
        elif state == "runeEtching":
            description = "'Different runes... different effects. Bend the barrier between magical realm and ours.'"
        elif state == "runeEtching" and substate == "tooExpensive":
            description = "'Bring more gold.'"
        elif state == "confirmEtch": 
            description = "'I will etch " + self.targetItem.name + " with " + self.targetRune.name + "?"
        elif state == "runeEnhancement":
            description = "'More intricate runes... more potent effects.'"
        elif state == "runeEnhancement" and substate == "tooExpensive":
            description = "'Bring more gold.'"
        elif state == "confirmEnhancement":
            description = "'I will enhance your " + self.targetItem.name + "'s rune from " + self.targetItem.rune.getRuneLevelString() + " to " + self.targetItem.rune.getRuneLevelString(self.targetItem.rune.level+1) + "'?"
        return description

    def calculateEtchPrice(self,item):
        return 200
    
    def calculateEnhancePrice(self,item):
        if item.rune.level == 1:
            return 500
        elif item.rune.level == 2:
            return 1000

    def printEquipment(self,game):
        list = game.player.party.equipment
        for i in range(5):
            if i < len(list):
                write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.pageModifier) + ") " + self.directory.getItemName(list[i]))
            else:
                write(game, 20, self.left+35, (self.top+310)+(25*i), str(i+1+self.pageModifier) + ")")
        write(game, 15, self.left+300, (self.top+310)+(25*self.cursorPos), "<-")

    def fillRuneList(self):
        self.runeList = []
        tempRuneList = []
        for item in self.directory.runeDirectory:
            tempRuneList.append(self.directory.getRune(item.id))
        random.shuffle(tempRuneList)
        self.runeList = tempRuneList[0:4]
        for item in self.runeList:
            print(self.directory.getItemName(item))
    
    def printStatBlock(self,item,game):
        write(game, 15, self.left + 10, 315, item.name)
        wrapWrite(game, 15, item.description, self.right - self.left - 210, self.left + 10, 370)
        writeOrientation(game, 15, self.right - self.left - 185, 315, "Level " + item.getRuneLevelString() + " Rune", "R")
        