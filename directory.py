from items import *
from characters import *
from encounterbuilder import *
from constants import *
from utility import *
from enum import Enum
import copy

# The Directory class is responsible for compiling all distinct items, creatures, classes, and names into a comprehensive 
# class. All items are assigned a unique ID, making it so other parts of the program need only hold/transfer an item's 
# ID, and Directory can be used to pull the proper item accordingly. This helps to avoid complications from having multiple 
# data types populating the same list, as inventories will all contain IDs (integer values).

class Directory():
    def __init__(self):
        self.weaponDirectory = initWeaponDirectory()            # 0 - 99
        self.armorDirectory = initArmorDirectory()              # 100 - 199
        self.potionDirectory = initPotionDirectory()            # 200 - 299
        self.atkSpellDirectory = initAtkSpellDirectory()        # 300 - 399
        self.sptSpellDirectory = initSptSpellDirectory()        # 400 - 499
        self.talentDirectory = initTalentDirectory()            # 500 - 599
        self.accessoryDirectory = initAccessoryDirectory()      # 600 - 699
        self.foodDirectory = initFoodDirectory()                # 700 - 799
        self.consumableDirectory = initConsumableDirectory()    # 800 - 899
        self.runeDirectory = initRuneDirectory()                # 900 - 999
        self.classDirectory = initClassDirectory()              # 0 - 99
        self.creatureDirectory = initCreatureDirectory()        # 0 - 99
        self.nameDirectory = initNameDirectory()                # 0 - 99

    def getItem(self,id):
        item = Item()
        if id < 100:
            item = self.getWeapon(id)
        elif id < 200:
            item = self.getArmor(id)
        elif id < 300:
            item = self.getPotion(id)
        elif id < 400:
            item = self.getAtkSpell(id)
        elif id < 500:
            item = self.getSptSpell(id)
        elif id < 600:
            item = self.getTalent(id)
        elif id < 700:
            item = self.getAccessory(id)
        elif id < 800:
            item = self.getFood(id)
        elif id < 900:
            item = self.getConsumable(id)
        elif id < 1000:
            item = self.getRune(id)
        return item

    def getItemName(self,id,scroll=False):
        if type(id) != int:
            return id.name
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
        elif id < 600:
            name = self.talentDirectory[id-500].name
        elif id < 700:
            name = self.accessoryDirectory[id-600].name
        elif id < 800:
            name = self.foodDirectory[id-700].name
        elif id < 900:
            name = self.consumableDirectory[id-800].name
        elif id < 1000:
            name = self.runeDirectory[id-900].name
        return name

    def getItemDesc(self,id):
        if type(id) != int:
            id = id.id
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
        elif id < 600:
            desc = self.talentDirectory[id-500].description
        elif id < 700:
            desc = self.accessoryDirectory[id-600].description
        elif id < 800:
            desc = self.foodDirectory[id-700].description
        elif id < 900:
            desc = self.consumableDirectory[id-800].description
        elif id < 1000:
            desc = self.runeDirectory[id-900].description
        return desc

    def getItemRarity(self,id):
        if type(id) != int:
            id = id.id
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
        elif id < 600:
            rarity = self.talentDirectory[id-500].rarity
        elif id < 700:
            rarity = self.accessoryDirectory[id-600].rarity
        elif id < 800:
            rarity = self.foodDirectory[id-700].rarity
        elif id < 900:
            rarity = self.consumableDirectory[id-800].rarity
        elif id < 1000:
            rarity = self.runeDirectory[id-900].rarity
        return rarity
    
    def getItemType(self,id):
        if type(id) != int:
            id = id.id
        itemType = Type.Empty
        if id < 0:
            itemType = Type.Empty
        elif id < 100:
            itemType = Type.Weapon
        elif id < 200:
            itemType = Type.Armor
        elif id < 300:
            itemType = Type.Potion
        elif id < 400:
            itemType = Type.AtkSpell
        elif id < 500:
            itemType = Type.SptSpell
        elif id < 600:
            itemType = Type.Talent
        elif id < 700:
            itemType = Type.Accessory
        elif id < 800:
            itemType = Type.Food
        elif id < 900:
            itemType = Type.Consumable
        elif id < 1000:
            itemType = Type.Rune
        return itemType

    def getSpellTarget(self,id):
        if id < 400:
            target = self.atkSpellDirectory[id-300].target
        elif id < 500:
            target = self.sptSpellDirectory[id-400].target
        return target
    
    def getTalentTarget(self,id):
        return self.talentDirectory[id-500].target
    
    def getConsumableTarget(self,id):
        return self.consumableDirectory[id-800].target

    def getManaCost(self,id):
        if id < 400:
            cost = self.atkSpellDirectory[id-300].manacost
        elif id < 500:
            cost = self.sptSpellDirectory[id-400].manacost
        elif id < 600:
            cost = self.talentDirectory[id-500].mpcost
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
    
    def getTalent(self,id):
        return self.copy(self.talentDirectory[id-500])
    
    def getAccessory(self,id):
        return self.copy(self.accessoryDirectory[id-600])
    
    def getFood(self,id):
        return self.copy(self.foodDirectory[id-700])
    
    def getConsumable(self,id):
        return self.copy(self.consumableDirectory[id-800])
    
    def getRune(self,id):
        return self.copy(self.runeDirectory[id-900])

    def getItemByRarity(self,type,rarity):
        print(f'Fetching {type} of rarity {rarity}...')
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
        elif type == Type.Talent:
            for item in self.talentDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        elif type == Type.Accessory:
            for item in self.accessoryDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        elif type == Type.Food:
            for item in self.foodDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        elif type == Type.Consumable:
            for item in self.consumableDirectory:
                if item.rarity == rarity:
                    options.append(item.id)
        elif type == Type.Rune:
            for item in self.runeDirectory:
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
    
    def getWeaponByRarity(self,types,rarity):
        print(f'WeaponByRarity: {types}')
        options = []
        correctOptions = []
        for item in self.weaponDirectory:
            if item.rarity == rarity:
                options.append(item.id)
        for type in types:
            for item in options:
                if type == self.getItem(item).type:
                    correctOptions.append(item)
        choice = random.choice(correctOptions)
        print(f'Chose {self.getItemName(choice)}')
        return choice
    
    def getArmorByRarity(self,types,rarity):
        print(f'ArmorByRarity: {types}')
        options = []
        correctOptions = []
        for item in self.armorDirectory:
            if item.rarity == rarity:
                options.append(item.id)
        for type in types:
            for item in options:
                if type == self.getItem(item).type:
                    correctOptions.append(item)
        choice = random.choice(correctOptions)
        print(f'Chose {self.getItemName(choice)}')
        return choice

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
        elif type == Type.Talent:
            for item in self.talentDirectory:
                for rarity in range(rarityA,rarityB+1):
                    if item.rarity == rarity:
                        options.append(item.id)
        elif type == Type.Accessory:
            for item in self.accessoryDirectory:
                for rarity in range(rarityA,rarityB+1):
                    if item.rarity == rarity:
                        options.append(item.id)
        elif type == Type.Consumable:
            for item in self.consumableDirectory:
                for rarity in range(rarityA,rarityB+1):
                    if item.rarity == rarity:
                        options.append(item.id)
        elif type == Type.Rune:
            for item in self.runeDirectory:
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
    
    def getLootRarity(self,rarity,type):
        if type == Type.Weapon:
            divVal = MAX_DIFFICULTY / MAX_WEAPON_RARITY
            lootRarity = math.ceil(rarity / divVal)
        if type == Type.Armor:
            divVal = MAX_DIFFICULTY / MAX_ARMOR_RARITY
            lootRarity = math.ceil(rarity / divVal)
        if type == Type.Potion:
            divVal = MAX_DIFFICULTY / MAX_POTION_RARITY
            lootRarity = math.ceil(rarity / divVal)
        if type == Type.AtkSpell:
            divVal = MAX_DIFFICULTY / MAX_ATKSPELL_RARITY
            lootRarity = math.ceil(rarity / divVal)
        if type == Type.SptSpell:
            divVal = MAX_DIFFICULTY / MAX_SPTSPELL_RARITY
            lootRarity = math.ceil(rarity / divVal)
        if type == Type.Accessory:
            divVal = MAX_DIFFICULTY / MAX_ACCESSORY_RARITY
            lootRarity = math.ceil(rarity / divVal)
        if type == Type.Consumable:
            divVal = MAX_DIFFICULTY / MAX_CONSUMABLE_RARITY
            lootRarity = math.ceil(rarity / divVal)
        if type == Type.Rune:
            divVal = MAX_DIFFICULTY / MAX_RUNE_RARITY
            lootRarity = math.ceil(rarity / divVal)
        return lootRarity
    
    def getLootRarityForCharacter(self,level,type):
        if type == Type.Weapon:
            divVal = MAX_LEVEL / MAX_WEAPON_RARITY
            lootRarity = math.ceil(level / divVal)
        if type == Type.Armor:
            divVal = MAX_LEVEL / MAX_ARMOR_RARITY
            lootRarity = math.ceil(level / divVal)
        if type == Type.Potion:
            divVal = MAX_LEVEL / MAX_POTION_RARITY
            lootRarity = math.ceil(level / divVal)
        if type == Type.AtkSpell:
            divVal = MAX_LEVEL / MAX_ATKSPELL_RARITY
            lootRarity = math.ceil(level / divVal)
        if type == Type.SptSpell:
            divVal = MAX_LEVEL / MAX_SPTSPELL_RARITY
            lootRarity = math.ceil(level / divVal)
        if type == Type.Accessory:
            divVal = MAX_LEVEL / MAX_ACCESSORY_RARITY
            lootRarity = math.ceil(level / divVal)
        if type == Type.Consumable:
            divVal = MAX_LEVEL / MAX_RUNE_RARITY
            lootRarity = math.ceil(level / divVal)
        if type == Type.Rune:
            divVal = MAX_LEVEL / MAX_ACCESSORY_RARITY
            lootRarity = math.ceil(level / divVal)
        return lootRarity
    
    def rollForLoot(self,difficulty,rarity,types):
        chosenType = types[random.randint(0,len(types)-1)]
        itemRarity = difficulty + rarity.value
        #print(f'itemRarity ({itemRarity})= diff ({difficulty}) + rarity ({rarity.value})')
        if itemRarity < 1:
            itemRarity = 1
        if itemRarity > MAX_DIFFICULTY:
            itemRarity = MAX_DIFFICULTY
        itemRarity = self.getLootRarity(itemRarity, chosenType)
        #print(f'Translated rarity for {chosenType}: {itemRarity}')
        return self.getItemByRarity(chosenType,itemRarity)

    def getCharacterName(self,members):
        good = False
        while good == False:
            good = True
            candidate = self.nameDirectory[random.randint(0,len(self.nameDirectory)-1)]
            for member in members:
                if candidate == member.name:
                    good = False
        return candidate
    
    def getRandomClass(self):
        return self.classDirectory[random.randint(0,len(self.classDirectory)-1)]
    
    def getRandomPersonality(self):
        return random.choice(list(Personality))
    
    def getRandomFood(self,listSize):
        list = []
        burnout = 0
        for i in range(listSize):
            food = random.choice(self.foodDirectory)
            if food not in list:
                list.append(food)
            else:
                i -= 1
                burnout += 1
            if burnout >= 50:
                break
        return list
    
    def getMagicWeapon(self,diff):
        weapon = self.getWeapon(self.rollForLoot(diff,LootRarity.Rare,[Type.Weapon]))
        rune = self.getRune(self.getItemByRarity(Type.Rune,1))
        weapon.etchRune(rune)
        weapon.name = self.getMagicWeaponName(weapon)
        return weapon
    
    def getMagicWeaponName(self,weapon):
        #
        # W - Weapon
        # o - of
        # N - Noun
        # D - Describer
        # t - The
        #
        nameFormats = ["WotN","NW","DW","tNW","tDW"]
        nameFormat = random.choice(nameFormats)
        weaponName = ""
        for char in nameFormat:
            if weaponName != "":
                weaponName += " "
            if char == "W":
                if weapon.type == WeaponType.Axe:
                    weaponWord = [
                        "Axe",
                        "Hatchet",
                        "Greataxe",
                        "Battleaxe"
                    ]
                elif weapon.type == WeaponType.Sword:
                    weaponWord = [
                        "Sword",
                        "Blade",
                        "Greatsword",
                        "Broadsword"
                    ]
                elif weapon.type == WeaponType.Spear:
                    weaponWord = [
                        "Spear",
                        "Lance",
                        "Javelin",
                        "Trident"
                    ]
                elif weapon.type == WeaponType.Dagger:
                    weaponWord = [
                        "Dagger",
                        "Knife",
                        "Shortsword",
                        "Dirk"
                    ]
                elif weapon.type == WeaponType.Staff:
                    weaponWord = [
                        "Staff",
                        "Rod",
                        "Sceptre",
                        "Wand"
                    ]
                weaponName += random.choice(weaponWord)
            elif char == "o":
                weaponName += "of"
            elif char == "N":
                if weapon.rune.name == "Rune of Power":
                    nounWord = [
                        "Sun",
                        "Bear"
                    ]
                elif weapon.rune.name == "Rune of Surging":
                    nounWord = [
                        "Wave",
                        "Moon"
                    ]
                elif weapon.rune.name == "Rune of Piercing":
                    nounWord = [
                        "Fang",
                        "Drill"
                    ]
                elif weapon.rune.name == "Rune of Flames":
                    nounWord = [
                        "Inferno",
                        "Flame"
                    ]
                elif weapon.rune.name == "Rune of Sparks":
                    nounWord = [
                        "Spark",
                        "Thunder"
                    ]
                elif weapon.rune.name == "Rune of Freezing":
                    nounWord = [
                        "Frost",
                        "Winter"
                    ]
                elif weapon.rune.name == "Rune of Siphoning":
                    nounWord = [
                        "Archmage",
                        "Siphon"
                    ]
                elif weapon.rune.name == "Rune of Blood":
                    nounWord = [
                        "Blood",
                        "Vampire"
                    ]
                elif weapon.rune.name == "Rune of Corruption":
                    nounWord = [
                        "Curse",
                        "Demon"
                    ]
                elif weapon.rune.name == "Rune of Channeling":
                    nounWord = [
                        "Wild",
                        "Tome"
                    ]
                elif weapon.rune.name == "Rune of Expertise":
                    nounWord = [
                        "Eye",
                        "Critical"
                    ]
                weaponName += random.choice(nounWord)
            elif char == "D":
                if weapon.rune.name == "Rune of Power":
                    descriptorWord = [
                        "Power",
                        "Solar"
                    ]
                elif weapon.rune.name == "Rune of Surging":
                    descriptorWord = [
                        "Raging",
                        "Lunar"
                    ]
                elif weapon.rune.name == "Rune of Piercing":
                    descriptorWord = [
                        "Piercing",
                        "Slicing"
                    ]
                elif weapon.rune.name == "Rune of Flames":
                    descriptorWord = [
                        "Burning",
                        "Flaming"
                    ]
                elif weapon.rune.name == "Rune of Sparks":
                    descriptorWord = [
                        "Electric",
                        "Charged"
                    ]
                elif weapon.rune.name == "Rune of Freezing":
                    descriptorWord = [
                        "Frigid",
                        "Cold"
                    ]
                elif weapon.rune.name == "Rune of Siphoning":
                    descriptorWord = [
                        "Siphoning",
                        "Absorption"
                    ]
                elif weapon.rune.name == "Rune of Blood":
                    descriptorWord = [
                        "Draining",
                        "Bloody"
                    ]
                elif weapon.rune.name == "Rune of Corruption":
                    descriptorWord = [
                        "Corrupted",
                        "Tainted"
                    ]
                elif weapon.rune.name == "Rune of Channeling":
                    descriptorWord = [
                        "Channeling",
                        "Magic"
                    ]
                elif weapon.rune.name == "Rune of Expertise":
                    descriptorWord = [
                        "Master",
                        "Warrior's"
                    ]
                weaponName += random.choice(descriptorWord)
            elif char == "t":
                if weaponName == "":
                    weaponName += "The"
                else:
                    weaponName += "the"
        return weaponName
    
    def buildCharacter(self,level,members,id,cls=-1):
        if cls == -1:
            cls = random.randint(0,11)
        newChar = Character(self.getCharacterName(members),level,self.classDirectory[cls],self.getRandomPersonality(),id)
        newChar.eqpWpn = self.getWeapon(self.getWeaponByRarity(weaponProfArrayToList(newChar.type.weaponProficiency),self.getLootRarityForCharacter(level,Type.Weapon)))
        newChar.eqpAmr = self.getArmor(self.getArmorByRarity(armorProfArrayToList(newChar.type.armorProficiency),self.getLootRarityForCharacter(level,Type.Armor)))
        return newChar

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
