import pygame
import random
from directory import *
from constants import *

class Feature():
    def __init__(self,id=-1,names=[],desc="",lootType=[Type.Empty],lootOdds=LootOdds.Impossible,lootRarity=LootRarity.Common):
        self.id = id
        self.names = names
        self.description = desc
        self.lootType = lootType        # Types of loot that could be contained in this feature.
        self.lootOdds = lootOdds        # Odds of loot appearing in this feature
        self.lootRarity = lootRarity    # Rarity of the potential item found in this feature, relative to party's power
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
        return item

class FeatureList():
    def __init__(self):
        self.featureList = []
        self.initFeatureList()
    def initFeatureList(self):
######################################################################## FEATURE LIST #########################################################################################
        Chest = Feature(0,["chest","box","treasure","treasure chest"],"There is an unlocked chest.",
                        [Type.Weapon,Type.Armor,Type.Potion,Type.AtkSpell,Type.SptSpell], LootOdds.Definite, LootRarity.Uncommon)
        self.featureList.append(Chest)

        Spellbook = Feature(1,["book","tattered book","spellbook","spell book","old book"],"An old, tattered spellbook, filled with runes.",
                            [Type.AtkSpell,Type.SptSpell], LootOdds.Definite, LootRarity.Uncommon)
        self.featureList.append(Spellbook)

        Table = Feature(2,["table","wooden table","small table"],"A small, wooden table.",
                        [Type.Potion], LootOdds.Likely, LootRarity.Common)
        self.featureList.append(Table)

        Rug = Feature(3,["rug","tattered rug","carpet"],"An old, tattered carpet on the floor.",
                      [Type.Weapon,Type.Potion], LootOdds.Unlikely, LootRarity.Rare)
        self.featureList.append(Rug)
