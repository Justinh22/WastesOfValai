import random

def pickLevels(level):
    encounterLevels = []
    picker = random.randint(0,1)
    if level == 1:
        encounterLevels = [1]
    elif level == 2:
        if picker == 0:
            encounterLevels = [2]
        else:
            encounterLevels = [1,1]
    elif level == 3:
        if picker == 0:
            encounterLevels = [2,1]
        else:
            encounterLevels = [1,1,1,1]
    elif level == 4:
        if picker == 0:
            encounterLevels = [2,2]
        else:
            encounterLevels = [2,1,1,1]
    elif level == 5:
        if picker == 0:
            encounterLevels = [5]
        else:
            encounterLevels = [2,2,2]
    elif level == 6:
        if picker == 0:
            encounterLevels = [5,2]
        else:
            encounterLevels = [2,2,2,2]
    elif level == 7:
        encounterLevels = [5,2,2]
    elif level == 8:
        if picker == 0:
            encounterLevels = [8]
        else:
            encounterLevels = [5,5]
    elif level == 9:
        if picker == 0:
            encounterLevels = [8,2,2]
        else:
            encounterLevels = [5,5,2,2]
    elif level == 10:
        if picker == 0:
            encounterLevels = [8,5]
        else:
            encounterLevels = [10]
    elif level == 11:
        if picker == 0:
            encounterLevels = [8,5,5]
        else:
            encounterLevels = [10,5]
    elif level == 12:
        if picker == 0:
            encounterLevels = [12]
        else:
            encounterLevels = [8,8]
    elif level == 13:
        if picker == 0:
            encounterLevels = [12,5,5]
        else:
            encounterLevels = [10,8]
    elif level == 14:
        if picker == 0:
            encounterLevels = [10,10]
        else:
            encounterLevels = [12,5,5,5]
    elif level == 15:
        if picker == 0:
            encounterLevels = [10,8,8]
        else:
            encounterLevels = [15]
    elif level == 16:
        if picker == 0:
            encounterLevels = [12,10,10]
        else:
            encounterLevels = [15,8,8,8]
    elif level == 17:
        if picker == 0:
            encounterLevels = [15,12]
        else:
            encounterLevels = [12,12,12]
    elif level == 18:
        if picker == 0:
            encounterLevels = [15,15,12]
        else:
            encounterLevels = [18]
    elif level == 19:
        if picker == 0:
            encounterLevels = [18,12,12,12]
        else:
            encounterLevels = [15,15,15]
    elif level == 20:
        if picker == 0:
            encounterLevels = [18,15,12,10]
        else:
            encounterLevels = [20]
    # BENEATH THIS POINT, THESE ENCOUNTERS ARE UNUSED NOW
    elif level == 21:
        encounterLevels = [15,2,2,2]
    elif level == 22:
        if picker == 0:
            encounterLevels = [12,10]
        else:
            encounterLevels = [15,5,2]
    elif level == 23:
        encounterLevels = [15,8]
    elif level == 24:
        if picker == 0:
            encounterLevels = [12,12]
        else:
            encounterLevels = [8,8,8]
    elif level == 25:
        if picker == 0:
            encounterLevels = [15,10]
        else:
            encounterLevels = [20,5]
    elif level == 26:
        encounterLevels = [10,8,8]
    elif level == 27:
        encounterLevels = [15,12]
    elif level == 28:
        if picker == 0:
            encounterLevels = [18,10]
        else:
            encounterLevels = [12,12,2,2]
    elif level == 29:
        if picker == 0:
            encounterLevels = [12,12,5]
        else:
            encounterLevels = [20,5,2,2]
    elif level == 30:
        picker = random.randint(0,2)
        if picker == 0:
            encounterLevels = [15,15]
        elif picker == 1:
            encounterLevels = [20,10]
        else:
            encounterLevels = [10,10,10]
    elif level == 31:
        encounterLevels = [12,12,5,2]
    elif level == 32:
        if picker == 0:
            encounterLevels = [12,10,10]
        else:
            encounterLevels = [20,12]
    elif level == 33:
        if picker == 0:
            encounterLevels = [18,15]
        else:
            encounterLevels = [20,8,5]
    elif level == 34:
        if picker == 0:
            encounterLevels = [18,8,8]
        else:
            encounterLevels = [12,12,10]
    elif level == 35:
        if picker == 0:
            encounterLevels = [20,15]
        else:
            encounterLevels = [15,10,10]
    elif level == 36:
        picker = random.randint(0,2)
        if picker == 0:
            encounterLevels = [12,12,12]
        elif picker == 1:
            encounterLevels = [20,8,8]
        else:
            encounterLevels = [18,18]
    elif level == 37:
        if picker == 0:
            encounterLevels = [15,12,10]
        else:
            encounterLevels = [20,12,5]
    elif level == 38:
        if picker == 0:
            encounterLevels = [20,18]
        else:
            encounterLevels = [15,15,8]
    elif level == 39:
        encounterLevels = [15,12,12]
    elif level == 40:
        picker = random.randint(0,2)
        if picker == 0:
            encounterLevels = [20,20]
        elif picker == 1:
            encounterLevels = [20,10,10]
        else:
            encounterLevels = [15,15,10]
    return encounterLevels
