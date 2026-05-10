"""
Monster module.
Contains the Monster class and factory functions.
"""

from .character import Character
from utils.dice import Die
import random

class Monster(Character):
    """
    Monster class. Inherits from Character and adds race bonuses.
    """
    def __init__(self, race):
        super().__init__(race)
        # Loot is calculated at monster creation
        self.leather = Die.roll(1, 4) if self.can_give_leather else 0
        self.gold = Die.roll(1, 6) if self.can_give_gold else 0

        # Image path
        import os
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image_path = os.path.join(base_path, 'assets', 'Mosters', f'{race}_dithered.png')

    @property
    def endurance(self):
        bonus = 0
        if self.race in ["HellParasite", "StrygMoth"]:
            bonus = 2
        elif self.race in ["NightScreamer"]:
            bonus = 1
        return self._endurance_base + bonus

    @property
    def strength(self):
        bonus = 0
        if self.race in ["HellParasite", "NightScreamer"]:
            bonus = 2
        elif self.race in ["StingFish"]:
            bonus = 1
        return self._strength_base + bonus

    @property
    def can_give_leather(self):
        return self.race in ["StingFish", "HellParasite", "NightScreamer"]

    @property
    def can_give_gold(self):
        return self.race in ["BloodFairy", "StrygMoth", "HellParasite"]

def create_random_monster():
    """
    Create a random monster.
    """
    monster_races = ["BloodFairy", "HellParasite", "NightScreamer", "StingFish", "StrygMoth"]
    chosen_race = random.choice(monster_races)
    return Monster(chosen_race)

def create_hermit_boss():
    """Create the final boss (The True Hermit in their real form)."""
    boss = Monster("The True Hermit")
    # Overpowered stats
    boss._endurance_base = 50
    boss._strength_base = 50
    boss.max_hp = 1000
    boss.hp = 1000

    # Boss image
    import os
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    boss.image_path = os.path.join(base_path, 'assets', 'Mosters', 'TheTrueHermit.png')

    return boss
