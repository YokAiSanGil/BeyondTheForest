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
    def __init__(self, race: str, name: str = None):
        self.race: str = race
        self.name: str = name
        self._endurance_base: int = Die.roll_n_dice(4, 3)
        self._strength_base: int = Die.roll_n_dice(4, 3)
        self.max_hp: int = self.endurance + modifier(self.endurance)
        self.hp: int = self.max_hp

    @property
    def endurance(self) -> int:
        return self._endurance_base

    @property
    def strength(self) -> int:
        return self._strength_base

    def is_alive(self) -> bool:
        return self.hp > 0

    def rest(self) -> None:
        self.hp = self.max_hp

    def __str__(self) -> str:
        display_name = f"{self.name} ({self.race})" if self.name else self.race
        return f"{display_name} | END: {self.endurance}, STR: {self.strength}, HP: {self.hp}/{self.max_hp}"
