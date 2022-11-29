import pygame;

class Item():
    def __init__(self,nm,desc,rar,i):
        self.name = nm
        self.description = desc
        self.rarity = rar
        self.id = i

class Weapon(Item):
    def __init__(self,nm="NULL",desc="NULL",rar=-1,i=-1,atk=0,acc=0,crt=0,amp=0):
        Item.__init__(self,nm,desc,rar,i)
        self.attack = atk
        self.accuracy = acc
        self.critrate = crt
        self.amplifier = amp

class Armor(Item):
    def __init__(self,nm="NULL",desc="NULL",rar=-1,i=-1,df=0,ddg=0,mpr=0):
        Item.__init__(self,nm,desc,rar,i)
        self.defense = df
        self.dodge = ddg
        self.manaregen = mpr

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
        self.type = tp
        self.element = el
        self.target = tgt

class SupportMagic(Item):
    def __init__(self,nm,desc,rar,i,ptc,mpc,tp,tgt):
        Item.__init__(self,nm,desc,rar,i)
        self.potency = ptc
        self.manacost = mpc
        self.type = tp
        self.target = tgt
    def getHeal(self):
        return self.potency[6]
