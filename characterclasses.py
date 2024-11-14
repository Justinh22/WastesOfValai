import pygame;
import random;
import math;
from items import *
from constants import *

class Character():
    charNum = 100
    def __init__(self,nm,lv,tp,p,id):
        self.name = nm
        self.level = lv
        self.id = id
        self.xp = 0
        self.nextLevel = 0
        for i in range(1,lv+1):
            self.nextLevel += i*100
        self.type = tp # Class; Type is used to avoid defined 'class' name
        self.spells = []
        self.talents = []
        self.talents.append(522) # Give character the Guard talent
        for i in range(self.level):
            if self.type.knownSpells[i] >= 0:
                self.spells.append(self.type.knownSpells[i])
            if self.type.knownTalents[i] >= 0:
                self.talents.append(self.type.knownTalents[i])
        self.eqpWpn = Weapon()
        self.eqpAmr = Armor()
        self.eqpAcc = Accessory()
        self.hpMax = self.type.startingStats[0]
        self.mpMax = self.type.startingStats[1]
        self.attack = self.type.startingStats[2]
        self.accuracy = self.type.startingStats[3]
        self.critrate = self.type.startingStats[4]
        self.defense = self.type.startingStats[5]
        self.dodge = self.type.startingStats[6]
        self.luck = self.type.startingStats[7]
        self.speed = self.type.startingStats[8]
        self.amplifier = self.type.startingStats[9]
        self.manaregen = self.type.startingStats[10]
        for i in range(1,lv):
            growth = tp.getGrowths()
            self.hpMax += growth[0]
            self.mpMax += growth[1]
            self.attack += growth[2]
            self.critrate += growth[3]
            self.defense += growth[4]
            self.dodge += growth[5]
            self.luck += growth[6]
            self.speed += growth[7]
        self.lastLearned = []
        self.hp = self.hpMax
        self.mp = self.mpMax
        self.hpregen = 0
        self.buffs = [0,0,0,0,0,0,0]
        self.universalEffects = UniversalEffects()
        self.activeBuffs = []
        self.status = Status.NoStatus
        self.statusCount = 0
        self.personality = p
    def getHP(self):
        return self.hp
    def getMaxHP(self):
        return self.hpMax + self.universalEffects.hp
    def getMP(self):
        return self.mp
    def getMaxMP(self):
        return self.mpMax + self.universalEffects.mp
    def getAttack(self):
        return self.eqpWpn.getAttack() + self.attack + self.universalEffects.attack + self.getBuff("ATK")
    def getDefense(self):
        return self.eqpAmr.getDefense() + self.defense + self.universalEffects.defense + self.getBuff("DEF")
    def getCritRate(self):
        return self.eqpWpn.getCritrate() + self.critrate + self.universalEffects.critrate + self.getBuff("CRT")
    def getAccuracy(self):
        ablazePenalty = 0
        if self.status is Status.Ablaze:
            ablazePenalty = 33
        if self.eqpWpn.getAccuracy() > 0:
            return self.eqpWpn.getAccuracy() + self.universalEffects.accuracy + self.getBuff("ACC") - ablazePenalty
        else:
            return self.accuracy + self.universalEffects.accuracy + self.getBuff("ACC") - ablazePenalty
    def getDodge(self):
        if self.status is Status.Shocked:
            return 0
        return self.eqpAmr.getDodge() + self.dodge + self.universalEffects.dodge + self.getBuff("DDG")
    def getLuck(self):
        return self.luck + self.universalEffects.luck + self.getBuff("LCK")
    def getAmplifier(self):
        return self.amplifier + self.universalEffects.amplifier + self.eqpWpn.amplifier
    def getManaRegen(self):
        return self.manaregen + self.universalEffects.manaregen + self.eqpAmr.manaregen
    def getHPRegen(self):
        return self.hpregen + self.universalEffects.hpregen
    def getSpeed(self):
        return self.speed + self.universalEffects.speed
    def getCumulativeXP(self):
        cumulativeXPTable = [200, 600, 1200, 2000, 3000, 4200, 5600, 7200, 9000, 11000]
        return cumulativeXPTable[self.level-1] + self.xp
    def amplify(self,val):
        val = math.ceil(val + (val * (self.getAmplifier()/100)))
        return val
    def takeDamage(self,val):
        print(f'{self.name} took {val} damage!')
        if val >= self.hp:
            self.hp = 0
            print(f'{self.name} has fallen!')
            self.resetStatus()
            self.resetBuffs()
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
        if self.hp > self.getMaxHP():
            self.hp = self.getMaxHP()
    def gainMP(self,val):
        self.mp += val
        if self.mp > self.getMaxMP():
            self.mp = self.getMaxMP()
    def gainXP(self,val):
        self.xp += val
        if self.xp > self.nextLevel and self.level < 10:
            return True
        return False
    def addSpell(self,spellID):
        if spellID not in self.spells:
            self.spells.append(spellID)
            return True 
        return False
    def levelUp(self):
        if self.level != 10:
            self.level += 1
        self.xp = 0
        self.nextLevel += self.level*100
        growth = self.type.getGrowths()
        self.hpMax += growth[0]
        self.mpMax += growth[1]
        self.attack += growth[2]
        self.critrate += growth[3]
        self.defense += growth[4]
        self.dodge += growth[5]
        self.luck += growth[6]
        self.speed += growth[7]
        self.lastLearned = []
        if self.type.knownSpells[self.level-1] != -11 and self.type.knownSpells[self.level-1] not in self.spells:
            self.spells.append(self.type.knownSpells[self.level-1])
            self.lastLearned.append(self.type.knownSpells[self.level-1])
        if self.type.knownTalents[self.level-1] != -11:
            self.talents.append(self.type.knownTalents[self.level-1])
            self.lastLearned.append(self.type.knownTalents[self.level-1])
        return growth
    def equip(self,item,dir):
        print(dir.getItemType(item))
        if dir.getItemType(item) == Type.Weapon:
            returner = self.eqpWpn.id
            self.eqpWpn = dir.getItem(item)
        elif dir.getItemType(item) == Type.Armor:
            returner = self.eqpAmr.id
            self.eqpAmr = dir.getItem(item)
        elif dir.getItemType(item) == Type.Accessory:
            returner = self.eqpAcc.id
            if returner != -1:
                print("Unequip")
                if dir.getItem(returner).timing == Timing.Universal:
                    self.universalEffectHandler(self.eqpAcc,"Unequip")
            self.eqpAcc = dir.getItem(item)
            if self.eqpAcc.timing == Timing.Universal:
                print("Equip")
                self.universalEffectHandler(self.eqpAcc,"Equip")
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
        else:
            return True
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
    def checkSpellProficiency(self,id,dir):
        print("Checking proficiency...")
        out = False
        if id >= 300 and id < 400:
            out = self.checkAtkSpellProficiency(id,dir)
        else:
            out = self.checkSptSpellProficiency(id,dir)
        return out
    def checkAtkSpellProficiency(self,id,dir):
        idRarity = dir.getItemRarity(id)
        print(f'Level: {self.type.attackMagicLevel[self.level-1] + self.universalEffects.atkMagicLevel} vs Spell: {idRarity}')
        return self.type.attackMagicLevel[self.level-1] + self.universalEffects.atkMagicLevel >= idRarity
    def checkSptSpellProficiency(self,id,dir):
        idRarity = dir.getItemRarity(id)
        print(f'Level: {self.type.supportMagicLevel[self.level-1] + self.universalEffects.sptMagicLevel} vs Spell: {idRarity}')
        return self.type.supportMagicLevel[self.level-1] + self.universalEffects.sptMagicLevel >= idRarity
    def fullRestore(self):
        self.hp = self.getMaxHP()
        self.mp = self.getMaxMP()
        self.resetStatus()
    def canCast(self,spellbookIndex,dir):
        return dir.getManaCost(self.spells[spellbookIndex]) <= self.mp
    def expendMana(self,spellbookIndex,dir):
        self.mp -= dir.getManaCost(self.spells[spellbookIndex])
        if self.mp < 0:
            self.mp = 0
    def changeMana(self,amount):
        self.mp += amount
        if self.mp < 0:
            self.mp = 0
        if self.mp > self.getMaxMP():
            self.mp = self.getMaxMP()
    def canPerform(self,talentID,dir):
        return dir.getManaCost(talentID) <= self.mp
    def universalEffectHandler(self,accessory,mode):
        mod = 0
        if mode == "Equip":
            mod = 1
        elif mode == "Unequip":
            mod = -1

        if accessory.id == 600: # Solar Band
            self.universalEffects.hp += accessory.data * mod
        elif accessory.id == 601: # Lunar Band
            self.universalEffects.mp += accessory.data * mod
        elif accessory.id == 602: # Mercury Band
            self.universalEffects.accuracy += accessory.data * mod
        elif accessory.id == 603: # Venus Band
            self.universalEffects.critrate += accessory.data * mod
        elif accessory.id == 604: # Earth Band
            self.universalEffects.defense += accessory.data * mod
        elif accessory.id == 605: # Mars Band
            self.universalEffects.attack += accessory.data * mod
        elif accessory.id == 606: # Jupiter Band
            self.universalEffects.luck += accessory.data * mod
        elif accessory.id == 607: # Saturn Band
            self.universalEffects.manaregen += accessory.data * mod
        elif accessory.id == 608: # Uranus Band
            self.universalEffects.amplifier += accessory.data * mod
        elif accessory.id == 609: # Neptune Band
            self.universalEffects.dodge += accessory.data * mod
        elif accessory.id == 610: # Pluto Band
            self.universalEffects.speed += accessory.data * mod
        elif accessory.id == 613: # Marble Heart
            self.universalEffects.hpregen += accessory.data * mod
        elif accessory.id == 624: # Mystic Journal
            self.universalEffects.sptMagicLevel += accessory.data * mod
        elif accessory.id == 625: # Wicked Journal
            self.universalEffects.atkMagicLevel += accessory.data * mod


