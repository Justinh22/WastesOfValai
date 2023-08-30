import pygame
import random
import time
from characters import Action
from characters import Buff
from dialogue import *

class Combat():
    def __init__(self,game):
        self.game = game
        self.inCombat = False
        self.left = 10
        self.top = 10
        self.right = self.game.width - 20
        self.bottom = self.game.height - 20
        self.menu_top = 350
        self.menu_height = self.bottom-340
        self.font = pygame.font.Font('freesansbold.ttf',20)
        self.party = None
        self.encounter = []
        self.combatOrder = []
        self.currentTurn = 0
        self.actions = []
        self.actionVal = -1
        self.state = "mainWindow"
        self.delay = 0
        self.ex = False
        self.exTurn = 0
        self.timeStart = 0
        self.dmg = 0
        self.waitFlag = False
        self.cursorPos = -1
        self.menuTop = -1
        self.itemID = -1
        self.spellID = -1
        self.lowMana = False
        self.buffs = []
        self.combatDialogue = ""

    def initialize(self,party,encounter):
        self.party = party
        for i in range(0,len(self.party.members)):
            print(f'{self.party.members[i].name}, {self.party.members[i].type.name}, {self.party.members[i].level} (ID {self.party.members[i].id}) - WPN: {self.party.members[i].eqpWpn.name}, AMR: {self.party.members[i].eqpAmr.name}, HP: {self.party.members[i].hpMax}, MP: {self.party.members[i].mpMax}, ATK: {self.party.members[i].attack}, CRT: {self.party.members[i].critrate}, DEF: {self.party.members[i].defense}, DDG: {self.party.members[i].dodge}, LCK: {self.party.members[i].luck}, SPD: {self.party.members[i].speed}, PRS: {self.party.members[i].personality}, SPELLS: {self.party.members[i].spells}')
        self.encounter = encounter
        for i in range(0,len(self.encounter)):
            print(f'{self.encounter[i].name}, {self.encounter[i].level} - SPD: {self.encounter[i].speed}')

        self.combatOrder = []
        members = self.party.members + self.encounter
        members.sort(key=lambda x: x.speed)
        members.reverse()
        for i in range(len(members)-1,-1,-1):
            if members[i].hp <= 0:
                members.pop(i)
        seenPty = [0] * len(self.party.members)
        seenEnc = [0] * len(self.encounter)
        for entry in members:
            for i in range(len(self.party.members)):
                if entry.id == self.party.members[i].id:
                    if seenPty[i] == 1:
                        continue
                    self.combatOrder.append(("Party",i))
                    seenPty[i] = 1
                    break
            for i in range(len(self.encounter)):
                if entry.id == self.encounter[i].id:
                    if seenEnc[i] == 1:
                        continue
                    self.combatOrder.append(("Encounter",i))
                    seenEnc[i] = 1
                    break

        for entry in self.combatOrder:
            print(entry)
        if self.combatOrder[self.currentTurn][0] == "Encounter":
            self.enemyAction(self.combatOrder[self.currentTurn])
            self.next()
        if self.combatOrder[self.currentTurn][0] == "Party":
            self.combatDialogue = getCombatDialogue(self.party.members[self.combatOrder[self.currentTurn][1]])
        self.inCombat = True
        self.state = "mainWindow"
        self.delay = 5

    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0,0))
        pygame.display.update()
        self.game.buttonReset()

    def display(self):
        self.game.screen.fill(self.game.black)
        self.state = "mainWindow"
        self.drawScreen()
        while self.inCombat:
            self.game.eventHandler()
            self.getInput()
            if self.inCombat == False:
                break
            self.execute()
            self.gameStatus()
            self.drawScreen()
            self.blitScreen()
        self.game.screen.fill(self.game.black)
        self.blitScreen()

    def getInput(self):
        if self.delay > 0:
            self.delay -= 1
            return
        if self.game.A:
            if self.state == "mainWindow":
                self.cursorPos = 0
                self.actionVal = 0
                self.state = "targetSelect"
                print("ATTACK")
            elif self.state == "useMenu":
                if self.cursorPos == 0:
                    self.state = "spellList"
                    self.cursorPos = 0
                    self.menuTop = 0
                    print("SPELL")
                elif self.cursorPos == 1:
                    self.state = "itemList"
                    self.cursorPos = 0
                    self.menuTop = 0
                    print("ITEM")
                elif self.cursorPos == 2:
                    self.state = "useMenu"
                    print("ART")
                elif self.cursorPos == 3:
                    self.state = "mainWindow"
                    print("CANCEL")
            elif self.state == "targetSelect":
                self.state = "mainWindow"
                if self.party.members[self.combatOrder[self.currentTurn][1]].status == "Paralyzed":
                    self.actionVal = -2
                if self.party.members[self.combatOrder[self.currentTurn][1]].status == "Freezing" and random.randint(0,2)==0:
                    self.actionVal = -3
                self.actions.append(Action(self.combatOrder[self.currentTurn],self.cursorPos,self.actionVal))
                self.next()
                self.cursorPos = -1
                print("TARGET")
            elif self.state == "spellList":
                if self.cursorPos+self.menuTop < len(self.party.members[self.combatOrder[self.currentTurn][1]].spells):
                    self.spellID = self.menuTop + self.cursorPos
                    self.state = "spellSummary"
                    print("SPELLSUMMARY")
            elif self.state == "itemList":
                if self.cursorPos+self.menuTop < len(self.party.inventory):
                    self.itemID = self.menuTop + self.cursorPos
                    self.state = "itemSummary"
                    print("ITEMSUMMARY")
            elif self.state =="spellSummary":
                if self.validManaCost(self.party.members[self.combatOrder[self.currentTurn][1]],self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]):
                    self.lowMana = False
                    self.actionVal = self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]
                    if self.game.directory.getSpellTarget(self.actionVal) == "Single":
                        self.state = "targetSelect"
                        self.cursorPos = 0
                    else:
                        self.state = "mainWindow"
                        if self.party.members[self.combatOrder[self.currentTurn][1]].status == "Paralyzed" or (self.party.members[self.combatOrder[self.currentTurn][1]].status == "Freezing" and random.randint(0,2)==0):
                            self.actionVal = -1
                        self.actions.append(Action(self.combatOrder[self.currentTurn],0,self.actionVal))
                        self.next()
                        self.cursorPos = -1
                    print("SPELL")
                else:
                    self.lowMana = True
            elif self.state =="itemSummary":
                self.actionVal = self.party.inventory[self.itemID]
                self.party.inventory.pop(self.itemID)
                self.state = "targetSelect"
                self.cursorPos = 0
                print("ITEM")
        if self.game.B:
            if self.state == "mainWindow":
                self.state = "useMenu"
                self.cursorPos = 0
                print("USE")
            elif self.state == "useMenu":
                self.state = "mainWindow"
                self.cursorPos = -1
                print("CANCEL")
            elif self.state == "targetSelect":
                self.state = "mainWindow"
                print("BACK")
            elif self.state == "spellList":
                self.state = "useMenu"
                print("BACK")
            elif self.state == "itemList":
                self.state = "useMenu"
                print("BACK")
            elif self.state == "spellSummary":
                self.state = "spellList"
                print("BACK")
            elif self.state == "itemSummary":
                self.state = "itemList"
                print("BACK")
        if self.game.X:
            if self.state == "mainWindow":
                self.state = "mainWindow"
                print("CANCEL")
                self.inCombat = False
        if self.game.Y:
            if self.state == "mainWindow":
                self.state = "mainWindow"
                print("RUN")
        if self.game.UP:
            if self.state == "targetSelect" and self.cursorPos > 0:
                self.cursorPos -= 1
            elif self.state == "useMenu":
                if self.cursorPos == 2 or self.cursorPos == 3:
                    self.cursorPos -= 2
            elif self.state == "spellList" or self.state == "itemList":
                if self.cursorPos == 0 or self.cursorPos == 1:
                    if self.menuTop > 0:
                        self.menuTop -= 2
                else:
                    self.cursorPos -= 2
        if self.game.DOWN:
            if self.state == "targetSelect":
                if (self.actionVal < 200 and self.cursorPos < len(self.encounter)-1) or (self.actionVal >= 200 and self.cursorPos < len(self.party.members)-1):
                    self.cursorPos += 1
            elif self.state == "useMenu":
                if self.cursorPos == 0 or self.cursorPos == 1:
                    self.cursorPos += 2
            elif self.state == "spellList":
                if self.cursorPos == 2 or self.cursorPos == 3:
                    if self.menuTop+4 < len(self.party.members[self.combatOrder[self.currentTurn][1]].spells):
                        self.menuTop += 2
                else:
                    self.cursorPos += 2
            elif self.state == "itemList":
                if self.cursorPos == 2 or self.cursorPos == 3:
                    if self.menuTop+4 < len(self.party.inventory):
                        self.menuTop += 2
                else:
                    self.cursorPos += 2
        if self.game.LEFT:
            if self.state == "spellList" or self.state == "itemList":
                if self.cursorPos == 1 or self.cursorPos == 3:
                    self.cursorPos -= 1
            elif self.state == "useMenu":
                if self.cursorPos > 0:
                    self.cursorPos -= 1
        if self.game.RIGHT:
            if self.state == "spellList" or self.state == "itemList":
                if self.cursorPos == 0 or self.cursorPos == 2:
                    self.cursorPos += 1
            elif self.state == "useMenu":
                if self.cursorPos < 3:
                    self.cursorPos += 1

    def drawScreen(self):
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
        self.combatInfo()
        if self.state == "mainWindow":
            self.write(20, self.left+15, 325, self.party.members[self.combatOrder[self.currentTurn][1]].name+"'s turn!")
            self.write(20,45,375,"A) ATTACK")
            self.write(20,210,375,"B) USE") #SPELL, ITEM, COMBAT ART
            self.write(20,45,420,"X) CANCEL")
            self.write(20,210,420,"Y) RUN")
            self.statBlock()
        if self.state == "useMenu":
            self.write(20, self.left+15, 325, "Use what?")
            self.write(20, 28+(int(self.cursorPos%2)*165), 373+(int(self.cursorPos/2)*45), ">")
            self.write(20,45,375,"SPELL")
            self.write(13,45,395,str(self.party.members[self.combatOrder[self.currentTurn][1]].mp)+"/"+str(self.party.members[self.combatOrder[self.currentTurn][1]].mpMax))
            self.write(20,210,375,"ITEM")
            self.write(20,45,420,"ART")
            self.write(20,210,420,"CANCEL")
            self.statBlock()
        if self.state == "targetSelect":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            self.write(20, self.left+15, 325, "Select a target")
            if self.actionVal < 200 or (self.actionVal >= 300 and self.actionVal < 400):
                self.write(20, 480, 30+(self.cursorPos*30), "<")
                self.write(20,30,400,"A) SELECT")
                self.write(20,180,400,"B) BACK")
            else:
                self.write(20, 230, 172+(self.cursorPos*30), ">")
                self.write(20,30,400,"A) SELECT")
                self.write(20,180,400,"B) BACK")
        if self.state == "spellList":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            if self.lowMana:
                self.write(18, self.left+15, 325, "You don't have enough mana to cast that.")
            else:
                self.write(18, self.left+15, 325, "Select a spell: (B to cancel)")
            self.write(20, 40+((self.cursorPos%2)*300), 380+((int(self.cursorPos/2))*40), ">")
            if self.menuTop < len(self.party.members[self.combatOrder[self.currentTurn][1]].spells):
                self.write(18,60,380,str(self.menuTop+1)+") "+self.game.directory.getItemName(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.menuTop]))
            else:
                self.write(18,60,380,str(self.menuTop+1)+")")
            if self.menuTop+1 < len(self.party.members[self.combatOrder[self.currentTurn][1]].spells):
                self.write(18,360,380,str(self.menuTop+2)+") "+self.game.directory.getItemName(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.menuTop+1]))
            else:
                self.write(18,360,380,str(self.menuTop+2)+")")
            if self.menuTop+2 < len(self.party.members[self.combatOrder[self.currentTurn][1]].spells):
                self.write(18,60,420,str(self.menuTop+3)+") "+self.game.directory.getItemName(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.menuTop+2]))
            else:
                self.write(18,60,420,str(self.menuTop+3)+")")
            if self.menuTop+3 < len(self.party.members[self.combatOrder[self.currentTurn][1]].spells):
                self.write(18,360,420,str(self.menuTop+4)+") "+self.game.directory.getItemName(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.menuTop+3]))
            else:
                self.write(18,360,420,str(self.menuTop+4)+")")
        if self.state == "itemList":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            self.write(20, self.left+15, 325, "Select an item: (B to cancel)")
            self.write(20, 40+((self.cursorPos%2)*300), 380+((int(self.cursorPos/2))*40), ">")
            if self.menuTop < len(self.party.inventory):
                self.write(18,60,380,str(self.menuTop+1)+") "+self.game.directory.getItemName(self.party.inventory[self.menuTop]))
            else:
                self.write(18,60,380,str(self.menuTop+1)+")")
            if self.menuTop+1 < len(self.party.inventory):
                self.write(18,360,380,str(self.menuTop+2)+") "+self.game.directory.getItemName(self.party.inventory[self.menuTop+1]))
            else:
                self.write(18,360,380,str(self.menuTop+2)+")")
            if self.menuTop+2 < len(self.party.inventory):
                self.write(18,60,420,str(self.menuTop+3)+") "+self.game.directory.getItemName(self.party.inventory[self.menuTop+2]))
            else:
                self.write(18,60,420,str(self.menuTop+3)+")")
            if self.menuTop+3 < len(self.party.inventory):
                self.write(18,360,420,str(self.menuTop+4)+") "+self.game.directory.getItemName(self.party.inventory[self.menuTop+3]))
            else:
                self.write(18,360,420,str(self.menuTop+4)+")")
        if self.state == "spellSummary":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            self.write(20, self.left+15, 325, "Do you want to cast this spell?")
            self.write(16, self.left+15, 360, self.game.directory.getItemName(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID])+": Costs "+str(self.game.directory.getManaCost(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]))+" MP")
            if self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID] < 400:
                self.writeOrientation(16,self.right-10, 360, str(self.game.directory.getAtkSpell(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).attack)+" Damage","R")
            else:
                if self.game.directory.getSptSpell(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).type == "Heal":
                    self.writeOrientation(16,self.right-10, 360, "Restores "+str(self.game.directory.getSptSpell(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).getHeal())+" HP","R")
                if self.game.directory.getSptSpell(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).type == "Buff":
                    i = 0
                    for id, buff in enumerate(self.game.directory.getSptSpell(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).potency):
                        if buff > 0:
                            self.writeOrientation(16,self.right-10, 360+(i*20), self.lookupBuffName(id)+" "+str(buff),"R")
                            i += 1
            self.write(16, self.left+15, 380, self.game.directory.getItemDesc(self.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]))
            self.write(20,150,425,"A) CONFIRM")
            self.write(20,385,425,"B) BACK")
        if self.state == "itemSummary":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            self.write(20, self.left+15, 325, "Do you want to use this item?")
            self.write(16, self.left+15, 360, self.game.directory.getItemName(self.party.inventory[self.itemID]))
            if self.game.directory.getPotion(self.party.inventory[self.itemID]).hpGain > 0 and self.game.directory.getPotion(self.party.inventory[self.itemID]).mpGain > 0:
                self.writeOrientation(16,self.right-10, 360, "Restores "+str(self.game.directory.getPotion(self.party.inventory[self.itemID]).hpGain)+" HP and "+str(self.game.directory.getPotion(self.party.inventory[self.itemID]).mpGain)+" MP","R")
            elif self.game.directory.getPotion(self.party.inventory[self.itemID]).hpGain > 0 and self.game.directory.getPotion(self.party.inventory[self.itemID]).mpGain == 0:
                self.writeOrientation(16,self.right-10, 360, "Restores "+str(self.game.directory.getPotion(self.party.inventory[self.itemID]).hpGain)+" HP","R")
            elif self.game.directory.getPotion(self.party.inventory[self.itemID]).hpGain == 0 and self.game.directory.getPotion(self.party.inventory[self.itemID]).mpGain > 0:
                self.writeOrientation(16,self.right-10, 360, "Restores "+str(self.game.directory.getPotion(self.party.inventory[self.itemID]).mpGain)+" MP","R")
            self.write(16, self.left+15, 380, self.game.directory.getItemDesc(self.party.inventory[self.itemID]))
            self.write(20,150,425,"A) CONFIRM")
            self.write(20,385,425,"B) BACK")

        #if self.state == "itemList":

        #if self.state == "combatArtList":

        if self.state == "execute":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            combatStr = ""
            if self.actions[self.exTurn-1].action == 0:
                if self.actions[self.exTurn-1].source[0] == "Encounter":
                    combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " attacks " + self.party.members[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
                else:
                    combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " attacks " + self.encounter[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
            elif self.actions[self.exTurn-1].action == -2:
                combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " is paralyzed, and cannot move!"
            elif self.actions[self.exTurn-1].action == -3:
                combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " is freezing, and cannot move!"
            elif self.actions[self.exTurn-1].action >= 200 and self.actions[self.exTurn-1].action < 300:
                combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " used " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.party.members[self.actions[self.exTurn-1].target].name + "!"
            elif self.actions[self.exTurn-1].action >= 300 and self.actions[self.exTurn-1].action < 400:
                if self.actions[self.exTurn-1].source[0] == "Encounter":
                    if self.game.directory.getAtkSpell(self.actions[self.exTurn-1].action).target == "Single":
                        combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " at " + self.party.members[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
                    else:
                        combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " for " + str(self.dmg) + " damage!"
                else:
                    if self.game.directory.getAtkSpell(self.actions[self.exTurn-1].action).target == "Single":
                        combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " at " + self.encounter[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
                    else:
                        combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " for " + str(self.dmg) + " damage!"
            elif self.actions[self.exTurn-1].action >= 400 and self.actions[self.exTurn-1].action < 500:
                if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).type == "Buff":
                    if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).target == "Single":
                        combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.party.members[self.actions[self.exTurn-1].target].name + "!"
                    else:
                        combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + "!"
                elif self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).type == "Heal":
                    if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).target == "Single":
                        combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.party.members[self.actions[self.exTurn-1].target].name + ", restoring " + str(self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).getHeal()) + " HP!"
                    else:
                        combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + ", restoring " + str(self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).getHeal()) + " HP!"
                elif self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).type == "Raise":
                    if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).target == "Single":
                        combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.party.members[self.actions[self.exTurn-1].target].name + ", bringing them back to life!"
                    else:
                        combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + ", raising all fallen party members!"
                elif self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).type == "Cleanse":
                    if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).target == "Single":
                        combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.party.members[self.actions[self.exTurn-1].target].name + ", removing status effects!"
                    else:
                        combatStr = self.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + ", removing all status effects!"
            self.write(20, self.left+15, 325, combatStr)

        if self.state == "win":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            self.write(20, self.left+15, 325, "You win!")
            if pygame.time.get_ticks() - self.timeStart >= 3000:
                difficulty = 0
                for monster in self.encounter:
                    difficulty += monster.level
                for member in self.party.members:
                    member.gainXP((difficulty * 3) + (round(difficulty/2) * random.randint(2,4)))
                self.inCombat = False

        if self.state == "lose":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            self.write(20, self.left+15, 325, "You have fallen...")
            if pygame.time.get_ticks() - self.timeStart >= 3000:
                self.inCombat = False
                pygame.quit()

    def write(self,size,x,y,text):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text, True, self.game.white)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.game.screen.blit(text_surface,text_rect)
        return font.size(text)

    def writeOrientation(self,size,x,y,text,orn):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text, True, self.game.white)
        text_rect = text_surface.get_rect()
        if orn == "L":
            text_rect.topleft = (x,y)
        elif orn == "R":
            text_rect.topright = (x,y)
        self.game.screen.blit(text_surface,text_rect)
        return font.size(text)

    def combatInfo(self):
        self.game.screen.fill(self.game.black)
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
        #Setting name widths
        maxEncWidth = 0
        maxPtyWidth = 0
        for i in range(0,len(self.encounter)):
            textWidth, textHeight = self.font.size(self.encounter[i].name)
            if textWidth > maxEncWidth:
                maxEncWidth = textWidth
        for i in range(0,len(self.party.members)):
            textWidth, textHeight = self.font.size(self.party.members[i].name)
            if textWidth > maxPtyWidth:
                maxPtyWidth = textWidth
        #Writing names and health bars
        for i in range(0,len(self.encounter)):
            offset = 30*i
            textWidth, textHeight = self.write(20, 30, 30+offset, self.encounter[i].name)
            enemyRect = pygame.Rect(50+maxEncWidth,30+offset,(self.encounter[i].hp/self.encounter[i].hpMax)*100,20)
            outlineRect = pygame.Rect(50+maxEncWidth,30+offset,100,20)
            pygame.draw.rect(self.game.screen,self.game.white,enemyRect)
            pygame.draw.rect(self.game.screen,self.game.white,outlineRect,1)
            self.write(20, 180+maxEncWidth, 30+offset, str(self.encounter[i].hp)+"/"+str(self.encounter[i].hpMax))
            if self.encounter[i].status != "None":
                if self.encounter[i].status == "Paralyzed":
                    self.write(20, 280+maxEncWidth, 30+offset, "<P"+str(self.encounter[i].statusCount)+">")
                elif self.encounter[i].status == "Burned":
                    self.write(20, 280+maxEncWidth, 30+offset, "<B>")
                elif self.encounter[i].status == "Freezing":
                    self.write(20, 280+maxEncWidth, 30+offset, "<F>")
        for i in range(0,len(self.party.members)):
            offset = 30*i
            textWidth, textHeight = self.font.size(self.party.members[i].name)
            self.write(20, self.right-textWidth-20, 170+offset, self.party.members[i].name)
            partyHPRect = pygame.Rect(self.right-maxPtyWidth-140,170+offset,(self.party.members[i].hp/self.party.members[i].hpMax)*100,10)
            partyMPRect = pygame.Rect(self.right-maxPtyWidth-140,180+offset,(self.party.members[i].mp/self.party.members[i].mpMax)*100,10)
            outlineRect = pygame.Rect(self.right-maxPtyWidth-140,170+offset,100,20)
            pygame.draw.rect(self.game.screen,self.game.white,partyHPRect)
            pygame.draw.rect(self.game.screen,self.game.white,partyMPRect)
            pygame.draw.rect(self.game.screen,self.game.white,outlineRect,1)
            self.write(20, self.right-maxPtyWidth-220, 170+offset, str(self.party.members[i].hp)+"/"+str(self.party.members[i].hpMax))
            if self.party.members[i].status != "None":
                if self.party.members[i].status == "Paralyzed":
                    self.write(20, self.right-maxPtyWidth-290, 170+offset, "<P>")
                elif self.party.members[i].status == "Burned":
                    self.write(20, self.right-maxPtyWidth-290, 170+offset, "<B>")
                elif self.party.members[i].status == "Freezing":
                    self.write(20, self.right-maxPtyWidth-290, 170+offset, "<F>")
        #Setting border
        pygame.draw.line(self.game.screen,self.game.white,(self.left,320),(self.right+9,320),2)

    def statBlock(self):
        pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(350,350),2)
        pygame.draw.line(self.game.screen,self.game.white,(350,320),(350,self.bottom+7),2)
        self.write(11, 360, 328, self.party.members[self.combatOrder[self.currentTurn][1]].name+", Level "+str(self.party.members[self.combatOrder[self.currentTurn][1]].level)+" "+self.party.members[self.combatOrder[self.currentTurn][1]].type.name)
        self.write(11, 360, 345, "HP "+str(self.party.members[self.combatOrder[self.currentTurn][1]].hp)+"/"+str(self.party.members[self.combatOrder[self.currentTurn][1]].hpMax))
        self.write(11, 420, 345, "MP "+str(self.party.members[self.combatOrder[self.currentTurn][1]].mp)+"/"+str(self.party.members[self.combatOrder[self.currentTurn][1]].mpMax))
        self.write(11, 360, 360, "ATK "+str(self.party.members[self.combatOrder[self.currentTurn][1]].getAttack()))
        self.write(11, 420, 360, "DEF "+str(self.party.members[self.combatOrder[self.currentTurn][1]].getDefense()))
        self.write(11, 360, 375, "ACC "+str(self.party.members[self.combatOrder[self.currentTurn][1]].getAccuracy()))
        self.write(11, 420, 375, "DDG "+str(self.party.members[self.combatOrder[self.currentTurn][1]].getDodge()))
        self.write(11, 360, 390, "CRT "+str(self.party.members[self.combatOrder[self.currentTurn][1]].getCritRate()))
        self.write(11, 420, 390, "LCK "+str(self.party.members[self.combatOrder[self.currentTurn][1]].getLuck()))
        self.write(11, 360, 405, "AMP "+str(self.party.members[self.combatOrder[self.currentTurn][1]].getAmplifier()))
        self.write(11, 420, 405, "MPG "+str(self.party.members[self.combatOrder[self.currentTurn][1]].getManaRegen()))
        self.write(16, 360, 430, "\""+self.combatDialogue+"\"")
        iNext = 0
        for i in range(len(self.party.members[self.combatOrder[self.currentTurn][1]].activeBuffs)):
            self.writeOrientation(11, self.right, 330+(i*15), self.party.members[self.combatOrder[self.currentTurn][1]].activeBuffs[i][0]+" ("+str(self.party.members[self.combatOrder[self.currentTurn][1]].activeBuffs[i][1])+")","R")
            iNext += 1
        if self.party.members[self.combatOrder[self.currentTurn][1]].status != "None":
            self.writeOrientation(11, self.right, 330+(iNext*15), self.party.members[self.combatOrder[self.currentTurn][1]].status+" ("+str(self.party.members[self.combatOrder[self.currentTurn][1]].statusCount)+")","R")

    def next(self):
        self.currentTurn += 1
        if self.currentTurn >= len(self.combatOrder):
            self.startExecute()
        else:
            self.skip()
            self.gameStatus()
            if self.state == "lose" or self.state == "win":
                return
            if self.currentTurn >= len(self.combatOrder):
                self.startExecute()
            #print(self.party.members[self.combatOrder[self.currentTurn][1]].name)
        if self.combatOrder[self.currentTurn][0] == "Party":
            self.combatDialogue = getCombatDialogue(self.party.members[self.combatOrder[self.currentTurn][1]])

    def enemyAction(self,source):
        if not self.isAlive(source):
            self.actions.append(Action(source,0,-1))
            return
        elif self.encounter[self.combatOrder[self.currentTurn][1]].status == "Paralyzed":
            self.actions.append(Action(source,0,-2))
            return
        elif self.encounter[self.combatOrder[self.currentTurn][1]].status == "Freezing" and random.randint(0,2)==0:
            self.actions.append(Action(source,0,-3))
            return
        target = random.randint(0,len(self.party.members)-1)
        timeout = 0
        while self.party.members[target].hp <= 0 and timeout < 20:
            target = random.randint(0,len(self.party.members)-1)
            timeout += 1
        move = random.randint(0,len(self.encounter[self.combatOrder[self.currentTurn][1]].knownSpells))
        if move == 0 or self.encounter[self.combatOrder[self.currentTurn][1]].spellCooldown > 0:
            act = Action(source, target, 0)
            if self.encounter[self.combatOrder[self.currentTurn][1]].spellCooldown > 0:
                self.encounter[self.combatOrder[self.currentTurn][1]].spellCooldown -= 1
        else:
            self.encounter[self.combatOrder[self.currentTurn][1]].spellCooldown = 2
            act = Action(source, target, self.encounter[self.combatOrder[self.currentTurn][1]].knownSpells[move-1])
        self.actions.append(act)

    def attack(self,source,target):
        if source[0] == "Encounter":
            if self.encounter[source[1]].attack - self.party.members[target].getDefense() < 0:
                self.dmg = 0
            else:
                self.dmg = self.encounter[source[1]].attack - self.party.members[target].getDefense()
            self.party.members[target].takeDamage(self.dmg)
        if source[0] == "Party":
            if self.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                self.dmg = 0
            else:
                self.dmg = self.party.members[source[1]].getAttack() - self.encounter[target].defense
            self.encounter[target].takeDamage(self.dmg)

    def usePotion(self,target,itemID):
        self.party.usePotion(target,itemID,self.game.directory)

    def cast(self,source,target,spellID):
        if spellID < 400:
            spell = self.game.directory.getAtkSpell(spellID)
            if spell.target == "Single":
                if source[0] == "Encounter":
                    if spell.type == "Attack":
                        print("Attack!")
                        self.dmg = self.party.members[target].takeDamage(spell.attack)
                    elif spell.type == "Debuff":
                        print("Debuff!")
                        if (spell.id > 326) or random.randint(0,1) == 1: # 50% Chance for 324, 325, 326
                            if spell.element == "Lightning":
                                self.party.members[target].status = "Paralyzed"
                                self.party.members[target].statusCount = 3
                            elif spell.element == "Fire":
                                self.party.members[target].status = "Burned"
                                self.party.members[target].statusCount = -1
                            elif spell.element == "Ice":
                                self.party.members[target].status = "Freezing"
                                self.party.members[target].statusCount = -1
                else:
                    if spell.type == "Attack":
                        print("Attack!")
                        self.dmg = spell.attack
                        if spell.element == self.encounter[target].resistance:
                            self.dmg = int(self.dmg/2)
                        self.encounter[target].takeDamage(self.dmg)
                        self.party.members[source[1]].mp -= spell.manacost
                    elif spell.type == "Debuff":
                        print("Debuff!")
                        if spell.id > 326 or random.randint(0,1) == 1: # 50% Chance for 324, 325, 326
                            if spell.element == "Lightning":
                                self.encounter[target].status = "Paralyzed"
                                self.encounter[target].statusCount = 3
                            elif spell.element == "Fire":
                                self.encounter[target].status = "Burned"
                                self.encounter[target].statusCount = -1
                            elif spell.element == "Ice":
                                self.encounter[target].status = "Freezing"
                                self.encounter[target].statusCount = -1
                        self.party.members[source[1]].mp -= spell.manacost
            else:
                if source[0] == "Encounter":
                    if spell.type == "Attack":
                        for member in self.party.members:
                            self.dmg = member.takeDamage(spell.attack)
                    elif spell.type == "Debuff":
                        print("Debuff!")
                        for member in self.party.members:
                            if random.randint(0,1) == 1:
                                if spell.element == "Lightning":
                                    member.status = "Paralyzed"
                                    member.statusCount = 3
                                elif spell.element == "Fire":
                                    member.status = "Burned"
                                    member.statusCount = -1
                                elif spell.element == "Ice":
                                    member.status = "Freezing"
                                    member.statusCount = -1
                else:
                    if spell.type == "Attack":
                        for member in self.encounter:
                            self.dmg = spell.attack
                            if spell.element == member.resistance:
                                self.dmg = int(self.dmg/2)
                            member.takeDamage(self.dmg)
                        self.dmg = spell.attack
                        self.party.members[source[1]].mp -= spell.manacost
                    elif spell.type == "Debuff":
                        print("Debuff!")
                        for member in self.encounter:
                            if random.randint(0,1) == 1:
                                if spell.element == "Lightning":
                                    member.status = "Paralyzed"
                                    member.statusCount = 3
                                elif spell.element == "Fire":
                                    member.status = "Burned"
                                    member.statusCount = -1
                                elif spell.element == "Ice":
                                    member.status = "Freezing"
                                    member.statusCount = -1
                        self.party.members[source[1]].mp -= spell.manacost
        elif spellID < 500:
            spell = self.game.directory.getSptSpell(spellID)
            if spell.target == "Single":
                if spell.type == "Heal":
                    if self.party.members[target].hp > 0:
                        self.party.members[target].hp += spell.getHeal()
                    if self.party.members[target].hp > self.party.members[target].hpMax:
                        self.party.members[target].hp = self.party.members[target].hpMax
                elif spell.type == "Buff":
                    self.applyBuff(spell,target)
                elif spell.type == "Raise":
                    if self.party.members[target].hp <= 0:
                        self.party.members[target].hp += spell.getHeal()
                    if self.party.members[target].hp > self.party.members[target].hpMax:
                        self.party.members[target].hp = self.party.members[target].hpMax
                elif spell.type == "Cleanse":
                    if self.party.members[target].hp > 0:
                        self.party.members[target].resetStatus()
                self.party.members[source[1]].mp -= spell.manacost
            elif spell.target == "All":
                if spell.type == "Heal":
                    for member in self.party.members:
                        if member.hp > 0:
                            member.hp += spell.getHeal()
                        if member.hp > member.hpMax:
                            member.hp = member.hpMax
                elif spell.type == "Buff":
                    self.applyBuff(spell,-1)
                elif spell.type == "Raise":
                    for member in self.party.members:
                        if member.hp <= 0:
                            member.hp += spell.getHeal()
                        if member.hp > member.hpMax:
                            member.hp = member.hpMax
                elif spell.type == "Cleanse":
                    for member in self.party.members:
                        if member.hp > 0:
                            member.resetStatus()
                self.party.members[source[1]].mp -= spell.manacost

    def validManaCost(self,user,spell):
        return user.mp > self.game.directory.getManaCost(spell)

    def execute(self):
        if self.ex == False:
            return
        if pygame.time.get_ticks() - self.timeStart > 2000:
            if self.exTurn < len(self.combatOrder):
                while self.actions[self.exTurn].action == -1 or not self.isAlive(self.actions[self.exTurn].source):
                    if self.exTurn < len(self.combatOrder)-1:
                        self.exTurn += 1
                    else:
                        self.endExecute()
                        return
                print(f'Action: {self.actions[self.exTurn].source} -> {self.actions[self.exTurn].target}, {self.actions[self.exTurn].action} (exTurn {self.exTurn})')
                if self.actions[self.exTurn].action == 0:
                    self.attack(self.actions[self.exTurn].source,self.actions[self.exTurn].target)
                elif self.actions[self.exTurn].action >= 200 and self.actions[self.exTurn].action < 300:
                    self.usePotion(self.actions[self.exTurn].target,self.actions[self.exTurn].action)
                elif self.actions[self.exTurn].action >= 300 and self.actions[self.exTurn].action < 400:
                    self.cast(self.actions[self.exTurn].source,self.actions[self.exTurn].target,self.actions[self.exTurn].action)
                elif self.actions[self.exTurn].action >= 400 and self.actions[self.exTurn].action < 500:
                    self.cast(self.actions[self.exTurn].source,self.actions[self.exTurn].target,self.actions[self.exTurn].action)
                self.exTurn += 1
                self.timeStart = pygame.time.get_ticks()
            else:
                self.endExecute()

    def wait(self,waitVal):
        fullWaits = int(waitVal / 500)
        remWait = waitVal % 500
        for i in range(fullWaits):
            pygame.time.delay(500)
        pygame.time.delay(remWait)

    def isAlive(self,source):
        if source[0]=="Party":
            if self.party.members[source[1]].hp<=0:
                return False
        if source[0]=="Encounter":
            if self.encounter[source[1]].hp<=0:
                return False
        return True

    def startExecute(self):
        print("Execute!")
        self.ex = True
        self.exTurn = 0
        self.timeStart = pygame.time.get_ticks()-2001
        self.state = "execute"
        self.currentTurn = 0

    def endExecute(self):
        for i in range(len(self.combatOrder)):
            self.actions.pop(0)
        for i in range(len(self.combatOrder)-1,-1,-1):
            if self.isAlive(self.combatOrder[i]) == False:
                self.combatOrder.pop(i)
        for member in self.combatOrder:
            print(member)
        self.state = "mainWindow"
        self.ex = False
        self.currentTurn = -1
        self.processBuffs()
        self.upkeep()
        self.next()

    def upkeep(self):
        for member in self.party.members:
            member.mp += member.getManaRegen()
            if member.mp > member.mpMax:
                member.mp = member.mpMax
            member.tickStatus()
            if member.status == "Burned":
                member.takeDamage(5)
        for member in self.encounter:
            member.tickStatus()
            if member.status == "Burned":
                member.takeDamage(5)

    def skip(self):
        while self.combatOrder[self.currentTurn][0] == "Encounter" or not self.isAlive(self.combatOrder[self.currentTurn]):
            #print(self.encounter[self.combatOrder[self.currentTurn][1]].name)
            if self.combatOrder[self.currentTurn][0] == "Encounter":
                self.enemyAction(self.combatOrder[self.currentTurn])
            else:
                self.actions.append(Action(self.combatOrder[self.currentTurn],0,-1))
            self.currentTurn += 1
            if self.currentTurn >= len(self.combatOrder):
                return

    def gameStatus(self):
        if self.state == "lose" or self.state == "win":
            return
        encFlag = False
        ptyFlag = False
        for member in self.combatOrder:
            if member[0] == "Encounter":
                encFlag = True
            else:
                ptyFlag = True
        if ptyFlag == False:
            self.state = "lose"
            self.timeStart = pygame.time.get_ticks()
        if encFlag == False:
            self.state = "win"
            self.timeStart = pygame.time.get_ticks()

    def applyBuff(self,buff,target):
        newBuff = Buff(buff.name,buff.potency,5,target)
        print(newBuff.target)
        self.buffs.append(newBuff)
        if newBuff.target == -1:
            for member in self.party.members:
                member.addBuffs(newBuff)
        else:
            self.party.members[newBuff.target].addBuffs(newBuff)

    def processBuffs(self):
        for member in self.party.members:
            member.resetBuffs()
        for bf in self.buffs:
            if bf.target == -1:
                for member in self.party.members:
                    member.addBuffs(bf)
            else:
                self.party.members[bf.target].addBuffs(bf)
            print(f'{bf.name}, {bf.duration}')
            bf.tick()
        for i in range(len(self.buffs)-1,-1,-1):
            if self.buffs[i].checkExpiry():
                print(f'{bf.name} expired.')
                self.buffs.pop(i)
        for member in self.party.members:
            print(member.buffs)

    def lookupBuffName(self,i):
        if i == 0:
            return "ATK"
        elif i == 1:
            return "ACC"
        elif i == 2:
            return "CRT"
        elif i == 3:
            return "DEF"
        elif i == 4:
            return "DDG"
        elif i == 5:
            return "LCK"
        elif i == 6:
            return "HP"
