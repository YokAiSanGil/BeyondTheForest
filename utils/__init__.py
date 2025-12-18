"""
Module utils - Utilitaires généraux du jeu.
Contient les outils, le système de dés et la gestion audio.
"""

from .de6faces import De
from .music import battle_music, stop_music

__all__ = [
    'De',
    'battle_music',
    'stop_music'
]
