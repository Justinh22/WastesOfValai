import json

def getDebug(typ):
    with open('debug.json') as readfile:
        debugdata = json.load(readfile)
        if typ == 0:
            return debugdata['StartLevel']
        if typ == 1:
            return debugdata['StartClass']
        if typ == 2:
            return debugdata['ManualEncounters']
        if typ == 3:
            return debugdata['ManualLevelUp']
        if typ == 4:
            return debugdata['StartingItems']
        if typ == 5:
            return debugdata['StartingZone']

