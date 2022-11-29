import pygame
from itemclasses import *

######### WEAPONS #########
def initWeaponDirectory():
    weaponDirectory = []

    #1
    Rusty_Axe = Weapon("Rusty Axe","A dull axe, coated in rust.",1,0,6,60,0,0)
    weaponDirectory.append(Rusty_Axe)
    Rusty_Sword = Weapon("Rusty Sword","A dull blade, coated in rust.",1,1,5,65,0,0)
    weaponDirectory.append(Rusty_Sword)
    Rusty_Spear = Weapon("Rusty Spear","A dull spear, coated in rust.",1,2,4,70,0,0)
    weaponDirectory.append(Rusty_Spear)
    Rusty_Dagger = Weapon("Rusty Dagger","A dull knife, coated in rust.",1,3,3,75,5,0)
    weaponDirectory.append(Rusty_Dagger)
    Rusty_Sceptre = Weapon("Rusty Sceptre","A bent metal staff, coated in rust.",1,4,2,70,0,5)
    weaponDirectory.append(Rusty_Sceptre)

    #2
    Jagged_Axe = Weapon("Jagged Axe","A hastily-crafted iron axe, with a sharp and jagged edge.",2,5,7,70,5,0)
    weaponDirectory.append(Jagged_Axe)
    Crooked_Saber = Weapon("Crooked Saber","A jagged iron blade, resembling a long piece of schrapnel.",2,6,6,75,0,0)
    weaponDirectory.append(Crooked_Saber)
    Vicious_Pike = Weapon("Vicious Pike","A long spear, with a sharp shard of iron affixed to the end.",2,7,5,80,0,0)
    weaponDirectory.append(Vicious_Pike)
    Crooked_Dagger = Weapon("Crooked Dagger","A sharp fragment of metal, shaped into a dagger.",2,8,4,85,10,0)
    weaponDirectory.append(Crooked_Dagger)
    Gnarled_Rod = Weapon("Gnarled Rod","A tangled wooden rod, containing a green gem at its top.",2,9,4,75,0,10)
    weaponDirectory.append(Gnarled_Rod)

    #3
    Iron_Axe = Weapon("Iron Axe","A sturdy iron axe.",3,10,9,70,5,0)
    weaponDirectory.append(Iron_Axe)
    Iron_Sword = Weapon("Iron Sword","A sturdy iron sword.",3,11,8,80,0,0)
    weaponDirectory.append(Iron_Sword)
    Iron_Spear = Weapon("Iron Spear","A sturdy iron spear.",3,12,7,85,0,0)
    weaponDirectory.append(Iron_Spear)
    Iron_Dagger = Weapon("Iron Dagger","A sturdy iron dagger.",3,13,6,90,10,0)
    weaponDirectory.append(Iron_Dagger)
    Iron_Sceptre = Weapon("Iron Sceptre","A tall iron staff, woven around a sapphire.",3,14,5,80,0,15)
    weaponDirectory.append(Iron_Sceptre)

    #4
    Steel_Axe = Weapon("Steel Axe","A sharp, shining steel axe.",4,15,11,75,5,0)
    weaponDirectory.append(Steel_Axe)
    Steel_Sword = Weapon("Steel Sword","A sharp, shining steel sword.",4,16,10,80,0,0)
    weaponDirectory.append(Steel_Sword)
    Steel_Spear = Weapon("Steel Spear","A sharp, shining steel spear.",4,17,9,85,5,0)
    weaponDirectory.append(Steel_Spear)
    Steel_Dagger = Weapon("Steel Dagger","A sharp, shining steel dagger.",4,18,8,90,15,0)
    weaponDirectory.append(Steel_Dagger)
    Steel_Wand = Weapon("Steel Wand","A long, shining steel wand.",4,19,7,80,0,20)
    weaponDirectory.append(Steel_Wand)

    #5
    Ebonite_Axe = Weapon("Ebonite Axe","An axe made of a dark, menacing steel, emanating an evil aura.",5,20,13,70,15,0)
    weaponDirectory.append(Ebonite_Axe)
    Ebonite_Sword = Weapon("Ebonite Sword","A sword made of a dark, menacing steel, emanating an evil aura.",5,21,12,75,10,0)
    weaponDirectory.append(Ebonite_Sword)
    Ebonite_Spear = Weapon("Ebonite Spear","A spear made of a dark, menacing steel, emanating an evil aura.",5,22,11,80,15,0)
    weaponDirectory.append(Ebonite_Spear)
    Ebonite_Dagger = Weapon("Ebonite Dagger","A dagger made of a dark, menacing steel, emanating an evil aura.",5,23,10,85,25,0)
    weaponDirectory.append(Ebonite_Dagger)
    Ebonite_Sceptre = Weapon("Ebonite Sceptre","A long, menacing sceptre made of a dark black metal.",5,24,8,80,10,25)
    weaponDirectory.append(Ebonite_Sceptre)

    #6
    Golden_Axe = Weapon("Golden Axe","An axe made of shimmering gold.",6,25,15,80,10,0)
    weaponDirectory.append(Golden_Axe)
    Golden_Sword = Weapon("Golden Sword","A sword made of shimmering gold.",6,26,14,85,5,0)
    weaponDirectory.append(Golden_Sword)
    Golden_Spear = Weapon("Golden Spear","A spear made of shimmering gold.",6,27,12,90,10,0)
    weaponDirectory.append(Golden_Spear)
    Golden_Dagger = Weapon("Golden Dagger","A dagger made of shimmering gold.",6,28,11,95,20,0)
    weaponDirectory.append(Golden_Dagger)
    Golden_Staff = Weapon("Golden Staff","A shining, golden staff, radiating magical energy.",6,29,10,85,0,30)
    weaponDirectory.append(Golden_Staff)

    #7
    Runic_Axe = Weapon("Runic Axe","An axe made of shining steel, with shimmering runes etched into it.",7,30,17,85,5,10)
    weaponDirectory.append(Runic_Axe)
    Runic_Sword = Weapon("Runic Sword","A sword made of shining steel, with shimmering runes etched into it.",7,31,15,90,0,10)
    weaponDirectory.append(Runic_Sword)
    Runic_Spear = Weapon("Runic Spear","A spear made of shining steel, with shimmering runes etched into it.",7,32,14,95,5,10)
    weaponDirectory.append(Runic_Spear)
    Runic_Dagger = Weapon("Runic Dagger","A dagger made of shining steel, with shimmering runes etched into it.",7,33,12,100,15,10)
    weaponDirectory.append(Runic_Dagger)
    Runic_Wand = Weapon("Runic Wand","A powerful steel wand, with shimmering runes etched into it.",7,34,11,90,0,45)
    weaponDirectory.append(Runic_Wand)

    #8
    Valentium_Axe = Weapon("Valentium Axe","An axe made of a magical, indestructable metal.",8,35,20,85,15,5)
    weaponDirectory.append(Valentium_Axe)
    Valentium_Sword = Weapon("Valentium Sword","A sword made of a magical, indestructable metal.",8,36,18,90,10,5)
    weaponDirectory.append(Valentium_Sword)
    Valentium_Spear = Weapon("Valentium Spear","A spear made of a magical, indestructable metal.",8,37,16,95,15,5)
    weaponDirectory.append(Valentium_Spear)
    Valentium_Dagger = Weapon("Valentium Dagger","An dagger made of a magical, indestructable metal.",8,38,14,100,25,5)
    weaponDirectory.append(Valentium_Dagger)
    Valentium_Sceptre = Weapon("Valentium Sceptre","A sceptre made of a magical, indestructable metal.",8,39,14,90,10,40)
    weaponDirectory.append(Valentium_Sceptre)

    #9
    Mechanical_Axe = Weapon("Mechanical Axe","An axe covered in whirring gears, arcing with electricity.",9,40,23,85,35,0)
    weaponDirectory.append(Mechanical_Axe)
    Mechanical_Sword = Weapon("Mechanical Sword","A sword covered in whirring gears, arcing with electricity.",9,41,21,90,30,0)
    weaponDirectory.append(Mechanical_Sword)
    Mechanical_Spear = Weapon("Mechanical Spear","A spear covered in whirring gears, arcing with electricity.",9,42,18,95,35,0)
    weaponDirectory.append(Mechanical_Spear)
    Mechanical_Dagger = Weapon("Mechanical Dagger","A dagger covered in whirring gears, arcing with electricity.",9,43,16,100,45,0)
    weaponDirectory.append(Mechanical_Dagger)
    Rod_of_Order = Weapon("Rod of Order","A magic staff, covered in spinning gears.",9,44,15,90,20,45)
    weaponDirectory.append(Rod_of_Order)

    #10
    Teratra = Weapon("Teratra","A mythical axe of legend, raised from the earth.",10,45,27,80,20,5)
    weaponDirectory.append(Teratra)
    Pyrithia = Weapon("Pyrithia","A mythical sword of legend, born from flame.",10,46,25,90,10,10)
    weaponDirectory.append(Pyrithia)
    Hyliat = Weapon("Hyliat","A mythical spear of legend, created in the depths of the ocean.",10,47,22,95,20,10)
    weaponDirectory.append(Hyliat)
    Aerolinde = Weapon("Aerolinde","A mythical dagger of legend, formed from the raging winds.",10,48,19,100,35,10)
    weaponDirectory.append(Aerolinde)
    Ordointh = Weapon("Ordointh","A magical staff of legend, formed from the forces of balance and order.",10,49,18,90,10,50)
    weaponDirectory.append(Ordointh)

    return weaponDirectory

