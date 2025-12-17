import pygame
import random

def create_scanlines(width, height):
    """
    Génère une surface avec des lignes de balayage (scanlines) semi-transparentes.
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(0, height, 2):
        # Alpha augmenté à 100 (sur 255) pour être visible partout
        pygame.draw.line(surface, (0, 0, 0, 100), (0, y), (width, y), 1)
    return surface

def get_flicker_color(min_val=200, max_val=255):
    """
    Retourne une couleur grise aléatoire pour simuler un scintillement.
    """
    val = random.randint(min_val, max_val)
    return (val, val, val)
