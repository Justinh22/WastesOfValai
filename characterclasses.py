import pygame;
import random;
from items import *

class Character():
    charNum = 100
    def __init__(self,nm,lv,tp):
        self.name = nm
        self.level = lv
        Character.charNum += 1
        self.id = Character.charNum
        self.xp = 0
        self.nextLevel = 20*lv
        self.type = tp
        self.spells = []
        for i in range(self.level):
            if self.type.knownSpells[i] >= 0:
                self.spells.append(self.type.knownSpells[i])
        self.eqpWpn = Weapon();
        self.eqpAmr = Armor();
        self.hpMax = 20
        self.mpMax = 20
        self.attack = 0
        self.critrate = 0
        self.defense = 0
        self.dodge = 0
        self.luck = 0
        self.speed = 0
        for i in range(0,lv):
            growth = tp.getGrowths()
            self.hpMax += growth[0]
            self.mpMax += growth[1]
            self.attack += growth[2]
            self.critrate += growth[3]
            self.defense += growth[4]
            self.dodge += growth[5]
            self.luck += growth[6]
            self.speed += growth[7]
        self.hp = self.hpMax
        self.mp = self.mpMax
        self.accuracy = 70
        self.amplifier = 0
        self.manaregen = 0
        self.buffs = [0,0,0,0,0,0,0]
    def getAttack(self):
        return self.eqpWpn.attack + self.attack
    def getDefense(self):
        return self.eqpAmr.defense + self.defense
    def getCritRate(self):
        return self.eqpWpn.critrate + self.critrate
    def getDodge(self):
        return self.eqpAmr.dodge + self.dodge
    def getSpeed(self):
        return self.speed
    def takeDamage(self,val):
        print(f'{self.name} took {val} damage!')
        if val > self.hp:
            self.hp = 0
        else:
            self.hp -= val
        return val
    def buffUp(self,type,val):
        if type == "ATK":
            self.buffs[0] += val
        elif type == "ACC":
            self.buffs[1] += val
        elif type == "CRT":
            self.buffs[2] += val
        elif type == "DEF":
            self.buffs[3] += val
        elif type == "DDG":
            self.buffs[4] += val
        elif type == "LCK":
            self.buffs[5] += val
        elif type == "HP":
            self.buffs[6] += val
    def addBuffs(self,buff):
        for i in range(len(self.buffs)):
            self.buffs[i] += buff[i]
    def getBuff(self,type):
        if type == "ATK":
            return self.buffs[0]
        elif type == "ACC":
            return self.buffs[1]
        elif type == "CRT":
            return self.buffs[2]
        elif type == "DEF":
            return self.buffs[3]
        elif type == "DDG":
            return self.buffs[4]
        elif type == "LCK":
            return self.buffs[5]
        elif type == "HP":
            return self.buffs[6]
    def resetBuffs(self):
        self.buffs = [0,0,0,0,0,0,0]


class ClassType():
    def __init__(self,nm,wpnPrf,amrPrf,atkLv,sptLv,hpg,mpg,atg,ctg,dfg,dgg,lkg,sdg,splsLrn,idIN):
        self.name = nm
        self.weaponProficiency = wpnPrf # [AXE,SWORD,SPEAR,DAGGER,STAFF]
        self.armorProficiency = amrPrf # [LIGHT,MEDIUIM,HEAVY,ROBE,ARCANIST]
        self.attackMagicLevel = atkLv
        self.supportMagicLevel = sptLv
        self.hpGrowth = hpg
        self.mpGrowth = mpg
        self.atkGrowth = atg
        self.crtGrowth = ctg
        self.defGrowth = dfg
        self.ddgGrowth = dgg
        self.lckGrowth = lkg
        self.spdGrowth = sdg
        self.knownSpells = splsLrn
        self.id = idIN
    def getGrowths(self):
        return [self.hpGrowth[random.randint(0,2)], self.mpGrowth[random.randint(0,2)], self.atkGrowth[random.randint(0,2)], self.crtGrowth[random.randint(0,2)], self.defGrowth[random.randint(0,2)], self.ddgGrowth[random.randint(0,2)], self.lckGrowth[random.randint(0,2)], self.spdGrowth[random.randint(0,2)]]

class Party():
    def __init__(self):
        self.members = []

class Creature():
    def __init__(self,nm,lv,idIN,hpIN,at,ac,df,dg,sd,res,type,spells):
        self.name = nm
        self.level = lv
        self.id = idIN
        self.hpMax = hpIN
        self.hp = hpIN
        self.attack = at
        self.accuracy = ac
        self.defense = df
        self.dodge = dg
        self.speed = sd
        self.resistance = res
        self.biomeType = type
        self.knownSpells = spells
        self.spellCooldown = 0
    def takeDamage(self,val):
        print(f'{self.name} took {val} damage!')
        if val > self.hp:
            self.hp = 0
        else:
            self.hp -= val
        return val

class Encounter():
    def __init__(self):
        self.members = []

class Action():
    def __init__(self,src,tgt,act):
        self.source = src
        self.target = tgt
        self.action = act # 0 = ATTACK, 1 = GUARD, ID = SPELL, ID = ART, ID = ITEM

class Buff():
    def __init__(self,nme,buf,dur,tgt):
        self.name = nme
        self.duration = dur
        self.buff = buf
        self.target = tgt
    def tick(self):
        self.duration -= 1
        self.checkExpiry()
    def checkExpiry(self):
        if duration <= 0:
            return True
    def getBuff(self,type):
        if type == "ATK":
            return self.buff[0]
        elif type == "ACC":
            return self.buff[1]
        elif type == "CRT":
            return self.buff[2]
        elif type == "DEF":
            return self.buff[3]
        elif type == "DDG":
            return self.buff[4]
        elif type == "LCK":
            return self.buff[5]
        elif type == "HP":
            return self.buff[6]
