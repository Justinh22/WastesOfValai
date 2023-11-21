import pygame

def write(game,size,x,y,text):
    font = pygame.font.Font('freesansbold.ttf',size)
    text_surface = font.render(text, True, game.white)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x,y)
    game.screen.blit(text_surface,text_rect)
    return font.size(text)

def writeOrientation(game,size,x,y,text,orn):
    font = pygame.font.Font('freesansbold.ttf',size)
    text_surface = font.render(text, True, game.white)
    text_rect = text_surface.get_rect()
    if orn == "L":
        text_rect.topleft = (x,y)
    elif orn == "R":
        text_rect.topright = (x,y)
    game.screen.blit(text_surface,text_rect)
    return font.size(text)

def wrapWrite(game,size,text,xBound,x=20,y=25):
    font = pygame.font.Font('freesansbold.ttf',size)
    textList = wrap(font,text,xBound)
    for i in range(0,len(textList)):
        text_surface = font.render(textList[i], True, game.white)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y+((size+5)*i))
        game.screen.blit(text_surface,text_rect)
    return font.size(text)

def wrap(font,text,windowsize):
    fullText = [text]
    if font.size(text)[0] > windowsize:
        fullText.clear()
        listText = text.split()
        lineList = []
        for word in listText:
            lineList.append(word)
            line = ' '.join(lineList)
            if font.size(line)[0] > windowsize:
                lastWord = lineList[-1]
                lineList.pop(-1)
                line = ' '.join(lineList)
                fullText.append(line)
                lineList.clear()
                lineList.append(lastWord)
                line = ' '.join(lineList)
        fullText.append(line)
    return fullText