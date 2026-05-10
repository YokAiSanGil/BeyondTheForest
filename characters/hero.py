"""
Hero class module.
Contains the Hero class with race bonuses.
"""

from .character import Character

class Hero(Character):
    """
    Hero class. Inherits from Character and adds race bonuses.
    """
    def __init__(self, name: str, race: str):
        super().__init__(race, name)
        self.id: str = None
        self.gold: int = 0
        self.leather: int = 0
        self.morts: int = 0

    @property
    def endurance(self) -> int:
        bonus = 2 if self.race == "Dwarf" else (1 if self.race == "Human" else 0)
        return self._endurance_base + bonus

    @property
    def strength(self) -> int:
        bonus = 1 if self.race == "Human" else 0
        return self._strength_base + bonus