########## ARMOR ##########

def initArmorDirectory():
    armorDirectory = []

    #1
    Light_Rusty_Armor = Armor("Light Rusty Armor","A tough, leather breastplate.",1,100,0,10,0)
    armorDirectory.append(Light_Rusty_Armor)
    Rusty_Armor = Armor("Rusty Armor","A tough, leather breastplate.",1,101,1,5,0)
    armorDirectory.append(Rusty_Armor)
    Heavy_Rusty_Armor = Armor("Heavy Rusty Armor","A rusted iron breastplate.",1,102,2,0,0)
    armorDirectory.append(Heavy_Rusty_Armor)
    Tattered_Robe = Armor("Tattered Robe","A tattered, cloth robe.",1,103,0,5,1)
    armorDirectory.append(Tattered_Robe)

    #2
    Leather_Armor = Armor("Leather Armor","A suit of sturdy leather armor.",2,104,1,10,0)
    armorDirectory.append(Leather_Armor)
    Studded_Leather_Armor = Armor("Studded Leather Armor","A suit of leather armor, studded with steel.",2,105,2,5,0)
    armorDirectory.append(Studded_Leather_Armor)
    Chainmail = Armor("Chainmail","A suit of armor made from intertwined links of chains.",2,106,3,0,0)
    armorDirectory.append(Chainmail)
    Silk_Robe = Armor("Silk Robe","A soft, silk robe.",2,107,2,0,1)
    armorDirectory.append(Silk_Robe)

    #3
    Light_Iron_Armor = Armor("Light Iron Armor","A partial suit of armor made from solid iron.",3,108,3,15,0)
    armorDirectory.append(Light_Iron_Armor)
    Iron_Armor = Armor("Iron Armor","A suit of solid iron armor.",3,109,4,5,0)
    armorDirectory.append(Iron_Armor)
    Heavy_Iron_Armor = Armor("Heavy Iron","A thick suit of solid iron armor.",3,110,5,0,0)
    armorDirectory.append(Heavy_Iron_Armor)
    Shimmering_Robe = Armor("Shimmering Robe","A long velvet robe, that seems to shimmer magically.",3,111,3,5,2)
    armorDirectory.append(Shimmering_Robe)
    #4
    Light_Steel_Armor = Armor("Light Steel Armor","A suit of lightweight steel armor.",4,112,5,15,0)
    armorDirectory.append(Light_Steel_Armor)
    Steel_Armor = Armor("Steel Armor","A suit of standard steel armor.",4,113,6,5,0)
    armorDirectory.append(Steel_Armor)
    Heavy_Steel_Armor = Armor("Heavy Steel Armor","A suit of heavy steel armor.",4,114,7,0,0)
    armorDirectory.append(Heavy_Steel_Armor)
    Enchanted_Robe = Armor("Enchanted Robe","An enchanted robe, which glows magically.",4,115,4,10,2)
    armorDirectory.append(Enchanted_Robe)
    #5
    Light_Ebonite_Armor = Armor("Light Ebonite Armor","A suit of lightweight ebonite armor.",5,116,7,15,0)
    armorDirectory.append(Light_Ebonite_Armor)
    Ebonite_Armor = Armor("Ebonite Armor","A suit of standard ebonite armor.",5,117,8,5,0)
    armorDirectory.append(Ebonite_Armor)
    Heavy_Ebonite_Armor = Armor("Heavy Ebonite Armor","A suit of heavy ebonite armor.",5,118,9,0,0)
    armorDirectory.append(Heavy_Ebonite_Armor)
    Amethyst_Robe = Armor("Amethyst Robe","A bright purple robe, pulsing with dark energy.",5,119,5,10,3)
    armorDirectory.append(Amethyst_Robe)
    Ebonite_Arcanist_Armor = Armor("Ebonite Arcanist Armor","A set of ebonite battlemage armor, with magical capabilities.",6,120,7,5,1)
    armorDirectory.append(Ebonite_Arcanist_Armor)
    #6
    Light_Golden_Armor = Armor("Light Golden Armor","A suit of lightweight golden armor.",6,121,8,20,0)
    armorDirectory.append(Light_Golden_Armor)
    Golden_Armor = Armor("Golden Armor","A suit of standard golden armor.",6,122,10,10,0)
    armorDirectory.append(Golden_Armor)
    Heavy_Golden_Armor = Armor("Heavy Golden Armor","A suit of heavy golden armor.",6,123,12,0,0)
    armorDirectory.append(Heavy_Golden_Armor)
    Gilded_Robe = Armor("Gilded Robe","A flowing robe sewn from golden threads, imbued with magical power.",6,124,6,15,3)
    armorDirectory.append(Gilded_Robe)
    Golden_Arcanist_Armor = Armor("Golden Arcanist Armor","A set of golden battlemage armor, with magical capabilities.",6,125,8,10,1)
    armorDirectory.append(Golden_Arcanist_Armor)
    #7
    Light_Runic_Armor = Armor("Light Runic Armor","A suit of lightweight steel armor inscribed with ancient runes.",7,126,9,25,1)
    armorDirectory.append(Light_Runic_Armor)
    Runic_Armor = Armor("Runic Armor","A suit of standard steel armor inscribed with ancient runes.",7,127,11,15,1)
    armorDirectory.append(Runic_Armor)
    Heavy_Runic_Armor = Armor("Heavy Runic Armor","A suit of heavy steel armor inscribed with ancient runes.",7,128,13,0,1)
    armorDirectory.append(Runic_Armor)
    Runic_Robe = Armor("Runic Robe","A flowing robe sewn from golden threads, with arcane runes inscribed at the base.",8,129,7,20,4)
    armorDirectory.append(Runic_Robe)
    Runic_Arcanist_Armor = Armor("Runic Arcanist Armor","A suit of steel armor, inscribed with ancient runes.",8,130,10,15,2)
    armorDirectory.append(Runic_Arcanist_Armor)
    #8
    Light_Valentium_Armor = Armor("Light Valentium Armor","A suit of lightweight Valentium armor, which pulses with magical energy.",8,131,12,30,2)
    armorDirectory.append(Light_Valentium_Armor)
    Valentium_Armor = Armor("Valentium Armor","A suit of Valentium armor, which pulses with magical energy.",8,132,15,15,2)
    armorDirectory.append(Valentium_Armor)
    Heavy_Valentium_Armor = Armor("Heavy Valentium Armor","A suit of heavy Valentium armor, which pulses with magical energy.",8,133,18,0,2)
    armorDirectory.append(Heavy_Valentium_Armor)
    Valentium_Robe = Armor("Valentium Robe","A robe sewn from threads of Valentium, which pulses with magical energy.",8,134,8,25,4)
    armorDirectory.append(Valentium_Robe)
    Valentium_Arcanist_Armor = Armor("Valentium Arcanist Armor","A set of Valentium battlemage armor, which pulses with unbridled magical energy.",8,135,12,15,2)
    armorDirectory.append(Valentium_Arcanist_Armor)
    #9
    Light_Mechanical_Armor = Armor("Light Mechanical Armor","A suit of lightweight armor with cogs and pipes whirring along it.",9,136,13,45,0)
    armorDirectory.append(Light_Mechanical_Armor)
    Mechanical_Armor = Armor("Mechanical Armor","A suit of armor with cogs and pipes whirring along it.",9,137,16,30,0)
    armorDirectory.append(Mechanical_Armor)
    Heavy_Mechanical_Armor = Armor("Heavy Mechanical Armor","A suit of heavy armor with cogs and pipes whirring along it.",9,138,19,15,0)
    armorDirectory.append(Heavy_Mechanical_Armor)
    Clockwork_Robe = Armor("Clockwork Robe","A robe sewn from threads of time itself.",9,139,10,30,5)
    armorDirectory.append(Clockwork_Robe)
    Clockwork_Arcanist_Armor = Armor("Clockwork Arcanist Armor","A set of clockwork battlemage armor, with magical energy flowing through it like time itself.",9,140,13,30,3)
    armorDirectory.append(Clockwork_Arcanist_Armor)
    #10
    Cloak_of_the_Whisper = Armor("Cloak of the Whisper","A cloak that envelops its wearer in shadow.",10,141,13,60,0)
    armorDirectory.append(Cloak_of_the_Whisper)
    Plate_of_the_Vanguard = Armor("Plate of the Vanguard","A suit of regal armor worn by a hero of legend.",10,142,18,30,0)
    armorDirectory.append(Plate_of_the_Vanguard)
    Shield_of_the_Conquerer = Armor("Shield of the Conquerer","A massive suit of heavy armor once worn by the ruler of an ancient kingdom.",10,143,24,0,0)
    armorDirectory.append(Shield_of_the_Conquerer)
    Robe_of_the_Archmage = Armor("Robe of the Archmage","A robe that harnesses the magical power of the world.",10,144,12,30,7)
    armorDirectory.append(Robe_of_the_Archmage)
    Helm_of_the_Ancients = Armor("Helm of the Ancients","A demigod's suit of armor, passed down from an ancient kingdom of magic.",10,145,16,25,5)
    armorDirectory.append(Helm_of_the_Ancients)

    return armorDirectory

