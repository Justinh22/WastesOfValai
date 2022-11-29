import pygame
import random
from characterclasses import *

def getCombatDialogue(character):
    dialogue = ""
    hpPercentage = (character.hp / character.hpMax) * 100
    choice = random.randint(0,2)
    if character.personality == "Brave":
        if hpPercentage >= 90:
            if choice == 0:
                dialogue = "Let's do this!"
            elif choice == 1:
                dialogue = "Nothing will take me down."
            else:
                dialogue = "I won't fall to the likes of you."
        elif hpPercentage >= 50:
            if choice == 0:
                dialogue = "Still going strong."
            elif choice == 1:
                dialogue = "Ha! Barely a scratch."
            else:
                dialogue = "Nothing will take me down."
        elif hpPercentage >= 25:
            if choice == 0:
                dialogue = "Still kicking."
            elif choice == 1:
                dialogue = "I'm fine. Let me at them!"
            else:
                dialogue = "Didn't feel a thing!"
        else:
            if choice == 0:
                dialogue = "Agh... I need some healing."
            elif choice == 1:
                dialogue = "Damn... this is it, then."
            else:
                dialogue = "Thanks for everything, friends..."
    elif character.personality == "Angry":
        if hpPercentage >= 90:
            if choice == 0:
                dialogue = "Let me at them!"
            elif choice == 1:
                dialogue = "You'll fall like the rest of them."
            else:
                dialogue = "I'll paint the earth with blood!"
        elif hpPercentage >= 50:
            if choice == 0:
                dialogue = "This? Nothing."
            elif choice == 1:
                dialogue = "You'll pay for that one, cretin!"
            else:
                dialogue = "You're dead, fiend."
        elif hpPercentage >= 25:
            if choice == 0:
                dialogue = "I've had worse wounds."
            elif choice == 1:
                dialogue = "I'll kill you for that!"
            else:
                dialogue = "That's it!!"
        else:
            if choice == 0:
                dialogue = "So this is what it's like..."
            elif choice == 1:
                dialogue = "I'm taking you with me!"
            else:
                dialogue = "No! You're going down, fiend!"
    elif character.personality == "Friendly":
        if hpPercentage >= 90:
            if choice == 0:
                dialogue = "Let's do this!"
            elif choice == 1:
                dialogue = "Together, as one!"
            else:
                dialogue = "Nothing will take me down."
        elif hpPercentage >= 50:
            if choice == 0:
                dialogue = "Still doing fine!"
            elif choice == 1:
                dialogue = "I'll carry my weight!"
            else:
                dialogue = "We are gonna take you down!"
        elif hpPercentage >= 25:
            if choice == 0:
                dialogue = "Ouch... that hurts."
            elif choice == 1:
                dialogue = "Haha... barely a scratch..."
            else:
                dialogue = "Help me out here!"
        else:
            if choice == 0:
                dialogue = "Sorry, everyone..."
            elif choice == 1:
                dialogue = "You're going down with me!"
            else:
                dialogue = "Goodbye, everyone..."
    elif character.personality == "Cowardly":
        if hpPercentage >= 90:
            if choice == 0:
                dialogue = "Do we have to?"
            elif choice == 1:
                dialogue = "Okay, here we go..."
            else:
                dialogue = "You guys lead the way..."
        elif hpPercentage >= 50:
            if choice == 0:
                dialogue = "Ouch... that's enough for me."
            elif choice == 1:
                dialogue = "Get back!"
            else:
                dialogue = "Take this!"
        elif hpPercentage >= 25:
            if choice == 0:
                dialogue = "Looking for an exit..."
            elif choice == 1:
                dialogue = "Uh... you sure about this?"
            else:
                dialogue = "I need some healing!"
        else:
            if choice == 0:
                dialogue = "Hey, someone help me here!"
            elif choice == 1:
                dialogue = "Alright, I'm out of here..."
            else:
                dialogue = "So this is it..."
    elif character.personality == "Headstrong":
        if hpPercentage >= 90:
            if choice == 0:
                dialogue = "Ha! Bring it on!"
            elif choice == 1:
                dialogue = "What? Just you?"
            else:
                dialogue = "You don't stand a chance!"
        elif hpPercentage >= 50:
            if choice == 0:
                dialogue = "That all you got?"
            elif choice == 1:
                dialogue = "You're a joke!"
            else:
                dialogue = "I thought this would be tough..."
        elif hpPercentage >= 25:
            if choice == 0:
                dialogue = "It's nothing! Take this!"
            elif choice == 1:
                dialogue = "Let's take them down!"
            else:
                dialogue = "You're dead! Get over here!"
        else:
            if choice == 0:
                dialogue = "I'm not going down here!"
            elif choice == 1:
                dialogue = "I could use a hand here!"
            else:
                dialogue = "Not today!"
    elif character.personality == "Lazy":
        if hpPercentage >= 90:
            if choice == 0:
                dialogue = "Do we have to?"
            elif choice == 1:
                dialogue = "*Yawn*... you guys go ahead."
            else:
                dialogue = "Ugh, fine."
        elif hpPercentage >= 50:
            if choice == 0:
                dialogue = "Alright, you take this one..."
            elif choice == 1:
                dialogue = "I'm good, thanks..."
            else:
                dialogue = "Ouch... got a bandage?"
        elif hpPercentage >= 25:
            if choice == 0:
                dialogue = "I'd better lie down..."
            elif choice == 1:
                dialogue = "Alright, now you made me mad."
            else:
                dialogue = "You guys get them, I'm out..."
        else:
            if choice == 0:
                dialogue = "Ugh... what a drag."
            elif choice == 1:
                dialogue = "Well, at least now I can rest..."
            else:
                dialogue = "I should have stayed home..."
    return dialogue
