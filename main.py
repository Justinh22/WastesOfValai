from game import *
from mapgenerator import *

WoV = Game()
pygame_icon = pygame.image.load('desert.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('Wastes of Valai')

while WoV.running:
    WoV.mainmenu.display()
    WoV.run()