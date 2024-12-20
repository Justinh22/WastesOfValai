import pygame
from itemclasses import *
from constants import *

######### WEAPONS #########
def initWeaponDirectory():
    weaponDirectory = []

    #1
    Rusty_Axe = Weapon("Rusty Axe","A dull axe, coated in rust.",1,0,10,60,0,0,WeaponType.Axe)
    weaponDirectory.append(Rusty_Axe)
    Rusty_Sword = Weapon("Rusty Sword","A dull blade, coated in rust.",1,1,9,65,0,0,WeaponType.Sword)
    weaponDirectory.append(Rusty_Sword)
    Rusty_Spear = Weapon("Rusty Spear","A dull spear, coated in rust.",1,2,8,70,0,0,WeaponType.Spear)
    weaponDirectory.append(Rusty_Spear)
    Rusty_Dagger = Weapon("Rusty Dagger","A dull knife, coated in rust.",1,3,7,75,5,0,WeaponType.Dagger)
    weaponDirectory.append(Rusty_Dagger)
    Rusty_Sceptre = Weapon("Rusty Sceptre","A bent metal staff, coated in rust.",1,4,5,70,0,5,WeaponType.Staff)
    weaponDirectory.append(Rusty_Sceptre)

    #2
    Jagged_Axe = Weapon("Jagged Axe","A hastily-crafted iron axe, with a sharp and jagged edge.",2,5,12,70,5,0,WeaponType.Axe)
    weaponDirectory.append(Jagged_Axe)
    Crooked_Saber = Weapon("Crooked Saber","A jagged iron blade, resembling a long piece of schrapnel.",2,6,11,75,0,0,WeaponType.Sword)
    weaponDirectory.append(Crooked_Saber)
    Vicious_Pike = Weapon("Vicious Pike","A long spear, with a sharp shard of iron affixed to the end.",2,7,10,80,0,0,WeaponType.Spear)
    weaponDirectory.append(Vicious_Pike)
    Crooked_Dagger = Weapon("Crooked Dagger","A sharp fragment of metal, shaped into a dagger.",2,8,9,85,10,0,WeaponType.Dagger)
    weaponDirectory.append(Crooked_Dagger)
    Gnarled_Rod = Weapon("Gnarled Rod","A tangled wooden rod, containing a green gem at its top.",2,9,7,75,0,10,WeaponType.Staff)
    weaponDirectory.append(Gnarled_Rod)

    #3
    Iron_Axe = Weapon("Iron Axe","A sturdy iron axe.",3,10,14,70,5,0,WeaponType.Axe)
    weaponDirectory.append(Iron_Axe)
    Iron_Sword = Weapon("Iron Sword","A sturdy iron sword.",3,11,13,80,0,0,WeaponType.Sword)
    weaponDirectory.append(Iron_Sword)
    Iron_Spear = Weapon("Iron Spear","A sturdy iron spear.",3,12,12,85,0,0,WeaponType.Spear)
    weaponDirectory.append(Iron_Spear)
    Iron_Dagger = Weapon("Iron Dagger","A sturdy iron dagger.",3,13,11,90,10,0,WeaponType.Dagger)
    weaponDirectory.append(Iron_Dagger)
    Iron_Sceptre = Weapon("Iron Sceptre","A tall iron staff, woven around a sapphire.",3,14,9,80,0,15,WeaponType.Staff)
    weaponDirectory.append(Iron_Sceptre)

    #4
    Steel_Axe = Weapon("Steel Axe","A sharp, shining steel axe.",4,15,16,75,5,0,WeaponType.Axe)
    weaponDirectory.append(Steel_Axe)
    Steel_Sword = Weapon("Steel Sword","A sharp, shining steel sword.",4,16,15,80,0,0,WeaponType.Sword)
    weaponDirectory.append(Steel_Sword)
    Steel_Spear = Weapon("Steel Spear","A sharp, shining steel spear.",4,17,14,85,0,0,WeaponType.Spear)
    weaponDirectory.append(Steel_Spear)
    Steel_Dagger = Weapon("Steel Dagger","A sharp, shining steel dagger.",4,18,13,90,10,0,WeaponType.Dagger)
    weaponDirectory.append(Steel_Dagger)
    Steel_Wand = Weapon("Steel Wand","A long, shining steel wand.",4,19,11,80,0,20,WeaponType.Staff)
    weaponDirectory.append(Steel_Wand)

    #5
    Ebonite_Axe = Weapon("Ebonite Axe","An axe made of a dark, menacing steel, emanating an evil aura.",5,20,19,70,15,0,WeaponType.Axe)
    weaponDirectory.append(Ebonite_Axe)
    Ebonite_Sword = Weapon("Ebonite Sword","A sword made of a dark, menacing steel, emanating an evil aura.",5,21,17,75,10,0,WeaponType.Sword)
    weaponDirectory.append(Ebonite_Sword)
    Ebonite_Spear = Weapon("Ebonite Spear","A spear made of a dark, menacing steel, emanating an evil aura.",5,22,16,80,15,0,WeaponType.Spear)
    weaponDirectory.append(Ebonite_Spear)
    Ebonite_Dagger = Weapon("Ebonite Dagger","A dagger made of a dark, menacing steel, emanating an evil aura.",5,23,14,85,20,0,WeaponType.Dagger)
    weaponDirectory.append(Ebonite_Dagger)
    Ebonite_Sceptre = Weapon("Ebonite Sceptre","A long, menacing sceptre made of a dark black metal.",5,24,12,80,10,25,WeaponType.Staff)
    weaponDirectory.append(Ebonite_Sceptre)

    #6
    Golden_Axe = Weapon("Golden Axe","An axe made of shimmering gold.",6,25,22,80,5,0,WeaponType.Axe)
    weaponDirectory.append(Golden_Axe)
    Golden_Sword = Weapon("Golden Sword","A sword made of shimmering gold.",6,26,20,85,0,0,WeaponType.Sword)
    weaponDirectory.append(Golden_Sword)
    Golden_Spear = Weapon("Golden Spear","A spear made of shimmering gold.",6,27,19,90,0,0,WeaponType.Spear)
    weaponDirectory.append(Golden_Spear)
    Golden_Dagger = Weapon("Golden Dagger","A dagger made of shimmering gold.",6,28,17,95,10,0,WeaponType.Dagger)
    weaponDirectory.append(Golden_Dagger)
    Golden_Staff = Weapon("Golden Staff","A shining, golden staff, radiating magical energy.",6,29,15,85,0,30,WeaponType.Staff)
    weaponDirectory.append(Golden_Staff)

    #7
    Runic_Axe = Weapon("Runic Axe","An axe made of shining steel, with shimmering runes etched into it.",7,30,24,85,5,10,WeaponType.Axe)
    weaponDirectory.append(Runic_Axe)
    Runic_Sword = Weapon("Runic Sword","A sword made of shining steel, with shimmering runes etched into it.",7,31,22,90,0,10,WeaponType.Sword)
    weaponDirectory.append(Runic_Sword)
    Runic_Spear = Weapon("Runic Spear","A spear made of shining steel, with shimmering runes etched into it.",7,32,21,95,0,10,WeaponType.Spear)
    weaponDirectory.append(Runic_Spear)
    Runic_Dagger = Weapon("Runic Dagger","A dagger made of shining steel, with shimmering runes etched into it.",7,33,19,100,10,10,WeaponType.Dagger)
    weaponDirectory.append(Runic_Dagger)
    Runic_Wand = Weapon("Runic Wand","A powerful steel wand, with shimmering runes etched into it.",7,34,17,90,0,45,WeaponType.Staff)
    weaponDirectory.append(Runic_Wand)

    #8
    Valentium_Axe = Weapon("Valentium Axe","An axe made of a magical, indestructable metal.",8,35,26,85,5,5,WeaponType.Axe)
    weaponDirectory.append(Valentium_Axe)
    Valentium_Sword = Weapon("Valentium Sword","A sword made of a magical, indestructable metal.",8,36,24,90,0,5,WeaponType.Sword)
    weaponDirectory.append(Valentium_Sword)
    Valentium_Spear = Weapon("Valentium Spear","A spear made of a magical, indestructable metal.",8,37,23,95,0,5,WeaponType.Spear)
    weaponDirectory.append(Valentium_Spear)
    Valentium_Dagger = Weapon("Valentium Dagger","An dagger made of a magical, indestructable metal.",8,38,21,100,10,5,WeaponType.Dagger)
    weaponDirectory.append(Valentium_Dagger)
    Valentium_Sceptre = Weapon("Valentium Sceptre","A sceptre made of a magical, indestructable metal.",8,39,19,90,0,40,WeaponType.Staff)
    weaponDirectory.append(Valentium_Sceptre)

    #9
    Mechanical_Axe = Weapon("Mechanical Axe","An axe covered in whirring gears, arcing with electricity.",9,40,29,85,15,0,WeaponType.Axe)
    weaponDirectory.append(Mechanical_Axe)
    Mechanical_Sword = Weapon("Mechanical Sword","A sword covered in whirring gears, arcing with electricity.",9,41,27,90,10,0,WeaponType.Sword)
    weaponDirectory.append(Mechanical_Sword)
    Mechanical_Spear = Weapon("Mechanical Spear","A spear covered in whirring gears, arcing with electricity.",9,42,26,95,10,0,WeaponType.Spear)
    weaponDirectory.append(Mechanical_Spear)
    Mechanical_Dagger = Weapon("Mechanical Dagger","A dagger covered in whirring gears, arcing with electricity.",9,43,24,100,20,0,WeaponType.Dagger)
    weaponDirectory.append(Mechanical_Dagger)
    Rod_of_Order = Weapon("Rod of Order","A magic staff, covered in spinning gears.",9,44,22,90,20,45,WeaponType.Staff)
    weaponDirectory.append(Rod_of_Order)

    #10
    Teratra = Weapon("Teratra","A mythical axe of legend, raised from the earth.",10,45,34,80,10,5,WeaponType.Axe)
    weaponDirectory.append(Teratra)
    Pyrithia = Weapon("Pyrithia","A mythical sword of legend, born from flame.",10,46,32,90,5,10,WeaponType.Sword)
    weaponDirectory.append(Pyrithia)
    Hyliat = Weapon("Hyliat","A mythical spear of legend, created in the depths of the ocean.",10,47,31,95,10,10,WeaponType.Spear)
    weaponDirectory.append(Hyliat)
    Aerolinde = Weapon("Aerolinde","A mythical dagger of legend, formed from the raging winds.",10,48,29,100,30,10,WeaponType.Dagger)
    weaponDirectory.append(Aerolinde)
    Ordointh = Weapon("Ordointh","A magical staff of legend, formed from the forces of balance and order.",10,49,27,90,5,50,WeaponType.Staff)
    weaponDirectory.append(Ordointh)

    return weaponDirectory

