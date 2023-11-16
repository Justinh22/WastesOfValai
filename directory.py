from items import *
from characters import *
from encounterbuilder import *
from constants import *
from enum import Enum
import copy

# The Directory class is responsible for compiling all distinct items, creatures, classes, and names into a comprehensive 
# class. All items are assigned a unique ID, making it so other parts of the program need only hold/transfer an item's 
# ID, and Directory can be used to pull the proper item accordingly. This helps to avoid complications from having multiple 
# data types populating the same list, as inventories will all contain IDs (integer values).

class Directory():
    def __init__(self):
        self.weaponDirectory = initWeaponDirectory()        # 0 - 99
        self.armorDirectory = initArmorDirectory()          # 100 - 199
        self.potionDirectory = initPotionDirectory()        # 200 - 299
        self.atkSpellDirectory = initAtkSpellDirectory()    # 300 - 399
        self.sptSpellDirectory = initSptSpellDirectory()    # 400 - 499
        self.classDirectory = initClassDirectory()          # 0 - 99
        self.creatureDirectory = initCreatureDirectory()    # 0 - 99
        self.nameDirectory = initNameDirectory()            # 0 - 99

    def getItem(self,id):
        item = Item()
        if id < 100:
            item = self.weaponDirectory[id]
        elif id < 200:
            item = self.armorDirectory[id-100]
        elif id < 300:
            item = self.potionDirectory[id-200]
        elif id < 400:
            item = self.atkSpellDirectory[id-300]
        elif id < 500:
            item = self.sptSpellDirectory[id-400]
        return item

    def getItemName(self,id,scroll=False):
        name = "NULL"
        if id < 100:
            name = self.weaponDirectory[id].name
        elif id < 200:
            name = self.armorDirectory[id-100].name
        elif id < 300:
            name = self.potionDirectory[id-200].name
        elif id < 400:
            name = self.atkSpellDirectory[id-300].name
            if scroll:
                name += " Scroll"
        elif id < 500:
            name = self.sptSpellDirectory[id-400].name
            if scroll:
                name += " Scroll"
        return name

    def getItemDesc(self,id):
        desc = "NULL"
        if id < 100:
            desc = self.weaponDirectory[id].description
        elif id < 200:
            desc = self.armorDirectory[id-100].description
        elif id < 300:
            desc = self.potionDirectory[id-200].description
        elif id < 400:
            desc = self.atkSpellDirectory[id-300].description
        elif id < 500:
            desc = self.sptSpellDirectory[id-400].description
        return desc

    def getItemRarity(self,id):
        rarity = "NULL"
        if id < 100:
            rarity = self.weaponDirectory[id].rarity
        elif id < 200:
            rarity = self.armorDirectory[id-100].rarity
        elif id < 300:
            rarity = self.potionDirectory[id-200].rarity
        elif id < 400:
            rarity = self.atkSpellDirectory[id-300].rarity
        elif id < 500:
            rarity = self.sptSpellDirectory[id-400].rarity
        return rarity
    
    def getItemType(self,id):
        type = Type.Empty
        if id < 0:
            type = Type.Empty
        elif id < 100:
            type = Type.Weapon
        elif id < 200:
            type = Type.Armor
        elif id < 300:
            type = Type.Potion
        elif id < 400:
            type = Type.AtkSpell
        elif id < 500:
            type = Type.SptSpell
        return type

    def getSpellTarget(self,id):
        if id < 400:
            target = self.atkSpellDirectory[id-300].target
        elif id < 500:
            target = self.sptSpellDirectory[id-400].target
        return target

    def getManaCost(self,id):
        if id < 400:
            cost = self.atkSpellDirectory[id-300].manacost
        elif id < 500:
            cost = self.sptSpellDirectory[id-400].manacost
        return cost

    def getWeapon(self,id):
        return self.copy(self.weaponDirectory[id])

    def getArmor(self,id):
        return self.copy(self.armorDirectory[id-100])

    def getPotion(self,id):
        return self.copy(self.potionDirectory[id-200])

    def getAtkSpell(self,id):
        return self.copy(self.atkSpellDirectory[id-300])

    def getSptSpell(self,id):
        return self.copy(self.sptSpellDirectory[id-400])

    def getItemByRarity(self,type,rarity):
        options = []
        if type == Type.Weapon:
            for item in self.weaponDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        elif type == Type.Armor:
            for item in self.armorDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        elif type == Type.Potion:
            for item in self.potionDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        elif type == Type.AtkSpell:
            for item in self.atkSpellDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        elif type == Type.SptSpell:
            for item in self.sptSpellDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        elif type == Type.Creature:
            for item in self.creatureDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        elif type == Type.Class:
            for item in self.classDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        else:
            return -1
        return options[random.randint(0,len(options)-1)]

    def getItemByRarities(self,type,rarityA,rarityB):
        options = []
        if type == Type.Weapon:
            for item in self.weaponDirectory:
                for rarity in range(rarityA,rarityB+1):
                    if item.rarity == rarity:
                        options.append(item.id)
        elif type == Type.Armor:
            for item in self.armorDirectory:
                for rarity in range(rarityA,rarityB+1):
                    if item.rarity == rarity:
                        options.append(item.id)
        elif type == Type.Potion:
            for item in self.potionDirectory:
                for rarity in range(rarityA,rarityB+1):
                    if item.rarity == rarity:
                        options.append(item.id)
        elif type == Type.AtkSpell:
            for item in self.atkSpellDirectory:
                for rarity in range(rarityA,rarityB+1):
                    if item.rarity == rarity:
                        options.append(item.id)
        elif type == Type.SptSpell:
            for item in self.sptSpellDirectory:
                for rarity in range(rarityA,rarityB+1):
                    if item.rarity == rarity:
                        options.append(item.id)
        elif type == Type.Creature:
            for item in self.creatureDirectory:
                for rarity in range(rarityA,rarityB+1):
                    if item.rarity == rarity:
                        options.append(item.id)
        elif type == Type.Class:
            for item in self.classDirectory:
                for rarity in range(rarityA,rarityB+1):
                    if item.rarity == rarity:
                        options.append(item.id)
        else:
            return -1
        return options[random.randint(0,len(options)-1)]

    def getCharacterName(self,members):
        good = False
        while good == False:
            good = True
            candidate = self.nameDirectory[random.randint(0,len(self.nameDirectory)-1)]
            for member in members:
                if candidate == member.name:
                    good = False
        return candidate

    def buildEncounter(self,level,biome):
        biomeCreatures = []
        encounter = []
        for creature in self.creatureDirectory:
            if creature.biomeType == biome:
                biomeCreatures.append(creature)
        encounterLevels = pickLevels(level)
        print(encounterLevels)
        for lev in encounterLevels:
            random.shuffle(biomeCreatures)
            for creature in biomeCreatures:
                if creature.level == lev:
                    newCreat = copy.deepcopy(creature)
                    encounter.append(newCreat)
                    break
        return encounter

    def copy(self,item):
        return copy.deepcopy(item)
