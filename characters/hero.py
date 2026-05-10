"""
Hero class module.
Contains the Hero class with race bonuses.
"""

from .character import Character

class Hero(Character):
    """
    Hero class. Inherits from Character and adds race bonuses.
    """
    def __init__(self, name, race):
        super().__init__(race, name)
        self.id = None  # Unique identifier for saves
        self.gold = 0
        self.leather = 0
        # Number of times the hero has died (for save tracking)
        self.morts = 0

    @property
    def endurance(self):
        bonus = 2 if self.race == "Dwarf" else (1 if self.race == "Human" else 0)
        return self._endurance_base + bonus

    @property
    def strength(self):
        bonus = 1 if self.race == "Human" else 0
        return self._strength_base + bonus