########## POTIONS ##########

def initPotionDirectory():
    potionDirectory = []

    #1
    Potion_of_Minor_Healing = Potion("Potion of Minor Healing","A potion capable of restoring a meager amount of life.",1,200,10,0);
    potionDirectory.append(Potion_of_Minor_Healing);
    Potion_of_Minor_Calming = Potion("Potion of Minor Calming","A potion capable of restoring a meager amount of magical ability.",1,201,0,10);
    potionDirectory.append(Potion_of_Minor_Calming);
    #2
    Potion_of_Lesser_Healing = Potion("Potion of Lesser Healing","A potion capable of restoring a small amount of life.",2,202,20,0);
    potionDirectory.append(Potion_of_Lesser_Healing);
    Potion_of_Lesser_Calming = Potion("Potion of Lesser Calming","A potion capable of restoring a small amount of magical ability.",2,203,0,20);
    potionDirectory.append(Potion_of_Lesser_Calming);
    #3
    Potion_of_Healing = Potion("Potion of Healing","A potion capable of restoring life.",3,204,30,0);
    potionDirectory.append(Potion_of_Healing);
    Potion_of_Calming = Potion("Potion of Calming","A potion capable of restoring magical ability.",3,205,0,30);
    potionDirectory.append(Potion_of_Calming);
    #4
    Potion_of_Greater_Healing = Potion("Potion of Greater Healing","A potion capable of restoring a great amount of life.",4,206,50,0);
    potionDirectory.append(Potion_of_Greater_Healing);
    Potion_of_Greater_Calming = Potion("Potion of Greater Calming","A potion capable of restoring a great amount of magical ability.",4,207,0,50);
    potionDirectory.append(Potion_of_Greater_Calming);
    Potion_of_Replenishment = Potion("Potion of Replenishment","A potion capable of restoring both life and magical ability.",4,208,30,30);
    potionDirectory.append(Potion_of_Replenishment);
    #5
    Potion_of_Full_Healing = Potion("Potion of Full Healing","A potion capable of restoring all life.",5,209,100,0);
    potionDirectory.append(Potion_of_Full_Healing);
    Potion_of_Full_Calming = Potion("Potion of Full Calming","A potion capable of restoring all magical ability.",5,210,0,100);
    potionDirectory.append(Potion_of_Full_Calming);
    Potion_of_Greater_Replenishment = Potion("Potion of Greater Replenishment","A potion capable of restoring both life and magical ability.",5,211,50,50);
    potionDirectory.append(Potion_of_Greater_Replenishment);

    return potionDirectory

