from constants import *
import math

def difficultyToLevel(difficulty):
    divVal = MAX_DIFFICULTY / MAX_LEVEL
    return math.floor(difficulty / divVal) if math.floor(difficulty / divVal) > 0 else 1

def weaponProfArrayToList(arr):
    profList = []
    if arr[0] == 1:
        profList.append(WeaponType.Axe)
    if arr[1] == 1:
        profList.append(WeaponType.Sword)
    if arr[2] == 1:
        profList.append(WeaponType.Spear)
    if arr[3] == 1:
        profList.append(WeaponType.Dagger)
    if arr[4] == 1:
        profList.append(WeaponType.Staff)
    return profList

def armorProfArrayToList(arr):
    profList = []
    if arr[0] == 1:
        profList.append(ArmorType.Light)
    if arr[1] == 1:
        profList.append(ArmorType.Medium)
    if arr[2] == 1:
        profList.append(ArmorType.Heavy)
    if arr[3] == 1:
        profList.append(ArmorType.Robe)
    if arr[4] == 1:
        profList.append(ArmorType.Arcanist)
    return profList