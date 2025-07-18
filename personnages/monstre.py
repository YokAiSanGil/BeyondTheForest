"""
Module Monstre.
Ce module contient les classes et fonctions pour la gestion des monstres.
"""

from .personnage import Personnage
from utils.de6faces import De
import random

class Monster(Personnage):
    """
    Classe pour les monstres. Hérite de Personnage et ajoute les bonus de race.
    """
    def __init__(self, race):
        super().__init__(race)
        # Le loot est calculé à la création du monstre
        self.cuir = De.lancer(1, 4) if self.peut_donner_cuir else 0
        self.gold = De.lancer(1, 6) if self.peut_donner_or else 0

    @property
    def endurance(self):
        bonus = 1 if self.race == "Dragonnet" else 0
        return self._endurance_base + bonus

    @property
    def force(self):
        bonus = 1 if self.race == "Orque" else 0
        return self._force_base + bonus

    @property
    def peut_donner_cuir(self):
        return self.race in ["Loup", "Dragonnet"]

    @property
    def peut_donner_or(self):
        return self.race in ["Orque", "Dragonnet"]

def creer_monstre_aleatoire():
    """
    Fonction pour créer un monstre aléatoire.
    """
    races_monstres = ["Loup", "Orque", "Dragonnet"]
    race_choisie = random.choice(races_monstres)
    return Monster(race_choisie)
