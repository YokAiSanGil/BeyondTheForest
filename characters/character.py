"""
Character module.
Contains the base class for all game entities.
"""
from characters.utils import modifier
from utils.dice import Die


class Character:
    """
    Base class for all game characters.
    Handles shared stats and actions.
    """
    def __init__(self, race, name=None):
        self.race = race
        self.name = name
        self._endurance_base = Die.roll_n_dice(4, 3)
        self._strength_base = Die.roll_n_dice(4, 3)
        self.max_hp = self.endurance + modifier(self.endurance)
        self.hp = self.max_hp

    @property
    def endurance(self):
        return self._endurance_base

    @property
    def strength(self):
        return self._strength_base

    def is_alive(self):
        return self.hp > 0

    def rest(self):
        self.hp = self.max_hp

    def __str__(self):
        display_name = f"{self.name} ({self.race})" if self.name else self.race
        return f"{display_name} | END: {self.endurance}, STR: {self.strength}, HP: {self.hp}/{self.max_hp}"
