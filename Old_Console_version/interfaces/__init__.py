"""
Module interfaces - Gestion des différentes phases du jeu.
Contient les classes pour les phases d'exploration, combat, soin et menus.
"""

from .base_interface import BaseInterface
from .phase_exploration import PhaseExploration
from .phase_combat import PhaseCombat
from .phase_soin import PhaseSoin
from .phase_menu import PhaseMenu

__all__ = [
    'BaseInterface',
    'PhaseExploration',
    'PhaseCombat', 
    'PhaseSoin',
    'PhaseMenu'
]
