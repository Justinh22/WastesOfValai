import pygame;
import random;
import math;
from items import *
from constants import *

class Character():
    charNum = 100
    def __init__(self,nm,lv,tp,p):
        self.name = nm
        self.level = lv
        Character.charNum += 1
        self.id = Character.charNum
        self.xp = 0
        self.nextLevel = 200*lv
        self.type = tp # Class; Type is used to avoid defined 'class' name
        self.spells = []
        for i in range(self.level):
            if self.type.knownSpells[i] >= 0:
                self.spells.append(self.type.knownSpells[i])
        self.eqpWpn = Weapon()
        self.eqpAmr = Armor()
        self.hpMax = 20
        self.mpMax = 20
        self.attack = 3
        self.critrate = 0
        self.defense = 1
        self.dodge = 0
        self.luck = 0
        self.speed = 1
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
        self.activeBuffs = []
        self.status = Status.NoStatus
        self.statusCount = 0
        self.personality = p
    def getAttack(self):
        return self.eqpWpn.attack + self.attack + self.getBuff("ATK")
    def getDefense(self):
        return self.eqpAmr.defense + self.defense + self.getBuff("DEF")
    def getCritRate(self):
        return self.eqpWpn.critrate + self.critrate + self.getBuff("CRT")
    def getAccuracy(self):
        if self.eqpWpn.accuracy > 0:
            return self.eqpWpn.accuracy + self.getBuff("ACC")
        else:
            return self.accuracy + self.getBuff("ACC")
    def getDodge(self):
        return self.eqpAmr.dodge + self.dodge + self.getBuff("DDG")
    def getLuck(self):
        return self.luck + self.getBuff("LCK")
    def getAmplifier(self):
        return self.amplifier + self.eqpWpn.amplifier
    def getManaRegen(self):
        return self.manaregen + self.eqpAmr.manaregen
    def getSpeed(self):
        return self.speed
    def amplify(self,val):
        val = math.ceil(val + (val * (self.getAmplifier()/100)))
        return val
    def takeDamage(self,val):
        print(f'{self.name} took {val} damage!')
        if val > self.hp:
            self.hp = 0
        else:
            self.hp -= val
        return val
    def addBuffs(self,buff):
        self.activeBuffs.append((buff.name,buff.duration))
        for i in range(len(self.buffs)):
            self.buffs[i] += buff.buff[i]
        self.hp += self.buffs[6]
        if self.hp > self.hpMax:
            self.hp = self.hpMax
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
        self.activeBuffs.clear()
    def tickStatus(self):
        if self.statusCount > 0:
            self.statusCount -= 1
            if self.statusCount == 0:
                self.status = Status.NoStatus
    def resetStatus(self):
        self.status = Status.NoStatus
        self.statusCount = 0
    def gainHP(self,val):
        self.hp += val
        if self.hp > self.hpMax:
            self.hp = self.hpMax
    def gainMP(self,val):
        self.mp += val
        if self.mp > self.mpMax:
            self.mp = self.mpMax
    def gainXP(self,val):
        self.xp += val
        if self.xp > self.nextLevel and self.level < 10:
            self.xp -= self.nextLevel
            self.nextLevel += 200
            return True
        return False
    def addSpell(self,spellID):
        if spellID not in self.spells:
            self.spells.append(spellID)
            return True 
        return False
    def levelUp(self):
        self.level += 1
        self.xp = 0
        growth = self.type.getGrowths()
        self.hpMax += growth[0]
        self.mpMax += growth[1]
        self.attack += growth[2]
        self.critrate += growth[3]
        self.defense += growth[4]
        self.dodge += growth[5]
        self.luck += growth[6]
        self.speed += growth[7]
        if self.type.knownSpells[self.level-1] != -11 and self.type.knownSpells[self.level-1] not in self.spells:
            self.spells.append(self.type.knownSpells[self.level-1])
        return growth
    def equip(self,item,dir):
        if dir.getItemType(item) == Type.Weapon:
            returner = self.eqpWpn.id
            self.eqpWpn = dir.getItem(item)
        elif dir.getItemType(item) == Type.Armor:
            returner = self.eqpAmr.id
            self.eqpAmr = dir.getItem(item)
        return returner
    def checkProficiency(self,id,dir):
        idType = dir.getItemType(id)
        if idType == Type.Weapon:
            return self.checkWeaponProficiency(id,dir)
        elif idType == Type.Armor:
            return self.checkArmorProficiency(id,dir)
        elif idType == Type.AtkSpell:
            return self.checkAtkSpellProficiency(id,dir)
        elif idType == Type.SptSpell:
            return self.checkSptSpellProficiency(id,dir)
    def checkWeaponProficiency(self,id,dir):
        idType = (dir.getItem(id)).type
        if idType == WeaponType.Axe:
            return self.type.weaponProficiency[0]==1
        elif idType == WeaponType.Sword:
            return self.type.weaponProficiency[1]==1
        elif idType == WeaponType.Spear:
            return self.type.weaponProficiency[2]==1
        elif idType == WeaponType.Dagger:
            return self.type.weaponProficiency[3]==1
        elif idType == WeaponType.Staff:
            return self.type.weaponProficiency[4]==1
    def checkArmorProficiency(self,id,dir):
        idType = (dir.getItem(id)).type
        if idType == ArmorType.Light:
            return self.type.armorProficiency[0]==1
        elif idType == ArmorType.Medium:
            return self.type.armorProficiency[1]==1
        elif idType == ArmorType.Heavy:

            return self.type.armorProficiency[2]==1
        elif idType == ArmorType.Robe:
            return self.type.armorProficiency[3]==1
        elif idType == ArmorType.Arcanist:
            return self.type.armorProficiency[4]==1
    def checkAtkSpellProficiency(self,id,dir):
        idRarity = dir.getItemRarity(id)
        return self.type.attackMagicLevel[self.level-1] >= idRarity
    def checkSptSpellProficiency(self,id,dir):
        idRarity = dir.getItemRarity(id)
        return self.type.supportMagicLevel[self.level-1] >= idRarity
    def fullRestore(self):
        self.hp = self.hpMax
        self.mp = self.mpMax
        self.resetStatus()
    def canCast(self,spellbookIndex,dir):
        return dir.getManaCost(self.spells[spellbookIndex]) <= self.mp
    def expendMana(self,spellbookIndex,dir):
        self.mp -= dir.getManaCost(self.spells[spellbookIndex])
        if self.mp < 0:
            self.mp = 0


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
        self.description = ""
        self.rating = []
    def setAdditionalInfo(self,rating,desc):
        self.description = desc
        self.rating = rating
    def getGrowths(self):
        return [self.hpGrowth[random.randint(0,2)], self.mpGrowth[random.randint(0,2)], self.atkGrowth[random.randint(0,2)], self.crtGrowth[random.randint(0,2)], self.defGrowth[random.randint(0,2)], self.ddgGrowth[random.randint(0,2)], self.lckGrowth[random.randint(0,2)], self.spdGrowth[random.randint(0,2)]]
    def wpnProfToString(self):
        ret = ""
        comma = ""
        if self.weaponProficiency[0] == 1:
            ret += "Axe"
            comma = ", "
        if self.weaponProficiency[1] == 1:
            ret += comma + "Sword"
            comma = ", "
        if self.weaponProficiency[2] == 1:
            ret += comma + "Spear"
            comma = ", "
        if self.weaponProficiency[3] == 1:
            ret += comma + "Dagger"
            comma = ", "
        if self.weaponProficiency[4] == 1:
            ret += comma + "Staff"
            comma = ", "
        return ret
    def amrProfToString(self):
        ret = ""
        comma = ""
        if self.armorProficiency[0] == 1:
            ret += "Light"
            comma = ", "
        if self.armorProficiency[1] == 1:
            ret += comma + "Medium"
            comma = ", "
        if self.armorProficiency[2] == 1:
            ret += comma + "Heavy"
            comma = ", "
        if self.armorProficiency[3] == 1:
            ret += comma + "Robe"
            comma = ", "
        if self.armorProficiency[4] == 1:
            ret += comma + "Arcanist"
            comma = ", "
        return ret


