"""
module Personnage.
Ce module contient les classes et fonctions pour la gestion des personnages.
"""
from utils.outils import modificateur
from utils.de6faces import De


class Personnage:
    """
    Classe de base pour tous les personnages du jeu.
    Gère les caractéristiques et actions communes.
    """
    def __init__(self, race, nom=None):
        self.race = race
        self.nom = nom
        self._endurance_base = De.lancer_n_des(4, 3)
        self._force_base = De.lancer_n_des(4, 3)
        self.points_de_vie_max = self.endurance + modificateur(self.endurance)
        self.points_de_vie = self.points_de_vie_max

    @property
    def endurance(self):
        return self._endurance_base

    @property
    def force(self):
        return self._force_base

    def est_vivant(self):
        return self.points_de_vie > 0

    def se_reposer(self):
        self.points_de_vie = self.points_de_vie_max

    def __str__(self):
        display_name = f"{self.nom} ({self.race})" if self.nom else self.race
        return f"{display_name} | END: {self.endurance}, FOR: {self.force}, PV: {self.points_de_vie}/{self.points_de_vie_max}"
