"""
Characters module - Game entity management.
Contains the Hero, Monster, Character classes and combat actions.
"""

from .character import Character
from .hero import Hero
from .monster import Monster, create_random_monster
from .actions import attack, flee, loot, calculate_damage

__all__ = [
    'Character',
    'Hero',
    'Monster',
    'create_random_monster',
    'attack',
    'flee',
    'loot',
    'calculate_damage'
]
