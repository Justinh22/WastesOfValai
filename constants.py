from enum import Enum

MAX_DIFFICULTY = 20
MAX_LEVEL = 10
MAX_WEAPON_RARITY = 10
MAX_ARMOR_RARITY = 10
MAX_POTION_RARITY = 5
MAX_ATKSPELL_RARITY = 5
MAX_SPTSPELL_RARITY = 5
MAX_ACCESSORY_RARITY = 3
MAX_INVENTORY_SIZE = 10

LANDMARK_COUNT = 300
MAP_WIDTH = 250
MAP_HEIGHT = 250
DUNGEON_DIM = 40
DUNGEON_MAX_FLOORS = 5
DUNGEON_ENEMY_SPEED = 120
MAP_GROWTH_CYCLES = 20

FOREST_CHAR = '#'
PLAINS_CHAR = ';'
DESERT_CHAR = '.'
OCEAN_CHAR = ' '
BORDER_CHAR = 'X'
PATH_CHAR = '%'
WELL_CHAR = 'W'
PYRAMID_CHAR = 'P'
BANDITCAMP_CHAR = 'B'
CAVE_CHAR = 'C'
RUINS_CHAR = 'R'
TREEHOUSE_CHAR = 'T'

SHACK_CHAR = 'S'
ABANDONED_VILLAGE_CHAR = 'A'
HAVEN_CHAR = 'H'

class Type(Enum):
    Empty = 0
    Weapon = 1
    Armor = 2
    Potion = 3
    AtkSpell = 4
    SptSpell = 5
    Talent = 6
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

class TalentType(Enum):
    PartyEffect = 0
    EncounterEffect = 1
    Action = 2

class Target(Enum):
    Single = 0
    All = 1
    Self = 2
    Ally = 3
    Party = 4

class Biome(Enum):
    Forest = 0
    Plains = 1
    Desert = 2
    Other = 3
    Path = 4

class Status(Enum):
    Shocked = 0
    Ablaze = 1
    Freezing = 2
    NoStatus = 3

class DungeonType(Enum):
    Well = 0
    Pyramid = 1
    BanditCamp = 2
    Cave = 3
    Ruins = 4
    Treehouse = 5

class Personality(Enum):
    Brave = 0
    Angry = 1
    Friendly = 2
    Cowardly = 3
    Headstrong = 4
    Lazy = 5

class AccessoryType(Enum):
    Passive = 0
    Active = 1

class Timing(Enum):
    PreAttack = 0
    Targeting = 1
    DamageTaken = 2
    DamageDealt = 3
    Support = 3
    Universal = 4
    InTurn = 5
    Ordering = 6