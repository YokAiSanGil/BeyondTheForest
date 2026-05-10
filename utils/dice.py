"""
Dice module.
Allows creating dice with any number of faces and rolling multiple dice keeping the best results.
"""
import random

class Die:
    def __init__(self, minimum: int = 1, maximum: int = 6):
        self._minimum = minimum
        self._maximum = maximum
        self.value: int = 0

    @property
    def minimum(self) -> int:
        return self._minimum

    @property
    def maximum(self) -> int:
        return self._maximum

    @staticmethod
    def roll(minimum: int = 1, maximum: int = 6) -> int:
        """Roll the die and return a random value between minimum and maximum."""
        return random.randint(minimum, maximum)

    @staticmethod
    def roll_n_dice(n: int, best: int = None, minimum: int = 1, maximum: int = 6) -> int:
        """Roll n dice and return the sum of the best results (if specified), otherwise the total sum."""
        rolls = [random.randint(minimum, maximum) for _ in range(n)]
        if best and best < n:
            rolls.sort(reverse=True)
            rolls = rolls[:best]
        return sum(rolls)

    def __str__(self):
        return f"Die value: {self.value}"
