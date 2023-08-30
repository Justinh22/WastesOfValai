import pygame
import random
from enum import Enum

class Type(Enum):
    Empty = 0
    Weapon = 1
    Armor = 2
    Potion = 3
    AtkSpell = 4
    SptSpell = 5
    Skill = 6
    Accessory = 7
    Creature = 8
    Class = 9

class LootOdds(Enum):
    Impossible = 0
    VeryUnlikely = 1
    Unlikely = 2
    Likely = 3
    VeryLikely = 4
    Definite = 5

class LootRarity(Enum):
    Common = -1
    Uncommon = 0
    Rare = 1

class LootStatus(Enum):
    Undiscovered = 0
    Discovered = 1
    Taken = 2