########## ATTACK SPELLS ##########

def initAtkSpellDirectory():
    attackSpellDirectory = []

    #1
    Jolt = AttackMagic("Jolt","Fires a small jolt of lightning at a target.",1,300,4,10,"Attack","Lightning","Single");
    attackSpellDirectory.append(Jolt);
    Ember = AttackMagic("Ember","Fires a small burst of flame at a target.",1,301,3,8,"Attack","Fire","Single");
    attackSpellDirectory.append(Ember);
    Frostbite = AttackMagic("Frostbite","Fires a small burst of cold at a target.",1,302,2,6,"Attack","Ice","Single");
    attackSpellDirectory.append(Frostbite);
    #2
    Thunderbolt = AttackMagic("Thunderbolt","Fires a bolt of lightning at a target.",2,303,8,16,"Attack","Lightning","Single");
    attackSpellDirectory.append(Thunderbolt);
    Firebolt = AttackMagic("Firebolt","Fires a bolt of fire at a target.",2,304,7,14,"Attack","Fire","Single");
    attackSpellDirectory.append(Firebolt);
    Frostbolt = AttackMagic("Frostbolt","Fires a bolt of freezing energy at a target.",2,305,6,12,"Attack","Ice","Single");
    attackSpellDirectory.append(Frostbolt);
    Thunder_Wave = AttackMagic("Thunder Wave","Summons a wave of electricity toward all foes.",2,306,10,10,"Attack","Lightning","All");
    attackSpellDirectory.append(Thunder_Wave);
    Fire_Wave = AttackMagic("Fire Wave","Summons a wave of flame toward all foes.",2,307,9,8,"Attack","Fire","All");
    attackSpellDirectory.append(Fire_Wave);
    Frost_Wave = AttackMagic("Frost Wave","Summons a wave of ice toward all foes.",2,308,8,6,"Attack","Ice","All");
    attackSpellDirectory.append(Frost_Wave);
    #3
    Lightning_Strike = AttackMagic("Lightning Strike","Strikes down a bolt of lightning at a target.",3,309,12,22,"Attack","Lightning","Single");
    attackSpellDirectory.append(Lightning_Strike);
    Fireball = AttackMagic("Fireball","Hurls a fireball at a target.",3,310,11,20,"Attack","Fire","Single");
    attackSpellDirectory.append(Fireball);
    Hail = AttackMagic("Hail","Launches a blast of freezing magic at a target.",3,311,10,18,"Attack","Ice","Single");
    attackSpellDirectory.append(Hail);
    Thunder_Wave_II = AttackMagic("Thunder Wave II","Hurls a large wave of electricity toward all foes.",2,312,14,16,"Attack","Lightning","All");
    attackSpellDirectory.append(Thunder_Wave_II);
    Fire_Wave_II = AttackMagic("Fire Wave II","Hurls a large wave of flame toward all foes.",2,313,13,14,"Attack","Fire","All");
    attackSpellDirectory.append(Fire_Wave_II);
    Frost_Wave_II = AttackMagic("Frost Wave II","Hurls a large wave of ice toward all foes.",2,314,12,12,"Attack","Ice","All");
    attackSpellDirectory.append(Frost_Wave_II);
    #4
    Electrocute = AttackMagic("Electrocute","Unleashes a massive jolt of electricity at a target.",4,315,16,28,"Attack","Lightning","Single");
    attackSpellDirectory.append(Electrocute);
    Fire_Blast = AttackMagic("Fire Blast","Unleashes a blast of flame at a target.",4,316,15,26,"Attack","Fire","Single");
    attackSpellDirectory.append(Fire_Blast);
    Cryo_Beam = AttackMagic("Cryo Beam","Fires a beam of pure freezing magic at a target.",4,317,14,24,"Attack","Ice","Single");
    attackSpellDirectory.append(Cryo_Beam);
    Thunder_Wave_III = AttackMagic("Thunder Wave III","Launches a massive wave of electricity toward all foes.",2,318,18,22,"Attack","Lightning","All");
    attackSpellDirectory.append(Thunder_Wave_III);
    Fire_Wave_III = AttackMagic("Fire Wave III","Launches a massive wave of flame toward all foes.",2,319,17,20,"Attack","Fire","All");
    attackSpellDirectory.append(Fire_Wave_III);
    Frost_Wave_III = AttackMagic("Frost Wave III","Launches a massive wave of ice toward all foes.",2,320,16,18,"Attack","Ice","All");
    attackSpellDirectory.append(Frost_Wave_III);
    #5
    Thunderstorm = AttackMagic("Thunderstorm","Calls down a raging storm to electrify a target.",5,321,20,28,"Attack","Lightning","All");
    attackSpellDirectory.append(Thunderstorm);
    Inferno = AttackMagic("Inferno","Calls a raging inferno to incinerate a target.",5,322,19,26,"Attack","Fire","All");
    attackSpellDirectory.append(Inferno);
    Blizzard = AttackMagic("Blizzard","Calls a raging blizzard to freeze a target.",5,323,18,24,"Attack","Ice","All");
    attackSpellDirectory.append(Blizzard);

    #DEBUFFS
    Paralyze = AttackMagic("Paralyze","Has a chance to inflict Paralysis on a target.",2,324,10,0,"Debuff","Lightning","Single");
    attackSpellDirectory.append(Paralyze);
    Burn = AttackMagic("Burn","Has a chance to inflict Burned on a target.",2,325,10,0,"Debuff","Fire","Single");
    attackSpellDirectory.append(Firebolt);
    Freeze = AttackMagic("Freeze","Has a chance to inflict Freezing on a target.",2,326,10,0,"Debuff","Ice","Single");
    attackSpellDirectory.append(Freeze);

    Paralyze_II = AttackMagic("Paralyze II","Inflicts Paralysis on a target.",3,327,16,0,"Debuff","Lightning","Single");
    attackSpellDirectory.append(Paralyze_II);
    Burn_II = AttackMagic("Burn II","Inflicts Burned on a target.",3,328,16,0,"Debuff","Fire","Single");
    attackSpellDirectory.append(Burn_II);
    Freeze_II = AttackMagic("Freeze II","Inflicts Freezing on a target.",3,329,16,0,"Debuff","Ice","Single");
    attackSpellDirectory.append(Freeze_II);

    Paralyze_Wave = AttackMagic("Paralyze Wave","Has a chance to inflict Paralysis on all targets.",4,330,30,0,"Debuff","Lightning","All");
    attackSpellDirectory.append(Paralyze_Wave);
    Burn_Wave = AttackMagic("Burn Wave","Has a chance to inflict Burned on all targets.",4,331,30,0,"Debuff","Fire","All");
    attackSpellDirectory.append(Burn_Wave);
    Freeze_Wave = AttackMagic("Freeze Wave","Has a chance to inflict Freezing on all targets.",4,332,30,0,"Debuff","Ice","All");
    attackSpellDirectory.append(Freeze_Wave);

    return attackSpellDirectory

