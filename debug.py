import json

def getDebug(typ):
    with open('debug.json') as readfile:
        debugdata = json.load(readfile)
        if typ == 0:
            return debugdata['StartLevel']
        if typ == 1:
            return debugdata['StartClass']

