import pygame
import random
import time
from characters import Action
from characters import Buff
from dialogue import *
from writing import *
from characterpopups import *

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
        self.activeEffects = []
        self.scheduledManaCosts = []
        self.actionVal = -1
        self.state = "mainWindow"
        self.delay = 0
        self.ex = False
        self.exTurn = 0
        self.timeStart = 0
        self.dmg = 0
        self.heal = 0
        self.miss = False
        self.crit = False
        self.waitFlag = False
        self.cursorPos = -1
        self.menuTop = -1
        self.itemID = -1
        self.spellID = -1
        self.talentID = -1
        self.lowMana = False
        self.buffs = []
        self.duration = 0
        self.combatDialogue = ""
        self.defeat = False
        self.showElementalEffectivenessColorsTo = None
        
        self.hitAll = False
        self.immune = False
        self.manaspent = False
        self.risen = False
        self.curse = []
        self.deathWish = []
        self.pyrilicVenom = {}

    def initialize(self,encounter):
        self.currentTurn = 0
        self.exTurn = 0
        for i in range(0,len(self.game.player.party.members)):
            print(f'{self.game.player.party.members[i].name}, {self.game.player.party.members[i].type.name}, {self.game.player.party.members[i].level} (ID {self.game.player.party.members[i].id}) - WPN: {self.game.player.party.members[i].eqpWpn.name}, AMR: {self.game.player.party.members[i].eqpAmr.name}, HP: {self.game.player.party.members[i].getMaxHP()}, MP: {self.game.player.party.members[i].getMaxMP()}, ATK: {self.game.player.party.members[i].attack}, CRT: {self.game.player.party.members[i].critrate}, DEF: {self.game.player.party.members[i].defense}, DDG: {self.game.player.party.members[i].dodge}, LCK: {self.game.player.party.members[i].luck}, SPD: {self.game.player.party.members[i].speed}, PRS: {self.game.player.party.members[i].personality}, SPELLS: {self.game.player.party.members[i].spells}')
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

        # Add accessory effects to combat
        self.activeEffects = []
        for i, member in enumerate(self.game.player.party.members):
            if member.eqpAcc is not None:
                if member.eqpAcc.timing is not Timing.Universal:
                    print(f'Effect of {member.eqpAcc.name} in play!')
                    self.activeEffects.append(ActiveEffect(member.eqpAcc.id,("Party",i),-1,100))

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
                    self.state = "talentList"
                    self.cursorPos = 0
                    self.menuTop = 0
                    print("TALENT")
                elif self.cursorPos == 3:
                    self.state = "mainWindow"
                    print("CANCEL")
            elif self.state == "targetSelect":
                self.state = "mainWindow"
                self.showElementalEffectivenessColorsTo = None
                if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Shocked and random.randint(0,1)==1:
                    self.actionVal = -2
                elif self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Freezing and (self.game.directory.getItemType(self.actionVal) == Type.AtkSpell or self.game.directory.getItemType(self.actionVal) == Type.SptSpell):
                    self.actionVal = -4
                elif self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Freezing and random.randint(0,1)==1:
                    self.actionVal = -3
                if self.game.directory.getItem(self.actionVal).type == TalentType.PartyEffect or self.game.directory.getItem(self.actionVal).type == TalentType.EncounterEffect:
                    self.useTalent(self.combatOrder[self.currentTurn],self.cursorPos,self.actionVal)
                else:
                    self.writeAction(self.combatOrder[self.currentTurn],self.cursorPos,self.actionVal)
                print(f'Action writing for {self.combatOrder[self.currentTurn]}, length {len(self.actions)}')
                self.next()
                self.cursorPos = -1
                print("TARGET")
            elif self.state == "spellList":
                if self.cursorPos+self.menuTop < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells):
                    self.spellID = self.menuTop + self.cursorPos
                    if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID] >= 300 and self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID] < 400:
                        self.showElementalEffectivenessColorsTo = self.game.directory.getItem(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).element
                    self.state = "spellSummary"
                    print("SPELLSUMMARY")
            elif self.state == "itemList":
                if self.cursorPos+self.menuTop < len(self.game.player.party.inventory):
                    self.itemID = self.menuTop + self.cursorPos
                    if self.game.player.party.inventory[self.itemID] >= 200 and self.game.player.party.inventory[self.itemID] < 300:
                        self.state = "itemSummary"
                        print("ITEMSUMMARY")
                    elif self.game.player.party.inventory[self.itemID] >= 800 and self.game.player.party.inventory[self.itemID] < 900 and self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).timing != Timing.Peacetime:
                        self.state = "itemSummary"
                        print("ITEMSUMMARY")
            elif self.state == "talentList":
                if self.cursorPos+self.menuTop < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents):
                    self.talentID = self.menuTop + self.cursorPos
                    self.state = "talentSummary"
                    print("TALENTSUMMARY")
            elif self.state =="spellSummary":
                if self.validManaCost(self.game.player.party.members[self.combatOrder[self.currentTurn][1]],self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]):
                    if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].checkSpellProficiency(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID],self.game.directory):
                        self.lowMana = False
                        self.actionVal = self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]
                        if self.game.directory.getSpellTarget(self.actionVal) == Target.Single:
                            self.state = "targetSelect"
                            self.cursorPos = 0
                            self.enterTargetSelect()
                        else:
                            self.state = "mainWindow"
                            self.showElementalEffectivenessColorsTo = None
                            if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Shocked and random.randint(0,1)==0:
                                self.actionVal = -2
                            elif self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Freezing:
                                self.actionVal = -4
                            elif self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Freezing and random.randint(0,1)==0:
                                self.actionVal = -3
                            self.writeAction(self.combatOrder[self.currentTurn],0,self.actionVal)
                            print(f'Action writing for {self.combatOrder[self.currentTurn]}, length {len(self.actions)}')
                            self.next()
                            self.cursorPos = -1
                        print("SPELL")
                else:
                    self.lowMana = True
            elif self.state =="itemSummary":
                if self.game.player.party.inventory[self.itemID] >= 200 and self.game.player.party.inventory[self.itemID] < 300:
                    self.actionVal = self.game.player.party.inventory[self.itemID]
                    self.state = "targetSelect"
                    if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Shocked and random.randint(0,1)==0:
                        self.actionVal = -2
                    elif self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Freezing and random.randint(0,1)==0:
                        self.actionVal = -3
                    self.cursorPos = 0
                    self.enterTargetSelect()
                    print("ITEM")
                elif self.game.player.party.inventory[self.itemID] >= 800 and self.game.player.party.inventory[self.itemID] < 900:
                    if self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).timing != Timing.Peacetime:
                        self.actionVal = self.game.player.party.inventory[self.itemID]
                        if self.game.directory.getConsumableTarget(self.actionVal) == Target.Single or self.game.directory.getConsumableTarget(self.actionVal) == Target.Ally:
                            self.state = "targetSelect"
                            self.cursorPos = 0
                            self.enterTargetSelect()
                        else:
                            self.state = "mainWindow"
                            if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Shocked and random.randint(0,1)==0:
                                self.actionVal = -2
                            elif self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Freezing and random.randint(0,1)==0:
                                self.actionVal = -3
                            self.writeAction(self.combatOrder[self.currentTurn],0,self.actionVal)
                            print(f'Action writing for {self.combatOrder[self.currentTurn]}, length {len(self.actions)}')
                            self.next()
                            self.cursorPos = -1
                        print("TALENT")
            elif self.state =="talentSummary":
                if self.validManaCost(self.game.player.party.members[self.combatOrder[self.currentTurn][1]],self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents[self.talentID]):
                    self.lowMana = False
                    self.actionVal = self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents[self.talentID]
                    print(f'Target was {self.game.directory.getTalentTarget(self.actionVal)}')
                    if self.game.directory.getTalentTarget(self.actionVal) == Target.Single or self.game.directory.getTalentTarget(self.actionVal) == Target.Ally:
                        self.state = "targetSelect"
                        self.cursorPos = 0
                        self.enterTargetSelect()
                    else:
                        self.state = "mainWindow"
                        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Shocked and random.randint(0,1)==0:
                            self.actionVal = -2
                        elif self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status == Status.Freezing and random.randint(0,1)==0:
                            self.actionVal = -3
                        if self.game.directory.getItemType(self.actionVal) == Type.Talent:
                            self.useTalent(self.combatOrder[self.currentTurn],0,self.actionVal)
                        else:
                            self.writeAction(self.combatOrder[self.currentTurn],0,self.actionVal)
                        print(f'Action writing for {self.combatOrder[self.currentTurn]}, length {len(self.actions)}')
                        self.next()
                        self.cursorPos = -1
                    print("TALENT")
                else:
                    self.lowMana = True
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
                self.showElementalEffectivenessColorsTo = None
                print("BACK")
            elif self.state == "spellList":
                self.state = "useMenu"
                print("BACK")
            elif self.state == "itemList":
                self.state = "useMenu"
                print("BACK")
            elif self.state == "talentList":
                self.state = "useMenu"
                print("BACK")
            elif self.state == "spellSummary":
                self.state = "spellList"
                self.showElementalEffectivenessColorsTo = None
                print("BACK")
            elif self.state == "itemSummary":
                self.state = "itemList"
                print("BACK")
            elif self.state == "talentSummary":
                self.state = "talentList"
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
                if self.actionVal >= 500:
                    tgtList = self.encounter if self.game.directory.getItem(self.actionVal).target == Target.Single else self.game.player.party.members
                if tgtList == self.encounter:
                    for i in range(0,self.cursorPos):
                        if tgtList[i].hp > 0:
                            self.cursorPos = i
                else:
                    self.cursorPos -= 1
                    if self.cursorPos < 0:
                        self.cursorPos = len(self.game.player.party.members)-1
            elif self.state == "useMenu":
                if self.cursorPos == 2 or self.cursorPos == 3:
                    self.cursorPos -= 2
            elif self.state == "spellList" or self.state == "itemList" or self.state == "talentList":
                if self.cursorPos == 0 or self.cursorPos == 1:
                    if self.menuTop > 0:
                        self.menuTop -= 2
                else:
                    self.cursorPos -= 2
        if self.game.DOWN:
            if self.state == "targetSelect":
                tgtList = self.encounter if self.actionVal < 200 or (self.actionVal >= 300 and self.actionVal < 400) else self.game.player.party.members
                if self.actionVal >= 500:
                    tgtList = self.encounter if self.game.directory.getItem(self.actionVal).target == Target.Single else self.game.player.party.members
                if tgtList == self.encounter:
                    for i in range(self.cursorPos+1,len(tgtList)):
                        if tgtList[i].hp > 0:
                            self.cursorPos = i
                            break
                else:
                    self.cursorPos += 1
                    if self.cursorPos > len(self.game.player.party.members)-1:
                        self.cursorPos = 0
            elif self.state == "useMenu":
                if self.cursorPos == 0 or self.cursorPos == 1:
                    self.cursorPos += 2
            elif self.state == "spellList":
                if self.cursorPos == 2 or self.cursorPos == 3:
                    if self.menuTop+4 < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells):
                        self.menuTop += 2
                else:
                    self.cursorPos += 2
            elif self.state == "talentList":
                if self.cursorPos == 2 or self.cursorPos == 3:
                    if self.menuTop+4 < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents):
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
            if self.state == "spellList" or self.state == "itemList" or self.state == "talentList":
                if self.cursorPos == 1 or self.cursorPos == 3:
                    self.cursorPos -= 1
            elif self.state == "useMenu":
                if self.cursorPos > 0:
                    self.cursorPos -= 1
        if self.game.RIGHT:
            if self.state == "spellList" or self.state == "itemList" or self.state == "talentList":
                if self.cursorPos == 0 or self.cursorPos == 2:
                    self.cursorPos += 1
            elif self.state == "useMenu":
                if self.cursorPos < 3:
                    self.cursorPos += 1

    def enterTargetSelect(self):
        self.cursorPos = 0
        tgtList = self.encounter if self.actionVal < 200 else self.game.player.party.members
        if self.actionVal >= 500:
            tgtList = self.encounter if self.game.directory.getItem(self.actionVal).target == Target.Single else self.game.player.party.members
        if tgtList == self.encounter:
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
            write(self.game, 20,210,375,"B) USE") #SPELL, ITEM, TALENT
            write(self.game, 20,45,420,"X) CANCEL")
            write(self.game, 20,210,420,"Y) RUN")
            self.statBlock()

        if self.state == "useMenu":
            write(self.game, 20, self.left+15, 325, "Use what?")
            write(self.game, 20, 28+(int(self.cursorPos%2)*165), 373+(int(self.cursorPos/2)*45), ">")
            write(self.game, 20,45,375,"SPELL")
            write(self.game, 13,45,395,str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].mp)+"/"+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getMaxMP()))
            write(self.game, 20,210,375,"ITEM")
            write(self.game, 20,45,420,"TALENT")
            write(self.game, 20,210,420,"CANCEL")
            self.statBlock()

        if self.state == "targetSelect":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "Select a target")
            group = "Encounter"
            if (self.actionVal >= 200 and self.actionVal < 300) or (self.actionVal >= 400 and self.actionVal < 500) or (self.actionVal >= 500 and self.game.directory.getItem(self.actionVal).target==Target.Ally):
                group = "Party"
            if group == "Encounter":
                write(self.game, 20, 480, 30+(self.cursorPos*30), "<")
                write(self.game, 20,30,400,"A) SELECT")
                write(self.game, 20,180,400,"B) BACK")
            elif group == "Party":
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
                write(self.game, 18,60,380,str(self.menuTop+1)+") "+self.game.directory.getItemName(self.game.player.party.inventory[self.menuTop],True))
            else:
                write(self.game, 18,60,380,str(self.menuTop+1)+")")
            if self.menuTop+1 < len(self.game.player.party.inventory):
                write(self.game, 18,360,380,str(self.menuTop+2)+") "+self.game.directory.getItemName(self.game.player.party.inventory[self.menuTop+1],True))
            else:
                write(self.game, 18,360,380,str(self.menuTop+2)+")")
            if self.menuTop+2 < len(self.game.player.party.inventory):
                write(self.game, 18,60,420,str(self.menuTop+3)+") "+self.game.directory.getItemName(self.game.player.party.inventory[self.menuTop+2],True))
            else:
                write(self.game, 18,60,420,str(self.menuTop+3)+")")
            if self.menuTop+3 < len(self.game.player.party.inventory):
                write(self.game, 18,360,420,str(self.menuTop+4)+") "+self.game.directory.getItemName(self.game.player.party.inventory[self.menuTop+3],True))
            else:
                write(self.game, 18,360,420,str(self.menuTop+4)+")")

        if self.state == "talentList":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "Select a talent: (B to cancel)")
            write(self.game, 20, 40+((self.cursorPos%2)*300), 380+((int(self.cursorPos/2))*40), ">")
            if self.menuTop < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents):
                write(self.game, 18,60,380,str(self.menuTop+1)+") "+self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents[self.menuTop],True))
            else:
                write(self.game, 18,60,380,str(self.menuTop+1)+")")
            if self.menuTop+1 < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents):
                write(self.game, 18,360,380,str(self.menuTop+2)+") "+self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents[self.menuTop+1],True))
            else:
                write(self.game, 18,360,380,str(self.menuTop+2)+")")
            if self.menuTop+2 < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents):
                write(self.game, 18,60,420,str(self.menuTop+3)+") "+self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents[self.menuTop+2],True))
            else:
                write(self.game, 18,60,420,str(self.menuTop+3)+")")
            if self.menuTop+3 < len(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents):
                write(self.game, 18,360,420,str(self.menuTop+4)+") "+self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents[self.menuTop+3],True))
            else:
                write(self.game, 18,360,420,str(self.menuTop+4)+")")

        if self.state == "spellSummary":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "Do you want to cast this spell?")
            write(self.game, 16, self.left+15, 360, self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID])+": Costs "+str(self.game.directory.getManaCost(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]))+" MP")
            if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID] < 400:
                writeOrientation(self.game, 16,self.right-10, 360, str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].amplify(self.game.directory.getAtkSpell(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).attack))+" Damage","R")
            else:
                if self.game.directory.getSptSpell(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).type == SpellType.Heal:
                    writeOrientation(self.game, 16,self.right-10, 360, "Restores "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].amplify(self.game.directory.getSptSpell(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).getHeal()))+" HP","R")
                if self.game.directory.getSptSpell(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).type == SpellType.Buff:
                    i = 0
                    for id, buff in enumerate(self.game.directory.getSptSpell(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]).potency):
                        if buff > 0:
                            writeOrientation(self.game, 16,self.right-10, 360+(i*20), self.lookupBuffName(id)+" "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].amplify(buff)),"R")
                            i += 1
            write(self.game, 16, self.left+15, 380, self.game.directory.getItemDesc(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].spells[self.spellID]))
            write(self.game, 20,150,425,"A) CONFIRM")
            write(self.game, 20,385,425,"B) BACK")

        if self.state == "itemSummary":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "Do you want to use this item?")
            write(self.game, 16, self.left+15, 360, self.game.directory.getItemName(self.game.player.party.inventory[self.itemID]))
            if self.game.directory.getItemType(self.game.player.party.inventory[self.itemID]) == Type.Potion:
                if self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).hpGain > 0 and self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).mpGain > 0:
                    writeOrientation(self.game, 16,self.right-10, 360, "Restores "+str(self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).hpGain)+" HP and "+str(self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).mpGain)+" MP","R")
                elif self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).hpGain > 0 and self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).mpGain == 0:
                    writeOrientation(self.game, 16,self.right-10, 360, "Restores "+str(self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).hpGain)+" HP","R")
                elif self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).hpGain == 0 and self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).mpGain > 0:
                    writeOrientation(self.game, 16,self.right-10, 360, "Restores "+str(self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).mpGain)+" MP","R")
            wrapWrite(self.game, 16, self.game.directory.getItem(self.game.player.party.inventory[self.itemID]).description, self.right-20, self.left+15, 380)
            write(self.game, 20,150,425,"A) CONFIRM")
            write(self.game, 20,385,425,"B) BACK")

        if self.state == "talentSummary":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "Do you want to perform this talent?")
            write(self.game, 16, self.left+15, 360, self.game.directory.getItemName(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents[self.talentID])+": Costs "+str(self.game.directory.getManaCost(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents[self.talentID]))+" MP")
            write(self.game, 16, self.left+15, 380, self.game.directory.getItemDesc(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].talents[self.talentID]))
            write(self.game, 20,150,425,"A) CONFIRM")
            write(self.game, 20,385,425,"B) BACK")

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
                    combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " is shocked, and cannot move!"
                else:
                    combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " is shocked, and cannot move!"
            elif self.actions[self.exTurn-1].action == -4:
                if self.actions[self.exTurn-1].source[0] == "Encounter":
                    combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " is freezing, and cannot cast spells!"
                else:
                    combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " is freezing, and cannot cast spells!"
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
                        combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " at " + self.game.player.party.members[self.actions[self.exTurn-1].target].name
                    else:
                        combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action)
                else:
                    if self.game.directory.getAtkSpell(self.actions[self.exTurn-1].action).target == Target.Single:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " at " + self.encounter[self.actions[self.exTurn-1].target].name
                    else:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action)
                if self.game.directory.getAtkSpell(self.actions[self.exTurn-1].action).type == SpellType.Attack:
                    combatStr += " for " + str(self.dmg) + " damage!"
                else:
                    combatStr += "!"
            elif self.actions[self.exTurn-1].action >= 400 and self.actions[self.exTurn-1].action < 500:
                if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).type == SpellType.Buff:
                    if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).target == Target.Single:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + "!"
                    else:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + "!"
                elif self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).type == SpellType.Heal:
                    if self.game.directory.getSptSpell(self.actions[self.exTurn-1].action).target == Target.Single:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + ", restoring " + str(self.heal) + " HP!"
                    else:
                        combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + ", restoring " + str(self.heal) + " HP!"
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
            elif self.actions[self.exTurn-1].action >= 500 and self.actions[self.exTurn-1].action < 600 and self.game.directory.getItem(self.actions[self.exTurn-1].action).timing==Timing.InTurn:
                if self.game.directory.getTalentTarget(self.actions[self.exTurn-1].action) == Target.Single or self.game.directory.getTalentTarget(self.actions[self.exTurn-1].action) == Target.Ally:
                    combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " performs " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.encounter[self.actions[self.exTurn-1].target].name + "!"
                else:
                    combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " performs " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + "!"
            elif self.actions[self.exTurn-1].action >= 800 and self.actions[self.exTurn-1].action < 900:
                if self.game.directory.getConsumableTarget(self.actions[self.exTurn-1].action) == Target.Single:
                    combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " uses " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.encounter[self.actions[self.exTurn-1].target].name + "!"
                elif self.game.directory.getConsumableTarget(self.actions[self.exTurn-1].action) == Target.Ally:
                    combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " uses " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " on " + self.game.player.party.members[self.actions[self.exTurn-1].target].name + "!"
                else:
                    combatStr = self.game.player.party.members[self.actions[self.exTurn-1].source[1]].name + " uses " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + "!"
            write(self.game, 20, self.left+15, 325, combatStr)

        if self.state == "win":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "You win!")
            if pygame.time.get_ticks() - self.timeStart >= 3000:
                difficulty = 0
                for monster in self.encounter:
                    difficulty += monster.level
                gold = self.game.player.awardGold(difficulty)
                levelups = self.game.player.party.awardXP(difficulty)
                for i in range(len(levelups)):
                    if levelups[i] == 1:
                        LevelUp(self.game, self.game.player.party.members[i])
                self.combatTeardown()
                self.inCombat = False

        if self.state == "lose":
            pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)
            write(self.game, 20, self.left+15, 325, "You have fallen...")
            if pygame.time.get_ticks() - self.timeStart >= 2000:
                self.combatTeardown()
                self.inCombat = False
                self.defeat = True
                self.game.load()

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
            color = self.game.white
            if self.showElementalEffectivenessColorsTo is not None:
                effectiveness = self.checkElementalEffectiveness(self.showElementalEffectivenessColorsTo, self.encounter[i].element)
                if effectiveness == "Vulnerability":
                    color = self.game.green
                elif effectiveness == "Resistance":
                    color = self.game.red
            textWidth, textHeight = writeColor(self.game, 20, 30, 30+offset, self.encounter[i].name,color)
            enemyRect = pygame.Rect(50+maxEncWidth,30+offset,(self.encounter[i].hp/self.encounter[i].getMaxHP())*100,20)
            outlineRect = pygame.Rect(50+maxEncWidth,30+offset,100,20)
            pygame.draw.rect(self.game.screen,self.game.red,enemyRect)
            pygame.draw.rect(self.game.screen,self.game.white,outlineRect,1)
            write(self.game, 20, 180+maxEncWidth, 30+offset, str(self.encounter[i].hp)+"/"+str(self.encounter[i].getMaxHP()))
            if self.encounter[i].status != Status.NoStatus:
                if self.encounter[i].status == Status.Shocked:
                    writeColor(self.game, 20, 280+maxEncWidth, 30+offset, "<S"+str(self.encounter[i].statusCount)+">", self.game.yellow)
                elif self.encounter[i].status == Status.Ablaze:
                    writeColor(self.game, 20, 280+maxEncWidth, 30+offset, "<A"+str(self.encounter[i].statusCount)+">", self.game.red)
                elif self.encounter[i].status == Status.Freezing:
                    writeColor(self.game, 20, 280+maxEncWidth, 30+offset, "<F"+str(self.encounter[i].statusCount)+">", self.game.lightblue)
        for i in range(0,len(self.game.player.party.members)):
            offset = 30*i
            textWidth, textHeight = self.font.size(self.game.player.party.members[i].name)
            write(self.game, 20, self.right-textWidth-20, 170+offset, self.game.player.party.members[i].name)
            partyHPRect = pygame.Rect(self.right-maxPtyWidth-140,170+offset,(self.game.player.party.members[i].hp/self.game.player.party.members[i].getMaxHP())*100,10)
            partyMPRect = pygame.Rect(self.right-maxPtyWidth-140,180+offset,(self.game.player.party.members[i].mp/self.game.player.party.members[i].getMaxMP())*100,10)
            outlineRect = pygame.Rect(self.right-maxPtyWidth-140,170+offset,100,20)
            pygame.draw.rect(self.game.screen,self.game.red,partyHPRect)
            pygame.draw.rect(self.game.screen,self.game.blue,partyMPRect)
            pygame.draw.rect(self.game.screen,self.game.white,outlineRect,1)
            write(self.game, 20, self.right-maxPtyWidth-220, 170+offset, str(self.game.player.party.members[i].hp)+"/"+str(self.game.player.party.members[i].getMaxHP()))
            if self.game.player.party.members[i].status != Status.NoStatus:
                if self.game.player.party.members[i].status == Status.Shocked:
                    writeColor(self.game, 20, self.right-maxPtyWidth-280, 170+offset, "<S"+str(self.game.player.party.members[i].statusCount)+">", self.game.yellow)
                elif self.game.player.party.members[i].status == Status.Ablaze:
                    writeColor(self.game, 20, self.right-maxPtyWidth-280, 170+offset, "<A"+str(self.game.player.party.members[i].statusCount)+">", self.game.red)
                elif self.game.player.party.members[i].status == Status.Freezing:
                    writeColor(self.game, 20, self.right-maxPtyWidth-280, 170+offset, "<F"+str(self.game.player.party.members[i].statusCount)+">", self.game.lightblue)
        #Setting border
        pygame.draw.line(self.game.screen,self.game.white,(self.left,320),(self.right+9,320),2)

    def statBlock(self):
        pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(350,350),2)
        pygame.draw.line(self.game.screen,self.game.white,(350,320),(350,self.bottom+7),2)
        write(self.game, 11, 360, 328, self.game.player.party.members[self.combatOrder[self.currentTurn][1]].name+", Level "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].level)+" "+self.game.player.party.members[self.combatOrder[self.currentTurn][1]].type.name)
        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("HP") > 0:
            write(self.game, 11, 360, 345, "HP "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].hp)+"/"+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getMaxHP()) + " (+" + str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("HP")) + ")")
        else:
            write(self.game, 11, 360, 345, "HP "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].hp)+"/"+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getMaxHP()))
        write(self.game, 11, 440, 345, "MP "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].mp)+"/"+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getMaxMP()))
        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("ATK") > 0:
            write(self.game, 11, 360, 360, "ATK "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getAttack()) + " (+" + str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("ATK")) + ")")
        else:
            write(self.game, 11, 360, 360, "ATK "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getAttack()))
        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("DEF") > 0:
            write(self.game, 11, 440, 360, "DEF "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getDefense()) + " (+" + str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("DEF")) + ")")
        else:
            write(self.game, 11, 440, 360, "DEF "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getDefense()))
        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("ACC") > 0:
            write(self.game, 11, 360, 375, "ACC "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getAccuracy()) + " (+" + str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("ACC")) + ")")
        else:
            write(self.game, 11, 360, 375, "ACC "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getAccuracy()))
        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("DDG") > 0:
            write(self.game, 11, 440, 375, "DDG "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getDodge()) + " (+" + str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("DDG")) + ")")
        else:
            write(self.game, 11, 440, 375, "DDG "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getDodge()))
        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("CRT") > 0:
            write(self.game, 11, 360, 390, "CRT "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getCritRate()) + " (+" + str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("CRT")) + ")")
        else:
            write(self.game, 11, 360, 390, "CRT "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getCritRate()))
        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("LCK") > 0:
            write(self.game, 11, 440, 390, "LCK "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getLuck()) + " (+" + str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getBuff("LCK")) + ")")
        else:
            write(self.game, 11, 440, 390, "LCK "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getLuck()))
        write(self.game, 11, 360, 405, "AMP "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getAmplifier()))
        write(self.game, 11, 440, 405, "MPG "+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].getManaRegen()))
        write(self.game, 16, 360, 430, "\""+self.combatDialogue+"\"")
        iNext = 0
        effectList = self.game.player.party.members[self.combatOrder[self.currentTurn][1]].activeBuffs[:]
        for effect in self.activeEffects:
            if effect.id >= 800 and effect.id < 900:
                if self.game.directory.getItem(effect.id).target == Target.All or effect.target == self.combatOrder[self.currentTurn][1]:
                    if effect.duration < 50:
                        effectList.append((self.game.directory.getItemName(effect.id),effect.duration))
                    else:
                        effectList.append((self.game.directory.getItemName(effect.id),"Inf"))
        for i in range(len(effectList)):
            writeOrientation(self.game, 11, self.right, 330+(i*15), effectList[i][0]+" ("+str(effectList[i][1])+")","R")
            iNext += 1
        if self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status != Status.NoStatus:
            writeOrientation(self.game, 11, self.right, 330+(iNext*15), self.game.player.party.members[self.combatOrder[self.currentTurn][1]].status.name+" ("+str(self.game.player.party.members[self.combatOrder[self.currentTurn][1]].statusCount)+")","R")

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
            self.writeAction(source,0,-1)
            print(f'Action writing for {source}, length {len(self.actions)}')
            return
        elif self.encounter[self.combatOrder[self.currentTurn][1]].status == Status.Shocked and random.randint(0,1)==0:
            self.writeAction(source,0,-2)
            print(f'Action writing for {source}, length {len(self.actions)}')
            return
        elif self.encounter[self.combatOrder[self.currentTurn][1]].status == Status.Freezing and random.randint(0,1)==0:
            self.writeAction(source,0,-3)
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
            self.writeAction(source, target, 0)
            if self.encounter[self.combatOrder[self.currentTurn][1]].spellCooldown > 0:
                self.encounter[self.combatOrder[self.currentTurn][1]].spellCooldown -= 1
        else:
            if self.encounter[self.combatOrder[self.currentTurn][1]].status == Status.Freezing:
                self.encounter[self.combatOrder[self.currentTurn][1]].spellCooldown = 2
                self.writeAction(source, target, -4)
            else:
                self.encounter[self.combatOrder[self.currentTurn][1]].spellCooldown = 2
                self.writeAction(source, target, self.encounter[self.combatOrder[self.currentTurn][1]].knownSpells[move-1])
        print(f'Action writing for {source}, length {len(self.actions)}')

    def attack(self,action):
        self.crit = False
        if action.source[0] == "Encounter":
            action.target = self.checkRecalculateTarget(action.source[0],action.target,"Party")
            self.checkEffectTiming(action,Timing.Targeting)
            if self.encounter[action.source[1]].attack - self.game.player.party.members[action.target].getDefense() < 0:
                self.dmg = 0
            else:
                self.dmg = self.encounter[action.source[1]].attack - self.game.player.party.members[action.target].getDefense()
            if self.calculateHit(self.encounter[action.source[1]],self.game.player.party.members[action.target]):
                self.miss = False
                self.checkEffectTiming(action,Timing.DamageTaken)
                self.game.player.party.members[action.target].takeDamage(self.dmg)
            else:
                self.miss = True
        if action.source[0] == "Party":
            if not self.hitAll:
                action.target = self.checkRecalculateTarget(action.source[0],action.target,"Encounter")
                self.checkEffectTiming(action,Timing.Targeting)
                if self.game.player.party.members[action.source[1]].getAttack() - self.encounter[action.target].defense < 0:
                    self.dmg = 0
                else:
                    self.dmg = self.game.player.party.members[action.source[1]].getAttack() - self.encounter[action.target].defense
                if self.calculateHit(self.game.player.party.members[action.source[1]],self.encounter[action.target]):
                    if self.calculateCrit(self.game.player.party.members[action.source[1]]):
                        self.dmg *= 2
                        self.crit = True
                    self.miss = False
                    self.checkEffectTiming(action,Timing.DamageDealt)
                    self.encounter[action.target].takeDamage(self.dmg)
                else:
                    self.miss = True
                    self.checkCursedItems(self.game.player.party.members[action.source[1]])
            elif self.hitAll:
                if self.calculateCrit(self.game.player.party.members[action.source[1]]):
                    self.crit = True
                for tgt in range(len(self.encounter)):
                    target = tgt
                    if self.isAlive(("Encounter",target)):
                        if self.game.player.party.members[action.source[1]].getAttack() - self.encounter[target].defense < 0:
                            self.dmg = 0
                        else:
                            self.dmg = self.game.player.party.members[action.source[1]].getAttack() - self.encounter[target].defense
                        if self.calculateHit(self.game.player.party.members[action.source[1]],self.encounter[target]):
                            if self.crit:
                                self.dmg *= 2
                            self.encounter[target].takeDamage(self.dmg)
                            self.miss = False
                        else:
                            self.miss = True
                            self.checkCursedItems(self.game.player.party.members[action.source[1]])

        self.hitAll = False

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
    
    def writeAction(self,source,target,action):
        if action > 500 and action <= 599:
            if self.game.directory.getItem(action).timing == Timing.Ordering:
                effect = ActiveEffect(action, source, target)
                self.activeEffects.insert(0,effect)
        act = Action(source, target, action)
        self.actions.append(act)

    def usePotion(self,target,itemID):
        target = self.checkRecalculateTarget("Party",target,"Party")
        for i in range(len(self.game.player.party.inventory)):
            if self.game.player.party.inventory[i] == itemID:
                index = i
                break
        self.game.player.party.usePotion(target,index,self.game.directory)

    def useTalent(self,source,target,id):
        talent = self.game.directory.getTalent(id)
        if talent.type == TalentType.PartyEffect or talent.type == TalentType.EncounterEffect:
            effect = ActiveEffect(talent.id, source, target)
            self.scheduledManaCosts.append((source[1],talent.mpcost))
            self.activeEffects.insert(0,effect)
            self.writeAction(source,target,-1)
        elif talent.type == TalentType.Action and talent.timing == Timing.Ordering:
            effect = ActiveEffect(talent.id, source, target)
            self.activeEffects.insert(0,effect)
            self.writeAction(source,target,-1)
        elif talent.type == TalentType.Action:
            self.writeAction(source,target,id)

    def cast(self,action):
        if action.action < 400:
            spell = self.game.directory.getAtkSpell(action.action)
            if spell.target == Target.Single:
                if action.source[0] == "Encounter":
                    action.target = self.checkRecalculateTarget(action.source[0],action.target,"Party")
                    self.checkEffectTiming(action,Timing.Targeting)
                    if spell.type == SpellType.Attack:
                        self.dmg = spell.attack
                        self.checkEffectTiming(action,Timing.DamageTaken)
                        self.game.player.party.members[action.target].takeDamage(self.dmg)
                    elif spell.type == SpellType.Debuff:
                        self.checkEffectTiming(action,Timing.DamageTaken)
                        if not self.immune:
                            self.applyStatusEffect(self.game.player.party.members,action.target,spell)
                        self.immune = False
                else:
                    action.target = self.checkRecalculateTarget(action.source[0],action.target,"Encounter")
                    self.checkEffectTiming(action,Timing.Targeting)
                    if spell.type == SpellType.Attack:
                        self.dmg = self.game.player.party.members[action.source[1]].amplify(spell.attack)
                        effectiveness = self.checkElementalEffectiveness(spell.element, self.encounter[action.target].element)
                        if effectiveness == "Resistance":
                            print("Resisted!")
                            self.dmg = math.ceil(self.dmg/2)
                        if effectiveness == "Vulnerability":
                            print("Vulnerable!")
                            self.dmg = math.ceil(self.dmg*1.5)
                        self.game.player.party.members[action.source[1]].mp -= spell.manacost
                        self.checkEffectTiming(action,Timing.DamageDealt)
                        self.encounter[action.target].takeDamage(self.dmg)
                    elif spell.type == SpellType.Debuff:
                        self.applyStatusEffect(self.encounter,action.target,spell)
                        self.game.player.party.members[action.source[1]].mp -= spell.manacost
            else:
                if action.source[0] == "Encounter":
                    if spell.type == SpellType.Attack:
                        for i, member in enumerate(self.game.player.party.members):
                            self.dmg = spell.attack
                            self.checkEffectTiming(Action(action.source,i,action.action),Timing.DamageTaken)
                            member.takeDamage(self.dmg)
                    elif spell.type == SpellType.Debuff:
                            for index, member in enumerate(self.game.player.party.members):
                                self.checkEffectTiming(action,Timing.DamageTaken)
                                if not self.immune:
                                    self.applyStatusEffect(self.game.player.party.members,index,spell)
                                self.immune = False
                else:
                    if spell.type == SpellType.Attack:
                        for member in self.encounter:
                            self.dmg = self.game.player.party.members[action.source[1]].amplify(spell.attack)
                            effectiveness = self.checkElementalEffectiveness(spell.element, self.encounter[action.target].element)
                            if effectiveness == "Resistance":
                                print("Resisted!")
                                self.dmg = math.ceil(self.dmg/2)
                            if effectiveness == "Vulnerability":
                                print("Vulnerable!")
                                self.dmg = math.ceil(self.dmg*1.5)
                            self.checkEffectTiming(action,Timing.DamageDealt)
                            member.takeDamage(self.dmg)
                        self.dmg = self.game.player.party.members[action.source[1]].amplify(spell.attack)
                        self.game.player.party.members[action.source[1]].mp -= spell.manacost
                    elif spell.type == SpellType.Debuff:
                        for index, member in enumerate(self.encounter):
                            self.applyStatusEffect(self.encounter,index,spell)
                        self.game.player.party.members[action.source[1]].mp -= spell.manacost
        elif action.action < 500:
            spell = self.game.directory.getSptSpell(action.action)
            if spell.target == Target.Single:
                if spell.type != SpellType.Raise:
                    action.target = self.checkRecalculateTarget(action.source[0],action.target,"Party")
                self.checkEffectTiming(action,Timing.Targeting)
                self.game.player.party.members[action.source[1]].mp -= spell.manacost
                if spell.type == SpellType.Heal:
                    if self.game.player.party.members[action.target].hp > 0:
                        self.heal = self.game.player.party.members[action.target].amplify(spell.getHeal())
                        print(f'Healing for {self.heal}')
                        self.checkEffectTiming(action,Timing.DamageDealt)
                        self.game.player.party.members[action.target].gainHP(self.heal)
                elif spell.type == SpellType.Buff:
                    self.buff = spell
                    print(f'Checking timing for {action}...')
                    self.duration = 5
                    self.checkEffectTiming(action,Timing.DamageDealt)
                    self.applyBuff(self.buff,action.target,action.source)
                elif spell.type == SpellType.Raise:
                    self.heal = spell.getHeal()
                    self.checkEffectTiming(action,Timing.DamageDealt)
                    if self.game.player.party.members[action.target].hp <= 0:
                        self.game.player.party.members[action.target].hp += self.heal
                    if self.game.player.party.members[action.target].hp > self.game.player.party.members[action.target].getMaxHP():
                        self.game.player.party.members[action.target].hp = self.game.player.party.members[action.target].getMaxHP()
                    self.risen = True
                elif spell.type == SpellType.Cleanse:
                    self.checkEffectTiming(action,Timing.DamageDealt)
                    if self.game.player.party.members[action.target].hp > 0:
                        self.game.player.party.members[action.target].resetStatus()
            elif spell.target == Target.All:
                self.game.player.party.members[action.source[1]].mp -= spell.manacost
                if spell.type == SpellType.Heal:
                    for member in self.game.player.party.members:
                        if member.hp > 0:
                            self.heal = self.game.player.party.members[action.target].amplify(spell.getHeal())
                            self.checkEffectTiming(action,Timing.DamageDealt)
                            member.hp += self.heal
                        if member.hp > member.getMaxHP():
                            member.hp = member.getMaxHP()
                elif spell.type == SpellType.Buff:
                    self.buff = spell
                    self.duration = 5
                    self.checkEffectTiming(action,Timing.DamageDealt)
                    self.applyBuff(self.buff,-1,action.source)
                elif spell.type == SpellType.Raise:
                    self.heal = spell.getHeal()
                    for member in self.game.player.party.members:
                        self.checkEffectTiming(action,Timing.DamageDealt)
                        if member.hp <= 0:
                            member.hp += self.heal
                        if member.hp > member.getMaxHP():
                            member.hp = member.getMaxHP()
                elif spell.type == SpellType.Cleanse:
                    self.checkEffectTiming(action,Timing.DamageDealt)
                    for member in self.game.player.party.members:
                        if member.hp > 0:
                            member.resetStatus()

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
                self.checkEffectTiming(self.actions[self.exTurn],Timing.PreAttack)
                if self.actions[self.exTurn].action == 0:
                    self.attack(self.actions[self.exTurn])
                elif self.actions[self.exTurn].action >= 200 and self.actions[self.exTurn].action < 300:
                    self.usePotion(self.actions[self.exTurn].target,self.actions[self.exTurn].action)
                elif self.actions[self.exTurn].action >= 300 and self.actions[self.exTurn].action < 400:
                    self.cast(self.actions[self.exTurn])
                elif self.actions[self.exTurn].action >= 400 and self.actions[self.exTurn].action < 500:
                    self.cast(self.actions[self.exTurn])
                elif self.actions[self.exTurn].action >= 500 and self.actions[self.exTurn].action < 600:
                    if self.game.directory.getItem(self.actions[self.exTurn].action).timing == Timing.InTurn:
                        self.talentActionHandler(self.actions[self.exTurn])
                elif self.actions[self.exTurn].action >= 800 and self.actions[self.exTurn].action < 900:
                    self.consumableActionHandler(self.actions[self.exTurn])
                self.tupleToMember(self.actions[self.exTurn].source).tickStatus()
                self.manaspent = False
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
        print(f'Is alive? {source}')
        if source[0]=="Party":
            if self.game.player.party.members[source[1]].hp<=0:
                return False
        if source[0]=="Encounter":
            if self.encounter[source[1]].hp<=0:
                return False
        return True

    def startExecute(self):
        print("Execute!")
        self.checkEffectTiming(None,Timing.Ordering)
        # Sending members with Shocked debuff to back of combat order
        stayList = []
        shockedList = []
        for index in range(len(self.actions)):
            if self.tupleToMember(self.actions[index].source).status == Status.Shocked:
                shockedList.append(self.actions[index])
            else:
                stayList.append(self.actions[index])
        self.actions = stayList + shockedList
        # Applying scheduled mana costs
        for cost in self.scheduledManaCosts:
            self.game.player.party.members[cost[0]].mp -= cost[1]
        self.scheduledManaCosts = []
        print(f'Combat order: {self.combatOrder}')
        self.ex = True
        self.exTurn = 0
        self.timeStart = pygame.time.get_ticks()-2001
        self.state = "execute"
        self.currentTurn = 0

    def endExecute(self):
        for i in range(len(self.combatOrder)):
            if self.isAlive(self.combatOrder[i]) == False and self.combatOrder[i][0] == 'Party':
                self.onDeathEffectHandler(self.combatOrder[i])
        for i in range(len(self.combatOrder)-1,-1,-1):
            if self.isAlive(self.combatOrder[i]) == False:
                self.combatOrder.pop(i)
        if self.risen:
            for index, member in enumerate(self.game.player.party.members):
                found = False
                for i in range(len(self.combatOrder)):
                    if self.tupleToMember(self.combatOrder[i]) == member:
                        found = True
                if found or not member.getHP() > 0:
                    continue
                print(f'{member.name} was found to have been raised! Adding to the combatOrder...')
                for i in range(len(self.combatOrder)):
                    if member.getSpeed() > self.tupleToMember(self.combatOrder[i]).getSpeed():
                        self.combatOrder.insert(i,('Party',index))
                        break
        self.actions.clear()
        self.state = "mainWindow"
        self.ex = False
        self.currentTurn = -1
        self.processBuffs()
        self.processEffects()
        self.upkeep()
        self.next()

    def upkeep(self):
        for member in self.game.player.party.members:
            member.mp += member.getManaRegen()
            if member.mp > member.getMaxMP():
                member.mp = member.getMaxMP()
            member.gainHP(member.getHPRegen())
            if member.status == Status.Ablaze:
                member.takeDamage(math.ceil(member.getMaxHP()*.10))
            if member.status == Status.Freezing:
                member.changeMana(-(math.ceil(member.getMaxMP()*.10)))
        for member in self.encounter:
            if member.status == Status.Ablaze:
                member.takeDamage(math.ceil(member.getMaxHP()*.10))
        for target in self.deathWish:
            self.encounter[target].takeDamage(math.ceil(self.encounter[target].getMaxHP()*.10))

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
        if ptyFlag == False: # Provide last chance to trigger OnDeath effects before loss
            for member in self.combatOrder:
                if member[0] == "Encounter":
                    if self.encounter[member[1]].hp > 0:
                        encFlag = True
                elif member[0] == "Party":
                    self.onDeathEffectHandler(member)
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

    def applyBuff(self,buff,target,source):
        for i in range(len(buff.potency)):
            buff.potency[i] = self.game.player.party.members[source[1]].amplify(buff.potency[i])
        newBuff = Buff(buff.name,buff.potency,self.duration,target)
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

    def applyStatusEffect(self,group,target,spell):
        if (spell.id > 326 and spell.id < 330) or random.randint(1,10) <= 6: # 60% Chance for regular debuffs and AoE debuffs
            if spell.element == Element.Lightning:
                group[target].status = Status.Shocked
                group[target].statusCount = 3
            elif spell.element == Element.Fire:
                group[target].status = Status.Ablaze
                group[target].statusCount = 3
            elif spell.element == Element.Ice:
                group[target].status = Status.Freezing
                group[target].statusCount = 3

    def processEffects(self):
        for i in range(len(self.activeEffects)-1,-1,-1):
            if self.activeEffects[i].tick():
                print(f'{self.game.directory.getItemName(self.activeEffects[i].id)} expired.')
                self.activeEffects.pop(i)

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
        
    def tupleToMember(self,tuple):
        if tuple[0] == "Party":
            return self.game.player.party.members[tuple[1]]
        else:
            return self.encounter[tuple[1]]
        
    def checkElementalEffectiveness(self,source,target):
        if source == target:
            return "Neutral"
        elif source == Element.Lightning:
            if target == Element.Fire:
                return "Vulnerability"
            if target == Element.Ice:
                return "Resistance"
        elif source == Element.Fire:
            if target == Element.Ice:
                return "Vulnerability"
            if target == Element.Lightning:
                return "Resistance"
        elif source == Element.Ice:
            if target == Element.Lightning:
                return "Vulnerability"
            if target == Element.Fire:
                return "Resistance"
        print("ERROR: Elemental Effectiveness Not Found")
        return "Neutral"
        
        
    def checkEffectTiming(self,action,timing):
        for effect in self.activeEffects:
            print(effect.id)
            if self.game.directory.getItemType(effect.id) is Type.Talent:
                talent = self.game.directory.getTalent(effect.id)
                if timing == talent.timing:
                    if talent.type == TalentType.PartyEffect:
                        self.talentPartyTargetEffectHandler(effect,action)
                    elif talent.type == TalentType.EncounterEffect:
                        self.talentEncounterTargetEffectHandler(effect,action)
                    elif talent.timing == Timing.Ordering:
                        self.talentOrderingEffectHandler(effect)
            elif self.game.directory.getItemType(effect.id) is Type.Accessory:
                accessory = self.game.directory.getAccessory(effect.id)
                #print(f'Checking for usage of {accessory.name} at {timing.name}...')
                if timing == accessory.timing:
                    if accessory.type == AccessoryType.Passive:
                        self.accessoryPassiveEffectHandler(effect,action)
                    if accessory.type == AccessoryType.Active:
                        self.accessoryActiveEffectHandler(effect,action)
            elif self.game.directory.getItemType(effect.id) is Type.Consumable:
                print("Consumable effect check...")
                consumable = self.game.directory.getConsumable(effect.id)
                if timing == consumable.timing:
                    self.consumableEffectHandler(effect,action)

    def checkAccessoryEffectTiming(self,action,timing):
        for effect in self.activeEffects:
            if effect.id >= 600 and effect.id < 700:
                accessory = self.game.directory.getAccessory(effect.id)
                #print(f'Checking for usage of {accessory.name} at {timing.name}...')
                if timing == accessory.timing:
                    if accessory.type == AccessoryType.Passive:
                        self.accessoryPassiveEffectHandler(effect,action)
                    if accessory.type == AccessoryType.Active:
                        self.accessoryActiveEffectHandler(effect,action)

    def talentOrderingEffectHandler(self,effect):
        talent = self.game.directory.getTalent(effect.id)
        
        self.scheduledManaCosts.append((effect.source[1],talent.mpcost))

        if talent.name == "Swift Strike":
            print("Swift Strike!")
            for index, action in enumerate(self.actions):
                if action.source == effect.source:
                    temp_action = action
                    self.actions.pop(index)
                    self.actions.insert(0,Action(temp_action.source,temp_action.target,0))

    def talentPartyTargetEffectHandler(self,effect,action):
        talent = self.game.directory.getTalent(effect.id)

        if talent.name == "Fortify": #! Maybe absorb some deflected damage as MP?
            if action.action == 0 and action.target == effect.source[1]:
                self.dmg = round(self.dmg/4)

        elif talent.name == "Breathe": #! Maybe absorb some deflected damage as MP?
            if action.action > 0 and action.target == effect.source[1]:
                self.dmg = round(self.dmg/4)

        elif talent.name == "Enrage":
            if action.source[0] == "Encounter" and random.randint(0,2) < 2:
                print("Enraged!")
                action.target = effect.source[1]

        elif talent.name == "Defend":
            if action.source[0] == "Encounter" and action.target == effect.target:
                print("Defended!")
                action.target = effect.source[1]

        elif talent.name == "Riposte":
            if action.source[0] == "Encounter" and action.target == effect.source[1]:
                self.encounter[action.source[1]].takeDamage(math.ceil(self.dmg*.75))

        elif talent.name == "Hide":
            if action.source[0] == "Encounter" and action.target == effect.source[1]:
                self.miss = True
                self.dmg = 0
                print("Hidden!")

        elif talent.name == "Pray":
            self.immune = True

        elif talent.name == "Guard":
            if action.target == effect.source[1]:
                if self.game.player.party.members[action.source[1]].eqpAcc.name == "Guardian's Belt":
                    self.dmg = round(self.dmg*.2)
                else:
                    self.dmg = round(self.dmg/2)

    def talentEncounterTargetEffectHandler(self,effect,action):
        talent = self.game.directory.getTalent(effect.id)
        if talent.name == "Curse":
            if action.action == 0 and action.target == effect.target:
                print("Cursed!")
                if not self.miss:
                    self.dmg = self.game.player.party.members[action.source[1]].getAttack() - math.ceil(self.encounter[action.target].defense * .70)
                    if self.crit:
                        self.dmg *= 2

    def talentActionHandler(self,action):
        talent = self.game.directory.getTalent(action.action)
        source = action.source
        target = action.target
        
        self.game.player.party.members[source[1]].mp -= talent.mpcost

        if talent.name == "Strike True":
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            self.checkAccessoryEffectTiming(action,Timing.Targeting)
            if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                self.dmg = 0
            else:
                self.dmg = math.ceil((self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense) * .70)
            if self.calculateCrit(self.game.player.party.members[source[1]]):
                print("Crit!")
                self.dmg *= 2
                self.crit = True
            self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
            self.encounter[target].takeDamage(self.dmg)
            self.miss = False

        elif talent.name == "Patch Up":
            self.game.player.party.members[source[1]].gainHP(math.ceil(self.game.player.party.members[source[1]].getMaxHP()*.20))

        elif talent.name == "Meditate":
            self.game.player.party.members[source[1]].gainMP(math.ceil(self.game.player.party.members[source[1]].getMaxMP()*.20))

        elif talent.name == "Wild Swing":
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            self.checkAccessoryEffectTiming(action,Timing.Targeting)
            if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                self.dmg = 0
            else:
                self.dmg = self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense
            randA = random.randint(0,99)
            randB = random.randint(0,99)
            successfulHit = (randA+randB) + (self.encounter[target].getDodge()*2) < ((self.game.player.party.members[source[1]].getAccuracy()-10)*2)
            if successfulHit:
                print("Hit!")
                if self.calculateCrit(self.game.player.party.members[source[1]]):
                    print("Crit!")
                    self.dmg *= 2
                    self.crit = True
                self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
                self.dmg = math.ceil(self.dmg*1.5)
                self.encounter[target].takeDamage(self.dmg)
                self.miss = False
            else:
                print("Miss!")
                self.miss = True

        elif talent.name == "Eviscerate":
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            self.checkAccessoryEffectTiming(action,Timing.Targeting)
            if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                self.dmg = 0
            else:
                self.dmg = self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense
            if self.calculateHit(self.game.player.party.members[source[1]],self.encounter[target]):
                print("Hit!")
                rand = random.randint(0,99)
                if rand < self.game.player.party.members[source[1]].getCritRate() + 15:
                    print("Crit!")
                    self.dmg *= 2
                    self.crit = True
                self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
                self.encounter[target].takeDamage(self.dmg)
                self.miss = False
            else:
                print("Miss!")
                self.miss = True

        elif talent.name == "Pierce":
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            self.checkAccessoryEffectTiming(action,Timing.Targeting)
            if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense/2 < 0:
                self.dmg = 0
            else:
                self.dmg = self.game.player.party.members[source[1]].getAttack() - round(self.encounter[target].defense/2)
            if self.calculateHit(self.game.player.party.members[source[1]],self.encounter[target]):
                print("Hit!")
                if self.calculateCrit(self.game.player.party.members[source[1]]):
                    print("Crit!")
                    self.dmg *= 2
                    self.crit = True
                self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
                self.encounter[target].takeDamage(self.dmg)
                self.miss = False
            else:
                print("Miss!")
                self.miss = True

        elif talent.name == "Swift Strike": # This is handled prior to this point, and is treated as a normal attack
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            self.checkAccessoryEffectTiming(action,Timing.Targeting)
            if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                self.dmg = 0
            else:
                self.dmg = self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense
            if self.calculateHit(self.game.player.party.members[source[1]],self.encounter[target]):
                print("Hit!")
                if self.calculateCrit(self.game.player.party.members[source[1]]):
                    print("Crit!")
                    self.dmg *= 2
                    self.crit = True
                self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
                self.encounter[target].takeDamage(self.dmg)
                self.miss = False
            else:
                print("Miss!")
                self.miss = True

        elif talent.name == "Cleave":
            if self.calculateCrit(self.game.player.party.members[source[1]]):
                self.crit = True
            for tgt in range(len(self.encounter)):
                target = tgt
                if self.isAlive(("Encounter",target)):
                    if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                        self.dmg = 0
                    else:
                        self.dmg = self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense
                    if self.calculateHit(self.game.player.party.members[source[1]],self.encounter[target]):
                        if self.crit:
                            self.dmg *= 2
                        self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
                        self.encounter[target].takeDamage(self.dmg)
                        self.miss = False
                    else:
                        self.miss = True

        elif talent.name == "Heartrend":
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            self.checkAccessoryEffectTiming(action,Timing.Targeting)
            if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                self.dmg = 0
            else:
                self.dmg = self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense
            if self.calculateHit(self.game.player.party.members[source[1]],self.encounter[target]):
                print("Hit!")
                if self.calculateCrit(self.game.player.party.members[source[1]]):
                    print("Crit!")
                    self.dmg *= 2
                    self.crit = True
                self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
                self.encounter[target].takeDamage(self.dmg)
                self.game.player.party.members[source[1]].gainHP(self.dmg)
                self.miss = False
            else:
                print("Miss!")
                self.miss = True

        elif talent.name == "Soulrend":
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            self.checkAccessoryEffectTiming(action,Timing.Targeting)
            if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                self.dmg = 0
            else:
                self.dmg = self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense
            if self.calculateHit(self.game.player.party.members[source[1]],self.encounter[target]):
                print("Hit!")
                if self.calculateCrit(self.game.player.party.members[source[1]]):
                    print("Crit!")
                    self.dmg *= 2
                    self.crit = True
                self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
                self.encounter[target].takeDamage(self.dmg)
                self.game.player.party.members[source[1]].gainMP(self.dmg)
                self.miss = False
            else:
                print("Miss!")
                self.miss = True

        elif talent.name == "Blitz":
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            self.checkAccessoryEffectTiming(action,Timing.Targeting)
            for i in range(2):
                defeated = True
                for enemy in self.encounter:
                    if enemy.hp > 0:
                        defeated = False
                if defeated:
                    break

                if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                    self.dmg = 0
                else:
                    self.dmg = self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense
                if self.calculateHit(self.game.player.party.members[source[1]],self.encounter[target]):
                    print("Hit!")
                    if self.calculateCrit(self.game.player.party.members[source[1]]):
                        print("Crit!")
                        self.dmg *= 2
                        self.crit = True
                    self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
                    self.encounter[target].takeDamage(self.dmg)
                    self.miss = False
                else:
                    print("Miss!")
                    self.miss = True

        elif talent.name == "Havoc":
            for i in range(5):
                defeated = True
                for enemy in self.encounter:
                    if enemy.hp > 0:
                        defeated = False
                if defeated:
                    break
                        
                target = random.randint(0,len(self.encounter)-1)
                target = self.checkRecalculateTarget(source[0],target,"Encounter")
                self.checkAccessoryEffectTiming(action,Timing.Targeting)
                if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                    self.dmg = 0
                else:
                    self.dmg = self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense
                
                if self.calculateHit(self.game.player.party.members[source[1]],self.encounter[target]):
                    print("Hit!")
                    if self.calculateCrit(self.game.player.party.members[source[1]]):
                        print("Crit!")
                        self.dmg *= 2
                        self.crit = True
                    self.dmg = math.ceil(self.dmg/2)
                    self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
                    self.encounter[target].takeDamage(self.dmg)
                    self.miss = False
                else:
                    print("Miss!")
                    self.miss = True

        elif talent.name == "Smite":
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            self.checkAccessoryEffectTiming(action,Timing.Targeting)
            if self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense < 0:
                self.dmg = 0
            else:
                self.dmg = self.game.player.party.members[source[1]].getAttack() - self.encounter[target].defense
            
            if self.calculateHit(self.game.player.party.members[source[1]],self.encounter[target]):
                print("Hit!")
                if self.calculateCrit(self.game.player.party.members[source[1]]):
                    print("Crit!") 
                    self.dmg *= 2
                    self.crit = True
                self.dmg = math.ceil(self.dmg * 1.5)
                self.checkAccessoryEffectTiming(action,Timing.DamageDealt)
                self.encounter[target].takeDamage(self.dmg)
                self.miss = False
            else:
                print("Miss!")
                self.miss = True

        elif talent.name == "Death Wish":
            self.deathWish.append(target)


    def consumableActionHandler(self,action):
        consumable = self.game.directory.getConsumable(action.action)
        source = action.source
        target = action.target
        print(f'Consumable: {consumable.name}')

        if consumable.name == "Fire Arrow" or consumable.name == "Blast Arrow" or consumable.name == "Nova Arrow":
            target = self.checkRecalculateTarget(source[0],target,"Encounter")
            self.encounter[target].takeDamage(consumable.data)

        elif consumable.name == "Fire Bomb" or consumable.name == "Blast Bomb" or consumable.name == "Nova Bomb":
            for enemy in self.encounter:
                enemy.takeDamage(consumable.data)

        elif consumable.name == "Smoke Capsule":
            self.inCombat = False
            self.timeStart = pygame.time.get_ticks()
            self.exTurn = 10
            self.timeStart -= 1000

        elif consumable.name == "Honna Tear":
            if self.game.player.party.members[target].getHP() <= 0:
                self.risen = True
                self.game.player.party.members[target].setHP(round(self.game.player.party.members[target].getMaxHP()/2))
                if self.game.player.party.members[target].getMP() <= round(self.game.player.party.members[target].getMaxHP()/2):
                    self.game.player.party.members[target].setMP(round(self.game.player.party.members[target].getMaxHP()/2))
            else:
                return

        elif consumable.name == "Pyrilic Venom":
            effect = ActiveEffect(consumable.id, source, target, 500)
            self.activeEffects.insert(0,effect)

        elif consumable.name == "Rendai's Veil":
            effect = ActiveEffect(consumable.id, source, target, consumable.data)
            self.activeEffects.insert(0,effect)

        elif consumable.name == "Callaret's Grace":
            effect = ActiveEffect(consumable.id, source, target, consumable.data)
            self.activeEffects.insert(0,effect)

        self.game.player.party.inventory.remove(consumable.id)


    def consumableEffectHandler(self,effect,action):
        consumable = self.game.directory.getConsumable(effect.id)
        target = effect.target

        if consumable.name == "Pyrilic Venom":
            if action.source[1] == effect.target:
                if target not in self.pyrilicVenom:
                    self.pyrilicVenom[target] = 0
                self.pyrilicVenom[target] += consumable.data
                print(f'Venom damage: {self.pyrilicVenom[target]}')
                self.dmg += self.pyrilicVenom[target]

        elif consumable.name == "Rendai's Veil":
            if action.target == effect.target:
                self.dmg = 0

        elif consumable.name == "Callaret's Grace":
            if action.action >= 300 and action.action < 400:
                self.immune = True
                self.dmg = 0


    def accessoryPassiveEffectHandler(self, effect, action):
        accessory = self.game.directory.getAccessory(effect.id)

        if accessory.name == "Ruby Circlet":
            if action.target == effect.source[1] and action.action >= 300 and action.action < 400:
                if self.game.directory.getItem(action.action).type == SpellType.Debuff and self.game.directory.getItem(action.action).element == Element.Fire:
                    print(f'{accessory.name} triggered!')
                    self.immune = True

        elif accessory.name == "Topaz Circlet":
            if action.target == effect.source[1] and action.action >= 300 and action.action < 400:
                if self.game.directory.getItem(action.action).type == SpellType.Debuff and self.game.directory.getItem(action.action).element == Element.Lightning:
                    print(f'{accessory.name} triggered!')
                    self.immune = True

        elif accessory.name == "Sapphire Circlet":
            if action.target == effect.source[1] and action.action >= 300 and action.action < 400:
                if self.game.directory.getItem(action.action).type == SpellType.Debuff and self.game.directory.getItem(action.action).element == Element.Ice:
                    print(f'{accessory.name} triggered!')
                    self.immune = True

        # Guardian's Belt is included in the trigger for the Guard talent

        elif accessory.name == "Broken Pocketwatch":
            if action.source[1] == effect.source[1] and action.action >= 400 and action.action < 500:
                if self.game.directory.getItem(action.action).type == SpellType.Buff: # Buff
                    print(f'{accessory.name} triggered!')
                    self.duration += 2

        elif accessory.name == "Translucent Cowl":
            if action.source[0] == "Encounter" and action.target == effect.source[1]:
                if random.randint(0,2) >= 1:
                    print(f'{accessory.name} triggered!')
                    target = random.randint(0,len(self.game.player.party.members)-1)
                    target = self.checkRecalculateTarget(action.source[0],target,"Party")

        elif accessory.name == "Warlord's Emblem":
            print(f'{accessory.name} triggered!')
            if action.source[0] == "Encounter" and random.randint(0,2) == 2:
                print(f'{accessory.name} successful!')
                action.target = effect.source[1]

        elif accessory.name == "Light Mage's Diadem":
            if action.source[0] == "Encounter" and action.target == effect.source[1]:
                print(f'{accessory.name} triggered!')
                mpLoss = self.dmg
                self.game.player.party.members[effect.source[1]].mp -= mpLoss
                if self.game.player.party.members[effect.source[1]].mp < 0:
                    self.dmg = -(self.game.player.party.members[effect.source[1]].mp)
                    self.game.player.party.members[effect.source[1]].mp = 0
                else:
                    self.dmg = 0

        elif accessory.name == "Warped Sunglasses":
            if action.source[1] == effect.source[1] and action.action >= 300 and action.action < 400:
                print(f'{accessory.name} triggered!')
                action.target = random.randint(0,len(self.encounter)-1)
                action.target = self.checkRecalculateTarget(action.source[0],action.target,"Party")
                self.dmg = math.ceil(self.dmg*1.5)

        elif accessory.name == "Warped Eyeglasses":
            if action.source[1] == effect.source[1] and action.action >= 400 and action.action < 500:
                print(f'{accessory.name} triggered!')
                action.target = random.randint(0,len(self.game.player.party.members)-1)
                action.target = self.checkRecalculateTarget(action.source[0],action.target,"Party")
                spell = self.game.directory.getItem(action.action)
                if spell.type == SpellType.Buff: # Buff
                    for element in self.buff.potency:
                        element = math.ceil(element*1.5)
                if spell.type == SpellType.Heal: # Heal
                    self.heal = math.ceil(self.heal*1.5)

        elif accessory.name == "Enchanted Seedling":
            if action.target == effect.source[1] and action.action >= 400 and action.action < 500:
                if self.game.directory.getItem(action.action).type == SpellType.Buff: # Buff
                    print(f'{accessory.name} triggered!')
                    for i in range(len(self.buff.potency)):
                        self.buff.potency[i] *= 1.5
                        self.buff.potency[i] = math.ceil(self.buff.potency[i])

        elif accessory.name == "Cursed Bracer":
            if action.source == effect.source and action.action == 0:
                print(f'{accessory.name} triggered!')
                self.game.player.party.members[effect.source[1]].eqpAcc.data += 1
                self.dmg += self.game.player.party.members[effect.source[1]].eqpAcc.data

        elif accessory.name == "Cursed Earring":
            if action.source == effect.source and action.action == 0:
                print(f'{accessory.name} triggered!')
                self.dmg += self.game.player.party.members[effect.source[1]].eqpAcc.data
                if random.randint(1,2) == 2:
                    self.game.player.party.members[effect.source[1]].takeDamage(self.game.player.party.members[effect.source[1]].eqpAcc.data)
                

    def accessoryActiveEffectHandler(self, effect, action):
        accessory = self.game.directory.getAccessory(effect.id)
        luck = self.game.player.party.members[effect.source[1]].getLuck()
        chance = random.randint(1,100)

        if accessory.name == "Crimson Scarf":
            if action.source[1] == effect.source[1]:
                if accessory.activationRate + luck >= chance:
                    print(f'{accessory.name} triggered!')
                    self.game.player.party.members[effect.source[1]].gainHP(math.ceil(self.dmg/2))
        
        elif accessory.name == "Cerulean Scarf":
            if action.source[1] == effect.source[1]:
                if accessory.activationRate + luck >= chance:
                    print(f'{accessory.name} triggered!')
                    self.game.player.party.members[effect.source[1]].gainMP(math.ceil(self.dmg/2))

        elif accessory.name == "Jade Bracer":
            if action.target == effect.source[1] and action.action == 0:
                if accessory.activationRate + luck >= chance:
                    print(f'{accessory.name} triggered!')
                    self.dmg = round(self.dmg/2)

        elif accessory.name == "Bismuth Amulet":
            print("Bismuth!")
            if action.target == effect.source[1] and action.action != 0:
                if accessory.activationRate + luck >= chance:
                    print(f'{accessory.name} triggered!')
                    self.dmg = 0
                    
        elif accessory.name == "Opal Circlet":
            if action.target == effect.source[1] and action.action >= 300 and action.action < 400:
                if self.game.directory.getItem(action.action).type == SpellType.Debuff:
                    if accessory.activationRate + luck >= chance:
                        print(f'{accessory.name} triggered!')
                        self.immune = True

        elif accessory.name == "Magician's Tome":
            if action.source == effect.source and action.action >= 300 and action.action < 500:
                if accessory.activationRate + luck >= chance and not self.manaspent:
                    print(f'{accessory.name} triggered!')
                    self.manaspent = True
                    self.game.player.party.members[effect.source[1]].gainMP(self.game.directory.getManaCost(action.action))

        elif accessory.name == "Master's Tome":
            if action.source == effect.source and action.action >= 500 and action.action < 600:
                if accessory.activationRate + luck >= chance and not self.manaspent:
                    print(f'{accessory.name} triggered!')
                    self.manaspent = True
                    self.game.player.party.members[effect.source[1]].gainMP(self.game.directory.getManaCost(action.action))

        elif accessory.name == "Blitzing Boots":
            if action.source == effect.source and action.action == 0:
                if accessory.activationRate + luck >= chance:
                    print(f'{accessory.name} triggered!')
                    self.attack(action)

        elif accessory.name == "Whirlwind Cape":
            if action.source == effect.source and action.action == 0:
                if accessory.activationRate + luck >= chance:
                    print(f'{accessory.name} triggered!')
                    self.hitAll = True

        elif accessory.name == "Plasma Ring":
            if action.source == effect.source and action.action >= 300 and action.action < 500:
                if accessory.activationRate + luck >= chance:
                    print(f'{accessory.name} triggered!')
                    spell = self.game.directory.getItem(action.action)
                    if spell.type == SpellType.Attack: # Attack
                        self.dmg *= 2
                    if spell.type == SpellType.Buff: # Buff
                        for element in self.buff.potency:
                            element *= 2
                    if spell.type == SpellType.Heal: # Heal
                        self.heal *= 2

        elif accessory.name == "Ivory Mirror":
            if action.source[0] == "Encounter" and action.target == effect.source[1]:
                if accessory.activationRate + luck >= chance:
                    print(f'{accessory.name} triggered!')
                    self.encounter[action.source[1]].takeDamage(self.dmg)

        elif accessory.name == "Miracle Bracelet":
            if action.source[0] == "Encounter" and action.target == effect.source[1]:
                if self.game.player.party.members[effect.source[1]].getHP() - self.dmg <= 0:
                    if accessory.activationRate + luck >= chance:
                        print(f'{accessory.name} triggered!')
                        self.dmg = self.game.player.party.members[effect.source[1]].getHP() - 1


    def onDeathEffectHandler(self, member):
        # Second Soul
        for item in self.game.player.party.inventory:
            if self.game.directory.getItemName(item) == "Second Soul":
                print("The Second Soul bursts from its jar!")
                self.game.player.party.members[member[1]].fullRestore()
                self.game.player.party.inventory.remove(item)
                break

    def checkCursedItems(self,character):
        if character.eqpAcc.name == "Cursed Bracer":
            character.takeDamage(character.eqpAcc.data)
            character.eqpAcc.data = 0
        elif character.eqpAcc.name == "Cursed Earring":
            character.eqpAcc.data += 1
