import pygame
import random
import time
from characters import Action
from characters import Buff
from dialogue import *
from writing import *

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
        self.miss = False
        self.crit = False
        self.waitFlag = False
        self.cursorPos = -1
        self.menuTop = -1
        self.itemID = -1
        self.spellID = -1
        self.lowMana = False
        self.buffs = []
        self.combatDialogue = ""

    def initialize(self,encounter):
        self.currentTurn = 0
        for i in range(0,len(self.game.player.party.members)):
            print(f'{self.game.player.party.members[i].name}, {self.game.player.party.members[i].type.name}, {self.game.player.party.members[i].level} (ID {self.game.player.party.members[i].id}) - WPN: {self.game.player.party.members[i].eqpWpn.name}, AMR: {self.game.player.party.members[i].eqpAmr.name}, HP: {self.game.player.party.members[i].hpMax}, MP: {self.game.player.party.members[i].mpMax}, ATK: {self.game.player.party.members[i].attack}, CRT: {self.game.player.party.members[i].critrate}, DEF: {self.game.player.party.members[i].defense}, DDG: {self.game.player.party.members[i].dodge}, LCK: {self.game.player.party.members[i].luck}, SPD: {self.game.player.party.members[i].speed}, PRS: {self.game.player.party.members[i].personality}, SPELLS: {self.game.player.party.members[i].spells}')
        self.encounter = encounter
        for i in range(0,len(self.encounter)):
            print(f'{self.encounter[i].name}, {self.encounter[i].level} - SPD: {self.encounter[i].speed}')

        self.combatOrder = []
        self.actions = []
        members = self.game.player.party.members + self.encounter
        members.sort(key=lambda x: x.speed)
        members.reverse()
        for i in range(len(members)-1,-1,-1):
            if members[i].hp <= 0:
                members.pop(i)
        seenPty = [0] * len(self.game.player.party.members)
        seenEnc = [0] * len(self.encounter)
        for entry in members:
            for i in range(len(self.game.player.party.members)):
                if entry.id == self.game.player.party.members[i].id:
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
            self.combatDialogue = getCombatDialogue(self.game.player.party.members[self.combatOrder[self.currentTurn][1]])
        self.inCombat = True
        self.state = "mainWindow"
        self.delay = 5

    def combatTeardown(self):
        for member in self.game.player.party.members:
            member.resetBuffs()

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
            self.gameStatus()
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
                self.enterTargetSelect()
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
                if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Paralyzed:
                    self.actionVal = -2
                if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Freezing and random.randint(0,2)==0:
                    self.actionVal = -3
                self.actions.append(Action(self.combatOrder[self.currentTurn],self.cursorPos,self.actionVal))
                print(f'Action writing for {self.combatOrder[self.currentTurn]}, length {len(self.actions)}')
                self.next()
                self.cursorPos = -1
                print("TARGET")
            elif self.state == "spellList":
                if self.cursorPos+self.menuTop < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells):
                    self.spellID = self.menuTop + self.cursorPos
                    self.state = "spellSummary"
                    print("SPELLSUMMARY")
            elif self.state == "itemList":
                if self.cursorPos+self.menuTop < len(self.game.player.party.inventory):
                    self.itemID = self.menuTop + self.cursorPos
                    self.state = "itemSummary"
                    print("ITEMSUMMARY")
            elif self.state =="spellSummary":
                if self.validManaCost(self.game.player.party.members[self.combatOrder[self.currentTurn][1]],self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]):
                    self.lowMana = False
                    self.actionVal = self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]
                    if self.game.directory.getSpellTarget(self.actionVal) == Target.Single:
                        self.state = "targetSelect"
                        self.cursorPos = 0
                        self.enterTargetSelect()
                    else:
                        self.state = "mainWindow"
                        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Paralyzed or (self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Freezing and random.randint(0,2)==0):
                            self.actionVal = -1
                        self.actions.append(Action(self.combatOrder[self.currentTurn],0,self.actionVal))
                        print(f'Action writing for {self.combatOrder[self.currentTurn]}, length {len(self.actions)}')
                        self.next()
                        self.cursorPos = -1
                    print("SPELL")
                else:
                    self.lowMana = True
            elif self.state =="itemSummary":
                self.actionVal = self.game.player.party.inventory[self.itemID].id
                self.state = "targetSelect"
                self.cursorPos = 0
                self.enterTargetSelect()
                print("ITEM")
            elif self.state == "execute":
                self.timeStart -= 2000
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
                self.prev()
        if self.game.Y:
            if self.state == "mainWindow":
                self.state = "mainWindow"
                print("RUN")
                self.inCombat = False
        if self.game.UP:
            if self.state == "targetSelect" and self.cursorPos > 0:
                tgtList = self.encounter if self.actionVal < 200 else self.game.player.party.members
                for i in range(0,self.cursorPos):
                    if tgtList[i].hp > 0:
                        self.cursorPos = i
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
                tgtList = self.encounter if self.actionVal < 200 else self.game.player.party.members
                for i in range(self.cursorPos+1,len(tgtList)):
                    if tgtList[i].hp > 0:
                        self.cursorPos = i
                        break
            elif self.state == "useMenu":
                if self.cursorPos == 0 or self.cursorPos == 1:
                    self.cursorPos += 2
            elif self.state == "spellList":
                if self.cursorPos == 2 or self.cursorPos == 3:
                    if self.menuTop+4 < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells):
                        self.menuTop += 2
                else:
                    self.cursorPos += 2
            elif self.state == "itemList":
                if self.cursorPos == 2 or self.cursorPos == 3:
                    if self.menuTop+4 < len(self.game.player.party.inventory):
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

    def enterTargetSelect(self):
        self.cursorPos = 0
        tgtList = self.encounter if self.actionVal < 200 else self.game.player.party.members
        for i in range(0,len(tgtList)):
            if tgtList[i].hp > 0:
                self.cursorPos = i
                break

    def drawScreen(self):
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)
        self.combatInfo()
        if self.state == "mainWindow":
            write(self.game, 20, self.left+15, 325, self.game.player.party.members[self.combatOrder[self.currentTurn][1]].name+"'s turn!")
            write(self.game, 20,45,375,"A) ATTACK")
            write(self.game, 20,210,375,"B) USE") #SPELL, ITEM, COMBAT ART
            write(self.game, 20,45,420,"X) CANCEL")
            write(self.game, 20,210,420,"Y) RUN")
            self.statBlock()
        if self.state == "useMenu":
            write(self.game, 20, self.left+15, 325, "Use what?")
            write(self.game, 20, 28+(int(self.cursorPos%2)*165), 373+(int(self.cursorPos/2)*45), ">")
            write(self.game, 20,45,375,"SPELL")
            write(self.game, 13,45,395,str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].mp)+"/"+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].mpMax))
            write(self.game, 20,210,375,"ITEM")
            write(self.game, 20,45,420,"ART")
            write(self.game, 20,210,420,"CANCEL")
            self.statBlock()
        if self.state == "targetSelect":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "Select a target")
            if self.actionVal < 200 or (self.actionVal >= 300 and self.actionVal < 400):
                write(self.game, 20, 480, 30+(self.cursorPos*30), "<")
                write(self.game, 20,30,400,"A) SELECT")
                write(self.game, 20,180,400,"B) BACK")
            else:
                write(self.game, 20, 230, 172+(self.cursorPos*30), ">")
                write(self.game, 20,30,400,"A) SELECT")
                write(self.game, 20,180,400,"B) BACK")
        if self.state == "spellList":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            if self.lowMana:
                write(self.game, 18, self.left+15, 325, "You don't have enough mana to cast that.")
            else:
                write(self.game, 18, self.left+15, 325, "Select a spell: (B to cancel)")
            write(self.game, 20, 40+((self.cursorPos%2)*300), 380+((int(self.cursorPos/2))*40), ">")
            if self.menuTop < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells):
                write(self.game, 18,60,380,str(self.menuTop+1)+") "+self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.menuTop]))
            else:
                write(self.game, 18,60,380,str(self.menuTop+1)+")")
            if self.menuTop+1 < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells):
                write(self.game, 18,360,380,str(self.menuTop+2)+") "+self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.menuTop+1]))
            else:
                write(self.game, 18,360,380,str(self.menuTop+2)+")")
            if self.menuTop+2 < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells):
                write(self.game, 18,60,420,str(self.menuTop+3)+") "+self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.menuTop+2]))
            else:
                write(self.game, 18,60,420,str(self.menuTop+3)+")")
            if self.menuTop+3 < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells):
                write(self.game, 18,360,420,str(self.menuTop+4)+") "+self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.menuTop+3]))
            else:
                write(self.game, 18,360,420,str(self.menuTop+4)+")")
        if self.state == "itemList":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "Select an item: (B to cancel)")
            write(self.game, 20, 40+((self.cursorPos%2)*300), 380+((int(self.cursorPos/2))*40), ">")
            if self.menuTop < len(self.game.player.party.inventory):
                write(self.game, 18,60,380,str(self.menuTop+1)+") "+self.game.directory.getItemName(self.game.player.party.inventory[self.menuTop]))
            else:
                write(self.game, 18,60,380,str(self.menuTop+1)+")")
            if self.menuTop+1 < len(self.game.player.party.inventory):
                write(self.game, 18,360,380,str(self.menuTop+2)+") "+self.game.directory.getItemName(self.game.player.party.inventory[self.menuTop+1]))
            else:
                write(self.game, 18,360,380,str(self.menuTop+2)+")")
            if self.menuTop+2 < len(self.game.player.party.inventory):
                write(self.game, 18,60,420,str(self.menuTop+3)+") "+self.game.directory.getItemName(self.game.player.party.inventory[self.menuTop+2]))
            else:
                write(self.game, 18,60,420,str(self.menuTop+3)+")")
            if self.menuTop+3 < len(self.game.player.party.inventory):
                write(self.game, 18,360,420,str(self.menuTop+4)+") "+self.game.directory.getItemName(self.game.player.party.inventory[self.menuTop+3]))
            else:
                write(self.game, 18,360,420,str(self.menuTop+4)+")")
        if self.state == "spellSummary":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "Do you want to cast this spell?")
            write(self.game, 16, self.left+15, 360, self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID])+": Costs "+str(self.game.directory.getManaCost(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]))+" MP")
            if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID] < 400:
                writeOrientation(self.game, 16,self.right-10, 360, str(self.game.directory.getAtkSpell(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).attack)+" Damage","R")
            else:
                if self.game.directory.getSptSpell(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).type == SpellType.Heal:
                    writeOrientation(self.game, 16,self.right-10, 360, "Restores "+str(self.game.directory.getSptSpell(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).getHeal())+" HP","R")
                if self.game.directory.getSptSpell(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).type == SpellType.Buff:
                    i = 0
                    for id, buff in enumerate(self.game.directory.getSptSpell(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).potency):
                        if buff > 0:
                            writeOrientation(self.game, 16,self.right-10, 360+(i*20), self.lookupBuffName(id)+" "+str(buff),"R")
                            i += 1
            write(self.game, 16, self.left+15, 380, self.game.directory.getItemDesc(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]))
            write(self.game, 20,150,425,"A) CONFIRM")
            write(self.game, 20,385,425,"B) BACK")
        if self.state == "itemSummary":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "Do you want to use this item?")
            write(self.game, 16, self.left+15, 360, self.game.directory.getItemName(self.game.player.party.inventory[self.itemID]))
            if self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).hpGain > 0 and self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).mpGain > 0:
                writeOrientation(self.game, 16,self.right-10, 360, "Restores "+str(self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).hpGain)+" HP and "+str(self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).mpGain)+" MP","R")
            elif self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).hpGain > 0 and self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).mpGain == 0:
                writeOrientation(self.game, 16,self.right-10, 360, "Restores "+str(self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).hpGain)+" HP","R")
            elif self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).hpGain == 0 and self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).mpGain > 0:
                writeOrientation(self.game, 16,self.right-10, 360, "Restores "+str(self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).mpGain)+" MP","R")
            write(self.game, 16, self.left+15, 380, self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).description)
            write(self.game, 20,150,425,"A) CONFIRM")
            write(self.game, 20,385,425,"B) BACK")

        #if self.state == "itemList":

        #if self.state == "combatArtList":

        if self.state == "execute":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            combatStr = ""
            if self.actions[self.exTurn-1].action == 0:
                if self.actions[self.exTurn-1].source[0] == "Encounter":
                    if self.miss:
                        combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " attacks " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + ", but misses!"
                    else:
                        combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " attacks " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
                else:
                    if self.miss:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " attacks " + self.encounter[self.actions[self.exTurn-1].target].name + ", but misses!"
                    elif not self.crit:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " attacks " + self.encounter[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
                    elif self.crit:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " attacks " + self.encounter[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage! Critical hit!"
            elif self.actions[self.exTurn-1].action == -2:
                if self.actions[self.exTurn-1].source[0] == "Encounter":
                    combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " is paralyzed, and cannot move!"
                else:
                    combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " is paralyzed, and cannot move!"
            elif self.actions[self.exTurn-1].action == -3:
                if self.actions[self.exTurn-1].source[0] == "Encounter":
                    combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " is freezing, and cannot move!"
                else:
                    combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " is freezing, and cannot move!"
            elif self.actions[self.exTurn-1].action >= 200 and self.actions[self.exTurn-1].action < 300:
                combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " used " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + "!"
            elif self.actions[self.exTurn-1].action >= 300 and self.actions[self.exTurn-1].action < 400:
                if self.actions[self.exTurn-1].source[0] == "Encounter":
                    if self.game.directory.getAtkSpell(self.actions[self.exTurn-1].action).target == Target.Single:
                        combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " at " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
                    else:
                        combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " for " + str(self.dmg) + " damage!"
                else:
                    if self.game.directory.getAtkSpell(self.actions[self.exTurn-1].action).target == Target.Single:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " at " + self.encounter[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
                    else:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " for " + str(self.dmg) + " damage!"
            elif self.actions[self.exTurn-1].action >= 400 and self.actions[self.exTurn-1].action < 500:
                if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).type == SpellType.Buff:
                    if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).target == Target.Single:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + "!"
                    else:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + "!"
                elif self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).type == SpellType.Heal:
                    if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).target == Target.Single:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + ", restoring " + str(self.game.player.party.members[self.actions[self.exTurn-1].source[1]].amplify(self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).getHeal())) + " HP!"
                    else:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + ", restoring " + str(self.game.player.party.members[self.actions[self.exTurn-1].source[1]].amplify(self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).getHeal())) + " HP!"
                elif self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).type == SpellType.Raise:
                    if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).target == Target.Single:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + ", bringing them back to life!"
                    else:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + ", raising all fallen party members!"
                elif self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).type == SpellType.Cleanse:
                    if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).target == Target.Single:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + ", removing status effects!"
                    else:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + ", removing all status effects!"
            write(self.game, 20, self.left+15, 325, combatStr)

        if self.state == "win":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "You win!")
            if pygame.time.get_ticks() - self.timeStart >= 3000:
                difficulty = 0
                for monster in self.encounter:
                    difficulty += monster.level
                for member in self.game.player.party.members:
                    if member.hp > 0:
                        member.gainXP((difficulty * 3) + (round(difficulty/2) * random.randint(2,4)))
                self.combatTeardown()
                self.inCombat = False

        if self.state == "lose":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "You have fallen...")
            print(f'Lose: {pygame.time.get_ticks() - self.timeStart} > 3000 to get out')
            if pygame.time.get_ticks() - self.timeStart >= 2000:
                print("We out")
                self.combatTeardown()
                self.inCombat = False
                pygame.quit()

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
        for i in range(0,len(self.game.player.party.members)):
            textWidth, textHeight = self.font.size(self.game.player.party.members[i].name)
            if textWidth > maxPtyWidth:
                maxPtyWidth = textWidth
        #Writing names and health bars
        for i in range(0,len(self.encounter)):
            offset = 30*i
            textWidth, textHeight = write(self.game, 20, 30, 30+offset, self.encounter[i].name)
            enemyRect = pygame.Rect(50+maxEncWidth,30+offset,(self.encounter[i].hp/self.encounter[i].hpMax)*100,20)
            outlineRect = pygame.Rect(50+maxEncWidth,30+offset,100,20)
            pygame.draw.rect(self.game.screen,self.game.red,enemyRect)
            pygame.draw.rect(self.game.screen,self.game.white,outlineRect,1)
            write(self.game, 20, 180+maxEncWidth, 30+offset, str(self.encounter[i].hp)+"/"+str(self.encounter[i].hpMax))
            if self.encounter[i].status != Status.NoStatus:
                if self.encounter[i].status == Status.Paralyzed:
                    write(self.game, 20, 280+maxEncWidth, 30+offset, "<P"+str(self.encounter[i].statusCount)+">")
                elif self.encounter[i].status == Status.Burned:
                    write(self.game, 20, 280+maxEncWidth, 30+offset, "<B>")
                elif self.encounter[i].status == Status.Freezing:
                    write(self.game, 20, 280+maxEncWidth, 30+offset, "<F>")
        for i in range(0,len(self.game.player.party.members)):
            offset = 30*i
            textWidth, textHeight = self.font.size(self.game.player.party.members[i].name)
            write(self.game, 20, self.right-textWidth-20, 170+offset, self.game.player.party.members[i].name)
            partyHPRect = pygame.Rect(self.right-maxPtyWidth-140,170+offset,(self.game.player.party.members[i].hp/self.game.player.party.members[i].hpMax)*100,10)
            partyMPRect = pygame.Rect(self.right-maxPtyWidth-140,180+offset,(self.game.player.party.members[i].mp/self.game.player.party.members[i].mpMax)*100,10)
            outlineRect = pygame.Rect(self.right-maxPtyWidth-140,170+offset,100,20)
            pygame.draw.rect(self.game.screen,self.game.red,partyHPRect)
            pygame.draw.rect(self.game.screen,self.game.blue,partyMPRect)
            pygame.draw.rect(self.game.screen,self.game.white,outlineRect,1)
            write(self.game, 20, self.right-maxPtyWidth-220, 170+offset, str(self.game.player.party.members[i].hp)+"/"+str(self.game.player.party.members[i].hpMax))
            if self.game.player.party.members[i].status != Status.NoStatus:
                if self.game.player.party.members[i].status == Status.Paralyzed:
                    write(self.game, 20, self.right-maxPtyWidth-280, 170+offset, "<P>")
                elif self.game.player.party.members[i].status == Status.Burned:
                    write(self.game, 20, self.right-maxPtyWidth-280, 170+offset, "<B>")
                elif self.game.player.party.members[i].status == Status.Freezing:
                    write(self.game, 20, self.right-maxPtyWidth-280, 170+offset, "<F>")
        #Setting border
        pygame.draw.line(self.game.screen,self.game.white,(self.left,320),(self.right+9,320),2)

    def statBlock(self):
        pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(350,350),2)
        pygame.draw.line(self.game.screen,self.game.white,(350,320),(350,self.bottom+7),2)
        write(self.game, 11, 360, 328, self.game.player.party.members[self.combatOrder[self.currentTurn][1]].name+", Level "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].level)+" "+self.game.player.party.members[self.combatOrder[self.currentTurn][1]].type.name)
        write(self.game, 11, 360, 345, "HP "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].hp)+"/"+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].hpMax))
        write(self.game, 11, 420, 345, "MP "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].mp)+"/"+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].mpMax))
        write(self.game, 11, 360, 360, "ATK "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getAttack()))
        write(self.game, 11, 420, 360, "DEF "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getDefense()))
        write(self.game, 11, 360, 375, "ACC "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getAccuracy()))
        write(self.game, 11, 420, 375, "DDG "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getDodge()))
        write(self.game, 11, 360, 390, "CRT "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getCritRate()))
        write(self.game, 11, 420, 390, "LCK "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getLuck()))
        write(self.game, 11, 360, 405, "AMP "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getAmplifier()))
        write(self.game, 11, 420, 405, "MPG "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getManaRegen()))
        write(self.game, 16, 360, 430, "\""+self.combatDialogue+"\"")
        iNext = 0
        for i in range(len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].activeBuffs)):
            writeOrientation(self.game, 11, self.right, 330+(i*15), self.game.player.party.members[self.combatOrder[self.currentTurn][1]].activeBuffs[i][0]+" ("+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].activeBuffs[i][1])+")","R")
            iNext += 1
        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Paralyzed:
            writeOrientation(self.game, 11, self.right, 330+(iNext*15), self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status.name+" ("+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].statusCount)+")","R")
        elif self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status != Status.NoStatus:
            writeOrientation(self.game, 11, self.right, 330+(iNext*15), self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status.name,"R")

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
            #print(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].name)
        if self.combatOrder[self.currentTurn][0] == "Party":
            self.combatDialogue = getCombatDialogue(self.game.player.party.members[self.combatOrder[self.currentTurn][1]])

    def prev(self):
        print(f'Before: {self.currentTurn}')
        good = False
        for action in self.actions:
            if action.source[0] == "Party":
                good = True
        if not good:
            return
        while len(self.actions) > 0 and self.currentTurn > 0:
            if self.actions[-1].source[0] == "Encounter":
                self.actions.pop()
                self.currentTurn -= 1
            elif self.actions[-1].source[0] == "Party":
                self.actions.pop()
                self.currentTurn -= 1
                break
        print(f'After: {self.currentTurn}')


    def enemyAction(self,source):
        if not self.isAlive(source):
            self.actions.append(Action(source,0,-1))
            print(f'Action writing for {source}, length {len(self.actions)}')
            return
        elif self.encounter[self.combatOrder[self.currentTurn][1]].status == Status.Paralyzed:
            self.actions.append(Action(source,0,-2))
            print(f'Action writing for {source}, length {len(self.actions)}')
            return
        elif self.encounter[self.combatOrder[self.currentTurn][1]].status == Status.Freezing and random.randint(0,2)==0:
            self.actions.append(Action(source,0,-3))
            print(f'Action writing for {source}, length {len(self.actions)}')
            return
        target = random.randint(0,len(self.game.player.party.members)-1)
        target = self.checkRecalculateTarget(source[0],target,"Party")
        timeout = 0
        while self.game.player.party.members[target].hp <= 0 and timeout < 20:
            target = random.randint(0,len(self.game.player.party.members)-1)
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
        print(f'Action writing for {source}, length {len(self.actions)}')

    def attack(self,source,target):
        self.crit = False
        if source[0] == "Encounter":
            target = self.checkRecalculateTarget(source[0],target,"Party")
            if self.encounter[source[1]].attack - self.game.player.party.members[target].getDefense() < 0:
                self.dmg = 0
            else:
                self.dmg = self.encounter[source[1]].attack - self.game.player.party.members[target].getDefense()
            if self.calculateHit(self.encounter[source[1]],self.game.player.party.members[target]):
                self.game.player.party.members[target].takeDamage(self.dmg)
                self.miss = False
            else:
                self.miss = True
        if source[0] == "Party":
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                self.dmg = 0
            else:
                self.dmg = self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense
            
            if self.calculateHit(self.game.player.party.members[source[1]],self.encounter[target]):
                if self.calculateCrit(self.game.player.party.members[source[1]]):
                    self.dmg *= 2
                    self.crit = True
                self.encounter[target].takeDamage(self.dmg)
                self.miss = False
            else:
                self.miss = True

    def checkRecalculateTarget(self,source,target,tgtGroup):
        if source == "Encounter":
            while not self.isAlive((tgtGroup,target)):
                target += 1
                if target >= len(self.game.player.party.members):
                    target = 0
        elif source == "Party":
            while not self.isAlive((tgtGroup,target)):
                target += 1
                if target >= len(self.encounter):
                    target = 0
        return target

    def calculateHit(self,attacker,defender):
        randA = random.randint(0,99)
        randB = random.randint(0,99)
        return (randA+randB) + (defender.getDodge()*2) < (attacker.getAccuracy()*2)
    
    def calculateCrit(self,attacker):
        rand = random.randint(0,99)
        return rand < attacker.getCritRate()

    def usePotion(self,target,itemID):
        target = self.checkRecalculateTarget("Party",target,"Encounter")
        for i in range(len(self.game.player.party.inventory)):
            if self.game.player.party.inventory[i].id == itemID:
                index = i
                break
        self.game.player.party.usePotion(target,index)

    def cast(self,source,target,spellID):
        if spellID < 400:
            spell = self.game.directory.getAtkSpell(spellID)
            if spell.target == Target.Single:
                if source[0] == "Encounter":
                    target = self.checkRecalculateTarget(source[0],target,"Party")
                    if spell.type == SpellType.Attack:
                        self.dmg = self.game.player.party.members[target].takeDamage(spell.attack)
                    elif spell.type == SpellType.Debuff:
                        if (spell.id > 326) or random.randint(0,1) == 1: # 50% Chance for 324, 325, 326
                            if spell.element == Element.Lightning:
                                self.game.player.party.members[target].status = Status.Paralyzed
                                self.game.player.party.members[target].statusCount = 3
                            elif spell.element == Element.Fire:
                                self.game.player.party.members[target].status = Status.Burned
                                self.game.player.party.members[target].statusCount = -1
                            elif spell.element == Element.Ice:
                                self.game.player.party.members[target].status = Status.Freezing
                                self.game.player.party.members[target].statusCount = -1
                else:
                    target = self.checkRecalculateTarget(source[0],target,"Encounter")
                    if spell.type == SpellType.Attack:
                        self.dmg = spell.attack
                        if spell.element == self.encounter[target].resistance:
                            self.dmg = int(self.dmg/2)
                        self.encounter[target].takeDamage(self.dmg)
                        self.game.player.party.members[source[1]].mp -= spell.manacost
                    elif spell.type == SpellType.Debuff:
                        if spell.id > 326 or random.randint(0,1) == 1: # 50% Chance for 324, 325, 326
                            if spell.element == Element.Lightning:
                                self.encounter[target].status = Status.Paralyzed
                                self.encounter[target].statusCount = 3
                            elif spell.element == Element.Fire:
                                self.encounter[target].status = Status.Burned
                                self.encounter[target].statusCount = -1
                            elif spell.element == Element.Ice:
                                self.encounter[target].status = Status.Freezing
                                self.encounter[target].statusCount = -1
                        self.game.player.party.members[source[1]].mp -= spell.manacost
            else:
                if source[0] == "Encounter":
                    if spell.type == SpellType.Attack:
                        for member in self.game.player.party.members:
                            self.dmg = member.takeDamage(spell.attack)
                    elif spell.type == SpellType.Debuff:
                        for member in self.game.player.party.members:
                            if random.randint(0,1) == 1:
                                if spell.element == Element.Lightning:
                                    member.status = Status.Paralyzed
                                    member.statusCount = 3
                                elif spell.element == Element.Fire:
                                    member.status = Status.Burned
                                    member.statusCount = -1
                                elif spell.element == Element.Ice:
                                    member.status = Status.Freezing
                                    member.statusCount = -1
                else:
                    if spell.type == SpellType.Attack:
                        for member in self.encounter:
                            self.dmg = spell.attack
                            if spell.element == member.resistance:
                                self.dmg = int(self.dmg/2)
                            member.takeDamage(self.dmg)
                        self.dmg = spell.attack
                        self.game.player.party.members[source[1]].mp -= spell.manacost
                    elif spell.type == SpellType.Debuff:
                        for member in self.encounter:
                            if random.randint(0,1) == 1:
                                if spell.element == Element.Lightning:
                                    member.status = Status.Paralyzed
                                    member.statusCount = 3
                                elif spell.element == Element.Fire:
                                    member.status = Status.Burned
                                    member.statusCount = -1
                                elif spell.element == Element.Ice:
                                    member.status = Status.Freezing
                                    member.statusCount = -1
                        self.game.player.party.members[source[1]].mp -= spell.manacost
        elif spellID < 500:
            spell = self.game.directory.getSptSpell(spellID)
            if spell.target == Target.Single:
                target = self.checkRecalculateTarget(source[0],target,"Party")
                if spell.type == SpellType.Heal:
                    if self.game.player.party.members[target].hp > 0:
                        self.game.player.party.members[target].hp += spell.getHeal()
                    if self.game.player.party.members[target].hp > self.game.player.party.members[target].hpMax:
                        self.game.player.party.members[target].hp = self.game.player.party.members[target].hpMax
                elif spell.type == SpellType.Buff:
                    self.applyBuff(spell,target)
                elif spell.type == SpellType.Raise:
                    if self.game.player.party.members[target].hp <= 0:
                        self.game.player.party.members[target].hp += spell.getHeal()
                    if self.game.player.party.members[target].hp > self.game.player.party.members[target].hpMax:
                        self.game.player.party.members[target].hp = self.game.player.party.members[target].hpMax
                elif spell.type == SpellType.Cleanse:
                    if self.game.player.party.members[target].hp > 0:
                        self.game.player.party.members[target].resetStatus()
                self.game.player.party.members[source[1]].mp -= spell.manacost
            elif spell.target == Target.All:
                if spell.type == SpellType.Heal:
                    for member in self.game.player.party.members:
                        if member.hp > 0:
                            member.hp += spell.getHeal()
                        if member.hp > member.hpMax:
                            member.hp = member.hpMax
                elif spell.type == SpellType.Buff:
                    self.applyBuff(spell,-1)
                elif spell.type == SpellType.Raise:
                    for member in self.game.player.party.members:
                        if member.hp <= 0:
                            member.hp += spell.getHeal()
                        if member.hp > member.hpMax:
                            member.hp = member.hpMax
                elif spell.type == SpellType.Cleanse:
                    for member in self.game.player.party.members:
                        if member.hp > 0:
                            member.resetStatus()
                self.game.player.party.members[source[1]].mp -= spell.manacost

    def validManaCost(self,user,spell):
        return user.mp >= self.game.directory.getManaCost(spell)

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
            if self.game.player.party.members[source[1]].hp<=0:
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
        #for i in range(len(self.combatOrder)):
        #    self.actions.pop(0)
        for i in range(len(self.combatOrder)-1,-1,-1):
            if self.isAlive(self.combatOrder[i]) == False:
                self.combatOrder.pop(i)
        self.actions.clear()
        self.state = "mainWindow"
        self.ex = False
        self.currentTurn = -1
        self.processBuffs()
        self.upkeep()
        self.next()

    def upkeep(self):
        for member in self.game.player.party.members:
            member.mp += member.getManaRegen()
            if member.mp > member.mpMax:
                member.mp = member.mpMax
            member.tickStatus()
            if member.status == Status.Burned:
                member.takeDamage(5)
        for member in self.encounter:
            member.tickStatus()
            if member.status == Status.Burned:
                member.takeDamage(5)

    def skip(self):
        while self.combatOrder[self.currentTurn][0] == "Encounter" or not self.isAlive(self.combatOrder[self.currentTurn]):
            #print(self.encounter[self.combatOrder[self.currentTurn][1]].name)
            if self.combatOrder[self.currentTurn][0] == "Encounter":
                self.enemyAction(self.combatOrder[self.currentTurn])
            else:
                self.actions.append(Action(self.combatOrder[self.currentTurn],0,-1))
                print(f'Action writing for {self.combatOrder[self.currentTurn]}, length {len(self.actions)}')
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
                if self.encounter[member[1]].hp > 0:
                    encFlag = True
            elif member[0] == "Party":
                if self.game.player.party.members[member[1]].hp > 0:
                    ptyFlag = True
        if ptyFlag == False:
            self.state = "lose"
            self.timeStart = pygame.time.get_ticks()
            print("Lose!")
            self.exTurn = 10
            self.timeStart -= 1000
            return True
        if encFlag == False:
            self.state = "win"
            self.timeStart = pygame.time.get_ticks()
            print("Win!")
            self.exTurn = 10
            self.timeStart -= 1000
            return True
        return False

    def applyBuff(self,buff,target):
        newBuff = Buff(buff.name,buff.potency,5,target)
        self.buffs.append(newBuff)
        if newBuff.target == -1:
            for member in self.game.player.party.members:
                member.addBuffs(newBuff)
        else:
            self.game.player.party.members[newBuff.target].addBuffs(newBuff)

    def processBuffs(self):
        for member in self.game.player.party.members:
            member.resetBuffs()
        for bf in self.buffs:
            if bf.target == -1:
                for member in self.game.player.party.members:
                    member.addBuffs(bf)
            else:
                self.game.player.party.members[bf.target].addBuffs(bf)
            bf.tick()
        for i in range(len(self.buffs)-1,-1,-1):
            if self.buffs[i].checkExpiry():
                print(f'{bf.name} expired.')
                self.buffs.pop(i)

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
