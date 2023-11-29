from enum import Enum

MAX_DIFFICULTY = 25
MAX_WEAPON_RARITY = 10
MAX_ARMOR_RARITY = 10
MAX_POTION_RARITY = 5
MAX_ATKSPELL_RARITY = 5
MAX_SPTSPELL_RARITY = 5
MAX_INVENTORY_SIZE = 10

LANDMARK_COUNT = 500
MAP_WIDTH = 200
MAP_HEIGHT = 200
DUNGEON_DIM = 40
MAP_GROWTH_CYCLES = 30

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

class WeaponType(Enum):
    Axe = 0
    Spear = 1
    Sword = 2
    Dagger = 3
    Staff = 4

class ArmorType(Enum):
    Light = 0
    Medium = 1
    Heavy = 2
    Robe = 3
    Arcanist = 4

class Element(Enum):
    Lightning = 0
    Fire = 1
    Ice = 2

class SpellType(Enum):
    Attack = 0
    Debuff = 1
    Buff = 2
    Heal = 3
    Raise = 4
    Cleanse = 5

class Target(Enum):
    Single = 0
    All = 0

class Biome(Enum):
    Forest = 0
    Plains = 1
    Desert = 2
    Dungeon = 3

class Status(Enum):
    Paralyzed = 0
    Burned = 1
    Freezing = 2

class DungeonType(Enum):
    Well = 0
    Pyramid = 1
    BanditCamp = 2
    Cave = 3
    Ruins = 4
    Treehouse = 5