"""
Class hero - module python.
Ce module contient les classes et fonctions pour la gestion des héros.
"""

from .personnage import Personnage

class Hero(Personnage):
    """
    Classe pour les héros. Hérite de Personnage et ajoute les bonus de race.
    """
    def __init__(self, nom, race):
        super().__init__(race, nom)
        self.id = None # Identifiant unique pour la sauvegarde
        self.gold = 0
        self.cuir = 0
        # Nombre de fois que le héros est mort (pour la sauvegarde)
        self.morts = 0

    @property
    def endurance(self):
        bonus = 2 if self.race == "Nain" else (1 if self.race == "Humain" else 0)
        return self._endurance_base + bonus

    @property
    def force(self):
        bonus = 1 if self.race == "Humain" else 0
        return self._force_base + bonus
