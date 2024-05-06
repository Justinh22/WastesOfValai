import pygame
from characterclasses import *

def initClassDirectory():
    classDirectory = []
    # Weapon Prof: [AXE, SWORD, SPEAR, DAGGER, STAFF]
    # Armor Prof:  [LIGHT, MEDIUM, HEAVY, ROBE, ARCANIST]
    #                         NAME          Wpn Prof      Amr Prof      Atk Spell Proficiency   Spt Spell Proficiency   HP            MP        ATK       CRT       DEF       DDG       LCK       SPD        Learned Spells                             Learned Talents                            ID
    #                                       Rating          Description                           Rating Order: [Power,Sturdiness,Nimbleness,Arcana,Faith,Luck]

    Explorer =      ClassType("Explorer",   [1,1,1,1,1] , [1,1,1,1,1] , [1,1,1,2,2,2,3,3,3,3] , [1,1,1,2,2,2,3,3,3,3] , [8,10,10]  , [3,4,5] , [3,4,5] , [1,1,2] , [2,2,3] , [1,1,2] , [1,1,2] , [4,5,6] , [406,301,403,305,408,306,427,310,313,428] , [-11,-11,-11,-11,-11,-11,-11,-11,-11,-11] , 0) # Explorer
    Explorer.setAdditionalInfo(             [3,3,3,3,3,3] , "A versatile adventurer able to handle any situation. A true jack-of-all-trades.")
    classDirectory.append(Explorer)
    Warrior =       ClassType("Warrior",    [1,1,1,0,0] , [0,1,1,0,0] , [0,0,1,1,1,1,1,1,1,1] , [0,1,1,1,2,2,2,2,2,2] , [8,10,12]  , [0,1,2] , [4,5,6] , [0,1,2] , [2,3,3] , [0,1,2] , [1,1,2] , [3,4,5] , [-11,400,300,-11,409,-11,411,407,-11,408] , [508,-11,-11,-11,513,-11,-11,-11,-11,-11] , 1) # Warrior
    Warrior.setAdditionalInfo(              [4,4,2,1,1,3] , "A burly adventurer who handles physical threats with ease. Excels in ATK and DEF.")
    classDirectory.append(Warrior)
    Thief =         ClassType("Thief",      [0,1,0,1,0] , [1,1,0,0,1] , [0,0,0,1,1,1,1,1,1,1] , [0,0,0,1,1,1,1,2,2,2] , [6,6,8]    , [2,3,4] , [3,5,5] , [2,3,4] , [2,2,3] , [2,3,3] , [2,2,3] , [6,7,8] , [-11,-11,-11,404,302,-11,405,410,-11,412] , [505,-11,-11,-11,515,-11,-11,-11,-11,-11] , 2) # Thief
    Thief.setAdditionalInfo(                [3,2,5,1,2,4] , "A nimble adventurer who weaves around incoming attacks. Excels in CRT, DDG, SPD.")
    classDirectory.append(Thief)
    Knight =        ClassType("Knight",     [1,1,1,1,0] , [0,1,1,0,0] , [0,0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,1,1,1,1,1] , [10,12,14] , [0,1,2] , [3,4,4] , [0,1,2] , [3,3,4] , [0,0,1] , [0,1,2] , [2,3,3] , [-11,-11,-11,-11,-11,401,400,-11,-11,404] , [504,-11,-11,-11,506,-11,-11,-11,-11,-11] , 3) # Knight
    Knight.setAdditionalInfo(               [3,5,1,0,1,2] , "A sturdy adventurer that deflects blows easily. Excels in HP and DEF.")
    classDirectory.append(Knight)
    Vanguard =      ClassType("Vanguard",   [1,1,0,0,0] , [1,1,1,0,0] , [0,0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0,0,0] , [8,10,12]  , [0,1,2] , [5,6,7] , [1,2,3] , [2,3,3] , [1,1,2] , [1,1,2] , [3,4,5] , [-11,-11,-11,-11,-11,-11,-11,-11,-11,-11] , [510,-11,-11,-11,512,-11,-11,-11,-11,-11] , 4) # Vanguard
    Vanguard.setAdditionalInfo(             [5,4,3,0,0,3] , "A powerful adventurer that is unparalleled in physical combat. Excels in ATK and DEF.")
    classDirectory.append(Vanguard)
    Mercenary =     ClassType("Mercenary",  [1,1,1,1,0] , [1,1,1,0,1] , [0,0,0,1,1,1,2,2,2,2] , [0,1,1,1,2,2,2,2,2,2] , [8,10,10]  , [2,3,4] , [5,5,5] , [1,2,3] , [2,2,3] , [1,2,2] , [2,3,4] , [4,5,6] , [-11,402,405,-11,409,412,-11,308,-11,408] , [502,-11,-11,-11,516,-11,-11,-11,-11,-11] , 5) # Mercenary
    Mercenary.setAdditionalInfo(            [4,2,3,2,2,5] , "A lucky adventurer who often finds themselves in fortunate situations. Excels in ATK and LCK.")
    classDirectory.append(Mercenary)
    Mage =          ClassType("Mage",       [0,0,1,1,1] , [1,0,0,1,1] , [2,2,3,3,3,4,4,4,5,5] , [1,1,2,2,2,3,3,3,3,3] , [6,6,8]    , [4,5,6] , [2,3,3] , [0,1,2] , [1,2,2] , [1,2,2] , [0,1,2] , [4,5,6] , [304,302,312,411,310,316,421,318,418,322] , [501,-11,-11,-11,514,-11,-11,-11,-11,-11] , 6) # Mage
    Mage.setAdditionalInfo(                 [2,1,3,5,3,2] , "A gifted adventurer who can cast a wide range of attack spells. Excels in ATK Magic.")
    classDirectory.append(Mage)
    Cleric =        ClassType("Cleric",     [1,0,0,1,1] , [1,0,1,1,1] , [1,1,2,2,2,3,3,3,3,3] , [2,2,3,3,3,3,4,4,5,5] , [6,6,8]    , [4,5,6] , [3,3,4] , [0,1,2] , [1,2,2] , [1,1,2] , [0,1,2] , [3,4,5] , [406,407,413,427,428,456,445,442,454,453] , [500,-11,-11,-11,519,-11,-11,-11,-11,-11] , 7) # Cleric
    Cleric.setAdditionalInfo(               [2,2,2,3,5,2] , "A devout adventurer who relies on higher powers to keep their allies alive. Excels in SPT Magic.")
    classDirectory.append(Cleric)
    Paladin =       ClassType("Paladin",    [1,1,1,0,0] , [0,1,1,0,1] , [1,1,1,1,2,2,2,2,2,3] , [1,2,2,2,3,3,3,4,4,4] , [8,10,12]  , [3,4,4] , [4,5,6] , [0,1,1] , [2,3,4] , [0,1,1] , [0,1,2] , [2,3,4] , [406,408,414,407,424,427,325,435,457,441] , [507,-11,-11,-11,517,-11,-11,-11,-11,-11] , 8) # Paladin
    Paladin.setAdditionalInfo(              [3,4,2,3,4,1] , "A courageous adventurer who calls on those above to smite their enemies. Excels in DEF and SPT Magic.")
    classDirectory.append(Paladin)
    Warlock =       ClassType("Warlock",    [0,0,0,0,1] , [0,0,0,1,1] , [2,2,3,3,3,4,4,4,4,4] , [2,2,3,3,3,4,4,4,4,4] , [4,6,8]    , [5,6,7] , [1,2,3] , [0,0,1] , [1,1,2] , [1,2,2] , [2,2,3] , [4,5,6] , [305,411,312,329,311,315,439,442,319,330] , [503,-11,-11,-11,521,-11,-11,-11,-11,-11] , 9) # Warlock
    Warlock.setAdditionalInfo(              [1,1,3,4,4,3] , "A cursed adventurer who achieved incredible spellcasting prowess through questionable means. Excels in Atk Magic and Spt Magic.")
    classDirectory.append(Warlock)
    Assassin =      ClassType("Assassin",   [0,1,1,1,0] , [1,0,0,0,1] , [0,0,1,1,1,2,2,2,2,2] , [0,0,0,1,1,1,2,2,2,2] , [6,8,10]   , [2,3,4] , [4,5,7] , [2,2,3] , [2,2,2] , [2,2,3] , [1,2,3] , [6,7,8] , [-11,-11,302,402,301,303,410,-11,-11,405] , [509,-11,-11,-11,511,-11,-11,-11,-11,-11] , 10) # Assassin
    Assassin.setAdditionalInfo(             [5,2,4,2,2,4] , "A deadly adventurer whom killing comes as second nature to. Excels in ATK, SPD, and LCK.")
    classDirectory.append(Assassin)
    Witch =         ClassType("Witch",      [1,0,1,0,1] , [1,1,0,1,0] , [1,2,2,2,3,3,3,4,4,4] , [0,0,1,1,1,2,2,2,2,2] , [6,8,8]    , [4,5,6] , [2,2,3] , [1,2,3] , [2,2,3] , [2,3,4] , [1,2,3] , [5,6,7] , [302,325,406,308,311,414,329,320,327,413] , [518,-11,-11,-11,520,-11,-11,-11,-11,-11] , 11) # Witch
    Witch.setAdditionalInfo(                [1,2,4,4,2,3] , "An unholy adventurer who can cast powerful spells while staying out of harm's way. Excels in DDG and ATK Magic.")
    classDirectory.append(Witch)

    return classDirectory

