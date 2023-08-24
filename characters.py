import pygame
from characterclasses import *

def initClassDirectory():
    classDirectory = []
    #                         NAME          Wpn Prof      Amr Prof      Atk Spell Proficiency   Spt Spell Proficiency   HP            MP        ATK       CRT       DEF       DDG       LCK       SPD        Learned Spells                             ID

    Explorer =      ClassType("Explorer",   [1,1,1,1,1] , [1,1,1,1,1] , [1,1,1,2,2,2,3,3,3,3] , [1,1,1,2,2,2,3,3,3,3] , [8,10,12]  , [3,4,5] , [1,1,2] , [1,1,2] , [1,1,2] , [1,1,2] , [1,1,2] , [4,5,6] , [406,301,403,305,408,306,427,310,313,428] , 0)
    classDirectory.append(Explorer)
    Warrior =       ClassType("Warrior",    [1,1,1,0,0] , [0,1,1,0,0] , [0,0,0,0,0,0,0,1,1,1] , [0,0,0,0,0,0,1,1,1,1] , [8,10,12]  , [0,1,2] , [2,3,3] , [0,1,2] , [1,2,2] , [0,1,2] , [0,1,2] , [3,4,5] , [-11,-11,-11,-11,-11,-11,400,300,402,-11] , 1)
    classDirectory.append(Warrior)
    Thief =         ClassType("Thief",      [0,1,0,1,0] , [1,1,0,0,1] , [0,0,0,1,1,1,1,1,1,1] , [0,0,0,1,1,1,1,2,2,2] , [6,6,8]    , [2,3,4] , [2,2,3] , [2,3,4] , [1,1,2] , [2,3,3] , [2,2,3] , [6,7,8] , [-11,-11,-11,404,302,-11,405,410,-11,412] , 2)
    classDirectory.append(Thief)
    Knight =        ClassType("Knight",     [1,1,1,1,0] , [0,1,1,0,0] , [0,0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,1,1,1,1,1] , [10,12,14] , [0,1,2] , [1,2,3] , [0,1,2] , [2,2,3] , [0,0,1] , [0,1,2] , [2,3,3] , [-11,-11,-11,-11,-11,401,400,-11,-11,404] , 3)
    classDirectory.append(Knight)
    Vanguard =      ClassType("Vanguard",   [1,1,0,0,0] , [1,1,1,0,0] , [0,0,0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0,0,0] , [8,10,12]  , [0,1,2] , [2,3,4] , [1,2,3] , [1,1,2] , [1,1,2] , [1,1,2] , [3,4,5] , [-11,-11,-11,-11,-11,-11,-11,-11,-11,-11] , 4)
    classDirectory.append(Vanguard)
    Mercenary =     ClassType("Mercenary",  [1,1,1,1,0] , [1,1,1,0,1] , [0,0,0,1,1,1,2,2,2,2] , [0,1,1,1,2,2,2,2,2,2] , [8,10,12]  , [2,3,4] , [1,2,3] , [0,1,2] , [1,1,2] , [1,2,2] , [2,3,4] , [4,5,6] , [-11,402,405,-11,409,412,-11,308,-11,408] , 5)
    classDirectory.append(Mercenary)
    Mage =          ClassType("Mage",       [0,0,1,1,1] , [1,0,0,1,1] , [2,2,3,3,3,4,4,4,5,5] , [1,1,2,2,2,3,3,3,3,3] , [6,6,8]    , [4,5,6] , [1,1,2] , [0,1,2] , [1,1,1] , [1,2,2] , [0,1,2] , [4,5,6] , [304,302,312,411,310,316,421,318,418,322] , 6)
    classDirectory.append(Mage)
    Cleric =        ClassType("Cleric",     [1,0,0,1,1] , [1,0,1,1,1] , [1,1,2,2,2,3,3,3,3,3] , [2,2,2,3,3,3,4,4,5,5] , [6,6,8]    , [4,5,6] , [1,1,2] , [0,1,2] , [1,1,1] , [1,1,2] , [0,1,2] , [3,4,5] , [406,407,413,427,428,456,445,442,454,453] , 7)
    classDirectory.append(Cleric)
    Paladin =       ClassType("Paladin",    [1,1,1,0,0] , [0,1,1,0,1] , [1,1,1,1,2,2,2,2,2,3] , [1,2,2,2,3,3,3,4,4,4] , [8,10,12]  , [3,4,4] , [1,2,3] , [0,1,1] , [1,2,3] , [0,1,1] , [0,1,2] , [2,3,4] , [406,408,414,407,424,427,325,435,457,441] , 8)
    classDirectory.append(Paladin)
    Warlock =       ClassType("Warlock",    [0,0,0,0,1] , [0,0,0,1,1] , [2,2,3,3,3,4,4,4,4,4] , [2,2,3,3,3,4,4,4,4,4] , [4,6,8]    , [5,6,7] , [0,1,1] , [0,0,1] , [1,1,1] , [1,1,2] , [1,2,3] , [4,5,6] , [305,411,312,329,311,315,439,442,319,330] , 9)
    classDirectory.append(Warlock)
    Assassin =      ClassType("Assassin",   [0,1,1,1,0] , [1,0,0,0,1] , [0,0,1,1,1,2,2,2,2,2] , [0,0,0,1,1,1,2,2,2,2] , [4,6,8]    , [2,3,4] , [2,2,3] , [2,2,3] , [1,1,1] , [2,2,3] , [1,2,3] , [6,7,8] , [-11,-11,302,402,301,303,410,-11,-11,405] , 10)
    classDirectory.append(Assassin)
    Witch =         ClassType("Witch",      [1,0,1,0,1] , [1,1,0,1,0] , [1,2,2,2,3,3,3,4,4,4] , [0,0,1,1,1,2,2,2,2,2] , [6,6,8]    , [4,5,6] , [0,1,1] , [1,2,3] , [1,1,2] , [2,3,4] , [1,2,3] , [3,4,5] , [302,325,406,308,311,414,329,320,327,413] , 11)
    classDirectory.append(Witch)

    return classDirectory