class ClassType():
    def __init__(self,nm,wpnPrf,amrPrf,atkLv,sptLv,hpg,mpg,atg,ctg,dfg,dgg,lkg,sdg,splsLrn,tlntsLrn,idIN):
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
        self.knownTalents = tlntsLrn
        self.id = idIN
        self.description = ""
        self.rating = []
        self.startingStats = []
    def setAdditionalInfo(self,rating,stats,desc):
        self.description = desc
        self.rating = rating # Rating Order: [Power,Sturdiness,Nimbleness,Arcana,Faith,Luck]
        self.startingStats = stats # [HP,MP,ATK,ACC,CRT,DEF,DDG,LCK,SPD,AMP,MPG]
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
    def initializeMembers(self,dir,id):
        self.members.append(dir.buildCharacter(1,self.members,id,0))
        self.members[0].eqpWpn = dir.getWeapon(dir.getItemByRarity(Type.Weapon,1))
        self.members[0].eqpAmr = dir.getArmor(dir.getItemByRarity(Type.Armor,1))
    def debug_setToLevel(self,dir,lv,cls,id):
        self.members = []
        for i in range(0,4):
            self.members.append(dir.buildCharacter(lv,self.members,id+i,cls))
    def debug_RandomInventory(self,dir):
        while len(self.inventory) < MAX_INVENTORY_SIZE:
            self.addItem(dir.getItemByRarities(Type.Potion,1,5))
    def add(self,item,dir):
        if dir.getItemType(item) == Type.Weapon or dir.getItemType(item) == Type.Armor or dir.getItemType(item) == Type.Accessory:
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
    def getHighestLevel(self):
        high = 0
        for member in self.members:
            if member.level > high:
                high = member.level
        return high
    def dropEquipment(self,index):
        self.equipment.pop(index)
    def dropItem(self,index):
        self.inventory.pop(index)
    def fullRestore(self):
        for member in self.members:
            member.fullRestore()
    def awardXP(self,diff):
        underdogFactor = 0
        levelups = [0,0,0,0]
        for member in self.members:
            if member.getCumulativeXP() > underdogFactor:
                underdogFactor = member.getCumulativeXP()
        underdogMultiplier = 0
        for i in range(len(self.members)): #member in self.members:
            if self.members[i].hp > 0:
                # R
                underdogMultiplier = .5 * round(( (underdogFactor - self.members[i].getCumulativeXP()) / 50)/.5)
                if self.members[i].gainXP((diff * 3) + (round(diff/2) * random.randint(2,4)) + round((diff*3)*underdogMultiplier)):
                    levelups[i] = 1
        return levelups
    def removeAccessory(self,target):
        if self.members[target].eqpAcc != None and len(self.equipment) < MAX_INVENTORY_SIZE:
            self.equipment.append(self.members[target].eqpAcc.id)
            self.members[target].universalEffectHandler(self.members[target].eqpAcc,"Unequip")
            self.members[target].eqpAcc = Accessory()
            