########## SUPPORT SPELLS ##########

def initSptSpellDirectory():
    sptSpellDirectory = []

    # [ ATK ACC CRT DEF DDG LCK HP ]

    #1
    Rage =  SupportMagic("Rage","Increases Atk.",1,400,[5,0,0,0,0,0,0],8,"Buff","Single");
    sptSpellDirectory.append(Rage);
    Focus = SupportMagic("Focus","Increases Acc.",1,401,[0,15,0,0,0,0,0],8,"Buff","Single");
    sptSpellDirectory.append(Focus);
    Sense = SupportMagic("Sense","Increases Crt.",1,402,[0,0,15,0,0,0,0],8,"Buff","Single");
    sptSpellDirectory.append(Sense);
    Brace = SupportMagic("Brace","Increases Def.",1,403,[0,0,0,5,0,0,0],8,"Buff","Single");
    sptSpellDirectory.append(Brace);
    Speed = SupportMagic("Speed","Increases Ddg.",1,404,[0,0,0,0,15,0,0],8,"Buff","Single");
    sptSpellDirectory.append(Speed);
    Fortune = SupportMagic("Fortune","Increases Lck.",1,405,[0,0,0,0,0,15,0],8,"Buff","Single");
    sptSpellDirectory.append(Fortune);
    Minor_Heal = SupportMagic("Minor Heal","Heals for a small amount of health.",1,406,[0,0,0,0,0,0,10],5,"Heal","Single");
    sptSpellDirectory.append(Minor_Heal);
    #2
    Rally = SupportMagic("Rally","Increases Atk and Def.",2,407,[5,0,0,5,0,0,0],16,"Buff","Single");
    sptSpellDirectory.append(Rally);
    Wrath = SupportMagic("Wrath","Increases Atk and Acc.",2,408,[5,15,0,0,0,0,0],16,"Buff","Single");
    sptSpellDirectory.append(Wrath);
    Precision = SupportMagic("Precision","Increases Acc and Crt.",2,409,[0,15,15,0,0,0,0],16,"Buff","Single");
    sptSpellDirectory.append(Precision);
    Trance = SupportMagic("Trance","Increases Acc and Ddg.",2,410,[0,15,0,0,15,0,0],16,"Buff","Single");
    sptSpellDirectory.append(Trance);
    Veil = SupportMagic("Veil","Increases Def and Ddg.",2,411,[0,0,0,5,15,0,0],16,"Buff","Single");
    sptSpellDirectory.append(Veil);
    Fate = SupportMagic("Fate","Increases Crt and Lck.",2,412,[0,0,15,0,0,15,0],16,"Buff","Single");
    sptSpellDirectory.append(Fate);
    Heal = SupportMagic("Heal","Heals for a moderate amount of health.",2,413,[0,0,0,0,0,0,30],12,"Heal","Single");
    sptSpellDirectory.append(Heal);
    Minor_Regenerate = SupportMagic("Minor Regenerate","Heals for a small amount of health over time.",2,414,[0,0,0,0,0,0,6],12,"Buff","Single");
    sptSpellDirectory.append(Minor_Regenerate);
    #3
    Rage_II =  SupportMagic("Rage II","Increases Atk by a great amount.",1,415,[10,0,0,0,0,0,0],16,"Buff","Single");
    sptSpellDirectory.append(Rage_II);
    Focus_II = SupportMagic("Focus II","Increases Acc by a great amount.",1,416,[0,30,0,0,0,0,0],16,"Buff","Single");
    sptSpellDirectory.append(Focus_II);
    Sense_II = SupportMagic("Sense","Increases Crt by a great amount.",1,417,[0,0,30,0,0,0,0],16,"Buff","Single");
    sptSpellDirectory.append(Sense_II);
    Brace_II = SupportMagic("Brace II","Increases Def by a great amount.",1,418,[0,0,0,10,0,0,0],16,"Buff","Single");
    sptSpellDirectory.append(Brace_II);
    Speed_II = SupportMagic("Speed II","Increases Ddg by a great amount.",1,419,[0,0,0,0,30,0,0],16,"Buff","Single");
    sptSpellDirectory.append(Speed_II);
    Fortune_II = SupportMagic("Fortune II","Increases Lck by a great amount.",1,420,[0,0,0,0,0,30,0],16,"Buff","Single");
    sptSpellDirectory.append(Fortune_II);
    Rage_Aura =  SupportMagic("Rage Aura","Increases your party's Atk.",1,421,[5,0,0,0,0,0,0],20,"Buff","All");
    sptSpellDirectory.append(Rage_Aura);
    Focus_Aura = SupportMagic("Focus Aura","Increases your party's Acc.",1,422,[0,15,0,0,0,0,0],20,"Buff","All");
    sptSpellDirectory.append(Focus_Aura);
    Sense_Aura = SupportMagic("Sense Aura","Increases your party's Crt.",1,423,[0,0,15,0,0,0,0],20,"Buff","All");
    sptSpellDirectory.append(Sense_Aura);
    Brace_Aura = SupportMagic("Brace Aura","Increases your party's Def.",1,424,[0,0,0,5,0,0,0],20,"Buff","All");
    sptSpellDirectory.append(Brace_Aura);
    Speed_Aura = SupportMagic("Speed Aura","Increases your party's Ddg.",1,425,[0,0,0,0,15,0,0],20,"Buff","All");
    sptSpellDirectory.append(Speed_Aura);
    Fortune_Aura = SupportMagic("Fortune Aura","Increases your party's Lck.",1,426,[0,0,0,0,0,15,0],20,"Buff","All");
    sptSpellDirectory.append(Fortune_Aura);
    Minor_Heal_Aura = SupportMagic("Minor Heal Aura","Heals all party members for a small amount of health.",1,427,[0,0,0,0,0,0,10],12,"Heal","All");
    sptSpellDirectory.append(Minor_Heal_Aura);
    Regenerate = SupportMagic("Regenerate","Heals for a moderate amount of health over time.",3,428,[0,0,0,0,0,0,12],24,"Buff","Single");
    sptSpellDirectory.append(Regenerate);
    #4
    Rally_II = SupportMagic("Rally II","Increases Atk and Def by a great amount.",2,429,[10,0,0,10,0,0],24,"Buff","Single");
    sptSpellDirectory.append(Rally_II);
    Wrath_II = SupportMagic("Wrath II","Increases Atk and Acc by a great amount.",2,430,[10,30,0,0,0,0,0],24,"Buff","Single");
    sptSpellDirectory.append(Wrath_II);
    Precision_II = SupportMagic("Precision II","Increases Acc and Crt by a great amount.",2,431,[0,30,30,0,0,0,0],24,"Buff","Single");
    sptSpellDirectory.append(Precision_II);
    Trance_II = SupportMagic("Trance II","Increases Acc and Ddg by a great amount.",2,432,[0,30,0,0,30,0,0],24,"Buff","Single");
    sptSpellDirectory.append(Trance_II);
    Veil_II = SupportMagic("Veil II","Increases Def and Ddg by a great amount.",2,433,[0,0,0,10,30,0,0],24,"Buff","Single");
    sptSpellDirectory.append(Veil_II);
    Fate_II = SupportMagic("Fate II","Increases Crt and Lck by a great amount.",2,434,[0,0,30,0,0,30,0],24,"Buff","Single");
    sptSpellDirectory.append(Fate_II);
    Rally_Aura = SupportMagic("Rally Aura","Increases your party's Atk and Def.",2,435,[5,0,0,5,0,0,0],28,"Buff","All");
    sptSpellDirectory.append(Rally_Aura);
    Wrath_Aura = SupportMagic("Wrath Aura","Increases your party's Atk and Acc.",2,436,[5,15,0,0,0,0,0],28,"Buff","All");
    sptSpellDirectory.append(Wrath_Aura);
    Precision_Aura = SupportMagic("Precision Aura","Increases your party's Acc and Crt.",2,437,[0,15,15,0,0,0,0],28,"Buff","All");
    sptSpellDirectory.append(Precision_Aura);
    Trance_Aura = SupportMagic("Trance Aura","Increases your party's Acc and Ddg.",2,438,[0,15,0,0,15,0,0],28,"Buff","All");
    sptSpellDirectory.append(Trance_Aura);
    Veil_Aura = SupportMagic("Veil Aura","Increases your party's Def and Ddg.",2,439,[0,0,0,5,15,0,0],28,"Buff","All");
    sptSpellDirectory.append(Veil_Aura);
    Fate_Aura = SupportMagic("Fate Aura","Increases your party's Crt and Lck.",2,440,[0,0,15,0,0,15,0],28,"Buff","All");
    sptSpellDirectory.append(Fate_Aura);
    Spectrum = SupportMagic("Spectrum","Increases all stats.",2,441,[5,5,15,5,5,15,0],30,"Buff","Single");
    sptSpellDirectory.append(Spectrum);
    Heal_Aura = SupportMagic("Heal Aura","Heals all party members for a moderate amount of health.",1,442,[0,0,0,0,0,0,30],30,"Heal","All");
    sptSpellDirectory.append(Heal_Aura);
    Minor_Regenerate_Aura = SupportMagic("Minor Regenerate Aura","Heals all party members for a small amount of health over time.",2,443,[0,0,0,0,0,0,6],24,"Buff","All");
    sptSpellDirectory.append(Minor_Regenerate_Aura);
    Major_Heal = SupportMagic("Major Heal","Heals for a large amount of health.",2,444,[0,0,0,0,0,0,60],30,"Heal","Single");
    sptSpellDirectory.append(Major_Heal);
    Raise = SupportMagic("Raise","Raises a party member from the dead with 30 HP.",2,445,[0,0,0,0,0,0,30],30,"Heal","Single");
    sptSpellDirectory.append(Raise);
    #5
    Rage_Aura_II =  SupportMagic("Rage Aura II","Increases your party's Atk by a great amount.",1,446,[10,0,0,0,0,0,0],32,"Buff","All");
    sptSpellDirectory.append(Rage_Aura_II);
    Focus_Aura_II = SupportMagic("Focus Aura II","Increases your party's Acc by a great amount.",1,447,[0,30,0,0,0,0,0],32,"Buff","All");
    sptSpellDirectory.append(Focus_Aura_II);
    Sense_Aura_II = SupportMagic("Sense Aura II","Increases your party's Crt by a great amount.",1,448,[0,0,30,0,0,0,0],32,"Buff","All");
    sptSpellDirectory.append(Sense_Aura_II);
    Brace_Aura_II = SupportMagic("Brace Aura II","Increases your party's Def by a great amount.",1,449,[0,0,0,10,0,0,0],32,"Buff","All");
    sptSpellDirectory.append(Brace_Aura_II);
    Speed_Aura_II = SupportMagic("Speed Aura II","Increases your party's Ddg by a great amount.",1,450,[0,0,0,0,30,0,0],32,"Buff","All");
    sptSpellDirectory.append(Speed_Aura_II);
    Fortune_Aura_II = SupportMagic("Fortune Aura II","Increases your party's Lck by a great amount.",1,451,[0,0,0,0,0,30,0],32,"Buff","All");
    sptSpellDirectory.append(Fortune_Aura_II);
    Spectrum_Aura = SupportMagic("Spectrum Aura","Increases all stats for all party members.",2,452,[5,5,15,5,5,15,0],40,"Buff","All");
    sptSpellDirectory.append(Spectrum_Aura);
    Major_Regenerate = SupportMagic("Major Regenerate","Heals for a large amount of health over time.",3,453,[0,0,0,0,0,0,24],40,"Buff","Single");
    sptSpellDirectory.append(Major_Regenerate);
    Regenerate_Aura = SupportMagic("Regenerate Aura","Heals all party members for a moderate amount of health over time.",2,454,[0,0,0,0,0,0,12],40,"Buff","All");
    sptSpellDirectory.append(Regenerate_Aura);
    Raise_Aura = SupportMagic("Raise Aura","Raises all fallen party members from the dead with 30 HP.",2,455,[0,0,0,0,0,0,30],50,"Heal","All");
    sptSpellDirectory.append(Raise_Aura);

    #Cleansing Spells
    Cleanse = SupportMagic("Cleanse","Cleanses a party member of status effects.",2,456,[0,0,0,0,0,0,0],10,"Cleanse","Single");
    sptSpellDirectory.append(Cleanse);
    Cleanse_Aura = SupportMagic("Cleanse Aura","Cleanses all party members of status effects.",4,457,[0,0,0,0,0,0,0],24,"Cleanse","All");
    sptSpellDirectory.append(Cleanse_Aura);

    return sptSpellDirectory
