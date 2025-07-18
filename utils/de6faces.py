"""
Module de gestion des dé.
Permet de créer des dés de n'importe quel nombre de faces et de lancer plusieurs dés en gardant les meilleurs.
"""
import random

class De:
    def __init__(self, minimum=1, maximum=6):
        self._minimum = minimum
        self._maximum = maximum
        self.valeur = 0

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

    @staticmethod
    def lancer(minimum=1, maximum=6):
        """Lance le dé et retourne une valeur aléatoire entre minimum et maximum."""
        return random.randint(minimum, maximum)

    @staticmethod
    def lancer_n_des(n, meilleurs=None, minimum=1, maximum=6):
        """Lance n dés et retourne la somme des meilleurs (si précisé), sinon la somme totale."""
        lancers = [random.randint(minimum, maximum) for _ in range(n)]
        if meilleurs and meilleurs < n:
            lancers.sort(reverse=True)
            lancers = lancers[:meilleurs]
        return sum(lancers)

    def __str__(self):
        return f"Valeur du dé: {self.valeur}"