def initCreatureDirectory():
    creatureDirectory = []
    #                          Name LV ID HP ATK ACC DEF DDG SPD RES BIOME
    #1
    Slime = Creature("Slime",1,0,16,7,65,2,5,1,Element.Ice,Biome.Forest,[])
    creatureDirectory.append(Slime)
    Goblin = Creature("Goblin",1,1,10,10,60,2,5,3,Element.Fire,Biome.Plains,[])
    creatureDirectory.append(Goblin)
    Bandit = Creature("Bandit",1,2,14,8,70,3,0,3,Element.Lightning,Biome.Desert,[])
    creatureDirectory.append(Bandit)
    Skeleton = Creature("Skeleton",1,3,12,9,65,2,0,2,Element.Ice,Biome.Dungeon,[])
    creatureDirectory.append(Skeleton)
    #2
    Giant_Spider = Creature("Giant Spider",2,4,22,10,65,4,5,9,Element.Ice,Biome.Forest,[])
    creatureDirectory.append(Giant_Spider)
    Kobold = Creature("Kobold",2,5,20,11,65,5,5,7,Element.Fire,Biome.Plains,[])
    creatureDirectory.append(Kobold)
    Imp = Creature("Imp",2,6,18,13,70,3,5,8,Element.Fire,Biome.Desert,[301])
    creatureDirectory.append(Imp)
    Spectre = Creature("Spectre",2,7,20,12,65,4,10,7,Element.Ice,Biome.Dungeon,[302])
    creatureDirectory.append(Spectre)
    #5
    Serpent = Creature("Serpent",5,8,40,19,80,4,20,13,Element.Ice,Biome.Forest,[])
    creatureDirectory.append(Serpent)
    Wyrm = Creature("Wyrm",5,9,43,18,75,4,25,12,Element.Lightning,Biome.Plains,[325])
    creatureDirectory.append(Wyrm)
    Cultist = Creature("Cultist",5,10,40,18,90,5,10,14,Element.Lightning,Biome.Desert,[307])
    creatureDirectory.append(Cultist)
    Wight = Creature("Wight",5,11,42,16,85,7,5,11,Element.Ice,Biome.Dungeon,[326])
    creatureDirectory.append(Wight)
    #8
    Water_Elemental = Creature("Water Elemental",8,12,64,27,85,10,25,18,Element.Ice,Biome.Forest,[314])
    creatureDirectory.append(Water_Elemental)
    Air_Elemental = Creature("Air Elemental",8,13,60,25,95,8,35,19,Element.Lightning,Biome.Plains,[312])
    creatureDirectory.append(Air_Elemental)
    Earth_Elemental = Creature("Earth Elemental",8,14,75,29,70,13,5,12,Element.Lightning,Biome.Desert,[312])
    creatureDirectory.append(Earth_Elemental)
    Fire_Elemental = Creature("Fire Elemental",8,15,63,33,75,9,15,16,Element.Fire,Biome.Dungeon,[313])
    creatureDirectory.append(Fire_Elemental)
    #10 -- REBALANCE ALL CREATURES BENEATH THIS POINT
    Ogre = Creature("Ogre",10,16,87,37,75,16,5,15,Element.Lightning,Biome.Forest,[])
    creatureDirectory.append(Ogre)
    Wyvern = Creature("Wyvern",10,17,81,34,100,14,30,23,Element.Lightning,Biome.Plains,[316,325])
    creatureDirectory.append(Wyvern)
    Giant = Creature("Giant",10,18,89,40,70,16,0,17,Element.Fire,Biome.Desert,[])
    creatureDirectory.append(Giant)
    Basilisk = Creature("Basilisk",10,19,93,35,85,18,0,21,Element.Ice,Biome.Dungeon,[327])
    creatureDirectory.append(Basilisk)
    #12
    Chimera = Creature("Chimera",12,20,100,44,110,24,15,27,Element.Fire,Biome.Forest,[312])
    creatureDirectory.append(Chimera)
    Demon = Creature("Demon",12,21,96,46,120,20,15,28,Element.Fire,Biome.Plains,[319,328])
    creatureDirectory.append(Demon)
    Dark_Sorcerer = Creature("Dark Sorcerer",12,22,88,50,110,16,30,25,Element.Lightning,Biome.Desert,[315,319,329])
    creatureDirectory.append(Dark_Sorcerer)
    Vampire = Creature("Vampire",12,23,92,48,115,20,25,28,Element.Ice,Biome.Dungeon,[])
    creatureDirectory.append(Vampire)
    #15
    Gorgon = Creature("Gorgon",15,24,129,53,120,28,10,26,Element.Fire,Biome.Forest,[327])
    creatureDirectory.append(Gorgon)
    Iron_Golem = Creature("Iron Golem",15,25,140,51,110,30,5,18,Element.Ice,Biome.Plains,[])
    creatureDirectory.append(Iron_Golem)
    Behemoth = Creature("Behemoth",15,26,125,55,120,30,15,20,Element.Ice,Biome.Desert,[])
    creatureDirectory.append(Behemoth)
    Pheonix = Creature("Pheonix",15,27,115,57,130,26,30,29,Element.Fire,Biome.Dungeon,[322,331])
    creatureDirectory.append(Pheonix)
    #18
    Gaia_Giant = Creature("Gaia Giant",18,28,190,66,130,33,5,20,Element.Lightning,Biome.Forest,[327,316])
    creatureDirectory.append(Gaia_Giant)
    Fallen_Angel = Creature("Fallen Angel",18,29,175,70,140,29,20,34,Element.Lightning,Biome.Plains,[321])
    creatureDirectory.append(Fallen_Angel)
    Duskwalker = Creature("Duskwalker",18,30,165,72,145,27,25,33,Element.Ice,Biome.Desert,[329])
    creatureDirectory.append(Duskwalker)
    Valentium_Golem = Creature("Valentium Golem",18,31,210,64,120,35,0,18,Element.Fire,Biome.Dungeon,[])
    creatureDirectory.append(Valentium_Golem)
    #20
    Blue_Dragon = Creature("Blue Dragon",20,32,250,75,150,30,35,45,Element.Ice,Biome.Forest,[323,332])
    creatureDirectory.append(Blue_Dragon)
    Green_Dragon = Creature("Green Dragon",20,33,250,70,140,30,50,44,Element.Lightning,Biome.Plains,[321,330])
    creatureDirectory.append(Green_Dragon)
    Bronze_Dragon = Creature("Bronze Dragon",20,34,250,80,130,40,5,41,Element.Lightning,Biome.Desert,[321,330])
    creatureDirectory.append(Bronze_Dragon)
    Red_Dragon = Creature("Red Dragon",20,35,250,85,140,35,20,43,Element.Fire,Biome.Dungeon,[322,331])
    creatureDirectory.append(Red_Dragon)

    return creatureDirectory

def initNameDirectory():
    names = ["Abrielle",
             "Adara",
             "Alissa",
             "Amara",
             "Amelia",
             "Anya",
             "Aurelia",
             "Brielle",
             "Balthus",
             "Cara",
             "Cassius",
             "Cirius",
             "Corvo",
             "Darius",
             "Dagen",
             "Eira",
             "Elysia",
             "Finean",
             "Gareth",
             "Guinevere",
             "Hesperos",
             "Ignacio",
             "Isolde",
             "Jace",
             "Kara",
             "Kyra",
             "Kyrielle",
             "Leila",
             "Lilina",
             "Lucien",
             "Lucius",
             "Matthew",
             "Mathilda",
             "Natania",
             "Orion",
             "Orin",
             "Perseus",
             "Pyralia",
             "Quincy",
             "Rialda",
             "Sebastian",
             "Sirian",
             "Terra",
             "Thalia",
             "Torin",
             "Ulysses",
             "Vanora",
             "Xanthus",
             "Zeke",
             "Zorian"]
    return names
