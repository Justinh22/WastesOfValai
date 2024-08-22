import pygame
from characterclasses import *

def initClassDirectory():
    classDirectory = []
    # Weapon Prof: [AXE, SWORD, SPEAR, DAGGER, STAFF]
    # Armor Prof:  [LIGHT, MEDIUM, HEAVY, ROBE, ARCANIST]
    #                         NAME          Wpn Prof      Amr Prof      Atk Spell Proficiency   Spt Spell Proficiency   HP            MP        ATK       CRT       DEF       DDG       LCK       SPD        Learned Spells                             Learned Talents                            ID
    #                                       Rating         Stats [HP,MP,ATK,ACC,CRT,DEF,DDG,LCK,SPD,AMP,MPG]       Description
    #                                       Rating Order: [Power,Sturdiness,Nimbleness,Arcana,Faith,Luck]

    Explorer =      ClassType("Explorer",   [1,1,1,1,1] , [1,1,1,1,1] , [1,1,1,2,2,2,3,3,3,3] , [1,1,1,2,2,2,3,3,3,3] , [18,20,20]  , [6,8,10]   , [3,4,5] , [1,1,2] , [2,2,3] , [1,1,2] , [1,1,2] , [4,5,6] , [406,301,403,305,408,306,427,310,313,428] , [-11,-11,-11,-11,-11,-11,-11,-11,-11,-11] , 0) # Explorer
    Explorer.setAdditionalInfo(             [3,3,3,3,3,3] , [50,50,25,70,0,25,0,5,10,0,2]                          , "A versatile adventurer able to handle any situation. A true jack-of-all-trades.")
    classDirectory.append(Explorer)
    
    Warrior =       ClassType("Warrior",    [1,1,1,0,0] , [0,1,1,0,0] , [0,0,1,1,1,1,1,1,1,1] , [0,1,1,1,2,2,2,2,2,2] , [18,20,22]  , [0,2,4]    , [4,5,6] , [0,1,2] , [3,3,4] , [0,1,2] , [1,1,2] , [3,4,5] , [-11,400,300,-11,409,-11,411,407,-11,408] , [508,-11,-11,-11,513,-11,-11,-11,-11,-11] , 1) # Warrior
    Warrior.setAdditionalInfo(              [4,4,2,1,1,3] , [55,30,27,70,0,26,-5,0,5,0,0]                          , "A burly adventurer who handles physical threats with ease. Excels in ATK and DEF.")
    classDirectory.append(Warrior)
    
    Thief =         ClassType("Thief",      [0,1,0,1,0] , [1,1,0,0,1] , [0,0,0,1,1,1,1,1,1,1] , [0,0,0,1,1,1,1,2,2,2] , [16,16,18]    , [4,6,8]    , [3,5,5] , [2,3,4] , [2,2,3] , [2,3,3] , [2,2,3] , [6,7,8] , [-11,-11,-11,404,302,-11,405,410,-11,412] , [505,-11,-11,-11,515,-11,-11,-11,-11,-11] , 2) # Thief
    Thief.setAdditionalInfo(                [3,2,5,1,2,4] , [45,35,27,70,5,23,5,5,16,0,0]                          , "A nimble adventurer who weaves around incoming attacks. Excels in CRT, DDG, SPD.")
    classDirectory.append(Thief)
    
    Knight =        ClassType("Knight",     [1,1,1,1,0] , [0,1,1,0,0] , [0,0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,1,1,1,1,1] , [22,22,24] , [0,2,4]    , [3,4,4] , [0,1,2] , [3,4,5] , [0,0,1] , [0,1,2] , [2,3,3] , [-11,-11,-11,-11,-11,401,400,-11,-11,404] , [504,-11,-11,-11,506,-11,-11,-11,-11,-11] , 3) # Knight
    Knight.setAdditionalInfo(               [3,5,1,0,1,2] , [70,20,23,70,-5,27,-10,0,3,0,0]                        , "A sturdy adventurer that deflects blows easily. Excels in HP and DEF.")
    classDirectory.append(Knight)
    
    Vanguard =      ClassType("Vanguard",   [1,1,0,0,0] , [1,1,1,0,0] , [0,0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0,0,0] , [18,20,22]  , [0,2,4]    , [5,6,7] , [1,2,3] , [2,3,3] , [2,2,2] , [0,1,1] , [3,4,5] , [-11,-11,-11,-11,-11,-11,-11,-11,-11,-11] , [510,-11,-11,-11,512,-11,-11,-11,-11,-11] , 4) # Vanguard
    Vanguard.setAdditionalInfo(             [5,3,4,0,0,1] , [55,20,28,70,-5,23,5,0,12,0,0]                         , "A powerful adventurer that is unparalleled in physical combat. Excels in ATK and DDG.")
    classDirectory.append(Vanguard)
    
    Mercenary =     ClassType("Mercenary",  [1,1,1,1,0] , [1,1,1,0,1] , [0,0,0,1,1,1,2,2,2,2] , [0,1,1,1,2,2,2,2,2,2] , [18,20,20]  , [4,6,8]    , [5,5,5] , [1,2,3] , [1,2,3] , [1,2,2] , [2,3,4] , [4,5,6] , [-11,402,405,-11,409,412,-11,308,-11,408] , [502,-11,-11,-11,516,-11,-11,-11,-11,-11] , 5) # Mercenary
    Mercenary.setAdditionalInfo(            [4,2,3,2,2,5] , [50,40,28,70,5,24,0,10,11,0,0]                         , "A lucky adventurer who often finds themselves in fortunate situations. Excels in ATK and LCK.")
    classDirectory.append(Mercenary)
    
    Mage =          ClassType("Mage",       [0,0,1,1,1] , [1,0,0,1,1] , [2,2,3,3,3,4,4,4,5,5] , [1,1,2,2,2,3,3,3,3,3] , [16,16,18]    , [8,10,12]  , [2,3,3] , [0,1,2] , [1,1,2] , [1,2,2] , [0,1,2] , [4,5,6] , [304,302,312,411,310,316,421,318,418,322] , [501,-11,-11,-11,514,-11,-11,-11,-11,-11] , 6) # Mage
    Mage.setAdditionalInfo(                 [2,1,3,5,3,2] , [40,70,22,70,0,22,0,0,9,10,0]                          , "A gifted adventurer who can cast a wide range of attack spells. Excels in ATK Magic.")
    classDirectory.append(Mage)
    
    Cleric =        ClassType("Cleric",     [1,0,0,1,1] , [1,0,1,1,1] , [1,1,2,2,2,3,3,3,3,3] , [2,2,3,3,3,3,4,4,5,5] , [16,16,18]    , [8,10,12]  , [3,3,4] , [0,1,2] , [1,1,2] , [1,1,2] , [0,1,2] , [3,4,5] , [406,407,413,427,428,456,445,442,454,453] , [500,-11,-11,-11,519,-11,-11,-11,-11,-11] , 7) # Cleric
    Cleric.setAdditionalInfo(               [2,2,2,3,5,2] , [40,70,22,70,0,22,0,0,8,0,2]                           , "A devout adventurer who relies on higher powers to keep their allies alive. Excels in SPT Magic.")
    classDirectory.append(Cleric)
    
    Paladin =       ClassType("Paladin",    [1,1,1,0,0] , [0,1,1,0,1] , [1,1,1,1,2,2,2,2,2,3] , [1,2,2,2,3,3,3,4,4,4] , [20,20,22]  , [6,8,8]    , [4,5,6] , [0,1,1] , [2,3,4] , [0,1,1] , [0,1,2] , [2,3,4] , [406,408,414,407,424,427,325,435,457,441] , [507,-11,-11,-11,517,-11,-11,-11,-11,-11] , 8) # Paladin
    Paladin.setAdditionalInfo(              [3,4,2,3,4,1] , [55,50,24,70,0,27,-5,0,8,0,0]                          , "A courageous adventurer who calls on those above to smite their enemies. Excels in DEF and SPT Magic.")
    classDirectory.append(Paladin)
    
    Warlock =       ClassType("Warlock",    [0,0,0,0,1] , [0,0,0,1,1] , [2,2,3,3,3,4,4,4,4,4] , [2,2,3,3,3,4,4,4,4,4] , [12,14,16]    , [10,12,14] , [1,2,3] , [0,0,1] , [0,1,2] , [1,2,2] , [2,2,3] , [4,5,6] , [305,411,312,329,311,315,439,442,319,330] , [503,-11,-11,-11,521,-11,-11,-11,-11,-11] , 9) # Warlock
    Warlock.setAdditionalInfo(              [1,1,3,4,4,3] , [35,75,21,70,0,22,0,5,11,10,0]                         , "A cursed adventurer who achieved incredible spellcasting prowess through questionable means. Excels in Atk Magic and Spt Magic.")
    classDirectory.append(Warlock)
    
    Assassin =      ClassType("Assassin",   [0,1,1,1,0] , [1,0,0,0,1] , [0,0,1,1,1,2,2,2,2,2] , [0,0,0,1,1,1,2,2,2,2] , [16,18,20]   , [4,6,8]    , [4,5,7] , [2,2,3] , [2,2,2] , [2,2,3] , [1,2,3] , [6,7,8] , [-11,-11,302,402,301,303,410,-11,-11,405] , [509,-11,-11,-11,511,-11,-11,-11,-11,-11] , 10) # Assassin
    Assassin.setAdditionalInfo(             [5,2,4,2,2,4] , [40,35,28,70,5,23,5,5,14,0,0]                          , "A deadly adventurer whom killing comes as second nature to. Excels in ATK, SPD, and LCK.")
    classDirectory.append(Assassin)
    
    Witch =         ClassType("Witch",      [1,0,1,0,1] , [1,1,0,1,0] , [1,2,2,2,3,3,3,4,4,4] , [0,0,1,1,1,2,2,2,2,2] , [14,16,18]    , [8,10,12]  , [2,2,3] , [1,2,3] , [2,2,3] , [2,3,4] , [1,2,3] , [5,6,7] , [302,325,406,308,311,414,329,320,327,413] , [518,-11,-11,-11,520,-11,-11,-11,-11,-11] , 11) # Witch
    Witch.setAdditionalInfo(                [1,2,4,4,2,3] , [40,60,21,70,0,22,5,0,13,0,2]                          , "An unholy adventurer who can cast powerful spells while staying out of harm's way. Excels in DDG and ATK Magic.")
    classDirectory.append(Witch)

    return classDirectory