########## ARMOR ##########

def initArmorDirectory():
    armorDirectory = []

    #1
    Light_Rusty_Armor = Armor("Light Rusty Armor","A tough, leather breastplate.",1,100,0,10,0,ArmorType.Light)
    armorDirectory.append(Light_Rusty_Armor)
    Rusty_Armor = Armor("Rusty Armor","A tough, leather breastplate.",1,101,2,5,0,ArmorType.Medium)
    armorDirectory.append(Rusty_Armor)
    Heavy_Rusty_Armor = Armor("Heavy Rusty Armor","A rusted iron breastplate.",1,102,4,0,0,ArmorType.Heavy)
    armorDirectory.append(Heavy_Rusty_Armor)
    Tattered_Robe = Armor("Tattered Robe","A tattered, cloth robe.",1,103,0,5,2,ArmorType.Robe)
    armorDirectory.append(Tattered_Robe)

    #2
    Leather_Armor = Armor("Leather Armor","A suit of sturdy leather armor.",2,104,2,10,0,ArmorType.Light)
    armorDirectory.append(Leather_Armor)
    Studded_Leather_Armor = Armor("Studded Leather Armor","A suit of leather armor, studded with steel.",2,105,4,5,0,ArmorType.Medium)
    armorDirectory.append(Studded_Leather_Armor)
    Chainmail = Armor("Chainmail","A suit of armor made from intertwined links of chains.",2,106,6,0,0,ArmorType.Heavy)
    armorDirectory.append(Chainmail)
    Silk_Robe = Armor("Silk Robe","A soft, silk robe.",2,107,1,0,3,ArmorType.Robe)
    armorDirectory.append(Silk_Robe)

    #3
    Light_Iron_Armor = Armor("Light Iron Armor","A partial suit of armor made from solid iron.",3,108,4,15,0,ArmorType.Light)
    armorDirectory.append(Light_Iron_Armor)
    Iron_Armor = Armor("Iron Armor","A suit of solid iron armor.",3,109,6,5,0,ArmorType.Medium)
    armorDirectory.append(Iron_Armor)
    Heavy_Iron_Armor = Armor("Heavy Iron Armor","A thick suit of solid iron armor.",3,110,8,0,0,ArmorType.Heavy)
    armorDirectory.append(Heavy_Iron_Armor)
    Shimmering_Robe = Armor("Shimmering Robe","A long velvet robe, that seems to shimmer magically.",3,111,3,5,4,ArmorType.Robe)
    armorDirectory.append(Shimmering_Robe)
    #4
    Light_Steel_Armor = Armor("Light Steel Armor","A suit of lightweight steel armor.",4,112,6,15,0,ArmorType.Light)
    armorDirectory.append(Light_Steel_Armor)
    Steel_Armor = Armor("Steel Armor","A suit of standard steel armor.",4,113,8,5,0,ArmorType.Medium)
    armorDirectory.append(Steel_Armor)
    Heavy_Steel_Armor = Armor("Heavy Steel Armor","A suit of heavy steel armor.",4,114,10,0,0,ArmorType.Heavy)
    armorDirectory.append(Heavy_Steel_Armor)
    Enchanted_Robe = Armor("Enchanted Robe","An enchanted robe, which glows magically.",4,115,5,10,5,ArmorType.Robe)
    armorDirectory.append(Enchanted_Robe)
    #5
    Light_Ebonite_Armor = Armor("Light Ebonite Armor","A suit of lightweight ebonite armor.",5,116,8,15,0,ArmorType.Light)
    armorDirectory.append(Light_Ebonite_Armor)
    Ebonite_Armor = Armor("Ebonite Armor","A suit of standard ebonite armor.",5,117,10,5,0,ArmorType.Medium)
    armorDirectory.append(Ebonite_Armor)
    Heavy_Ebonite_Armor = Armor("Heavy Ebonite Armor","A suit of heavy ebonite armor.",5,118,12,0,0,ArmorType.Heavy)
    armorDirectory.append(Heavy_Ebonite_Armor)
    Amethyst_Robe = Armor("Amethyst Robe","A bright purple robe, pulsing with dark energy.",5,119,5,10,6,ArmorType.Robe)
    armorDirectory.append(Amethyst_Robe)
    Ebonite_Arcanist_Armor = Armor("Ebonite Arcanist Armor","A set of ebonite battlemage armor, with magical capabilities.",6,120,6,5,2,ArmorType.Arcanist)
    armorDirectory.append(Ebonite_Arcanist_Armor)
    #6
    Light_Golden_Armor = Armor("Light Golden Armor","A suit of lightweight golden armor.",6,121,9,20,0,ArmorType.Light)
    armorDirectory.append(Light_Golden_Armor)
    Golden_Armor = Armor("Golden Armor","A suit of standard golden armor.",6,122,12,10,0,ArmorType.Medium)
    armorDirectory.append(Golden_Armor)
    Heavy_Golden_Armor = Armor("Heavy Golden Armor","A suit of heavy golden armor.",6,123,14,0,0,ArmorType.Heavy)
    armorDirectory.append(Heavy_Golden_Armor)
    Gilded_Robe = Armor("Gilded Robe","A flowing robe sewn from golden threads, imbued with magical power.",6,124,8,15,7,ArmorType.Robe)
    armorDirectory.append(Gilded_Robe)
    Golden_Arcanist_Armor = Armor("Golden Arcanist Armor","A set of golden battlemage armor, with magical capabilities.",6,125,10,10,3,ArmorType.Arcanist)
    armorDirectory.append(Golden_Arcanist_Armor)
    #7
    Light_Runic_Armor = Armor("Light Runic Armor","A suit of lightweight steel armor inscribed with ancient runes.",7,126,11,25,1,ArmorType.Light)
    armorDirectory.append(Light_Runic_Armor)
    Runic_Armor = Armor("Runic Armor","A suit of standard steel armor inscribed with ancient runes.",7,127,14,15,1,ArmorType.Medium)
    armorDirectory.append(Runic_Armor)
    Heavy_Runic_Armor = Armor("Heavy Runic Armor","A suit of heavy steel armor inscribed with ancient runes.",7,128,16,0,1,ArmorType.Heavy)
    armorDirectory.append(Heavy_Runic_Armor)
    Runic_Robe = Armor("Runic Robe","A flowing robe sewn from golden threads, with arcane runes inscribed at the base.",8,129,10,20,8,ArmorType.Robe)
    armorDirectory.append(Runic_Robe)
    Runic_Arcanist_Armor = Armor("Runic Arcanist Armor","A suit of steel armor, inscribed with ancient runes.",8,130,12,15,4,ArmorType.Arcanist)
    armorDirectory.append(Runic_Arcanist_Armor)
    #8
    Light_Valentium_Armor = Armor("Light Valentium Armor","A suit of lightweight Valentium armor, which pulses with magical energy.",8,131,13,30,2,ArmorType.Light)
    armorDirectory.append(Light_Valentium_Armor)
    Valentium_Armor = Armor("Valentium Armor","A suit of Valentium armor, which pulses with magical energy.",8,132,17,15,2,ArmorType.Medium)
    armorDirectory.append(Valentium_Armor)
    Heavy_Valentium_Armor = Armor("Heavy Valentium Armor","A suit of heavy Valentium armor, which pulses with magical energy.",8,133,21,0,2,ArmorType.Heavy)
    armorDirectory.append(Heavy_Valentium_Armor)
    Valentium_Robe = Armor("Valentium Robe","A robe sewn from threads of Valentium, which pulses with magical energy.",8,134,12,25,9,ArmorType.Robe)
    armorDirectory.append(Valentium_Robe)
    Valentium_Arcanist_Armor = Armor("Valentium Arcanist Armor","A set of Valentium battlemage armor, which pulses with unbridled magical energy.",8,135,15,15,5,ArmorType.Arcanist)
    armorDirectory.append(Valentium_Arcanist_Armor)
    #9
    Light_Mechanical_Armor = Armor("Light Mechanical Armor","A suit of lightweight armor with cogs and pipes whirring along it.",9,136,14,40,0,ArmorType.Light)
    armorDirectory.append(Light_Mechanical_Armor)
    Mechanical_Armor = Armor("Mechanical Armor","A suit of armor with cogs and pipes whirring along it.",9,137,18,20,0,ArmorType.Medium)
    armorDirectory.append(Mechanical_Armor)
    Heavy_Mechanical_Armor = Armor("Heavy Mechanical Armor","A suit of heavy armor with cogs and pipes whirring along it.",9,138,22,10,0,ArmorType.Heavy)
    armorDirectory.append(Heavy_Mechanical_Armor)
    Clockwork_Robe = Armor("Clockwork Robe","A robe sewn from threads of time itself.",9,139,12,25,10,ArmorType.Robe)
    armorDirectory.append(Clockwork_Robe)
    Clockwork_Arcanist_Armor = Armor("Clockwork Arcanist Armor","A set of clockwork battlemage armor, with magical energy flowing through it like time itself.",9,140,16,15,6,ArmorType.Arcanist)
    armorDirectory.append(Clockwork_Arcanist_Armor)
    #10
    Cloak_of_the_Whisper = Armor("Cloak of the Whisper","A cloak that envelops its wearer in shadow.",10,141,16,50,1,ArmorType.Light)
    armorDirectory.append(Cloak_of_the_Whisper)
    Plate_of_the_Vanguard = Armor("Plate of the Vanguard","A suit of regal armor worn by a hero of legend.",10,142,21,25,1,ArmorType.Medium)
    armorDirectory.append(Plate_of_the_Vanguard)
    Shield_of_the_Conquerer = Armor("Shield of the Conquerer","A massive suit of heavy armor once worn by the ruler of an ancient kingdom.",10,143,26,0,1,ArmorType.Heavy)
    armorDirectory.append(Shield_of_the_Conquerer)
    Robe_of_the_Archmage = Armor("Robe of the Archmage","A robe that harnesses the magical power of the world.",10,144,14,25,15,ArmorType.Robe)
    armorDirectory.append(Robe_of_the_Archmage)
    Helm_of_the_Ancients = Armor("Helm of the Ancients","A demigod's suit of armor, passed down from an ancient kingdom of magic.",10,145,19,25,10,ArmorType.Arcanist)
    armorDirectory.append(Helm_of_the_Ancients)

    return armorDirectory

