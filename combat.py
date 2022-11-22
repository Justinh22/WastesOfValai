import pygame
import random
import time
from characters import Action

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
        self.party = []
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
        self.lowMana = False
        self.buffs = []

    def initialize(self,party,encounter):
        self.party = party
        for i in range(0,len(self.party)):
            print(f'{self.party[i].name}, {self.party[i].type.name}, {self.party[i].level} (ID {self.party[i].id}) - HP: {self.party[i].hpMax}, MP: {self.party[i].mpMax}, ATK: {self.party[i].attack}, CRT: {self.party[i].critrate}, DEF: {self.party[i].defense}, DDG: {self.party[i].dodge}, LCK: {self.party[i].luck}, SPD: {self.party[i].speed}, SPELLS: {self.party[i].spells}')
        self.encounter = encounter
        for i in range(0,len(self.encounter)):
            print(f'{self.encounter[i].name}, {self.encounter[i].level} - SPD: {self.encounter[i].speed}')

        self.combatOrder = []
        members = self.party + self.encounter
        members.sort(key=lambda x: x.speed)
        members.reverse()
        seenPty = [0] * len(self.party)
        seenEnc = [0] * len(self.encounter)
        for entry in members:
            for i in range(len(self.party)):
                if entry.id == self.party[i].id:
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
                break;
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
                    self.state = "useMenu"
                    print("ITEM")
                elif self.cursorPos == 2:
                    self.state = "useMenu"
                    print("ART")
                elif self.cursorPos == 3:
                    self.state = "mainWindow"
                    print("CANCEL")
            elif self.state == "targetSelect":
                self.state = "mainWindow"
                self.actions.append(Action(self.combatOrder[self.currentTurn],self.cursorPos,self.actionVal))
                self.next()
                self.cursorPos = -1
                print("TARGET")
            elif self.state == "spellList":
                if self.cursorPos < len(self.party[self.combatOrder[self.currentTurn][1]].spells):
                    if self.validManaCost(self.party[self.combatOrder[self.currentTurn][1]],self.party[self.combatOrder[self.currentTurn][1]].spells[self.cursorPos+self.menuTop]):
                        self.lowMana = False
                        self.actionVal = self.party[self.combatOrder[self.currentTurn][1]].spells[self.cursorPos+self.menuTop]
                        if self.game.directory.getSpellTarget(self.actionVal) == "Single":
                            self.state = "targetSelect"
                            self.cursorPos = 0
                        else:
                            self.state = "mainWindow"
                            self.actions.append(Action(self.combatOrder[self.currentTurn],0,self.actionVal))
                            self.next()
                            self.cursorPos = -1
                        print("SPELL")
                    else:
                        self.lowMana = True
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
            elif self.state == "spellList":
                if self.cursorPos == 0 or self.cursorPos == 1:
                    if self.menuTop > 0:
                        self.menuTop -= 2
                else:
                    self.cursorPos -= 2
        if self.game.DOWN:
            if self.state == "targetSelect" and self.cursorPos < len(self.encounter)-1:
                self.cursorPos += 1
            elif self.state == "spellList":
                if self.cursorPos == 2 or self.cursorPos == 3:
                    if self.menuTop+5 < len(self.party[self.combatOrder[self.currentTurn][1]].spells):
                        self.menuTop += 2
                else:
                    self.cursorPos += 2
        if self.game.LEFT:
            if self.state == "spellList":
                if self.cursorPos == 1 or self.cursorPos == 3:
                    self.cursorPos -= 1
            elif self.state == "useMenu":
                if self.cursorPos > 0:
                    self.cursorPos -= 1
        if self.game.RIGHT:
            if self.state == "spellList":
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
            self.write(20, self.left+15, 325, self.party[self.combatOrder[self.currentTurn][1]].name+"'s turn!")
            self.write(20,30,400,"A) ATTACK")
            self.write(20,180,400,"B) USE") #SPELL, ITEM, COMBAT ART
            self.write(20,330,400,"X) CANCEL")
            self.write(20,480,400,"Y) RUN")
        if self.state == "useMenu":
            self.write(20, self.left+15, 325, "Use what?")
            self.write(20, 20+(self.cursorPos*150), 398, ">")
            self.write(20,50,400,"SPELL")
            self.write(15,60,425,str(self.party[self.combatOrder[self.currentTurn][1]].mp)+"/"+str(self.party[self.combatOrder[self.currentTurn][1]].mpMax))
            self.write(20,200,400,"ITEM")
            self.write(20,350,400,"ART")
            self.write(20,500,400,"CANCEL")
        if self.state == "targetSelect":
            self.write(20, self.left+15, 325, "Select a target")
            self.write(20, 450, 30+(self.cursorPos*30), "<")
            self.write(20,30,400,"A) SELECT")
            self.write(20,180,400,"B) BACK")
        if self.state == "spellList":
            if self.lowMana:
                self.write(20, self.left+15, 325, "You don't have enough mana to cast that.")
            else:
                self.write(20, self.left+15, 325, "Select a spell: (B to cancel)")
            self.write(20, 40+((self.cursorPos%2)*300), 380+((int(self.cursorPos/2))*40), ">")
            if self.menuTop < len(self.party[self.combatOrder[self.currentTurn][1]].spells):
                self.write(20,60,380,str(self.menuTop+1)+") "+self.game.directory.getItemName(self.party[self.combatOrder[self.currentTurn][1]].spells[self.menuTop]))
            else:
                self.write(20,60,380,str(self.menuTop+1)+")")
            if self.menuTop+1 < len(self.party[self.combatOrder[self.currentTurn][1]].spells):
                self.write(20,360,380,str(self.menuTop+2)+") "+self.game.directory.getItemName(self.party[self.combatOrder[self.currentTurn][1]].spells[self.menuTop+1]))
            else:
                self.write(20,360,380,str(self.menuTop+2)+")")
            if self.menuTop+2 < len(self.party[self.combatOrder[self.currentTurn][1]].spells):
                self.write(20,60,420,str(self.menuTop+3)+") "+self.game.directory.getItemName(self.party[self.combatOrder[self.currentTurn][1]].spells[self.menuTop+2]))
            else:
                self.write(20,60,420,str(self.menuTop+3)+")")
            if self.menuTop+3 < len(self.party[self.combatOrder[self.currentTurn][1]].spells):
                self.write(20,360,420,str(self.menuTop+4)+") "+self.game.directory.getItemName(self.party[self.combatOrder[self.currentTurn][1]].spells[self.menuTop+3]))
            else:
                self.write(20,360,420,str(self.menuTop+4)+")")

        #if self.state == "itemList":

        #if self.state == "combatArtList":

        if self.state == "execute":
            combatStr = ""
            if self.actions[self.exTurn-1].action == 0:
                if self.actions[self.exTurn-1].source[0] == "Encounter":
                    combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " attacks " + self.party[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
                else:
                    combatStr = self.party[self.actions[self.exTurn-1].source[1]].name + " attacks " + self.encounter[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
            elif self.actions[self.exTurn-1].action >= 300 and self.actions[self.exTurn-1].action < 400:
                if self.actions[self.exTurn-1].source[0] == "Encounter":
                    if self.game.directory.getAtkSpell(self.actions[self.exTurn-1].action).target == "Single":
                        combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " at " + self.party[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
                    else:
                        combatStr = self.encounter[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " for " + str(self.dmg) + " damage!"
                else:
                    if self.game.directory.getAtkSpell(self.actions[self.exTurn-1].action).target == "Single":
                        combatStr = self.party[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " at " + self.encounter[self.actions[self.exTurn-1].target].name + " for " + str(self.dmg) + " damage!"
                    else:
                        combatStr = self.party[self.actions[self.exTurn-1].source[1]].name + " casts " + self.game.directory.getItemName(self.actions[self.exTurn-1].action) + " for " + str(self.dmg) + " damage!"
            self.write(20, self.left+15, 325, combatStr)

        if self.state == "win":
            self.write(20, self.left+15, 325, "You win!")
            if pygame.time.get_ticks() - self.timeStart >= 3000:
                self.inCombat = False

        if self.state == "lose":
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
        for i in range(0,len(self.party)):
            textWidth, textHeight = self.font.size(self.party[i].name)
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
        for i in range(0,len(self.party)):
            offset = 30*i
            textWidth, textHeight = self.font.size(self.party[i].name)
            self.write(20, self.right-textWidth-20, 170+offset, self.party[i].name)
            partyHPRect = pygame.Rect(self.right-maxPtyWidth-140,170+offset,(self.party[i].hp/self.party[i].hpMax)*100,10)
            partyMPRect = pygame.Rect(self.right-maxPtyWidth-140,180+offset,(self.party[i].mp/self.party[i].mpMax)*100,10)
            outlineRect = pygame.Rect(self.right-maxPtyWidth-140,170+offset,100,20)
            pygame.draw.rect(self.game.screen,self.game.white,partyHPRect)
            pygame.draw.rect(self.game.screen,self.game.white,partyMPRect)
            pygame.draw.rect(self.game.screen,self.game.white,outlineRect,1)
            self.write(20, self.right-maxPtyWidth-220, 170+offset, str(self.party[i].hp)+"/"+str(self.party[i].hpMax))
        #Setting border
        pygame.draw.line(self.game.screen,self.game.white,(self.left,320),(self.right+9,320),2)
        pygame.draw.line(self.game.screen,self.game.white,(self.left,350),(self.right+9,350),2)

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
            #print(self.party[self.combatOrder[self.currentTurn][1]].name)

    def enemyAction(self,source):
        if not self.isAlive(source):
            self.actions.append(Action(source,0,-1))
            return
        target = random.randint(0,len(self.party)-1)
        timeout = 0
        while self.party[target].hp <= 0 and timeout < 20:
            target = random.randint(0,len(self.party)-1)
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
            if self.encounter[source[1]].attack - self.party[target].getDefense() < 0:
                self.dmg = 0
            else:
                self.dmg = self.encounter[source[1]].attack - self.party[target].getDefense()
            self.party[target].takeDamage(self.dmg)
        if source[0] == "Party":
            if self.party[source[1]].getAttack() - self.encounter[target].defense < 0:
                self.dmg = 0
            else:
                self.dmg = self.party[source[1]].getAttack() - self.encounter[target].defense
            self.encounter[target].takeDamage(self.dmg)

    def cast(self,source,target,spellID):
        if spellID < 400:
            spell = self.game.directory.getAtkSpell(spellID)
            if spell.target == "Single":
                if source[0] == "Encounter":
                    self.dmg = self.party[target].takeDamage(spell.attack)
                else:
                    self.dmg = spell.attack
                    if spell.type == self.encounter[target].resistance:
                        self.dmg = int(self.dmg/2)
                    self.encounter[target].takeDamage(self.dmg)
                    self.party[source[1]].mp -= spell.manacost
            else:
                if source[0] == "Encounter":
                    for member in self.party:
                        self.dmg = member.takeDamage(spell.attack)
                else:
                    for member in self.encounter:
                        self.dmg = spell.attack
                        if spell.type == member.resistance:
                            self.dmg = int(self.dmg/2)
                        member.takeDamage(self.dmg)
                    self.dmg = spell.attack
                    self.party[source[1]].mp -= spell.manacost

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
                elif self.actions[self.exTurn].action >= 300 and self.actions[self.exTurn].action < 400:
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
            if self.party[source[1]].hp<=0:
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
        self.next()

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

    def applyBuff(self,buff):
        self.buffs.append(buff):
        if bf.target == -1:
            for member in self.party:
                member.addBuffs(buff)
        else:
            self.party[i].addBuffs(buff)

    def processBuffs(self):
        for member in self.party:
            member.resetBuffs()
        for bf in self.buffs:
            if bf.target == -1:
                for member in self.party:
                    member.addBuffs(bf.buff)
            else:
                self.party[i].addBuffs(bf.buff)
            bf.tick()
        for i in range(len(self.buffs)-1,-1,-1):
            if self.buffs[i].checkExpiry():
                self.buffs.pop(i)