class Creature():
    def __init__(self,nm,lv,idIN,hpIN,at,ac,df,dg,sd,elm,type,spells):
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
        self.element = elm
        self.biomeType = type
        self.knownSpells = spells
        self.spellCooldown = 0
        self.status = Status.NoStatus
        self.statusCount = 0
    def getAccuracy(self):
        ablazePenalty = 0
        if self.status is Status.Ablaze:
            ablazePenalty = 30
        return self.accuracy - ablazePenalty
    def getDodge(self):
        if self.status is Status.Shocked:
            return 0
        return self.dodge
    def getSpeed(self):
        return self.speed
    def getHP(self):
        return self.hp
    def getMaxHP(self):
        return self.hpMax
    def getMP(self):
        return self.mp
    def getMaxMP(self):
        return self.mpMax
    def takeDamage(self,val):
        print(f'{self.name} took {val} damage!')
        if val > self.hp:
            self.hp = 0
            print(f'{self.name} has fallen!')
            self.resetStatus()
        else:
            self.hp -= val
        return val
    def tickStatus(self):
        if self.statusCount > 0:
            self.statusCount -= 1
            if self.statusCount == 0:
                self.status = Status.NoStatus
    def resetStatus(self):
        self.status = Status.NoStatus
        self.statusCount = 0

