import pygame;
from constants import *

class Item():
    def __init__(self,nm="NULLITEM",desc="NULLITEM",rar=-1,i=-1):
        self.name = nm
        self.description = desc
        self.rarity = rar
        self.id = i

class Weapon(Item):
    def __init__(self,nm="NULL",desc="NULL",rar=-1,i=-1,atk=0,acc=0,crt=0,amp=0,typ=WeaponType.Sword):
        Item.__init__(self,nm,desc,rar,i)
        self.attack = atk
        self.accuracy = acc
        self.critrate = crt
        self.amplifier = amp
        self.type = typ
        self.rune = None
        self.atkRefine = 0
        self.accRefine = 0
        self.crtRefine = 0
    def getAttack(self):
        return self.attack + (self.atkRefine * ATK_REFINE_BOOST)
    def getAccuracy(self):
        return self.accuracy + (self.accRefine * ACC_REFINE_BOOST)
    def getCritrate(self):
        return self.critrate + (self.crtRefine * CRT_REFINE_BOOST)
    def refine(self,newRefineValues):
        self.atkRefine = newRefineValues[0]
        self.accRefine = newRefineValues[1]
        self.crtRefine = newRefineValues[2]
        print(f'Refined! +{self.atkRefine}/+{self.accRefine}/+{self.crtRefine}')
    def reforge(self,newWeapon):
        self.name = newWeapon.name
        self.description = newWeapon.description
        self.id = newWeapon.id
        self.attack = newWeapon.attack
        self.accuracy = newWeapon.accuracy
        self.critrate = newWeapon.critrate
        self.amplifier = newWeapon.amplifier
        self.type = newWeapon.type
    def etchRune(self,rune):
        self.rune = rune

class Armor(Item):
    def __init__(self,nm="NULL",desc="NULL",rar=-1,i=-1,df=0,ddg=0,mpr=0,typ=ArmorType.Medium):
        Item.__init__(self,nm,desc,rar,i)
        self.defense = df
        self.dodge = ddg
        self.manaregen = mpr
        self.type = typ
        self.defRefine = 0
        self.ddgRefine = 0
    def getDefense(self):
        return self.defense + (self.defRefine * DEF_REFINE_BOOST)
    def getDodge(self):
        return self.dodge + (self.ddgRefine * DDG_REFINE_BOOST)
    def refine(self,newRefineValues):
        self.defRefine = newRefineValues[0]
        self.ddgRefine = newRefineValues[1]
        print(f'Refined! +{self.defRefine}/+{self.ddgRefine}')
    def reforge(self,newArmor):
        self.name = newArmor.name
        self.description = newArmor.description
        self.id = newArmor.id
        self.defense = newArmor.defense
        self.dodge = newArmor.dodge
        self.manaregen = newArmor.manaregen
        self.type = newArmor.type

class Potion(Item):
    def __init__(self,nm,desc,rar,i,hpg,mpg):
        Item.__init__(self,nm,desc,rar,i)
        self.hpGain = hpg
        self.mpGain = mpg
        self.type = "Potion"
        self.timing = ConsumableTiming.Anytime

class Consumable(Item):
    def __init__(self,nm,desc,rar,i,tgt,tmg,data):
        Item.__init__(self,nm,desc,rar,i)
        self.target = tgt # SELF, ALLY, SINGLE, ALL, PARTY
        self.timing = tmg # ANYTIME, INTURN, INSTANT, ONDEATH, PEACETIME
        self.data = data
        self.type = Type.Consumable

class Accessory(Item):
    def __init__(self,nm="NULL",desc="NULL",rar=-1,i=-1,ar=0,typ=ActivationType.Passive,tmg=Timing.Universal,data=0):
        Item.__init__(self,nm,desc,rar,i)
        self.activationRate = ar
        self.type = typ
        self.data = data
        self.timing = tmg

class AttackMagic(Item):
    def __init__(self,nm,desc,rar,i,mpc,atk,tp,el,tgt):
        Item.__init__(self,nm,desc,rar,i)
        self.attack = atk
        self.manacost = mpc
        self.type = tp      # Attack, Debuff
        self.element = el   # Lightning, Fire, Ice
        self.target = tgt   # Single, All

class SupportMagic(Item):
    def __init__(self,nm,desc,rar,i,ptc,mpc,tp,tgt):
        Item.__init__(self,nm,desc,rar,i)
        self.potency = ptc  # List of size 7: [ ATK ACC CRT DEF DDG LCK HP ]
        self.manacost = mpc
        self.type = tp      # Buff, Heal, Raise, Cleanse
        self.target = tgt   # Single, All
    def getHeal(self):
        return self.potency[6]

class Talent(Item):
    def __init__(self,nm,desc,rar,i,mpc,tp,tgt,tmg):
        Item.__init__(self,nm,desc,rar,i)
        self.mpcost = mpc
        self.type = tp # ATTACK, SUPPORT
        self.target = tgt # SELF, ALLY, SINGLE, ALL
        self.timing = tmg # INSTANT, INTURN

class Food(Item):
    def __init__(self,nm,desc,rar,i,buff):
        Item.__init__(self,nm,desc,rar,i)
        self.buff = buff # List of size 12: [HP,MP,ACC,CRT,DEF,ATK,LCK,MPG,AMP,DDG,SPD,HPG]

class Rune(Item):
    def __init__(self,nm,desc,rar,i,type,data=0,lvl=1):
        Item.__init__(self,nm,desc,rar,i)
        self.type = type
        self.data = data
        self.level = lvl
    def getRuneLevelString(self,lvl=-1):
        if lvl == -1:
            lvl = self.level
        levelString = ""
        for i in range(lvl):
            levelString += "I"
        return levelString