########## POTIONS ##########

def initPotionDirectory():
    potionDirectory = []

    #1
    Potion_of_Minor_Healing = Potion("Minor Healing Potion","A potion capable of restoring a meager amount of life.",1,200,30,0)
    potionDirectory.append(Potion_of_Minor_Healing)
    Potion_of_Minor_Calming = Potion("Minor Calming Potion","A potion capable of restoring a meager amount of magical ability.",1,201,0,30)
    potionDirectory.append(Potion_of_Minor_Calming)
    #2
    Potion_of_Lesser_Healing = Potion("Lesser Healing Potion","A potion capable of restoring a small amount of life.",2,202,70,0)
    potionDirectory.append(Potion_of_Lesser_Healing)
    Potion_of_Lesser_Calming = Potion("Lesser Calming Potion","A potion capable of restoring a small amount of magical ability.",2,203,0,70)
    potionDirectory.append(Potion_of_Lesser_Calming)
    #3
    Potion_of_Healing = Potion("Healing Potion","A potion capable of restoring life.",3,204,100,0)
    potionDirectory.append(Potion_of_Healing)
    Potion_of_Calming = Potion("Calming Potion","A potion capable of restoring magical ability.",3,205,0,100)
    potionDirectory.append(Potion_of_Calming)
    #4
    Potion_of_Greater_Healing = Potion("Greater Healing Potion","A potion capable of restoring a great amount of life.",4,206,150,0)
    potionDirectory.append(Potion_of_Greater_Healing)
    Potion_of_Greater_Calming = Potion("Greater Calming Potion","A potion capable of restoring a great amount of magical ability.",4,207,0,150)
    potionDirectory.append(Potion_of_Greater_Calming)
    Potion_of_Replenishment = Potion("Replenishment Potion","A potion capable of restoring both life and magical ability.",4,208,70,70)
    potionDirectory.append(Potion_of_Replenishment)
    #5
    Potion_of_Major_Healing = Potion("Major Healing Potion","A potion capable of restoring a massive amount of life.",5,209,250,0)
    potionDirectory.append(Potion_of_Major_Healing)
    Potion_of_Major_Calming = Potion("Major Calming Potion","A potion capable of restoring a massive amount of magical ability.",5,210,0,250)
    potionDirectory.append(Potion_of_Major_Calming)
    Potion_of_Greater_Replenishment = Potion("Gr. Replenishment Potion","A potion capable of restoring both life and magical ability.",5,211,100,100)
    potionDirectory.append(Potion_of_Greater_Replenishment)

    return potionDirectory

########## ATTACK SPELLS ##########

