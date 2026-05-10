"""
Dice module.
Allows creating dice with any number of faces and rolling multiple dice keeping the best results.
"""
import random

class Die:
    def __init__(self, minimum=1, maximum=6):
        self._minimum = minimum
        self._maximum = maximum
        self.value = 0

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

    @staticmethod
    def roll(minimum=1, maximum=6):
        """Roll the die and return a random value between minimum and maximum."""
        return random.randint(minimum, maximum)

    @staticmethod
    def roll_n_dice(n, best=None, minimum=1, maximum=6):
        """Roll n dice and return the sum of the best results (if specified), otherwise the total sum."""
        rolls = [random.randint(minimum, maximum) for _ in range(n)]
        if best and best < n:
            rolls.sort(reverse=True)
            rolls = rolls[:best]
        return sum(rolls)

    def __str__(self):
        return f"Die value: {self.value}"
