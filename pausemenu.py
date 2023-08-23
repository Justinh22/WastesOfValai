import pygame

class PauseMenu():
    def __init__(self,game):
        self.game = game
        self.currentPos = list(self.game.WorldMap.startingPos)
        self.paused = False
        self.state = "main"
        self.left = 10
        self.top = 10
        self.right = self.game.width - 20
        self.bottom = self.game.height - 20
        self.font = pygame.font.Font('freesansbold.ttf',20)

    def blitScreen(self):
        self.game.screen.blit(self.game.screen, (0,0))
        pygame.display.update()
        self.game.buttonReset()

    def display(self):
        self.game.screen.fill(self.game.black)
        self.state = "main"
        self.drawScreen()
        while self.paused:
            self.game.eventHandler()
            self.getInput()
            self.drawScreen()
            self.blitScreen()
        self.game.screen.fill(self.game.black)
        self.blitScreen()

    def pause(self):
        self.paused = True
        self.display()

    def drawScreen(self):
        screenOutline = pygame.Rect(self.left,self.top,self.right,self.bottom)
        pygame.draw.rect(self.game.screen,self.game.white,screenOutline,2)

    def getInput(self):
        if self.game.A:
            print('A')
        if self.game.B:
            print('B')
        if self.game.X:
            print('X')
        if self.game.Y:
            print('Y')

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