class Party():
    def __init__(self):
        self.members = []
        self.inventory = []         # List of int : Contains id of all items in inventory
        self.equipment = []         # List of int : Contains id of all equipment in inventory
    def printContents(self):
        for member in self.members:
            print(member.name)
    def initializeMembers(self,dir):
        self.members.append(Character(dir.getCharacterName(self.members),1,dir.classDirectory[0],dir.getRandomPersonality()))
        self.members[0].eqpWpn = dir.getWeapon(dir.getItemByRarity(Type.Weapon,1))
        self.members[0].eqpAmr = dir.getArmor(dir.getItemByRarity(Type.Armor,1))
        #for i in range(0,random.randint(3,4)):
        #    lvl = 2
        #   self.members.append(Character(dir.getCharacterName(self.members),lvl,dir.classDirectory[random.randint(0,11)],random.randint(0,5))) #random.randint(0,11)
        #    self.members[i].eqpWpn = dir.getWeapon(dir.getItemByRarities(Type.Weapon,lvl-1,lvl))
        #    self.members[i].eqpAmr = dir.getArmor(dir.getItemByRarities(Type.Armor,lvl-1,lvl))
    def debug_setToLevel(self,dir,lv):
        self.members = []
        for i in range(0,4):
            self.members.append(Character(dir.getCharacterName(self.members),lv,dir.classDirectory[random.randint(0,11)],random.randint(0,5))) #random.randint(0,11)
            self.members[i].eqpWpn = dir.getWeapon(dir.getItemByRarities(Type.Weapon,lv-1,lv))
            self.members[i].eqpAmr = dir.getArmor(dir.getItemByRarities(Type.Armor,lv-1,lv))
    def debug_RandomInventory(self,dir):
        while len(self.inventory) < MAX_INVENTORY_SIZE:
            self.addItem(dir.getItemByRarities(Type.Potion,1,5))
    def add(self,item,dir):
        print(dir.getItemType(item))
        if dir.getItemType(item) == Type.Weapon or dir.getItemType(item) == Type.Armor:
            return self.addEquipment(item)
        else:
            return self.addItem(item)
    def addItem(self,item):
        if len(self.inventory) < MAX_INVENTORY_SIZE:
            self.inventory.append(item)
            return True
        print("Item inventory is full")
        return False
    def addEquipment(self,item):
        if len(self.equipment) < MAX_INVENTORY_SIZE:
            self.equipment.append(item)
            return True
        print("Equipment inventory is full")
        return False
    def learnSpell(self,member,index):
        self.members[member].addSpell(self.inventory[index])
        self.inventory.pop(index)
    def usePotion(self,member,index,dir):
        self.members[member].gainHP(dir.getPotion(self.inventory[index]).hpGain)
        self.members[member].gainMP(dir.getPotion(self.inventory[index]).mpGain)
        self.inventory.pop(index)
    def getPower(self):
        power = 0
        for member in self.members:
            power += member.level
        return power
    def dropEquipment(self,index):
        self.equipment.pop(index)
    def dropItem(self,index):
        self.inventory.pop(index)
    def fullRestore(self):
        for member in self.members:
            member.fullRestore()

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
        self.status = "None"
        self.statusCount = 0
    def getAccuracy(self):
        return self.accuracy
    def getDodge(self):
        return self.dodge
    def takeDamage(self,val):
        print(f'{self.name} took {val} damage!')
        if val > self.hp:
            self.hp = 0
        else:
            self.hp -= val
        return val
    def tickStatus(self):
        if self.statusCount > 0:
            self.statusCount -= 1
            if self.statusCount == 0:
                self.status = "None"

class Encounter():
    def __init__(self):
        self.members = []

class Action():
    def __init__(self,src,tgt,act):
        self.source = src
        self.target = tgt
        self.action = act # 0 = ATTACK, 1 = GUARD, ID = SPELL, ID = ART, ID = ITEM
    def print(self):
        return str(self.source) + " -> " + str(self.target) + ": " + str(self.action)

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
        if self.duration <= 0:
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