def initAtkSpellDirectory():
    attackSpellDirectory = []

    #1
    Jolt = AttackMagic("Jolt","Fires a small jolt of lightning at a target.",1,300,10,20,SpellType.Attack,Element.Lightning,Target.Single)
    attackSpellDirectory.append(Jolt)
    Ember = AttackMagic("Ember","Fires a small burst of flame at a target.",1,301,9,18,SpellType.Attack,Element.Fire,Target.Single)
    attackSpellDirectory.append(Ember)
    Frostbite = AttackMagic("Frostbite","Fires a small burst of cold at a target.",1,302,8,16,SpellType.Attack,Element.Ice,Target.Single)
    attackSpellDirectory.append(Frostbite)
    #2
    Thunderbolt = AttackMagic("Thunderbolt","Fires a bolt of lightning at a target.",2,303,16,36,SpellType.Attack,Element.Lightning,Target.Single)
    attackSpellDirectory.append(Thunderbolt)
    Firebolt = AttackMagic("Firebolt","Fires a bolt of fire at a target.",2,304,15,34,SpellType.Attack,Element.Fire,Target.Single)
    attackSpellDirectory.append(Firebolt)
    Frostbolt = AttackMagic("Frostbolt","Fires a bolt of freezing energy at a target.",2,305,14,32,SpellType.Attack,Element.Ice,Target.Single)
    attackSpellDirectory.append(Frostbolt)
    Thunder_Wave = AttackMagic("Thunder Wave","Summons a wave of electricity toward all foes.",2,306,28,20,SpellType.Attack,Element.Lightning,Target.All)
    attackSpellDirectory.append(Thunder_Wave)
    Fire_Wave = AttackMagic("Fire Wave","Summons a wave of flame toward all foes.",2,307,26,18,SpellType.Attack,Element.Fire,Target.All)
    attackSpellDirectory.append(Fire_Wave)
    Frost_Wave = AttackMagic("Frost Wave","Summons a wave of ice toward all foes.",2,308,24,16,SpellType.Attack,Element.Ice,Target.All)
    attackSpellDirectory.append(Frost_Wave)
    #3
    Lightning_Strike = AttackMagic("Lightning Strike","Strikes down a bolt of lightning at a target.",3,309,24,52,SpellType.Attack,Element.Lightning,Target.Single)
    attackSpellDirectory.append(Lightning_Strike)
    Fireball = AttackMagic("Fireball","Hurls a fireball at a target.",3,310,23,50,SpellType.Attack,Element.Fire,Target.Single)
    attackSpellDirectory.append(Fireball)
    Hail = AttackMagic("Hail","Launches a blast of freezing magic at a target.",3,311,22,48,SpellType.Attack,Element.Ice,Target.Single)
    attackSpellDirectory.append(Hail)
    Thunder_Wave_II = AttackMagic("Thunder Wave II","Hurls a large wave of electricity toward all foes.",3,312,40,36,SpellType.Attack,Element.Lightning,Target.All)
    attackSpellDirectory.append(Thunder_Wave_II)
    Fire_Wave_II = AttackMagic("Fire Wave II","Hurls a large wave of flame toward all foes.",3,313,38,34,SpellType.Attack,Element.Fire,Target.All)
    attackSpellDirectory.append(Fire_Wave_II)
    Frost_Wave_II = AttackMagic("Frost Wave II","Hurls a large wave of ice toward all foes.",3,314,36,32,SpellType.Attack,Element.Ice,Target.All)
    attackSpellDirectory.append(Frost_Wave_II)
    #4
    Electrocute = AttackMagic("Electrocute","Unleashes a massive jolt of electricity at a target.",4,315,32,68,SpellType.Attack,Element.Lightning,Target.Single)
    attackSpellDirectory.append(Electrocute)
    Fire_Blast = AttackMagic("Fire Blast","Unleashes a blast of flame at a target.",4,316,31,66,SpellType.Attack,Element.Fire,Target.Single)
    attackSpellDirectory.append(Fire_Blast)
    Cryo_Beam = AttackMagic("Cryo Beam","Fires a beam of pure freezing magic at a target.",4,317,30,64,SpellType.Attack,Element.Ice,Target.Single)
    attackSpellDirectory.append(Cryo_Beam)
    Thunder_Wave_III = AttackMagic("Thunder Wave III","Launches a massive wave of electricity toward all foes.",4,318,52,52,SpellType.Attack,Element.Lightning,Target.All)
    attackSpellDirectory.append(Thunder_Wave_III)
    Fire_Wave_III = AttackMagic("Fire Wave III","Launches a massive wave of flame toward all foes.",4,319,50,50,SpellType.Attack,Element.Fire,Target.All)
    attackSpellDirectory.append(Fire_Wave_III)
    Frost_Wave_III = AttackMagic("Frost Wave III","Launches a massive wave of ice toward all foes.",4,320,48,48,SpellType.Attack,Element.Ice,Target.All)
    attackSpellDirectory.append(Frost_Wave_III)
    #5
    Thunderstorm = AttackMagic("Thunderstorm","Calls down a raging storm to electrify all enemies.",5,321,40,84,SpellType.Attack,Element.Lightning,Target.All)
    attackSpellDirectory.append(Thunderstorm)
    Inferno = AttackMagic("Inferno","Calls a raging inferno to incinerate all enemies.",5,322,39,82,SpellType.Attack,Element.Fire,Target.All)
    attackSpellDirectory.append(Inferno)
    Blizzard = AttackMagic("Blizzard","Calls a raging blizzard to freeze all enemies.",5,323,38,80,SpellType.Attack,Element.Ice,Target.All)
    attackSpellDirectory.append(Blizzard)

    #DEBUFFS

    # SHOCK: Has a 50% chance to have action cancelled. DDG is set to 0%. Moved to last in the combat order.
    # ABLAZE: Takes damage equal to 10% of max hp each turn. ACC is reduced by 33%.
    # FREEZING: Has a 50% chance to have action cancelled. Unable to cast spells. Saps 10% of max mp each turn. 
    Shock = AttackMagic("Shock","Has a chance to inflict Shocked on a target.",2,324,18,0,SpellType.Debuff,Element.Lightning,Target.Single)
    attackSpellDirectory.append(Shock)
    Ablaze = AttackMagic("Ablaze","Has a chance to inflict Ablaze on a target.",2,325,18,0,SpellType.Debuff,Element.Fire,Target.Single)
    attackSpellDirectory.append(Ablaze)
    Freeze = AttackMagic("Freeze","Has a chance to inflict Freezing on a target.",2,326,18,0,SpellType.Debuff,Element.Ice,Target.Single)
    attackSpellDirectory.append(Freeze)

    Shock_II = AttackMagic("Shock II","Inflicts Shocked on a target.",3,327,30,0,SpellType.Debuff,Element.Lightning,Target.Single)
    attackSpellDirectory.append(Shock_II)
    Ablaze_II = AttackMagic("Ablaze II","Inflicts Ablaze on a target.",3,328,30,0,SpellType.Debuff,Element.Fire,Target.Single)
    attackSpellDirectory.append(Ablaze_II)
    Freeze_II = AttackMagic("Freeze II","Inflicts Freezing on a target.",3,329,30,0,SpellType.Debuff,Element.Ice,Target.Single)
    attackSpellDirectory.append(Freeze_II)

    Shock_Wave = AttackMagic("Shock Wave","Has a chance to inflict Shocked on all targets.",4,330,50,0,SpellType.Debuff,Element.Lightning,Target.All)
    attackSpellDirectory.append(Shock_Wave)
    Ablaze_Wave = AttackMagic("Ablaze Wave","Has a chance to inflict Ablaze on all targets.",4,331,50,0,SpellType.Debuff,Element.Fire,Target.All)
    attackSpellDirectory.append(Ablaze_Wave)
    Freeze_Wave = AttackMagic("Freeze Wave","Has a chance to inflict Freezing on all targets.",4,332,50,0,SpellType.Debuff,Element.Ice,Target.All)
    attackSpellDirectory.append(Freeze_Wave)

    return attackSpellDirectory

########## SUPPORT SPELLS ##########