def initCreatureDirectory():
    creatureDirectory = []
    #                          Name LV ID HP ATK ACC DEF DDG RES BIOME
    #1
    Slime = Creature("Slime",1,0,16,4,65,0,5,1,"Fire","Forest",[])
    creatureDirectory.append(Slime)
    Goblin = Creature("Goblin",1,1,10,7,60,0,5,3,"Frost","Plains",[])
    creatureDirectory.append(Goblin)
    Bandit = Creature("Bandit",1,2,14,5,70,1,0,3,"Lightning","Desert",[])
    creatureDirectory.append(Bandit)
    Skeleton = Creature("Skeleton",1,3,12,6,65,0,0,2,"Frost","Dungeon",[])
    creatureDirectory.append(Skeleton)
    #2
    Giant_Spider = Creature("Giant Spider",2,4,18,6,65,1,5,9,"Frost","Forest",[])
    creatureDirectory.append(Giant_Spider)
    Kobold = Creature("Kobold",2,5,16,7,65,2,5,7,"Fire","Plains",[])
    creatureDirectory.append(Kobold)
    Imp = Creature("Imp",2,6,14,9,70,0,5,8,"Fire","Desert",[301])
    creatureDirectory.append(Imp)
    Spectre = Creature("Spectre",2,7,16,8,65,1,10,7,"Frost","Dungeon",[302])
    creatureDirectory.append(Spectre)
    #5
    Serpent = Creature("Serpent",5,8,28,16,80,1,20,13,"Frost","Forest",[])
    creatureDirectory.append(Serpent)
    Wyrm = Creature("Wyrm",5,9,31,15,75,1,25,12,"Lightning","Plains",[325])
    creatureDirectory.append(Wyrm)
    Cultist = Creature("Cultist",5,10,28,15,90,3,10,14,"Lightning","Desert",[307])
    creatureDirectory.append(Cultist)
    Wight = Creature("Wight",5,11,30,13,85,5,5,11,"Frost","Dungeon",[326])
    creatureDirectory.append(Wight)
    #8
    Water_Elemental = Creature("Water Elemental",8,12,42,23,85,7,25,18,"Fire","Forest",[314])
    creatureDirectory.append(Water_Elemental)
    Air_Elemental = Creature("Air Elemental",8,13,37,21,95,5,35,19,"Frost","Plains",[312])
    creatureDirectory.append(Air_Elemental)
    Earth_Elemental = Creature("Earth Elemental",8,14,53,25,70,10,5,12,"Lightning","Desert",[312])
    creatureDirectory.append(Earth_Elemental)
    Fire_Elemental = Creature("Fire Elemental",8,15,41,29,75,6,15,16,"Fire","Dungeon",[313])
    creatureDirectory.append(Fire_Elemental)
    #10
    Ogre = Creature("Ogre",10,16,68,36,75,12,5,15,"Lightning","Forest",[])
    creatureDirectory.append(Ogre)
    Wyvern = Creature("Wyvern",10,17,62,33,100,10,30,23,"Lightning","Plains",[316,325])
    creatureDirectory.append(Wyvern)
    Giant = Creature("Giant",10,18,70,39,70,12,0,17,"Fire","Desert",[])
    creatureDirectory.append(Giant)
    Basilisk = Creature("Basilisk",10,19,74,34,85,14,0,21,"Frost","Dungeon",[327])
    creatureDirectory.append(Basilisk)
    #12
    Chimera = Creature("Chimera",12,20,76,52,110,24,15,27,"Frost","Forest",[312])
    creatureDirectory.append(Chimera)
    Demon = Creature("Demon",12,21,72,54,120,20,15,28,"Fire","Plains",[319,328])
    creatureDirectory.append(Demon)
    Dark_Sorcerer = Creature("Dark Sorcerer",12,22,64,58,110,16,30,25,"Lightning","Desert",[315,319,329])
    creatureDirectory.append(Dark_Sorcerer)
    Vampire = Creature("Vampire",12,23,68,56,115,20,25,28,"Fire","Dungeon",[])
    creatureDirectory.append(Vampire)
    #15
    Gorgon = Creature("Gorgon",15,24,110,68,120,30,10,26,"Frost","Forest",[327])
    creatureDirectory.append(Gorgon)
    Iron_Golem = Creature("Iron Golem",15,25,125,66,110,32,5,18,"Fire","Plains",[])
    creatureDirectory.append(Iron_Golem)
    Behemoth = Creature("Behemoth",15,26,100,70,120,32,15,20,"Frost","Desert",[])
    creatureDirectory.append(Behemoth)
    Pheonix = Creature("Pheonix",15,27,90,76,130,28,30,29,"Fire","Dungeon",[322,331])
    creatureDirectory.append(Pheonix)
    #18
    Gaia_Giant = Creature("Gaia Giant",18,28,175,76,130,40,5,20,"Lightning","Forest",[327,316])
    creatureDirectory.append(Gaia_Giant)
    Fallen_Angel = Creature("Fallen Angel",18,29,160,80,140,36,20,34,"Lightning","Plains",[321])
    creatureDirectory.append(Fallen_Angel)
    Duskwalker = Creature("Duskwalker",18,30,145,82,145,34,25,33,"Frost","Desert",[329])
    creatureDirectory.append(Duskwalker)
    Valentium_Golem = Creature("Valentium Golem",18,31,200,73,120,42,0,18,"Fire","Dungeon",[])
    creatureDirectory.append(Valentium_Golem)
    #20
    Blue_Dragon = Creature("Blue Dragon",20,32,250,100,150,40,35,45,"Fire","Forest",[323,332])
    creatureDirectory.append(Blue_Dragon)
    Green_Dragon = Creature("Green Dragon",20,33,250,90,140,30,50,44,"Frost","Plains",[321,330])
    creatureDirectory.append(Green_Dragon)
    Bronze_Dragon = Creature("Bronze Dragon",20,34,250,105,130,45,5,41,"Lightning","Desert",[321,330])
    creatureDirectory.append(Bronze_Dragon)
    Red_Dragon = Creature("Red Dragon",20,35,250,115,140,35,20,43,"Fire","Dungeon",[322,331])
    creatureDirectory.append(Red_Dragon)

    return creatureDirectory

def initNameDirectory():
    names = ["Abrielle", "Adara", "Alissa", "Amara", "Amelia", "Anya", "Aurelia", "Brielle", "Balthus",
             "Cara", "Cassius", "Cirius", "Corvo", "Darius", "Dagen", "Eira", "Elysia", "Finean", "Gareth",
             "Guinevere", "Hesperos", "Ignacio", "Isolde", "Jace", "Kara", "Kyra", "Kyrielle", "Leila",
             "Lilina", "Lucien", "Lucius", "Matthew", "Mathilda", "Natania", "Orion", "Orin", "Perseus", "Pyralia",
             "Quincy", "Rialda", "Sebastian", "Sirian", "Terra", "Thalia", "Torin", "Ulysses", "Vanora",
             "Xanthus", "Zeke", "Zorian"]
    return names
