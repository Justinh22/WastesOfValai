import pygame
from room import * # Includes feature.py, directory.py, and constants.py
from writing import *
from utility import *
from characterpopups import *

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
        self.slept = False
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
        while self.inRoom and self.game.inGame:
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
        if self.game.keys["A"]:
            if self.state == "main":
                self.state = "lookList"
                self.delay = 5
            elif self.state == "lookList":
                self.delay = 5
                self.state = "featureCheck"
            elif self.state == "featureCheck":
                self.delay = 5
                if self.room.type == "room" or (self.room.type == "haven" and (self.room.features[self.cursorPos].name != "Beds" and self.room.features[self.cursorPos].name != "Wanderer")):
                    if self.room.features[self.cursorPos].lootStatus != LootStatus.Taken:
                        self.takeItem(self.cursorPos)
                if self.room.type == "haven" and self.room.features[self.cursorPos].name == "Beds":
                    self.game.player.party.fullRestore()
                    self.game.player.party.removeFoodEffect(self.game.directory)
                    self.game.save()
                    self.slept = True
                if self.room.type == "haven" and self.room.features[self.cursorPos].name == "Wanderer":
                    lvl = difficultyToLevel(self.room.difficulty)
                    if difficultyToLevel(self.room.difficulty) > self.game.player.party.getHighestLevel():
                        lvl = self.game.player.party.getHighestLevel()
                    if len(self.game.player.party.members) < 4:
                        self.game.player.party.members.append(self.game.directory.buildCharacter(lvl,self.game.player.party.members,self.game.player.getNewCharID()))
                    else:
                        CharacterSwap(self.game,self.game.directory.buildCharacter(lvl,self.game.player.party.members,self.game.player.getNewCharID()))
                    self.room.features[self.cursorPos].lootStatus = LootStatus.Taken
                    self.room.features.pop(self.cursorPos)
                    self.state = "lookList"
                    self.cursorPos = 0
                    self.room.featureLen -= 1
                    self.room.wanderer = False
            print("A")
        if self.game.keys["B"]:
            if self.state == "main":
                self.inRoom = False
            elif self.state == "lookList":
                self.delay = 5
                self.state = "main"
            elif self.state == "featureCheck":
                self.delay = 5
                self.state = "lookList"
            print("B")
        if self.game.keys["X"]:
            print("X")
            if self.state == "main" and self.room.type == "haven" and len(self.game.player.hostel) > 0:
                print("Hostel")
                Hostel(self.game)
        if self.game.keys["Y"]:
            print("Y")
        if self.game.keys["UP"]:
            if self.state == "lookList":
                self.cursorPos -= 1
                if self.cursorPos < 0:
                    self.cursorPos = self.room.featureLen-1
            print("UP")
        if self.game.keys["DOWN"]:
            if self.state == "lookList":
                self.cursorPos += 1
                if self.cursorPos > self.room.featureLen-1:
                       self.cursorPos = 0
            print("DOWN")
        if self.game.keys["LEFT"]:
            print("LEFT")
        if self.game.keys["RIGHT"]:
            print("RIGHT")

    def drawScreen(self):
        self.game.screen.fill(self.game.black)
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
        pygame.draw.line(self.game.screen,self.game.white,(self.left,300),(self.right+9,300),2)
        pygame.draw.line(self.game.screen,self.game.white,(self.right-self.left-180,300),(self.right-self.left-180,self.bottom+8),2)
        description = self.room.description
        if self.room.wanderer:
            description += " A figure sits by the hearth, warming by the flames."
        wrapWrite(self.game, 20,description,self.right-self.left-15)
        if self.state == "main":
            write(self.game, 25,self.right-150,self.top+340,"A) Look")
            write(self.game, 25,self.right-150,self.top+390,"B) Leave")
            if self.room.type == "haven" and len(self.game.player.hostel) > 0:
                write(self.game, 15, self.left+10, self.top+310, "Press (X) to access hostel.")
        if self.state == "lookList":
            write(self.game, 25,self.right-150,self.top+340,"A) Check")
            write(self.game, 25,self.right-150,self.top+390,"B) Back")
            write(self.game, 20,self.left+20,(self.top+310)+(25*self.cursorPos),">")
            for i in range(self.room.featureLen):
                write(self.game, 20,self.left+35,(self.top+310)+(25*i),str(i+1)+") "+self.room.features[i].name)
        if self.state == "featureCheck":
            text = self.room.features[self.cursorPos].description
            if self.room.features[self.cursorPos].loot != -1 and self.room.features[self.cursorPos].lootStatus != LootStatus.Taken:
                write(self.game, 25,self.right-150,self.top+340,"A) Take")
                text += " You see a " + self.game.directory.getItemName(self.room.features[self.cursorPos].loot,True) + "."
                self.room.features[self.cursorPos].lootStatus = LootStatus.Discovered
            if self.room.features[self.cursorPos].name == "Beds" and self.room.type == "haven" and self.slept == False:
                write(self.game, 25,self.right-150,self.top+340,"A) Sleep")
            if self.room.features[self.cursorPos].name == "Wanderer" and self.room.type == "haven":
                write(self.game, 25,self.right-150,self.top+340,"A) Speak")
            write(self.game, 25,self.right-150,self.top+390,"B) Back")
            wrapWrite(self.game, 15,text,self.right-self.left-200,self.left+10,self.top+310)

            
    def takeItem(self,index):
        id = self.room.features[index].loot
        type = self.game.directory.getItemType(id)
        if type == Type.Weapon or type == Type.Armor:
            if self.game.player.party.addEquipment(self.game.directory.getItem(id)):
                self.room.features[index].lootStatus = LootStatus.Taken
            else:
                return False
        elif type == Type.Potion or type == Type.Consumable:
            if self.game.player.party.addItem(id):
                self.room.features[index].lootStatus = LootStatus.Taken
            else:
                return False
        elif type == Type.AtkSpell or type == Type.SptSpell:
            if self.game.player.party.addItem(id):
                self.room.features[index].lootStatus = LootStatus.Taken
            else:
                return False
        return True