def initSptSpellDirectory():
    sptSpellDirectory = []

    # [ ATK ACC CRT DEF DDG LCK HP ]

    #1
    Rage =  SupportMagic("Rage","Increases Atk.",1,400,[10,0,0,0,0,0,0],16,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Rage)
    Focus = SupportMagic("Focus","Increases Acc.",1,401,[0,15,0,0,0,0,0],16,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Focus)
    Sense = SupportMagic("Sense","Increases Crt.",1,402,[0,0,15,0,0,0,0],16,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Sense)
    Brace = SupportMagic("Brace","Increases Def.",1,403,[0,0,0,10,0,0,0],16,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Brace)
    Speed = SupportMagic("Speed","Increases Ddg.",1,404,[0,0,0,0,15,0,0],16,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Speed)
    Fortune = SupportMagic("Fortune","Increases Lck.",1,405,[0,0,0,0,0,15,0],16,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Fortune)
    Minor_Heal = SupportMagic("Minor Heal","Heals for a small amount of health.",1,406,[0,0,0,0,0,0,30],16,SpellType.Heal,Target.Single)
    sptSpellDirectory.append(Minor_Heal)
    #2
    Rally = SupportMagic("Rally","Increases Atk and Def.",2,407,[10,0,0,10,0,0,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Rally)
    Wrath = SupportMagic("Wrath","Increases Atk and Acc.",2,408,[10,15,0,0,0,0,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Wrath)
    Precision = SupportMagic("Precision","Increases Acc and Crt.",2,409,[0,15,15,0,0,0,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Precision)
    Trance = SupportMagic("Trance","Increases Acc and Ddg.",2,410,[0,15,0,0,15,0,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Trance)
    Veil = SupportMagic("Veil","Increases Def and Ddg.",2,411,[0,0,0,10,15,0,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Veil)
    Fate = SupportMagic("Fate","Increases Crt and Lck.",2,412,[0,0,15,0,0,15,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Fate)
    Heal = SupportMagic("Heal","Heals for a moderate amount of health.",2,413,[0,0,0,0,0,0,75],30,SpellType.Heal,Target.Single)
    sptSpellDirectory.append(Heal)
    Minor_Regenerate = SupportMagic("Minor Regenerate","Heals for a small amount of health over time.",2,414,[0,0,0,0,0,0,15],24,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Minor_Regenerate)
    #3
    Rage_II =  SupportMagic("Rage II","Increases Atk by a great amount.",3,415,[20,0,0,0,0,0,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Rage_II)
    Focus_II = SupportMagic("Focus II","Increases Acc by a great amount.",3,416,[0,30,0,0,0,0,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Focus_II)
    Sense_II = SupportMagic("Sense","Increases Crt by a great amount.",3,417,[0,0,30,0,0,0,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Sense_II)
    Brace_II = SupportMagic("Brace II","Increases Def by a great amount.",3,418,[0,0,0,20,0,0,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Brace_II)
    Speed_II = SupportMagic("Speed II","Increases Ddg by a great amount.",3,419,[0,0,0,0,30,0,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Speed_II)
    Fortune_II = SupportMagic("Fortune II","Increases Lck by a great amount.",3,420,[0,0,0,0,0,30,0],30,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Fortune_II)
    Rage_Aura =  SupportMagic("Rage Aura","Increases your party's Atk.",3,421,[10,0,0,0,0,0,0],36,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Rage_Aura)
    Focus_Aura = SupportMagic("Focus Aura","Increases your party's Acc.",3,422,[0,15,0,0,0,0,0],36,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Focus_Aura)
    Sense_Aura = SupportMagic("Sense Aura","Increases your party's Crt.",3,423,[0,0,15,0,0,0,0],36,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Sense_Aura)
    Brace_Aura = SupportMagic("Brace Aura","Increases your party's Def.",3,424,[0,0,0,10,0,0,0],36,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Brace_Aura)
    Speed_Aura = SupportMagic("Speed Aura","Increases your party's Ddg.",3,425,[0,0,0,0,15,0,0],36,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Speed_Aura)
    Fortune_Aura = SupportMagic("Fortune Aura","Increases your party's Lck.",3,426,[0,0,0,0,0,15,0],36,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Fortune_Aura)
    Minor_Heal_Aura = SupportMagic("Minor Heal Aura","Heals all party members for a small amount of health.",3,427,[0,0,0,0,0,0,30],30,SpellType.Heal,Target.All)
    sptSpellDirectory.append(Minor_Heal_Aura)
    Regenerate = SupportMagic("Regenerate","Heals for a moderate amount of health over time.",3,428,[0,0,0,0,0,0,30],40,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Regenerate)
    #4
    Rally_II = SupportMagic("Rally II","Increases Atk and Def by a great amount.",4,429,[20,0,0,20,0,0],40,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Rally_II)
    Wrath_II = SupportMagic("Wrath II","Increases Atk and Acc by a great amount.",4,430,[20,30,0,0,0,0,0],40,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Wrath_II)
    Precision_II = SupportMagic("Precision II","Increases Acc and Crt by a great amount.",4,431,[0,30,30,0,0,0,0],40,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Precision_II)
    Trance_II = SupportMagic("Trance II","Increases Acc and Ddg by a great amount.",4,432,[0,30,0,0,30,0,0],40,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Trance_II)
    Veil_II = SupportMagic("Veil II","Increases Def and Ddg by a great amount.",4,433,[0,0,0,20,30,0,0],40,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Veil_II)
    Fate_II = SupportMagic("Fate II","Increases Crt and Lck by a great amount.",4,434,[0,0,30,0,0,30,0],40,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Fate_II)
    Rally_Aura = SupportMagic("Rally Aura","Increases your party's Atk and Def.",4,435,[10,0,0,10,0,0,0],46,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Rally_Aura)
    Wrath_Aura = SupportMagic("Wrath Aura","Increases your party's Atk and Acc.",4,436,[10,15,0,0,0,0,0],46,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Wrath_Aura)
    Precision_Aura = SupportMagic("Precision Aura","Increases your party's Acc and Crt.",4,437,[0,15,15,0,0,0,0],46,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Precision_Aura)
    Trance_Aura = SupportMagic("Trance Aura","Increases your party's Acc and Ddg.",4,438,[0,15,0,0,15,0,0],46,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Trance_Aura)
    Veil_Aura = SupportMagic("Veil Aura","Increases your party's Def and Ddg.",4,439,[0,0,0,10,15,0,0],46,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Veil_Aura)
    Fate_Aura = SupportMagic("Fate Aura","Increases your party's Crt and Lck.",4,440,[0,0,15,0,0,15,0],46,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Fate_Aura)
    Spectrum = SupportMagic("Spectrum","Increases all stats.",4,441,[10,15,15,10,15,15,0],50,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Spectrum)
    Heal_Aura = SupportMagic("Heal Aura","Heals all party members for a moderate amount of health.",4,442,[0,0,0,0,0,0,70],50,SpellType.Heal,Target.All)
    sptSpellDirectory.append(Heal_Aura)
    Minor_Regenerate_Aura = SupportMagic("Minor Regenerate Aura","Heals all party members for a small amount of health over time.",4,443,[0,0,0,0,0,0,15],46,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Minor_Regenerate_Aura)
    Major_Heal = SupportMagic("Major Heal","Heals for a large amount of health.",4,444,[0,0,0,0,0,0,120],40,SpellType.Heal,Target.Single)
    sptSpellDirectory.append(Major_Heal)
    Raise = SupportMagic("Raise","Raises a party member from the dead with 50 HP.",4,445,[0,0,0,0,0,0,50],40,SpellType.Raise,Target.Single)
    sptSpellDirectory.append(Raise)
    #5
    Rage_Aura_II =  SupportMagic("Rage Aura II","Increases your party's Atk by a great amount.",5,446,[20,0,0,0,0,0,0],50,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Rage_Aura_II)
    Focus_Aura_II = SupportMagic("Focus Aura II","Increases your party's Acc by a great amount.",5,447,[0,30,0,0,0,0,0],50,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Focus_Aura_II)
    Sense_Aura_II = SupportMagic("Sense Aura II","Increases your party's Crt by a great amount.",5,448,[0,0,30,0,0,0,0],50,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Sense_Aura_II)
    Brace_Aura_II = SupportMagic("Brace Aura II","Increases your party's Def by a great amount.",5,449,[0,0,0,20,0,0,0],50,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Brace_Aura_II)
    Speed_Aura_II = SupportMagic("Speed Aura II","Increases your party's Ddg by a great amount.",5,450,[0,0,0,0,30,0,0],50,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Speed_Aura_II)
    Fortune_Aura_II = SupportMagic("Fortune Aura II","Increases your party's Lck by a great amount.",5,451,[0,0,0,0,0,30,0],50,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Fortune_Aura_II)
    Spectrum_Aura = SupportMagic("Spectrum Aura","Increases all stats for all party members.",5,452,[10,15,15,10,15,15,0],64,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Spectrum_Aura)
    Major_Regenerate = SupportMagic("Major Regenerate","Heals for a large amount of health over time.",5,453,[0,0,0,0,0,0,50],64,SpellType.Buff,Target.Single)
    sptSpellDirectory.append(Major_Regenerate)
    Regenerate_Aura = SupportMagic("Regenerate Aura","Heals all party members for a moderate amount of health over time.",5,454,[0,0,0,0,0,0,30],64,SpellType.Buff,Target.All)
    sptSpellDirectory.append(Regenerate_Aura)
    Raise_Aura = SupportMagic("Raise Aura","Raises all fallen party members from the dead with 50 HP.",5,455,[0,0,0,0,0,0,50],80,SpellType.Raise,Target.All)
    sptSpellDirectory.append(Raise_Aura)

    #Cleansing Spells
    Cleanse = SupportMagic("Cleanse","Cleanses a party member of status effects.",2,456,[0,0,0,0,0,0,0],24,SpellType.Cleanse,Target.Single)
    sptSpellDirectory.append(Cleanse)
    Cleanse_Aura = SupportMagic("Cleanse Aura","Cleanses all party members of status effects.",4,457,[0,0,0,0,0,0,0],40,SpellType.Cleanse,Target.All)
    sptSpellDirectory.append(Cleanse_Aura)

    return sptSpellDirectory

########## TALENTS ##########

def initTalentDirectory():
    talentDirectory = []

    Fortify = Talent("Fortify","Reduce physical damage taken this turn by 75%.",1,500,0,TalentType.PartyEffect,Target.Self,Timing.DamageTaken)
    talentDirectory.append(Fortify)
    Breathe = Talent("Breathe","Reduce magical damage taken this turn by 75%.",1,501,0,TalentType.PartyEffect,Target.Self,Timing.DamageTaken)
    talentDirectory.append(Breathe)
    PatchUp = Talent("Patch Up","Restore 20% of max HP.",1,502,0,TalentType.Action,Target.Self,Timing.InTurn)
    talentDirectory.append(PatchUp)
    Meditate = Talent("Meditate","Restore 20% of max MP.",1,503,0,TalentType.Action,Target.Self,Timing.InTurn)
    talentDirectory.append(Meditate)
    Enrage = Talent("Enrage","Draw attention away from allies.",1,504,4,TalentType.PartyEffect,Target.Self,Timing.Targeting)
    talentDirectory.append(Enrage)
    Strike_True = Talent("Strike True","Attack an enemy for 70% damage, with no chance of missing.",1,505,6,TalentType.Action,Target.Single,Timing.InTurn)
    talentDirectory.append(Strike_True)
    Defend = Talent("Defend","Protect a party member.",1,506,6,TalentType.PartyEffect,Target.Ally,Timing.Targeting)
    talentDirectory.append(Defend)
    Riposte = Talent("Riposte","Deal 75% of damage taken back to attackers.",1,507,6,TalentType.PartyEffect,Target.Self,Timing.DamageTaken)
    talentDirectory.append(Riposte)
    Wild_Swing = Talent("Wild Swing","Attack with 150% damage, with ACC reduced by 10%",1,508,6,TalentType.Action,Target.Single,Timing.InTurn)
    talentDirectory.append(Wild_Swing)
    Eviscerate = Talent("Eviscerate","Attack with CRT increased by 15%.",1,509,8,TalentType.Action,Target.Single,Timing.InTurn)
    talentDirectory.append(Eviscerate)
    Pierce = Talent("Pierce","Attack an enemy, ignoring 50% of their defense.",1,510,10,TalentType.Action,Target.Single,Timing.InTurn)
    talentDirectory.append(Pierce)
    Swift_Strike = Talent("Swift Strike","Attack first in the combat order.",1,511,12,TalentType.Action,Target.Single,Timing.Ordering)
    talentDirectory.append(Swift_Strike)
    Cleave = Talent("Cleave","Attack all enemies.",1,512,16,TalentType.Action,Target.All,Timing.InTurn)
    talentDirectory.append(Cleave)
    Heartrend = Talent("Heartrend","Attack an enemy, restoring damage dealt as HP.",1,513,16,TalentType.Action,Target.Single,Timing.InTurn)
    talentDirectory.append(Heartrend)
    Soulrend = Talent("Soulrend","Attack an enemy, restoring damage dealt as MP.",1,514,8,TalentType.Action,Target.Single,Timing.InTurn)
    talentDirectory.append(Soulrend)
    Blitz = Talent("Blitz","Attack an enemy twice.",1,515,16,TalentType.Action,Target.Single,Timing.InTurn)
    talentDirectory.append(Blitz)
    Havoc = Talent("Havoc","Attack random enemies 5 times for half damage.",1,516,16,TalentType.Action,Target.All,Timing.InTurn)
    talentDirectory.append(Havoc)
    Smite = Talent("Smite","Sheathe your weapon in holy light, and attack an enemy for 150% damage.",1,517,12,TalentType.Action,Target.Single,Timing.InTurn)
    talentDirectory.append(Smite)
    Hide = Talent("Hide","Vanish into the shadows, making you impossible to hit with physical attacks.",1,518,6,TalentType.PartyEffect,Target.Self,Timing.DamageTaken)
    talentDirectory.append(Hide)
    Pray = Talent("Pray","Avoid status effects on your party this turn.",1,519,14,TalentType.PartyEffect,Target.Party,Timing.DamageTaken)
    talentDirectory.append(Pray)
    Curse = Talent("Curse","Put a curse on an enemy, reducing their defense by 30% until end of turn.",1,520,24,TalentType.EncounterEffect,Target.Single,Timing.DamageTaken)
    talentDirectory.append(Curse)
    DeathWish = Talent("Death Wish","Call upon a vile evil, causing enemy to lose 10% of hp each turn.",1,521,24,TalentType.Action,Target.Single,Timing.InTurn)
    talentDirectory.append(DeathWish)
    Guard = Talent("Guard","Take a defensive stance, halving damage taken this turn.",1,522,0,TalentType.PartyEffect,Target.Self,Timing.DamageTaken)
    talentDirectory.append(Guard)

    return talentDirectory

    ########## ACCESSORIES ##########

def initAccessoryDirectory():
    accessoryDirectory = []

    SolarBand = Accessory("Solar Band","Increases HP for the wearer by 10.",1,600,0,ActivationType.Passive,Timing.Universal,10)
    accessoryDirectory.append(SolarBand)
    LunarBand = Accessory("Lunar Band","Increases MP for the wearer by 10.",1,601,0,ActivationType.Passive,Timing.Universal,10)
    accessoryDirectory.append(LunarBand)
    MercuryBand = Accessory("Mercury Band","Increases ACC for the wearer by 10.",1,602,0,ActivationType.Passive,Timing.Universal,10)
    accessoryDirectory.append(MercuryBand)
    VenusBand = Accessory("Venus Band","Increases CRT for the wearer by 5.",1,603,0,ActivationType.Passive,Timing.Universal,5)
    accessoryDirectory.append(VenusBand)
    EarthBand = Accessory("Earth Band","Increases DEF for the wearer by 5.",1,604,0,ActivationType.Passive,Timing.Universal,5)
    accessoryDirectory.append(EarthBand)
    MarsBand = Accessory("Mars Band","Increases ATK for the wearer by 5.",1,605,0,ActivationType.Passive,Timing.Universal,5)
    accessoryDirectory.append(MarsBand)
    JupiterBand = Accessory("Jupiter Band","Increases LCK for the wearer by 10.",1,606,0,ActivationType.Passive,Timing.Universal,10)
    accessoryDirectory.append(JupiterBand)
    SaturnBand = Accessory("Saturn Band","Increases MPG for the wearer by 2.",1,607,0,ActivationType.Passive,Timing.Universal,2)
    accessoryDirectory.append(SaturnBand)
    UranusBand = Accessory("Uranus Band","Increases AMP for the wearer by 10.",1,608,0,ActivationType.Passive,Timing.Universal,10)
    accessoryDirectory.append(UranusBand)
    NeptuneBand = Accessory("Neptune Band","Increases DDG for the wearer by 10.",1,609,0,ActivationType.Passive,Timing.Universal,10)
    accessoryDirectory.append(NeptuneBand)
    PlutoBand = Accessory("Pluto Band","Increases SPD for the wearer by 5.",1,610,0,ActivationType.Passive,Timing.Universal,5)
    accessoryDirectory.append(PlutoBand)
    CrimsonScarf = Accessory("Crimson Scarf","Has a chance to regain HP to the wielder equal to half of damage dealt after a strike.",1,611,15,ActivationType.Active,Timing.DamageDealt)
    accessoryDirectory.append(CrimsonScarf)
    CeruleanScarf = Accessory("Cerulean Scarf","Has a chance to regain MP to the wielder equal to half of damage dealt after a strike.",1,612,15,ActivationType.Active,Timing.DamageDealt)
    accessoryDirectory.append(CeruleanScarf)
    MarbleHeart = Accessory("Marble Heart","Restores 4 of wielder's health each turn.",1,613,0,ActivationType.Passive,Timing.Universal,4)
    accessoryDirectory.append(MarbleHeart)
    JadeBracer = Accessory("Jade Bracer","Has a chance to decrease physical damage taken by 50%.",1,614,15,ActivationType.Active,Timing.DamageTaken)
    accessoryDirectory.append(JadeBracer)
    BismuthAmulet = Accessory("Bismuth Amulet","Has a chance to negate magical damage.",1,615,15,ActivationType.Active,Timing.DamageTaken)
    accessoryDirectory.append(BismuthAmulet)
    RubyCirclet = Accessory("Ruby Circlet","Grants immunity to Ablaze.",1,616,0,ActivationType.Passive,Timing.DamageTaken)
    accessoryDirectory.append(RubyCirclet)
    TopazCirclet = Accessory("Topaz Circlet","Grants immunity to Shock.",1,617,0,ActivationType.Passive,Timing.DamageTaken)
    accessoryDirectory.append(TopazCirclet)
    SapphireCirclet = Accessory("Sapphire Circlet","Grants immunity to Freezing.",1,618,0,ActivationType.Passive,Timing.DamageTaken)
    accessoryDirectory.append(SapphireCirclet)
    OpalCirclet = Accessory("Opal Circlet","Has a chance to negate a status effect.",1,619,30,ActivationType.Active,Timing.DamageTaken)
    accessoryDirectory.append(OpalCirclet)
    GuardiansBelt = Accessory("Guardian's Belt","Whenever the wearer uses the Guard talent, blocks 80% of damage rather than half.",2,620,0,ActivationType.Passive,Timing.DamageTaken)
    accessoryDirectory.append(GuardiansBelt)
    MagiciansTome = Accessory("Magician's Tome","Has a chance to allow the wielder to not consume mana upon casting a spell.",2,621,20,ActivationType.Active,Timing.DamageDealt)
    accessoryDirectory.append(MagiciansTome)
    MastersTome = Accessory("Master's Tome","Has a chance to allow the wielder to not consume mana upon performing a talent.",2,622,20,ActivationType.Active,Timing.DamageDealt)
    accessoryDirectory.append(MastersTome)
    BlitzingBoots = Accessory("Blitzing Boots","Has a chance to allow the wielder strike twice.",2,623,15,ActivationType.Active,Timing.PreAttack)
    accessoryDirectory.append(BlitzingBoots)
    MysticJournal = Accessory("Mystic Journal","Increases the wielder's SPT Magic Level by 1.",2,624,0,ActivationType.Passive,Timing.Universal,1)
    accessoryDirectory.append(MysticJournal)
    WickedJournal = Accessory("Wicked Journal","Increases the wielder's ATK Magic Level by 1.",2,625,0,ActivationType.Passive,Timing.Universal,1)
    accessoryDirectory.append(WickedJournal)
    WhirlwindCape = Accessory("Whirlwind Cape","Has a chance to allow the wielder's strike to target all enemies.",2,626,15,ActivationType.Active,Timing.PreAttack)
    accessoryDirectory.append(WhirlwindCape)
    PlasmaRing = Accessory("Plasma Ring","Has a chance to double the potency of a spell.",2,627,15,ActivationType.Active,Timing.DamageDealt)
    accessoryDirectory.append(PlasmaRing)
    IvoryMirror = Accessory("Ivory Mirror","Has a chance to reflect damage against the wielder back at its source.",2,628,15,ActivationType.Active,Timing.DamageTaken)
    accessoryDirectory.append(IvoryMirror)
    BrokenPocketwatch = Accessory("Broken Pocketwatch","All buffs cast by the wielder last two additional turns.",2,629,0,ActivationType.Passive,Timing.DamageDealt)
    accessoryDirectory.append(BrokenPocketwatch)
    TranslucentCowl = Accessory("Translucent Cowl","Enemies are less likely to target the wearer.",2,630,0,ActivationType.Passive,Timing.Targeting)
    accessoryDirectory.append(TranslucentCowl)
    WarlordsEmblem = Accessory("Warlord's Emblem","Enemies are more likely to target the wearer.",2,631,0,ActivationType.Passive,Timing.Targeting)
    accessoryDirectory.append(WarlordsEmblem)
    LightMagesDiadem = Accessory("Light Mage's Diadem","Taking damage depletes the wielder's MP before their HP.",3,632,0,ActivationType.Passive,Timing.DamageTaken)
    accessoryDirectory.append(LightMagesDiadem)
    WarpedSunglasses = Accessory("Warped Sunglasses","Attack spells target random enemies, and deal 150% damage.",3,633,0,ActivationType.Passive,Timing.DamageDealt)
    accessoryDirectory.append(WarpedSunglasses)
    WarpedEyeglasses = Accessory("Warped Eyeglasses","Support spells target random allies, and are 150% as potent.",3,634,0,ActivationType.Passive,Timing.DamageDealt)
    accessoryDirectory.append(WarpedEyeglasses)
    EnchantedSeedling = Accessory("Enchanted Seedling","Buffs cast on the wielder are 150% as potent.",3,635,0,ActivationType.Passive,Timing.DamageDealt)
    accessoryDirectory.append(EnchantedSeedling)
    MiracleBracelet = Accessory("Miracle Bracelet","Has a chance to keep the wielder from dying.",3,636,20,ActivationType.Active,Timing.DamageTaken)
    accessoryDirectory.append(MiracleBracelet)
    CursedBracer = Accessory("Cursed Bracer","Deals an additional damage for each subsequent hit without missing. Deals damage equal to its power and resets upon missing.",3,637,0,ActivationType.Passive,Timing.DamageDealt)
    accessoryDirectory.append(CursedBracer)
    CursedEarring = Accessory("Cursed Earring","Gains one permanent damage upon missing with a strike. Has a 50% chance to deal damage to its wielder equal to its power on a successful strike.",3,638,0,ActivationType.Passive,Timing.DamageDealt)
    accessoryDirectory.append(CursedEarring)

    return accessoryDirectory

    ######### FOOD #########

def initFoodDirectory():
    foodDirectory = []

    # Buff List: [HP,MP,ACC,CRT,DEF,ATK,LCK,MPG,AMP,DDG,SPD,HPG]

    ReelerSteak = Food("Reeler Steak","Meat cut from a Reeler, a large mammal known for running backwards on all four legs when threatened. Increases max HP by 10.",1,700,[10,0,0,0,0,0,0,0,0,0,0,0])
    foodDirectory.append(ReelerSteak)
    SourberryTart = Food("Sourberry Tart","A small pastry filled with crushed sourberries, known for temporarily changing the eye color of whoever eats them. Increases max MP by 10.",1,701,[0,10,0,0,0,0,0,0,0,0,0,0])
    foodDirectory.append(SourberryTart)
    DriedBladeleaf = Food("Dried Bladeleaf","A dehydraded leaf from the bladeleaf bush. Unexpectedly filling, armies have been known to carry bushels to feed their soldiers. Increases accuracy by 10.",1,702,[0,0,10,0,0,0,0,0,0,0,0,0])
    foodDirectory.append(DriedBladeleaf)
    GrilledMyrkafruit = Food("Grilled Myrkafruit","Grilled fruit of the Myrka tree. Can be lethal if eaten raw. Increases crit rate by 5.",1,703,[0,0,0,5,0,0,0,0,0,0,0,0])
    foodDirectory.append(GrilledMyrkafruit)
    TalliriteFragment = Food("Tallirite Fragment","A small piece of gemstone from Tallirite Isle. Eons ago, an ancient civilization was said to have evolved to subsist on these stones to survive. Increases defense by 5.",1,704,[0,0,0,0,5,0,0,0,0,0,0,0])
    foodDirectory.append(TalliriteFragment)
    WommiMilk = Food("Wommi Milk","Milk from the domesticated Wommi. Wommi are said to produce more potent milk if their caretakers are unhappy, in an attempt to help them. Increases attack by 5.",1,705,[0,0,0,0,0,5,0,0,0,0,0,0])
    foodDirectory.append(WommiMilk)
    StarrySalad = Food("Starry Salad","Salad made from greens in close proximity to the crash site in Bentro Forest. Plants taken from the area of the meteor impact are said to have special properties and provide good fortune. Increases luck by 10.",1,706,[0,0,0,0,0,0,10,0,0,0,0,0])
    foodDirectory.append(StarrySalad)
    SpellpaperCookie = Food("Spellpaper Cookie","A tiny shortbread cookie with a piece of an archmage's spell tome cooked into it. Mage's tomes are said to absorb some of their magical ability over time, which eventually led to many spellcasters abandoning tomes. Increases mana regen by 2.",1,707,[0,0,0,0,0,0,0,2,0,0,0,0])
    foodDirectory.append(SpellpaperCookie)
    PrombolStew = Food("Prombol Stew","Stew cooked with fresh vegetables and Prombol meat. Prombols are small six-legged frogs, which inexplicably teleport on an hourly basis. Increases magic amplification by 10.",1,708,[0,0,0,0,0,0,0,0,10,0,0,0])
    foodDirectory.append(PrombolStew)
    MirageDumplings = Food("Mirage Dumplings","Dumplings made with the meat and feathres of Mirage Owls, a semi-transparent bird that often lives underground. Increases dodge by 10.",1,709,[0,0,0,0,0,0,0,0,0,10,0,0])
    foodDirectory.append(MirageDumplings)
    SilkwingCandy = Food("Silkwing Candy","A hard candy made from melted silkwings, extraordinarily fast insects. Increases speed by 5.",1,710,[0,0,0,0,0,0,0,0,0,0,5,0])
    foodDirectory.append(SilkwingCandy)
    Ulvomelon = Food("Ulvomelon","A whole Ulvomelon, a fruit which regenerates rapidly once it is taken from the vine. Increases hp regen by 4.",1,711,[0,0,0,0,0,0,0,0,0,0,0,4])
    foodDirectory.append(Ulvomelon)

    return foodDirectory

    ######### CONSUMABLES #########

def initConsumableDirectory():
    consumableDirectory = []

    # Honna Tear - Raises a party member with half HP and MP
    HonnaTear = Consumable("Honna Tear","A small glass vial containing a tear from the rare Honna Falcon, said to be a messenger of Rendai. Raises a fallen party member with half HP and MP.",3,800,Target.Ally,Timing.Anytime,0)
    consumableDirectory.append(HonnaTear)
    # Fire Arrow - 50dmg to one target
    FireArrow = Consumable("Fire Arrow","A small, pre-loaded dart shooter, loaded with an arrow that bursts into flames on impact. Deals 50 damage to one target.",1,801,Target.Single,Timing.InTurn,50)
    consumableDirectory.append(FireArrow)
    # Blast Arrow - 150dmg to one target
    BlastArrow = Consumable("Blast Arrow","A small, pre-loaded dart shooter, loaded with an arrow that explodes on impact. Deals 150 damage to one target.",2,802,Target.Single,Timing.InTurn,150)
    consumableDirectory.append(BlastArrow)
    # Nova Arrow - 300dmg to one target
    NovaArrow = Consumable("Nova Arrow","A small, pre-loaded dart shooter, loaded with an arrow that releases an explosion of magical energy on impact. Deals 300 damage to one target.",3,803,Target.Single,Timing.InTurn,300)
    consumableDirectory.append(NovaArrow)
    # Fire Bomb - 50dmg to all enemies
    FireBomb = Consumable("Fire Bomb","A small leather satchel, with a fuse coming out of the top. On use, it releases a burst of flames and deals 50 damage to all enemies.",2,804,Target.All,Timing.InTurn,50)
    consumableDirectory.append(FireBomb)
    # Blast Bomb - 150dmg to all enemies
    BlastBomb = Consumable("Blast Bomb","A small glass flask, with a fuse coming out of the top. On use, it explodes and deals 150 damage to all enemies.",3,805,Target.All,Timing.InTurn,150)
    consumableDirectory.append(BlastBomb)
    # Nova Bomb - 300dmg to all enemies
    NovaBomb = Consumable("Nova Bomb","A small steel sphere, glowing with violet light. When activated, it releases an explosion of magical energy and deals 300 damage to all enemies.",4,806,Target.All,Timing.InTurn,300)
    consumableDirectory.append(NovaBomb)
    # Smoke Capsule - Instantly escape from combat
    SmokeCapsule = Consumable("Smoke Capsule","A glass orb, filled with smoke. When shattered, it allows for automatic escape from any non-boss combat.",1,807,Target.Party,Timing.InTurn,0)
    consumableDirectory.append(SmokeCapsule)
    # Pyrilic Venom - Apply a poison to a weapon that increases in damage over time
    PyrilicVenom = Consumable("Pyrilic Venom","A venom that increases in potency over time. When applied to a weapon, it increases the damage dealt by a character by 5 every round of combat.",2,808,Target.Ally,Timing.DamageDealt,5)
    consumableDirectory.append(PyrilicVenom)
    # Rendai's Veil - Makes a party member immune to damage for a short time
    RendaisVeil = Consumable("Rendai's Veil","A scrap of golden cloth. When torn, it protects the user from any damage for 3 rounds of combat.",3,809,Target.Ally,Timing.DamageTaken,4)
    consumableDirectory.append(RendaisVeil)
    # Callaret's Grace - Makes the party immune to magic damage for a short time
    CallaretsGrace = Consumable("Callaret's Grace","A small stone disk inscribed with the runes of Callaret, the God of Magic. When activated, it protects the party from magic damage and effects for 3 rounds of combat.",3,810,Target.Party,Timing.DamageTaken,4)
    consumableDirectory.append(CallaretsGrace)
    # Second Soul - Immediately raises the next fallen party member with full HP and MP
    SecondSoul = Consumable("Second Soul","A floating golden light in a jar. Whenever the next party member falls, the soul will burst from the jar and restore them to full HP and MP.",4,811,Target.Ally,Timing.OnDeath,0)
    consumableDirectory.append(SecondSoul)
    # Campfire Kit - Fully restores the party's HP
    CampfireKit = Consumable("Campfire Kit","A handy pack full of everything you need to set up camp for the night. Fully restores the party's HP.",2,812,Target.Party,Timing.Peacetime,0)
    consumableDirectory.append(CampfireKit)
    # Spirit Vapor - Fully restores the party's MP
    SpiritVapor = Consumable("Spirit Vapor","A small block of ice frozen from Lake Torren. When heated over a fire, it releases a vapor that fully restores the party's MP.",2,813,Target.Party,Timing.Peacetime,0)
    consumableDirectory.append(SpiritVapor)
    # Callaret's Compact - Returns the party to the last haven/village visited
    CallaretsCompact = Consumable("Callaret's Compact","A gold inlaid compact mirror that hums gently. When looked into, it teleports the party to the last haven or village that they visited.",3,814,Target.Party,Timing.Peacetime,0)
    consumableDirectory.append(CallaretsCompact)
    # Wommi Tuft - Cures an ally of any status effect
    WommiTuft = Consumable("Wommi Tuft","A tuft of wool from a Wommi. When rubbed on skin, it cures the target of any negative status effects.",2,815,Target.Ally,Timing.Anytime,0)
    consumableDirectory.append(WommiTuft)
    # Sun Sponge - Cures an ally of Ablaze
    SunSponge = Consumable("Sun Sponge","A soft sponge that is cool to the touch, known to draw in heat of anything touching it at an incredible rate. Cures an ally of Ablaze.",1,816,Target.Ally,Timing.Anytime,0)
    consumableDirectory.append(SunSponge)
    # Pulse Regulator - Cures an ally of any Shocked
    PulseRegulator = Consumable("Pulse Regulator","A small needle that pulses with a steady rate, which can reset the nervous system of a patient when pierced with it. Cures an ally of Shocked.",1,817,Target.Ally,Timing.Anytime,0)
    consumableDirectory.append(PulseRegulator)
    # Shaking Stone - Cures an ally of Freezing
    ShakingStone = Consumable("Shaking Stone","A small stone that vibrates rapidly, giving off heat. Cures an ally of Freezing.",1,818,Target.Ally,Timing.Anytime,0)
    consumableDirectory.append(ShakingStone)

    return consumableDirectory

    ######### RUNES #########

def initRuneDirectory():
    runeDirectory = []

    # Rune of Power - Passive Rune - Increases attack power by Level*10%
    PowerRune = Rune("Rune of Power", "An ancient rune, capable of enchanting weapons it is etched into. Increases the attack power of etched weapon.",1,900,ActivationType.Passive,10)
    runeDirectory.append(PowerRune)
    # Rune of Surging - Active Rune - Has a (Luck + Level*5)% chance to double damage dealt
    SurgingRune = Rune("Rune of Surging", "An ancient rune, capable of enchanting weapons it is etched into. Has a chance to double the damage dealt with etched weapon.",1,901,ActivationType.Active,5)
    runeDirectory.append(SurgingRune)
    # Rune of Piercing - Active Rune - Has a (Luck + Level*5)% chance to ignore 50% of an enemy's defense
    PiercingRune = Rune("Rune of Piercing", "An ancient rune, capable of enchanting weapons it is etched into. Has a chance to cut the enemy's defense in half when attacking with etched weapon.",1,902,ActivationType.Active,5)
    runeDirectory.append(PiercingRune)
    # Rune of Flames - Active Rune - Has a (Luck + (Level-1)*5)% chance to apply the Ablaze debuff to an enemy
    FlamesRune = Rune("Rune of Flames", "An ancient rune, capable of enchanting weapons it is etched into. Has a chance to apply the Ablaze debuff when attacking with etched weapon.",1,903,ActivationType.Active,5)
    runeDirectory.append(FlamesRune)
    # Rune of Sparks - Active Rune - Has a (Luck + (Level-1)*5)% chance to apply the Shocked debuff to an enemy
    SparksRune = Rune("Rune of Sparks", "An ancient rune, capable of enchanting weapons it is etched into. Has a chance to apply the Shocked debuff when attacking with etched weapon.",1,904,ActivationType.Active,5)
    runeDirectory.append(SparksRune)
    # Rune of Freezing - Active Rune - Has a (Luck + (Level-1)*5)% chance to apply the Freezing debuff to an enemy
    FreezingRune = Rune("Rune of Freezing", "An ancient rune, capable of enchanting weapons it is etched into. Has a chance to apply the Freezing debuff when attacking with etched weapon.",1,905,ActivationType.Active,5)
    runeDirectory.append(FreezingRune)
    # Rune of Syphoning - Passive Rune - Restores MP to the user equal to Level*10% of damage dealt
    SiphoningRune = Rune("Rune of Siphoning", "An ancient rune, capable of enchanting weapons it is etched into. Restores a portion of the damage dealt as MP when attacking with etched weapon.",1,906,ActivationType.Passive,10)
    runeDirectory.append(SiphoningRune)
    # Rune of Blood - Passive Rune - Restores HP to the user equal to Level*10% of damage dealt
    BloodRune = Rune("Rune of Blood", "An ancient rune, capable of enchanting weapons it is etched into. Restores a portion of the damage dealt as HP when attacking with etched weapon.",1,907,ActivationType.Passive,10)
    runeDirectory.append(BloodRune)
    # Rune of Corruption - Passive Rune - Increases attack power by Level*20%, but deals Level*10% of damage dealt back to the wielder
    CorruptionRune = Rune("Rune of Corruption", "An ancient rune, capable of enchanting weapons it is etched into. Significantly increases power when attacking with etched weapon, but hurts the wielder in the process.",1,908,ActivationType.Passive,10)
    runeDirectory.append(CorruptionRune)
    # Rune of Channeling - Passive Rune - Increases attack power by Level*20%, but saps Level*10% of MP from the wielder
    ChannelingRune = Rune("Rune of Channeling", "An ancient rune, capable of enchanting weapons it is etched into. Significantly increases power when attacking with etched weapon, but saps the wielder's MP in the process.",1,909,ActivationType.Passive,10)
    runeDirectory.append(ChannelingRune)
    # Rune of Expertise - Passive Rune - Increases the power of critical hits by Level*33%
    ExpertiseRune = Rune("Rune of Expertise", "An ancient rune, capable of enchanting weapons it is etched into. Significantly increases power of critical hits when attacking with etched weapon.",1,910,ActivationType.Passive,33)
    runeDirectory.append(ExpertiseRune)

    return runeDirectory