import pygame
import numpy as np
from affichage_gui.config import GameConfig

def apply_jarvis_judice_ninke_dithering(image_surface):
    """
    Applique l'algorithme de dithering Jarvis, Judice, and Ninke (Error Diffusion)
    sur une surface Pygame. Convertit l'image en noir et blanc (1-bit).
    
    Args:
        image_surface (pygame.Surface): L'image source.
        
    Returns:
        pygame.Surface: Une nouvelle surface en noir et blanc ditherée.
    """
    if not GameConfig().enable_dithering:
        return image_surface

    # Convertir la surface en tableau numpy (RGB)
    # On s'assure d'avoir du RGB
    width, height = image_surface.get_size()
    
    # On travaille sur une copie pour ne pas modifier l'original pendant le calcul
    # array3d renvoie (width, height, 3)
    pixels = pygame.surfarray.array3d(image_surface).astype(float)
    
    # Conversion en niveaux de gris (luminance)
    # Formule standard : 0.299*R + 0.587*G + 0.114*B
    gray = 0.299 * pixels[:, :, 0] + 0.587 * pixels[:, :, 1] + 0.114 * pixels[:, :, 2]
    
    # Matrice de diffusion d'erreur Jarvis, Judice, and Ninke
    #       X   7   5
    #   3   5   7   5
    #   1   3   5   3
    # Divisé par 48
    
    for y in range(height):
        for x in range(width):
            old_pixel = gray[x, y]
            new_pixel = 255 if old_pixel > 128 else 0
            gray[x, y] = new_pixel
            
            quant_error = old_pixel - new_pixel
            
            # Diffusion de l'erreur aux voisins
            if x + 1 < width:
                gray[x + 1, y] += quant_error * 7 / 48
            if x + 2 < width:
                gray[x + 2, y] += quant_error * 5 / 48
                
            if y + 1 < height:
                if x - 2 >= 0:
                    gray[x - 2, y + 1] += quant_error * 3 / 48
                if x - 1 >= 0:
                    gray[x - 1, y + 1] += quant_error * 5 / 48
                if x < width:
                    gray[x, y + 1] += quant_error * 7 / 48
                if x + 1 < width:
                    gray[x + 1, y + 1] += quant_error * 5 / 48
                if x + 2 < width:
                    gray[x + 2, y + 1] += quant_error * 3 / 48
            
            if y + 2 < height:
                if x - 2 >= 0:
                    gray[x - 2, y + 2] += quant_error * 1 / 48
                if x - 1 >= 0:
                    gray[x - 1, y + 2] += quant_error * 3 / 48
                if x < width:
                    gray[x, y + 2] += quant_error * 5 / 48
                if x + 1 < width:
                    gray[x + 1, y + 2] += quant_error * 3 / 48

    # Reconversion en tableau RGB (Noir et Blanc)
    # On crée un tableau (width, height, 3) où R=G=B=gray
    # On clip pour rester entre 0 et 255
    gray = np.clip(gray, 0, 255)
    final_pixels = np.stack((gray, gray, gray), axis=2).astype('uint8')
    
    return pygame.surfarray.make_surface(final_pixels)

def create_dither_surface(width, height, intensity=60):
    """
    Obsolète : Ancienne méthode de dithering par motif.
    Gardée pour compatibilité si besoin, mais on va utiliser apply_jarvis_judice_ninke_dithering
    directement sur les images.
    """
    return pygame.Surface((width, height), pygame.SRCALPHA)