class Encounter():
    def __init__(self):
        self.members = []

class Action():
    def __init__(self,src,tgt,act):
        self.source = src
        self.target = tgt
        self.action = act # 0 = ATTACK, 1 = GUARD, ID = SPELL, ID = TALENT, ID = ITEM
    def print(self):
        return str(self.source) + " -> " + str(self.target) + ": " + str(self.action)
    
class ActiveEffect():
    def __init__(self,id_IN,source_IN,target_IN,duration_IN=1):
        self.id = id_IN             # int ; id of corresponding talent/skill
        self.source = source_IN     # duple (string, int) ; index of party member who activated effect
        self.target = target_IN     # duple (string, int) ; index of corresponding party member/enemy who effect is targeted at
        self.duration = duration_IN # int ; number of rounds the effect will be active
    def tick(self):
        self.duration -= 1
        return self.checkExpiry()
    def checkExpiry(self):
        if self.duration <= 0:
            return True

class Buff():
    def __init__(self,nme,buf,dur,tgt):
        self.name = nme
        self.duration = dur
        self.buff = buf
        self.target = tgt
    def tick(self):
        self.duration -= 1
        return self.checkExpiry()
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
        
class UniversalEffects():
    def __init__(self):
        self.hp = 0
        self.mp = 0
        self.attack = 0
        self.accuracy = 0
        self.critrate = 0
        self.defense = 0
        self.dodge = 0
        self.speed = 0
        self.luck = 0
        self.amplifier = 0
        self.manaregen = 0
        self.hpregen = 0
        self.atkMagicLevel = 0
        self.sptMagicLevel = 0
