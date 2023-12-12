from directory import *
from utility import *
from constants import *
from writing import *
from pausemenu import *
import playerdata

class CharacterSwap():
    def __init__(self,game,newChar,inHostel=False):
        self.game = game
        self.inMenu = True
        self.cursorPos = 0
        self.newChar = newChar
        self.inHostel = inHostel
        self.left = 10
        self.top = 10
        self.right = self.game.width - 20
        self.bottom = self.game.height - 20
        self.pausemenu = PauseMenu(self.game)
        self.delay = 5
        self.display()

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
            self.cursorPos -= 1
            self.cursorPos %= 4
        if self.game.DOWN:
            self.cursorPos += 1
            self.cursorPos %= 4
        if self.game.A:
            print("A")
            self.game.player.hostel.append(self.game.player.party.members[self.cursorPos])
            self.game.player.party.members.pop(self.cursorPos)
            self.game.player.party.members.append(self.newChar)
            self.inMenu = False
        if self.game.B:
            print("B")
            self.game.player.hostel.append(self.newChar)
            self.inMenu = False
        if self.game.X:
            print("X")
        if self.game.Y:
            print("Y")
        if self.game.START:
            self.pausemenu.pause(self.game.player.currentPos)

    def drawScreen(self):
        self.game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)

        xPos, yPos = 250, 45
        outlineRect = pygame.Rect(xPos,yPos+450,350,90)
        pygame.draw.rect(self.game.screen,self.game.white,outlineRect,2)
        self.drawMinStatBlock(xPos,yPos,self.newChar)
        if not self.inHostel:
            write(self.game, 18, 25, 225, f'Choose someone to send to the hostel. Press (B) to send {self.newChar.name}.')
        else:
            write(self.game, 18, 25, 225, f'Choose someone to swap with {self.newChar.name}.')
        for i in range(0,len(self.game.player.party.members)):
            self.drawCharacterNameBlock(xPos-210, yPos + 240 + (i*40), self.game.player.party.members[i])
        write(self.game, 15, xPos+50, yPos + 247 + (self.cursorPos*40), "<-")
        
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

    def drawCharacterNameBlock(self,xPos,yPos,character):
        outlineRect = pygame.Rect(xPos,yPos,250,33)
        pygame.draw.rect(self.game.screen,self.game.white,outlineRect,2)
        write(self.game, 14, xPos+10, yPos+10, character.name + ", Level " + str(character.level) + " " + character.type.name)

    def intToRating(self,val):
        ret = ""
        for i in range(val):
            ret += "+"
        return ret
    

class Hostel():
    def __init__(self,game):
        self.game = game
        self.inMenu = True
        self.cursorPos = 0
        self.listTop = 0
        self.listBottom = 7
        self.left = 10
        self.top = 10
        self.right = self.game.width - 20
        self.bottom = self.game.height - 20
        self.pausemenu = PauseMenu(self.game)
        self.delay = 5
        self.display()

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
            self.cursorPos -= 1
            self.cursorPos %= len(self.game.player.hostel)
            if self.cursorPos < self.listTop:
                self.listTop -= 1
                self.listBottom -= 1
            if self.cursorPos >= self.listBottom:
                self.listBottom = self.cursorPos + 1
                self.listTop = self.listBottom - 7
        if self.game.DOWN:
            self.cursorPos += 1
            self.cursorPos %= len(self.game.player.hostel)
            if self.cursorPos < self.listTop:
                self.listTop = 0
                self.listBottom = 7
            if self.cursorPos >= self.listBottom:
                self.listBottom += 1
                self.listTop += 1
        if self.game.A:
            print("A")
            CharacterSwap(self.game, self.game.player.hostel[self.cursorPos], True)
            self.game.player.hostel.pop(self.cursorPos)
        if self.game.B:
            print("B")
            self.inMenu = False
        if self.game.X:
            print("X")
        if self.game.Y:
            print("Y")
        if self.game.START:
            self.pausemenu.pause(self.game.player.currentPos)

    def drawScreen(self):
        self.game.screen.fill((0,0,0))
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)

        xPos, yPos = 60, 100
        listEnd = len(self.game.player.hostel) if len(self.game.player.hostel) < self.listBottom else self.listBottom
        outlineRect = pygame.Rect(xPos,yPos+450,350,90)
        pygame.draw.rect(self.game.screen,self.game.white,outlineRect,2)
        write(self.game, 40, 30, 40, "Hostel")
        for i in range(self.listTop,listEnd):
            if i == self.cursorPos:
                self.drawMinStatBlock(xPos, yPos + ((i-self.listTop)*40), self.game.player.hostel[i])
            else:
                self.drawCharacterNameBlock(xPos, yPos + ((i-self.listTop)*40 + (0 if (i-self.listTop) <= (self.cursorPos-self.listTop) else 55)), self.game.player.hostel[i])
        write(self.game, 15, xPos-40, yPos + ((self.cursorPos-self.listTop)*40), "->")

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

    def drawCharacterNameBlock(self,xPos,yPos,character):
        outlineRect = pygame.Rect(xPos,yPos,250,33)
        pygame.draw.rect(self.game.screen,self.game.white,outlineRect,2)
        write(self.game, 14, xPos+10, yPos+10, character.name + ", Level " + str(character.level) + " " + character.type.name)

    def intToRating(self,val):
        ret = ""
        for i in range(val):
            ret += "+"
        return ret
    

#class LevelUp():

#class ItemReplace():

#class SpellReplace():

#class Message():