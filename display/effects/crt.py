import pygame
import random

def create_scanlines(width, height):
    """
    Generate a surface with semi-transparent scanlines.
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(0, height, 2):
        # Alpha set to 100 (out of 255) to be visible everywhere
        pygame.draw.line(surface, (0, 0, 0, 100), (0, y), (width, y), 1)
    return surface

def get_flicker_color(min_val=200, max_val=255):
    """
    Return a random grey color to simulate CRT flicker.
    """
    val = random.randint(min_val, max_val)
    return (val, val, val)
