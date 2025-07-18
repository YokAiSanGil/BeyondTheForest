"""
Module personnages - Gestion des entités du jeu.
Contient les classes Hero, Monster, Personnage et les actions de combat.
"""

from .personnage import Personnage
from .hero import Hero
from .monstre import Monster, creer_monstre_aleatoire
from .actions import frapper, fuir, depecer, calculer_degats

__all__ = [
    'Personnage',
    'Hero', 
    'Monster',
    'creer_monstre_aleatoire',
    'frapper',
    'fuir', 
    'depecer',
    'calculer_degats'
]
