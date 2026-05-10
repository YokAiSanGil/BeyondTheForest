"""
Utils module - General game utilities.
Contains dice system and audio management.
"""

from .dice import Die
from .music import battle_music, stop_music

__all__ = [
    'Die',
    'battle_music',
    'stop_music'
]