def initCreatureDirectory():
    creatureDirectory = []
    #                          Name LV ID HP ATK ACC DEF DDG SPD RES BIOME
    #1
    Slime = Creature("Slime",1,0,70,34,65,6,5,6,Element.Ice,Biome.Forest,[])
    creatureDirectory.append(Slime)
    Goblin = Creature("Goblin",1,1,60,36,60,2,5,10,Element.Fire,Biome.Plains,[])
    creatureDirectory.append(Goblin)
    Bandit = Creature("Bandit",1,2,55,37,70,2,0,11,Element.Lightning,Biome.Desert,[])
    creatureDirectory.append(Bandit)
    Skeleton = Creature("Skeleton",1,3,45,38,65,3,0,9,Element.Ice,Biome.Other,[])
    creatureDirectory.append(Skeleton)
    #2
    Giant_Spider = Creature("Giant Spider",2,4,110,41,65,8,5,16,Element.Ice,Biome.Forest,[])
    creatureDirectory.append(Giant_Spider)
    Kobold = Creature("Kobold",2,5,90,43,65,11,5,12,Element.Fire,Biome.Plains,[])
    creatureDirectory.append(Kobold)
    Imp = Creature("Imp",2,6,85,46,70,5,5,15,Element.Fire,Biome.Desert,[301])
    creatureDirectory.append(Imp)
    Spectre = Creature("Spectre",2,7,120,40,65,8,10,10,Element.Ice,Biome.Other,[302])
    creatureDirectory.append(Spectre)
    #5
    Serpent = Creature("Serpent",5,8,160,58,80,15,20,20,Element.Ice,Biome.Forest,[])
    creatureDirectory.append(Serpent)
    Wyrm = Creature("Wyrm",5,9,200,56,75,17,25,17,Element.Lightning,Biome.Plains,[325])
    creatureDirectory.append(Wyrm)
    Cultist = Creature("Cultist",5,10,130,60,90,14,10,15,Element.Lightning,Biome.Desert,[307])
    creatureDirectory.append(Cultist)
    Wight = Creature("Wight",5,11,200,55,85,22,5,9,Element.Ice,Biome.Other,[326])
    creatureDirectory.append(Wight)
    #8
    Water_Elemental = Creature("Water Elemental",8,12,300,80,85,24,25,32,Element.Ice,Biome.Forest,[314])
    creatureDirectory.append(Water_Elemental)
    Air_Elemental = Creature("Air Elemental",8,13,300,76,95,19,35,40,Element.Lightning,Biome.Plains,[312])
    creatureDirectory.append(Air_Elemental)
    Earth_Elemental = Creature("Earth Elemental",8,14,300,78,70,30,5,20,Element.Lightning,Biome.Desert,[312])
    creatureDirectory.append(Earth_Elemental)
    Fire_Elemental = Creature("Fire Elemental",8,15,300,84,75,24,15,35,Element.Fire,Biome.Other,[313])
    creatureDirectory.append(Fire_Elemental)
    #10
    Ogre = Creature("Ogre",10,16,400,91,75,28,5,24,Element.Lightning,Biome.Forest,[])
    creatureDirectory.append(Ogre)
    Wyvern = Creature("Wyvern",10,17,400,88,100,26,30,44,Element.Lightning,Biome.Plains,[316,325])
    creatureDirectory.append(Wyvern)
    Giant = Creature("Giant",10,18,400,87,70,32,0,25,Element.Fire,Biome.Desert,[])
    creatureDirectory.append(Giant)
    Basilisk = Creature("Basilisk",10,19,400,89,85,31,0,34,Element.Ice,Biome.Other,[327])
    creatureDirectory.append(Basilisk)
    #12
    Chimera = Creature("Chimera",12,20,550,100,110,36,15,32,Element.Fire,Biome.Forest,[312])
    creatureDirectory.append(Chimera)
    Demon = Creature("Demon",12,21,500,100,124,31,15,38,Element.Fire,Biome.Plains,[319,328])
    creatureDirectory.append(Demon)
    Dark_Sorcerer = Creature("Dark Sorcerer",12,22,400,114,110,26,30,46,Element.Lightning,Biome.Desert,[315,319,329])
    creatureDirectory.append(Dark_Sorcerer)
    Vampire = Creature("Vampire",12,23,450,107,115,29,25,44,Element.Ice,Biome.Other,[])
    creatureDirectory.append(Vampire)
    #15
    Gorgon = Creature("Gorgon",15,24,650,107,120,34,10,34,Element.Fire,Biome.Forest,[327])
    creatureDirectory.append(Gorgon)
    Iron_Golem = Creature("Iron Golem",15,25,750,112,95,40,0,18,Element.Ice,Biome.Plains,[])
    creatureDirectory.append(Iron_Golem)
    Behemoth = Creature("Behemoth",15,26,600,100,125,30,15,42,Element.Ice,Biome.Desert,[])
    creatureDirectory.append(Behemoth)
    Pheonix = Creature("Pheonix",15,27,500,116,130,28,30,56,Element.Fire,Biome.Other,[322,331])
    creatureDirectory.append(Pheonix)
    #18
    Gaia_Giant = Creature("Gaia Giant",18,28,750,118,130,46,5,46,Element.Lightning,Biome.Forest,[327,316])
    creatureDirectory.append(Gaia_Giant)
    Fallen_Angel = Creature("Fallen Angel",18,29,650,130,140,41,20,55,Element.Lightning,Biome.Plains,[321])
    creatureDirectory.append(Fallen_Angel)
    Duskwalker = Creature("Duskwalker",18,30,600,126,145,36,25,60,Element.Ice,Biome.Desert,[329])
    creatureDirectory.append(Duskwalker)
    Valentium_Golem = Creature("Valentium Golem",18,31,850,122,120,51,0,24,Element.Fire,Biome.Other,[])
    creatureDirectory.append(Valentium_Golem)
    #20
    Blue_Dragon = Creature("Blue Dragon",20,32,1000,155,160,47,40,45,Element.Ice,Biome.Forest,[323,332])
    creatureDirectory.append(Blue_Dragon)
    Green_Dragon = Creature("Green Dragon",20,33,1000,150,170,52,50,44,Element.Lightning,Biome.Plains,[321,330])
    creatureDirectory.append(Green_Dragon)
    Bronze_Dragon = Creature("Bronze Dragon",20,34,1000,145,130,67,5,41,Element.Lightning,Biome.Desert,[321,330])
    creatureDirectory.append(Bronze_Dragon)
    Red_Dragon = Creature("Red Dragon",20,35,1000,160,145,57,35,43,Element.Fire,Biome.Other,[322,331])
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
