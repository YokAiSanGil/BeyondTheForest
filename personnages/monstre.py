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
        
        # Chemin de l'image
        import os
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image_path = os.path.join(base_path, 'assets', 'Mosters', f'{race}.png')

    @property
    def endurance(self):
        bonus = 0
        if self.race in ["HellParasite", "StrygMoth"]:
            bonus = 2
        elif self.race in ["NightScreamer"]:
            bonus = 1
        return self._endurance_base + bonus

    @property
    def force(self):
        bonus = 0
        if self.race in ["HellParasite", "NightScreamer"]:
            bonus = 2
        elif self.race in ["StingFish"]:
            bonus = 1
        return self._force_base + bonus

    @property
    def peut_donner_cuir(self):
        return self.race in ["StingFish", "HellParasite", "NightScreamer"]

    @property
    def peut_donner_or(self):
        return self.race in ["BloodFairy", "StrygMoth", "HellParasite"]

def creer_monstre_aleatoire():
    """
    Fonction pour créer un monstre aléatoire.
    """
    races_monstres = ["BloodFairy", "HellParasite", "NightScreamer", "StingFish", "StrygMoth"]
    race_choisie = random.choice(races_monstres)
    return Monster(race_choisie)
