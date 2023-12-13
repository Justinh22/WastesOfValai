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

class Armor(Item):
    def __init__(self,nm="NULL",desc="NULL",rar=-1,i=-1,df=0,ddg=0,mpr=0,typ=ArmorType.Medium):
        Item.__init__(self,nm,desc,rar,i)
        self.defense = df
        self.dodge = ddg
        self.manaregen = mpr
        self.type = typ

class Potion(Item):
    def __init__(self,nm,desc,rar,i,hpg,mpg):
        Item.__init__(self,nm,desc,rar,i)
        self.hpGain = hpg
        self.mpGain = mpg

class Accessory(Item):
    def __init__(self,nm,desc,rar,i,ar):
        Item.__init__(self,nm,desc,rar,i)
        self.activationRate = ar

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

class Skill(Item):
    def __init__(self,nm,desc,rar,i,hpc,tgt,tp):
        Item.__init__(self,nm,desc,rar,i)
        self.hpcost = hpc
        self.type = tp # ATTACK, SUPPORT
        self.target = tgt # SELF, ALLY, SINGLE, ALL
