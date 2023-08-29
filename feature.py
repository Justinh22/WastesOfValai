import pygame
import random
from directory import *
from constants import *

class Feature():
    def __init__(self,id=-1,name="",desc="",lootType=[Type.Empty],lootOdds=LootOdds.Impossible,lootRarity=LootRarity.Common):
        self.id = id                    # int : Numeric id of this Feature
        self.name = name                # String : Contains written name of this Feature
        self.description = desc         # String : Contains written description of this Feature
        self.lootType = lootType        # List of Type : Types of loot that could be contained in this Feature.
        self.lootOdds = lootOdds        # List of LootOdds : Odds of loot appearing in this Feature
        self.lootRarity = lootRarity    # List of LootRarity : Rarity of the potential item found in this feature, relative to party's power
        self.loot = Item()              # Item() Implementation : The loot item contained within this Feature, if applicable

    def rollForLoot(self,rarity):
        odds = random.randint(1,5)
        if self.lootOdds >= odds:
            itemRarity = rarity + self.lootRarity
            if itemRarity < 1:
                itemRarity = 1
            if itemRarity > 10:
                itemRarity = 10
            item = Directory.getItemByRarity(self.lootType,itemRarity)
        else:
            item = Item()
        self.loot = item


class FeatureList():
    def __init__(self):
        self.featureList = []       # List of Feature : Complete directory of all Features
        self.initFeatureList()

    def getFeature(self,id):
        return self.featureList[id] # This will only work as long as the ids in the featureList align with their index.
    
    def initFeatureList(self):
######################################################################## FEATURE LIST #########################################################################################
        Chest = Feature(0,"Chest","There is an unlocked, ornate-looking chest.",
                        [Type.Weapon,Type.Armor,Type.Potion], LootOdds.Definite, LootRarity.Rare)
        self.featureList.append(Chest)

        Spellbook = Feature(1,"Spellbook","An old, tattered spellbook, filled with runes.",
                            [Type.AtkSpell,Type.SptSpell], LootOdds.Definite, LootRarity.Uncommon)
        self.featureList.append(Spellbook)

        Table = Feature(2,"Table","A small, wooden table.",
                        [Type.Potion], LootOdds.Likely, LootRarity.Common)
        self.featureList.append(Table)

        Rug = Feature(3,"Rug","An old, tattered rug on the floor.",
                      [Type.Weapon,Type.Potion], LootOdds.Unlikely, LootRarity.Rare)
        self.featureList.append(Rug)

        Painting = Feature(4,"Painting","An old oil painting, depicting a figure holding an axe, silhouetted in red light.",
                           [Type.AtkSpell], LootOdds.Unlikely, LootRarity.Rare)
        self.featureList.append(Painting)

        Cobblestones = Feature(5,"Cobblestone Floor","Stones are wedged in next to each other, composing the floor.",
                               [Type.Potion], LootOdds.Likely, LootRarity.Common)
        self.featureList.append(Cobblestones)

        Dirt = Feature(6,"Dirt Floor","Soft dirt covers the floor of the room, with some mounds piled up throughout.",
                       [Type.Potion], LootOdds.VeryLikely, LootRarity.Common)
        self.featureList.append(Dirt)

        SuitOfArmor = Feature(7,"Suit of Armor","A suit of solid armor stands vigilantly.",
                              [Type.Weapon,Type.Armor], LootOdds.VeryLikely, LootRarity.Uncommon)
        self.featureList.append(SuitOfArmor)

        WhisperingSpirits = Feature(8,"Whispering Spirits","Apparitions drift around you, whispering affirmations, threats, and forbidden knowledge in your ear.",
                                    [Type.AtkSpell,Type.SptSpell], LootOdds.Unlikely, LootRarity.Rare)
        self.featureList.append(WhisperingSpirits)

        Runes = Feature(9,"Runes","Glowing symbols, indecipherable to you. They make your head hurt when you look at them...",
                        [Type.AtkSpell,Type.SptSpell], LootOdds.Definite, LootRarity.Common)
        self.featureList.append(Runes)

        StoneWalls = Feature(10,"Stone Walls","Flat stone walls, cracked and degraded from age.",
                             [Type.Empty], LootOdds.Impossible, LootRarity.Common)
        self.featureList.append(StoneWalls)

        BlackSlime = Feature(11,"Black Slime","A thick black slime. If you listen close enough, it seems to have a heartbeat...",
                             [Type.Weapon,Type.Potion], LootOdds.Unlikely, LootRarity.Common)
        self.featureList.append(BlackSlime)

        Lockbox = Feature(12,"Lockbox","A small metal box, with the lock seemingly smashed off...",
                          [Type.Weapon,Type.Armor,Type.Potion], LootOdds.Definite, LootRarity.Uncommon)
        self.featureList.append(Lockbox)

        AncientScroll = Feature(13,"Ancient Scroll","A tattered old scroll, detailing the casting of a powerful spell.",
                                [Type.AtkSpell,Type.SptSpell], LootOdds.Definite, LootRarity.Rare)
        self.featureList.append(AncientScroll)

        Hearth = Feature(14,"Hearth","The crackling fire in the hearth fills the room with warmth.",
                         [Type.Empty], LootOdds.Impossible, LootRarity.Common)
        self.featureList.append(Hearth)

        WoodenFloor_Normal = Feature(15,"Wooden Floor","Old wooden floorboards creak under your feet as you step.",
                                     [Type.Empty], LootOdds.Impossible, LootRarity.Common)
        self.featureList.append(WoodenFloor_Normal)

        WoodenFloor_Secret = Feature(16,"Wooden Floor","Old wooden floorboards creak under your feet as you step. You notice something under a loose board...",
                                     [Type.Weapon,Type.Armor], LootOdds.Definite, LootRarity.Uncommon)
        self.featureList.append(WoodenFloor_Secret)

        WoodenDesk = Feature(17,"Desk","A small wooden desk, with paper and other junk cluttering its surface.",
                       [Type.Potion,Type.AtkSpell,Type.SptSpell], LootOdds.Likely, LootRarity.Common)
        self.featureList.append(WoodenDesk)

        WeaponRack = Feature(18,"Weapon Rack","A wooden rack holding a variety of weapons. Most are rusted over.",
                             [Type.Weapon], LootOdds.Definite, LootRarity.Rare)
        self.featureList.append(WeaponRack)

        MetalShelf = Feature(19,"Metal Shelf","A solid steel shelf. Some random tools and pieces of equipment lie on its surface.",
                             [Type.Weapon,Type.Potion], LootOdds.Unlikely, LootRarity.Uncommon)
        self.featureList.append(MetalShelf)

        MetalTable = Feature(20,"Table","A solid metal table. Some random pieces of paper with intelligible writing cover its surface.",
                             [Type.AtkSpell,Type.SptSpell], LootOdds.Likely, LootRarity.Common)
        self.featureList.append(MetalTable)

        Altar = Feature(21,"Altar","A tall stone altar, carved with unusual designs and glyphs on its surface.",
                        [Type.AtkSpell,Type.SptSpell], LootOdds.VeryUnlikely, LootRarity.Uncommon)
        self.featureList.append(Altar)

        StoneWalls_Smooth = Feature(22,"Stone Walls","Flat stone walls that are incredibly smooth. They have an otherworldly quality to them.",
                             [Type.Empty], LootOdds.Impossible, LootRarity.Common)
        self.featureList.append(StoneWalls_Smooth)
##################################################################################################################################################################################