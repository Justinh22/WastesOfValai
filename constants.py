from enum import Enum

MAX_DIFFICULTY = 20
MAX_LEVEL = 10
MAX_WEAPON_RARITY = 10
MAX_ARMOR_RARITY = 10
MAX_POTION_RARITY = 5
MAX_ATKSPELL_RARITY = 5
MAX_SPTSPELL_RARITY = 5
MAX_ACCESSORY_RARITY = 3
MAX_CONSUMABLE_RARITY = 4
MAX_RUNE_RARITY = 1
MAX_INVENTORY_SIZE = 10

LANDMARK_COUNT = 300
MAP_GROWTH_CYCLES = 20
VILLAGE_WEIGHT = 4 # 1 in every VILLAGE_WEIGHT havens is a village
MAP_WIDTH = 250
MAP_HEIGHT = 250
DUNGEON_DIM = 40

DUNGEON_MAX_FLOORS = 5
DUNGEON_ENEMY_SPEED = 100

VILLAGE_DIM = 30
TOWN_DIM = 40
CITY_DIM = 50
BUILDING_TYPES = 9

FOREST_CHAR = '#'
PLAINS_CHAR = ';'
DESERT_CHAR = '.'
OCEAN_CHAR = '~'
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
VILLAGE_CHAR = 'V'

ATK_REFINE_BOOST = 2
ACC_REFINE_BOOST = 5
CRT_REFINE_BOOST = 3
DEF_REFINE_BOOST = 2
DDG_REFINE_BOOST = 5
MAX_REFINE_LEVEL = 5

KEYDOWN_START_DELAY = 15
KEYDOWN_DELAY = 12

class Type(Enum):
    Empty = 0
    Weapon = 1
    Armor = 2
    Potion = 3
    AtkSpell = 4
    SptSpell = 5
    Talent = 6
    Accessory = 7
    Food = 8
    Consumable = 9
    Rune = 10
    Creature = 11
    Class = 12

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

class VillageType(Enum):
    Village = 0
    Town = 1
    City = 2

class Personality(Enum):
    Brave = 0
    Angry = 1
    Friendly = 2
    Cowardly = 3
    Headstrong = 4
    Lazy = 5

class ActivationType(Enum):
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
    Anytime = 7
    Peacetime = 9
    OnDeath = 10

class VillageBuildings(Enum):
    Forge = 0
    Weaponsmith = 1
    Armory = 2
    GeneralStore = 3
    Library = 4
    Temple = 5
    BlackMarket = 6
    Inn = 7
    RuneCarver = 8

class ConsumableTiming(Enum):
    Anytime = 0
    CombatInturn = 1
    CombatInstant = 2
    OnDeath = 3
    Peacetime = 4
