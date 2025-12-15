import pygame
import os
from affichage_gui.dithering import apply_jarvis_judice_ninke_dithering
from affichage_gui.gui_manager import SCREEN_WIDTH, SCREEN_HEIGHT

class MenuAssets:
    """Gère les ressources graphiques partagées des menus (Fond, Titre)."""
    def __init__(self):
        self.title_bg = None
        self.title_surface = None
        self._load_assets()

    def _load_assets(self):
        # Chargement de l'image de fond
        # On remonte de 3 niveaux : interfaces_gui/menus/ -> interfaces_gui/ -> root/ -> assets/
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.join(base_dir, "assets", "TitleScreen", "MRTN_A_lush_dark_fantasy_forest_hero_from_behind_going_in_lands_083a31f5-8ae7-4803-a97f-995a5245f382.png")
        
        if os.path.exists(img_path):
            try:
                img = pygame.image.load(img_path).convert()
                scaled_img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.title_bg = apply_jarvis_judice_ninke_dithering(scaled_img)
            except Exception as e:
                print(f"Erreur chargement image titre: {e}")
        
        self.title_surface = self._generate_dithered_title()

    def _generate_dithered_title(self):
        """Génère une surface avec le titre vertical dithered."""
        words = ["BEYOND", "the", "FOREST"]
        font = pygame.font.SysFont("Courier New", 60)
        
        max_w = 0
        total_h = 0
        surfaces = []
        for w in words:
            s = font.render(w, True, (255, 255, 255))
            surfaces.append(s)
            max_w = max(max_w, s.get_width())
            total_h += s.get_height()
            
        container = pygame.Surface((max_w, total_h))
        container.fill((0, 0, 0))
        
        y = 0
        for s in surfaces:
            x = (max_w - s.get_width()) // 2
            container.blit(s, (x, y))
            y += s.get_height()
            
        dithered = apply_jarvis_judice_ninke_dithering(container)
        dithered.set_colorkey((0, 0, 0))
        
        return dithered
